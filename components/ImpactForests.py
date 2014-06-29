# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactForestsState(Parameters):
    forests = IVariable2Dimensional(
        'forests', [
            'Timestep', 'Region'], 'double', None)
    forbm = IParameter1Dimensional('forbm', ['Region'], 'double', None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    acco2 = IParameter1Dimensional('acco2', ['Timestep'], 'double', None)
    income = IParameter2Dimensional(
        'income', [
            'Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', [
            'Timestep', 'Region'], 'double', None)
    temp = IParameter2Dimensional(
        'temp', [
            'Timestep', 'Region'], 'double', None)
    forel = ScalarVariable('forel', 'double', None)
    fornl = ScalarVariable('fornl', 'double', None)
    co2pre = ScalarVariable('co2pre', 'double', None)
    forco2 = ScalarVariable('forco2', 'double', None)

    options = [
        forests,
        forbm,
        gdp90,
        pop90,
        acco2,
        income,
        population,
        temp,
        forel,
        fornl,
        co2pre,
        forco2]


class ImpactForests(Behaviors):
    state_class = IImpactForestsState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (1000.0 * s.income[t, r] / s.population[t, r])
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.forests[t, r] = (s.forbm[r] *
                                   s.income[t, r] *
                                   math.pow(ypc /
                                            ypc90, s.forel) *
                                   (0.5 *
                                    math.pow(s.temp[t, r], s.fornl) +
                                    0.5 *
                                    math.log(s.acco2[t -
                                                     1] /
                                             s.co2pre) *
                                    s.forco2))

                if (s.forests[t, r] > 0.1 * s.income[t, r]):
                    s.forests[t, r] = (0.1 * s.income[t, r])


behavior_classes = [ImpactForests]
