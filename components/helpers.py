import threading

DBsT = 0.04

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

Timestep = threading.local

class Timestep():
   """
   The Timestep singleton is a crutch. It is easier to use this
   one weird hack than to intelligently rewrite the buggy C#.
   """
   
   _state = threading.local()
   
   @classmethod
   def FromYear(self, year):
      return Timestep(self._state.clock.FromYear(year))
   
   @classmethod
   def FromSimulationYear(self, year):
      return Timestep(self._state.clock.FromSimulationYear(year))
   
   def __init__(self, x):
      self.Value = x
   
   def __hash__(self):
      return hash(self.Value)
   
   def __cmp__(self, other):
      return self.Value.__cmp__(other.Value)
   
   def __sub__(self, x):
      return Timestep(self.Value - int(x))
   
   def __add__(self, x):
      return Timestep(self.Value + int(x))
   
   def __int__(self):
      return self.Value
   
   def __str__(self):
      return "{0}".format(self.Value)
   
   def __repr__(self):
      return "Timestamp({0})".format(self.Value)

class Variable(object):
   """
   A variable is a reference to a value that is tracked over
   time.
   """
   def __init__(self, machine_readable_name, index_by, return_value, description):
      self.machine_readable_name = "{0}_{1}".format(machine_readable_name, len(index_by or [ ]))
      self.index_by = index_by
      self.return_value = return_value
      self.description = description 
   
   def fold_description_from(self, other_variable):
      if self.description is None:
         self.description = other_variable.description
   
   def __get__(self, instance, klass):
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