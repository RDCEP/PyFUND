import argparse
from components.ExponentialGrowthTest import ExponentialGrowthTest
from components.helpers import Simulation

def main():
  sim = Simulation(components = [ ExponentialGrowthTest ], years = range(2010, 2100))
  
  for component, parameter in sim.all_parameters:
    print "{0:30} {1}".format(component.__class__.__name__, parameter.identifier)
  
  sim.run_simulation()

if __name__ == '__main__':
  main()