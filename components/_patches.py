# This file contains globals that are model-specific and too
# much of a bother to rewrite manually.

DBsT = 0.04

def Interact(M, N):
   import math
   
   d = 1.0 + math.pow(M * N, 0.75) * 2.01E-5 + math.pow(M * N, 1.52) * M * 5.31E-15
   return 0.47 * math.log(d)

class Convert(object):
  @classmethod
  def ToDouble(klass, x):
    return x

def reassociate_variables():
  """
  This fixes the occasional name clash in FUND.
  """
  
  from components.ClimateRegionalComponent import IClimateRegionalState
  
  IClimateRegionalState.inputtemp.name = "temp"
  IClimateRegionalState.inputtemp.machine_readable_name = "temp_1"
  