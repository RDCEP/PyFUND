import argparse
from components.ExponentialGrowthTest import ExponentialGrowthTest
from components.helpers import Simulation

def main():
  sim = Simulation(components = [ ExponentialGrowthTest ], years = range(2010, 2100))
  
  for parameter in sim.all_parameters.values():
    print "{0:30}".format(parameter.identifier)
  
  print "--start sim--"
  
  sim.run_simulation()
  
  print "--done with sim--"
  
  sim.plot_values('balance')

if __name__ == '__main__':
  main()