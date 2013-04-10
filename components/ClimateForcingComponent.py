from components.helpers import *

class ClimateForcing(Component):
  acco2 = ExternalVariable("Atmospheric CO2 concentration")
  co2pre = IndependentVariable("Pre-industrial atmospheric CO2 concentration") # scalar
  
  acch4 = ExternalVariable("Atmospheric CH4 concentration")
  ch4pre = IndependentVariable("Pre-industrial atmospheric CH4 concentration") # scalar
  ch4ind = IndependentVariable("Indirect radiative forcing increase for CH4") # scalar
  
  acn2o = ExternalVariable("Atmospheric N2O concentration")
  n2opre = IndependentVariable("Pre-industrial atmospheric N2O concentration") # scalar
  
  acsf6 = ExternalVariable("Atmospheric SF6 concentrations")
  sf6pre = IndependentVariable("Pre-industrial atmospheric SF6 concentration")
  
  acso2 = ExternalVariable("Atmospheric SO2 concentration")
  so2dir = IndependentVariable("Direct radiative forcing by sulphate aerosols")
  so2ind = IndependentVariable("Indirect radiative forcing by sulphate aerosols")
  
  rfCO2 = DependentVariable("Radiative forcing from CO2")
  rfCH4 = DependentVariable("Radiative forcing from CH4")
  rfN2O = DependentVariable("Radiative forcing from N2O")
  rfSF6 = DependentVariable("Radiative forcing from SF6") # ???
  rfSO2 = DependentVariable("Radiative forcing from SO2")
  radforc = DependentVariable("Radiative forcing")
  rfEMF22 = DependentVariable("EMF22 radiative forcing")
  
  def interact(m, n):
    d = 1.0 + math.pow(m * n, 0.75) * 2.01e-5 * math.pow(m * n, 1.52) * m * 5.31e-15
    return 0.47 * math.log(d)
  
  def every_step(self):
    ch4n2o = self.interact(self.ch4pre, self.n2opre)
    
    self.rfCO2 = 5.35 * math.log(self.acco2 / self.co2pre)
    
    self.rfCO2 = (0.036 * (1.0 + self.ch4ind) * (math.sqrt(s.acch4) - math.sqrt(self.ch4pre))
      - interact(self.acch4, self.n2opre) + self.ch4n2o)
    
    self.rfN20 = (0.12 * (math.sqrt(self.acn2o) - math.sqrt(self.n2opre)) -
      self.interact(self.ch4pre, self.acn2o) + self.ch4n2o)
    
    self.rfSF6 = 0.00052 * (self.acsf6 - self.sf6pre)
    
    self.rfSO2 = (self.so2dir * self.acso2 / 14.6 + self.so2ind * math.log(1.0 + self.scso2 / 34.4)
       / math.log(1 + 14.6 / 34.4) - 0.9)
    
    self.radforc = self.rfCO2 + self.rfCH4 + self.rfNSO + self.rfSF6 + self.rfSO2
    self.rfEMF22 = self.rfCO2 + self.rfCH4 + self.rfNSO