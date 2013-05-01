from components.helpers import *

class ClimateN2OCycle(Component):
  globn2o = DependentVariable("Global N2O Emissions in Mt of N")
  acn2o   = DependentVariable("!!!", requires_first = True) # default: 296
  lifen2o = IndependentVariable("N2O Lifetime")
  n2opre  = IndependentVariable("Pre-Industrial N2O Concentration")
  
  def every_step(self):
    self.acn2o += 0.2079 * self.globn2o - 1 / self.lifen2o * (self.acn2o - self.n2opre)
    
    if self.acn2o < 0:
      raise ValueError("acn2o out of range!")