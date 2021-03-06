# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactTropicalStormsState(Parameters):
    hurrdam = IVariable2Dimensional(
        'hurrdam', [
            'Timestep', 'Region'], 'double', None)
    hurrdead = IVariable2Dimensional(
        'hurrdead', [
            'Timestep', 'Region'], 'double', None)
    hurrbasedam = IParameter1Dimensional(
        'hurrbasedam',
        ['Region'],
        'double',
        None)
    hurrbasedead = IParameter1Dimensional(
        'hurrbasedead',
        ['Region'],
        'double',
        None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', [
            'Timestep', 'Region'], 'double', None)
    income = IParameter2Dimensional(
        'income', [
            'Timestep', 'Region'], 'double', None)
    regstmp = IParameter2Dimensional(
        'regstmp', [
            'Timestep', 'Region'], 'double', None)
    hurrdamel = ScalarVariable('hurrdamel', 'Double', None)
    hurrnl = ScalarVariable('hurrnl', 'Double', None)
    hurrpar = ScalarVariable('hurrpar', 'Double', None)
    hurrdeadel = ScalarVariable('hurrdeadel', 'Double', None)

    options = [
        hurrdam,
        hurrdead,
        hurrbasedam,
        hurrbasedead,
        gdp90,
        pop90,
        population,
        income,
        regstmp,
        hurrdamel,
        hurrnl,
        hurrpar,
        hurrdeadel]


class ImpactTropicalStormsComponent(Behaviors):
    state_class = IImpactTropicalStormsState

    def run(self, state, clock, dimensions):

        t = (clock.Current)
        s = (state)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.hurrdam[t, r] = (0.001 *
                               s.hurrbasedam[r] *
                               s.income[t, r] *
                               math.pow(ypc /
                                        ypc90, s.hurrdamel) *
                               (math.pow(1.0 +
                                         s.hurrpar *
                                         s.regstmp[t, r], s.hurrnl) -
                                   1.0))

            s.hurrdead[t, r] = (1000.0 *
                                s.hurrbasedead[r] *
                                s.population[t, r] *
                                math.pow(ypc /
                                         ypc90, s.hurrdeadel) *
                                (math.pow(1.0 +
                                          s.hurrpar *
                                          s.regstmp[t, r], s.hurrnl) -
                                    1.0))


behavior_classes = [ImpactTropicalStormsComponent]
