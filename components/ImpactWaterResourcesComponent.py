# This file was automatically generated by converter.py on
# 2013-06-01 10:58:58.647230. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactWaterResourcesState(Parameters):
    watech = IVariable1Dimensional('watech', ['Timestep'], 'double', None)
    water = IVariable2Dimensional('water', [
                                  'Timestep', 'Region'], 'double', None)
    wrbm = IParameter1Dimensional('wrbm', ['Region'], 'double', None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    income = IParameter2Dimensional('income', [
                                    'Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional('population', [
                                        'Timestep', 'Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    temp = IParameter2Dimensional('temp', [
                                  'Timestep', 'Region'], 'double', None)
    watechrate = ScalarVariable('watechrate', 'Double', None)
    wrel = ScalarVariable('wrel', 'Double', None)
    wrnl = ScalarVariable('wrnl', 'Double', None)
    wrpl = ScalarVariable('wrpl', 'Double', None)

    options = [watech, water, wrbm, gdp90, income,
               population, pop90, temp, watechrate, wrel, wrnl, wrpl]


class ImpactWaterResourcesComponent(Behaviors):
    state_class = IImpactWaterResourcesState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (t > Timestep.FromYear(2000)):
            s.watech[t] = (math.pow(
                1.0 - s.watechrate, t.Value - Timestep.FromYear(2000).Value))
        else:
            s.watech[t] = (1.0)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            water = (s.wrbm[r] * s.gdp90[r] * s.watech[t] * math.pow(ypc / ypc90, s.wrel) * math.pow(
                s.population[t, r] / s.pop90[r], s.wrpl) * math.pow(s.temp[t, r], s.wrnl))

            if (water > 0.1 * s.income[t, r]):
                s.water[t, r] = (0.1 * s.income[t, r])
            else:
                s.water[t, r] = (water)


behavior_classes = [ImpactWaterResourcesComponent]
