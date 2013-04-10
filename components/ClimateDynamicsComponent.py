from components.helpers import *

class ClimateDynamicsComponent(Component):
  radforc            = DependentVariable("Total radiative forcing", requiresFirst = True)
  temp               = DependentVariable("Average global temperature", requiresFirst = True)
  
  LifeTempConst      = IndependentVariable("LifeTempConst")
  LifeTempLin        = IndependentVariable("LifeTempLin")
  LifeTempQd         = IndependentVariable("LifeTempQd")
  ClimateSensitivity = IndependentVariable("Climate sensitivity")
  
  def every_step(self):
    LifeTemp = math.max(1.0, self.LifeTempConst + self.LifeTempLin * self.ClimateSensitivity +
                             self.LifeTempQd * math.pow(self.ClimateSensitivity, 2.0));
    
    delaytemp = 1.0 / LifeTemp
    
    temps = self.ClimateSensitivity / 5.35 / math.log(2)
    
    self.temp += delaytemp * temps * self.radforc - delaytemp * self.temp