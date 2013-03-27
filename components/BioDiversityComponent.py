from components.helpers import *

class BioDiversityComponent(Component):
  nospecies   = DependentVariable("Number of species", requiresFirst = True)
  
  temp        = ExternalVariable("Temperature")
  
  bioloss     = IndependentVariable("Additive parameter")
  biosens     = IndependentVariable("Multiplicative parameter")
  dbsta       = IndependentVariable("Benchmark temperature change")
  
  def step(self):
    dt = math.abs(self.delta(self.temp))
    
    self.nospecies = math.max(
      self.initial('nospecies') / 100,
      self.previous('nospecies') * (1.0 - self.bioloss - s.biosens * dt * dt / self.dbsta / self.dbsta)
    )