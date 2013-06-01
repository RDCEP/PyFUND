import glob
import warnings
from components.helpers import Timestep

def _find_fund_behaviors():
   """
   This function looks all modules in the components/ directory and 
   reads the model implemenations therein.
   """
   behaviors = [ ]
   
   for file in glob.glob('components/*.py'):
      module_name = file[:-3].split('/')[1]
      if module_name not in ('__init__', 'helpers'):
         module = getattr(__import__('components.{0}'.format(module_name)),
           module_name)
         behaviors.extend(module.behavior_classes)
   
   return behaviors

def _extract_options_from_behaviors(behaviors):
   """
   This functions attempts to link together all parameters
   from all model components.
   """
   options = dict( )
   
   for behavior in behaviors:
      for variable in behavior.state_class.options:
         name = variable.machine_readable_name
         if name not in options:
            options[name] = variable
         else:
            options[name].fold_description_from(variable)
   
   return options

def _cross_product_of_types(types = [ ], values = dict( )):
   """
   This function performs a recursive cross product of all
   possible values of all possible types. This allows us to
   initialize the variables more intelligently in the later
   code.
   """
   
   if types == [ ]:
      return [ ( ) ]
   
   child_values = _cross_product_of_types(types[1:], values)
   options = values[types[0]]
   
   return [ ( x, ) + y for x in options for y in child_values ]

def _choose_default_for_type(kind):
   """
   This function chooses the default value for a given type.
   """
   return {
      'double': 3.0,
      'timestep': Timestep(2),
      'region': 1,
      'boolean': True,
      'bool': True
   }[kind.lower()]

def _bastardize_list(python_list):
   """
   This function adds certain methods that C# expects to
   the standard library.
   """
   
   class CSharpList(list):
      def Select(self, closure):
         return CSharpList(map(closure, self))
      
      def Sum(self):
         return sum(self)
   
   cs_list = CSharpList(python_list)
   
   return cs_list
   
class Clock(object):
   """
   The Clock class represents the abstract time-keeper; it allows
   model components to transparently access both the current year
   and time-step.
   """
   def __init__(self, time_steps):
      self.time_steps = time_steps
      self.current_time_step = 1
   
   @property
   def can_advance(self):
      return self.current_time_step < len(self.time_steps)
   
   def advance(self):
      self.current_time_step += 1
   
   @property
   def Current(self):
      return Timestep(self.current_time_step)
   
   @property
   def IsFirstTimestep(self):
      return self.current_time_step == 1
   
   @property
   def StartTime(self):
      return self.time_steps[0]
   
   def FromYear(self, looking_for):
      for index, year in enumerate(self.time_steps):
         if year >= looking_for:
            return index
      
      raise ValueError, "The year {0!r} is not in this simulation.".format(looking_for)
   
   def FromSimulationYear(self, looking_for):
      return self.FromYear(looking_for + self.time_steps[0])

class Dimensions(object):
   """
   This class manages the size of the dimension. Most of these
   parameters (number of regions, for instance) are hard-coded.
   """
   
   def __init__(self, time_steps, regions):
      self.time_steps = time_steps
      self.regions = regions
   
   def GetValuesOfRegion(self):
      return _bastardize_list(self.regions)
   
   def generate_types(self):
      return {
         'Region': self.regions,
         'Timestep': [ Timestep(x) for x in range(0, len(self.time_steps)) ]
      }

class FUND(object):
   """
   FUND stands for Climate Framework for Uncertainty, Negotiation
   and Distribution. The logic of the framework is maintained
   by David Anthoff and Richard Tol, and, though it does not have
   an institutional home, it has a GitHub page at:
   
   https://github.com/fund-model/fund
   
   Please see the source documentation for original domain-
   specific advice. 
   """
   all_behaviors = _find_fund_behaviors() 
   all_options = _extract_options_from_behaviors(all_behaviors)
   
   def __init__(self, time_steps, **parameters):
      """
      Initializes a run of FUND. This method validates that the
      parameters passed in are valid according to the Parameter
      files.
      """
      
      # Prepare structure storing all variables
      self.variables = dict( parameters )
      
      # Save the list of all dimensions (regions, timesteps, etc.)
      self.dimensions = Dimensions(
         time_steps = time_steps,
         regions = range(0, 5)
      )
      
      # Precompute the values of all types
      types = self.dimensions.generate_types()
      
      # Ensure that all parameters are specified
      for name, variable in self.all_options.items():
         new_value = _choose_default_for_type(variable.return_value)
         
         if name not in parameters:
            if variable.is_parameter:
               warnings.warn("Missing parameter {0}; setting to an arbitrary value.".format(name))
               # new_value = _choose_default_for_type(variable.return_value)
            
            self.variables[name] = dict( )
         
            for value in _cross_product_of_types(variable.index_by or [ ], values = types):
               if len(value) == 0:
                  self.variables[name] = new_value
               elif len(value) == 1:
                  self.variables[name][value[0]] = new_value
               else:
                  self.variables[name][value] = new_value
   
   def run(self):
      """
      Performs every phase of the model in sequence over the
      entire time interval. After the model has finished running,
      the values of the various variables can be exported to CSV.
      """
      
      instances = [ ]
      for behavior_class in self.all_behaviors:
         behavior_instance = behavior_class()
         state_instance = behavior_class.state_class(self.variables)
         
         instances.append(( behavior_instance, state_instance ))
      
      clock = Clock(self.dimensions.time_steps)
      
      Timestep._state.clock = clock # This is terrible form.
      
      while clock.can_advance:
         warnings.warn("Masking divide by zero exceptions since parameters aren't specified.")
         
         for behavior, state in instances:
            try:
               behavior.run(state, clock, self.dimensions)
            except (ZeroDivisionError, ValueError):
               pass
         
         clock.advance()
      
      # Do stuff with the results
   
   def track(self, *variables):
      pass

def main():
   model = None
   
   with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      model = FUND(time_steps = range(1990, 2100))
   
   model.run()

if __name__ == '__main__':
   main()