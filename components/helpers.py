import threading

class Simulation(object):
  shared = threading.local()
  
  def __init__(self, components, years):
    self.all_parameters = [ ]
    self.values = dict( )
    self.current_time_step = 0
    self.total_time_steps = len(years) + 1
    self.years = years
    self.stages = [ x(self) for x in components ]
  
  @classmethod
  def current_simulation(klass):
    if klass.in_simulation():
      return klass.shared.simulation
    else:
      raise ValueError, "Not in a simulation yet."
  
  @classmethod
  def in_simulation(klass):
    return hasattr(klass.shared, 'simulation')
  
  def __enter__(self):
    if self.__class__.in_simulation():
      raise Exception("Already in simulation")
    
    self.__class__.shared.simulation = self
  
  def __exit__(self, type, value, traceback):
    del self.__class__.shared.simulation
  
  def set_parameters(self):
    for component, parameter in self.all_parameters:
      self.values[parameter.identifier] = [ None ] * self.total_time_steps
      
      parameter.set_initial_value(1)
  
  def run_simulation(self):
    with self:
      self.set_parameters()
      
      for year in self.years:
        self.current_time_step += 1
        for stage in self.stages:
          stage.every_step()

class Variable(object):
  def __init__(self, description, **dargs):
    self.identifier = None
    self.description = description
  
  def __get__(self, instance, owner):
    sim = Simulation.current_simulation()
    return sim.values[self.identifier][sim.current_time_step - 1]
  
  def __set__(self, instance, value):
    sim = Simulation.current_simulation()
    sim.values[self.identifier][sim.current_time_step] = value
  
  def set_initial_value(self, value):
    self.__set__(None, value)

class DependentVariable(Variable):
  pass

class IndependentVariable(Variable):
  def __get__(self, instance, owner):
    sim = Simulation.current_simulation()
    return sim.values[self.identifier]
  
  def __set__(self, instance, value):
    sim = Simulation.current_simulation()
    sim.values[self.identifier] = value

class ExternalVariable(Variable):
  pass

class Component(object):
  def __init__(self, simulation):
    d = self.__class__.__dict__
    for name in d.keys():
      if isinstance(d[name], Variable):
        d[name].identifier = name
        simulation.all_parameters.append((self, d[name]))