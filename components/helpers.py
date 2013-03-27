class Parameter(object):
  def __init__(self, name, temporal, description, default):
    self.name = name
    self.temporal = temporal
    self.description = description
    self.default = default
  
  def construct(self, simulation):
    if self.temporal:
      return [ None ] * simulation.time_steps
    else:
      return float(self.default)

class Component(object):
  parameters = [ ]

def TemporalParameter(*vargs, **dargs):
  param = Parameter(*vargs, temporal = True, **dars)
  
  def inner(klass):
    klass.parameters.append(param)
    return klass
  return inner

def ScalarParameter(*vargs, **dargs):
  param = Parameter(*vargs, temporal = False, **dars)
  
  def inner(klass):
    klass.parameters.append(param)
    return klass
  return inner