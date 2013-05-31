# This file was automatically generated by converter.py on
# 2013-05-31 15:40:37.716443. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IImpactExtratropicalStormsState(Parameters):
    extratropicalstormsdam = IVariable2Dimensional(
        'extratropicalstormsdam', ['Timestep', 'Region'], 'double', None)
    extratropicalstormsdead = IVariable2Dimensional(
        'extratropicalstormsdead', ['Timestep', 'Region'], 'double', None)
    extratropicalstormsbasedam = IParameter1Dimensional(
        'extratropicalstormsbasedam', ['Region'], 'double', None)
    extratropicalstormspar = IParameter1Dimensional(
        'extratropicalstormspar', ['Region'], 'double', None)
    extratropicalstormsbasedead = IParameter1Dimensional(
        'extratropicalstormsbasedead', ['Region'], 'double', None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    population = IParameter2Dimensional('population', [
                                        'Timestep', 'Region'], 'double', None)
    income = IParameter2Dimensional('income', [
                                    'Timestep', 'Region'], 'double', None)
    acco2 = IParameter1Dimensional('acco2', ['Timestep'], 'double', None)
    extratropicalstormsdamel = ScalarVariable(
        'extratropicalstormsdamel', 'Double', None)
    extratropicalstormsdeadel = ScalarVariable(
        'extratropicalstormsdeadel', 'Double', None)
    extratropicalstormsnl = ScalarVariable(
        'extratropicalstormsnl', 'Double', None)
    co2pre = ScalarVariable('co2pre', 'Double', None)

    options = [
        extratropicalstormsdam, extratropicalstormsdead, extratropicalstormsbasedam, extratropicalstormspar, extratropicalstormsbasedead,
        gdp90, pop90, population, income, acco2, extratropicalstormsdamel, extratropicalstormsdeadel, extratropicalstormsnl, co2pre]


class ImpactExtratropicalStormsComponent(Behaviors):
    state_class = IImpactExtratropicalStormsState

    def run(self, state, clock):

        t = (clock.Current)
        s = (state)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.extratropicalstormsdam[t, r] = (s.extratropicalstormsbasedam[r] * s.income[t, r] * math.pow(ypc / ypc90, s.extratropicalstormsdamel) * (
                math.pow(1.0 + (s.extratropicalstormspar[r] * (s.acco2[t] / s.co2pre)), s.extratropicalstormsnl) - 1.0))
            s.extratropicalstormsdead[t, r] = (1000.0 * s.extratropicalstormsbasedead[r] * s.population[t, r] * math.pow(
                ypc / ypc90, s.extratropicalstormsdeadel) * (math.pow(1.0 + (s.extratropicalstormspar[r] * (s.acco2[t] / s.co2pre)), s.extratropicalstormsnl) - 1.0))


behavior_classes = [ImpactExtratropicalStormsComponent]
