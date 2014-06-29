import threading

class ApplicationException(Exception):
   pass

class Parameters(object):
   """
   The Parameters class is the abstract superclass of all
   parameter configuration objects in the various model
   components.
   """
   
   def __init__(self, values):
      self.values = values

class Behaviors(object):
   """
   This is the abstract superclass for any component of
   the model that tracks changes over time. Every Behaviors
   subclass has an associated Paramters object that defines
   its interaction with the surrounding code.
   """
# Clock class is implemented in C# as the Timestep class; Clock is different.
class Clock(object):
   """
   The Clock class represents the abstract time-keeper; it allows
   model components to transparently access both the current year
   and time-step.
   """
   def __init__(self, time_step, first_time_step):
      self.first = first_time_step
      self.time_step = time_step
   
   @property
   def Current(self):
      return self.time_step
   
   @property
   def IsFirstTimestep(self):
      return self.first == self.time_step
   
   @property
   def StartTime(self):
      return self.first


   # correcting incorrect removal of Value property from C# conversion. This returns
   # the difference between base year and current year in model.
   @property
   def Value(self):
       return self.time_step - self.first

   def FromYear(self, year):
      return year
   
   def FromSimulationYear(self, looking_for):
      return looking_for + self.first

Timestep = Clock(None, None)

class Variable(object):
   """
   A variable is a reference to a value that is tracked over
   time.
   """
   def __init__(self, machine_readable_name, index_by, return_value, description):
      self.name = machine_readable_name
      self.machine_readable_name = "{0}_{1}".format(machine_readable_name, len(index_by or [ ]))
      self.index_by = index_by
      self.return_value = return_value
      self.description = description 
   
   def fold_description_from(self, other_variable):
      if self.description is None:
         self.description = other_variable.description
   
   def __get__(self, instance, klass):
      if instance is None:
        return self
      return instance.values[self.machine_readable_name]

class IVariable1Dimensional(Variable):
   is_parameter = False
   dimension = 1

class IVariable2Dimensional(Variable):
   is_parameter = False
   dimension = 2

class IParameter1Dimensional(Variable):
   is_parameter = True
   dimension = 1

class IParameter2Dimensional(Variable):
   is_parameter = True
   dimension = 2

class ScalarVariable(Variable):
   is_parameter = True
   dimension = 0
   
   def __init__(self, machine_readable_name, return_value, description):
      Variable.__init__(self, machine_readable_name, None, return_value, description)