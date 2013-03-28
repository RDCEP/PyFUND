from components.helpers import *

class ExponentialGrowthTest(Component):
  balance  = DependentVariable("Bank account balance", requiresFirst = True)
  interest = IndependentVariable("Bank account interest")
  
  def every_step(self):
    self.balance *= (1 + self.interest * 0.01)