from components.helpers import *

class ClimateCO2Cycle(Component):
  mco2                 = DependentVariable("Anthropogenic CO2 emissions in Mt of CO2")
  TerrestrialCO2       = DependentVariable("Terrestrial biosphere CO2 emissions in Mt of CO2")
  globc                = DependentVariable("Net CO2 emissions in Mt of CO2")
  cbox                 = DependentVariable("Carbon box", dimension = 5, initial =
                          [ 283.53, 5.62, 6.29, 2.19, 0.15 ] )
  
  lifeco               = IndependentVariable("Carbon decay", dimension = 5)
    # Something is very wrong in the original file; lifeco1 is different than lifeco2 et. al.,
    # and I'm not sure why. -J
  
  co2frac              = IndependentVariable("Fraction of carbon emissions", dimension = 5)
  
  acco2                = DependentVariable("Atmospheric CO2 concentration")
  TerrCO2Stock         = DependentVariable("Stock of CO2 in the terrestrial biospehere")
  temp                 = DependentVariable("Temperature")
  
  TerrCO2Sense         = IndependentVariable("Terrestrial CO2 sensitivity")
  tempIn2010           = DependentVariable("Mean global temperature in 2010")
  
  def step(self, time):
    self.tempIn2010 = self.at_time('temp', year = 2010)
    
    self.TerrCO2Stock = math.max(self.previous('TerrCO2Stock') - s.TerrestrialCO2, 0.0)
    self.globc = self.mco2 + self.TerrestrialCO2
    
    for i in xrange(5):
      self.cbox[i] = self.previous('cbox')[i] * self.co2decay + 0.000471 * self.co2frac[i] * self.globc
    
    self.acco2 = sum(self.cbox)