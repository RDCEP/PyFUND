from components.helpers import *

class ComponentName(Component):
  output      = DependentVariable("Output variable", requiresFirst = True)
  external    = ExternalVariable("Variable taken from another component")
  input       = IndependentVariable("Input parameter")
  
  def every_step(self):
    self.output = self.output * self.input + self.external
