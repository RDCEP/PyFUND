import glob
import os
import warnings
import csv
import re
from components.helpers import Timestep

class NormalDistribution(object):
  def __init__(self, *values):
    if len(values) == 1:
      match = re.match(r'NormalDistribution\(([^;]+); ([^;]+).+\)', values[0])
      if not match:
         raise ValueError('Improperly formatted normal distribution specifier.')
      
      self.mean, self.stddev = map(float, match.groups())
    else:
      self.mean, self.stddev = values
  
  def __repr__(self):
    return u'NormalDistribution({0}; {1})'.format(self.mean, self.stddev)

def _find_fund_behaviors():
   """
   This function looks all modules in the components/ directory and 
   reads the model implemenations therein.
   """
   behaviors = [ ]
   
   for file in glob.glob('components/*.py'):
      module_name = file[:-3].split('/')[1]
      if module_name not in ('__init__', 'helpers', '_patches'):
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

def _choose_default_for_variable(variable):
   dimension = variable.dimension
   result = {}
   filename = 'parameters/{0}.csv'.format(variable.name)
   
   if not os.path.isfile(filename):
     return None
   
   for row in csv.DictReader(open(filename)):
      if variable.name in row:
         value = row[variable.name]
      else:
         value = row[variable.name.lower()]
      
      try:
         value = float(value)
      except ValueError:
         try:
            value = NormalDistribution(value).mean
         except ValueError:
            warnings.warn('Caught an incomprehensible field value: {0!r}'.
              format(repr(value)))
            value = 0
      
      if dimension == 0:
         if row['Name'] == 'Value':
            return value
         
      elif dimension == 1:
         second_key = list(set(row.keys()) - set([variable.name]))[0]
         result[row[second_key]] = value
         
      elif dimension == 2:
         first = row[variable.index_by[0]]
         second = row[variable.index_by[1]]
         
         try: first = float(first)
         except ValueError: pass
         
         try: second = float(second)
         except ValueError: pass
         
         result[first, second] = value
   
   if dimension == 0:
      return None
   else:
      return result

def _choose_default_for_type(kind):
   """
   This function chooses the default value for a given type.
   """
   return {
      'double': float('NaN'),
      'timestep': 1950,
      'region': float('NaN'),
      'boolean': False,
      'bool': False
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
         'Timestep': self.time_steps
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
         regions = [ "USA", "CAN", "WEU", "JPK", "ANZ", "EEU", "FSU", "MDE",
                     "CAM", "LAM", "SAS", "SEA", "CHI", "MAF", "SSA", "SIS" ]
      )
      
      # Precompute the values of all types
      types = self.dimensions.generate_types()
      
      # Ensure that all parameters are specified
      for name, variable in self.all_options.items():
         new_value = _choose_default_for_variable(variable)
          
         if new_value:
            self.variables[name] = new_value
         
         else:
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
      
      for year in self.dimensions.time_steps:
         Timestep.__init__(year, self.dimensions.time_steps[1])
         print "year is {0} (is first = {1})".format(year, Timestep.IsFirstTimestep)
         
         if year == self.dimensions.time_steps[0]:
            continue
         
         for behavior, state in instances:
            behavior.run(state, Timestep, self.dimensions)
      
      # Do stuff with the results
   
   def track(self, *variables):
      pass

def main():
   model = None
   
   with warnings.catch_warnings():
      # warnings.simplefilter('ignore')
      model = FUND(time_steps = range(1960, 2100))
   
   model.run()

if __name__ == '__main__':
   main()