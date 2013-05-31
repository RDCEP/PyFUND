class Parameters(object):
   """
   The Parameters class is the abstract superclass of all
   parameter configuration objects in the various model
   components.
   """
class Behaviors(object):
   """
   This is the abstract superclass for any component of
   the model that tracks changes over time. Every Behaviors
   subclass has an associated Paramters object that defines
   its interaction with the surrounding code.
   """

class Variable(object):
   """
   A variable is a reference to a value that is tracked over
   time.
   """
   def __init__(self, machine_readable_name, index_by, return_value, description):
      self.machine_readable_name = machine_readable_name
      self.index_by = index_by
      self.return_value = return_value
      self.description = description 
   
   def fold_description_from(self, other_variable):
      if self.description is None:
         self.description = other_variable.description

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