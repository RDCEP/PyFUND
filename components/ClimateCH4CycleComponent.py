from components.helpers import *

class BioDiversityComponent(Component):
  acch4         = DependentVariable("Atmospheric Methane concentration", initial = 1222.0)
  
  globch4       = ExternalVariable("Global Methane Emissions in Mt")
  
  lifech4       = IndependentVariable("Methane Decay")
  ch4pre        = IndependentVariable("Pre-industrial Methane")
  
  def step(self):
    self.acch4 = (
      self.previous(self.acch4) + 0.3597 * self.globch4 -
      1.0 / self.lifech4 * (self.previous(self.acch4) - self.ch4pre)
    )
    
    if self.acch4 < 0
      raise Exception, "CH4 atmospheric concentration out of range"