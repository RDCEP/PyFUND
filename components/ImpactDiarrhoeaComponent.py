# This file was automatically generated by converter.py on
# 2013-05-31 15:40:37.236867. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IImpactDiarrhoeaState(Parameters):
    diadead = IVariable2Dimensional('diadead', [
                                    'Timestep', 'Region'], 'Double', None)
    diasick = IVariable2Dimensional('diasick', [
                                    'Timestep', 'Region'], 'Double', None)
    diamort = IParameter1Dimensional('diamort', ['Region'], 'Double', None)
    diayld = IParameter1Dimensional('diayld', ['Region'], 'Double', None)
    income = IParameter2Dimensional('income', [
                                    'Timestep', 'Region'], 'Double', None)
    population = IParameter2Dimensional('population', [
                                        'Timestep', 'Region'], 'Double', None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'Double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'Double', None)
    temp90 = IParameter1Dimensional('temp90', ['Region'], 'Double', None)
    bregtmp = IParameter1Dimensional('bregtmp', ['Region'], 'Double', None)
    regtmp = IParameter2Dimensional('regtmp', [
                                    'Timestep', 'Region'], 'Double', None)
    diamortel = ScalarVariable('diamortel', 'Double', None)
    diamortnl = ScalarVariable('diamortnl', 'Double', None)
    diayldel = ScalarVariable('diayldel', 'Double', None)
    diayldnl = ScalarVariable('diayldnl', 'Double', None)

    options = [diadead, diasick, diamort, diayld, income, population, gdp90,
               pop90, temp90, bregtmp, regtmp, diamortel, diamortnl, diayldel, diayldnl]


class ImpactDiarrhoeaComponent(Behaviors):
    state_class = IImpactDiarrhoeaState

    def run(self, state, clock):

        s = (state)
        t = (clock.Current)

        for r in dimensions.GetValuesOfRegion():

            ypc = (1000.0 * s.income[t, r] / s.population[t, r])
            ypc90 = (1000.0 * s.gdp90[r] / s.pop90[r])

            absoluteRegionalTempPreIndustrial = (
                s.temp90[r] - 0.49 * s.bregtmp[r])

            if (absoluteRegionalTempPreIndustrial > 0.0):

                s.diadead[t, r] = (s.diamort[r] * s.population[t, r] * math.pow(ypc / ypc90, s.diamortel)
                                   * (math.pow((absoluteRegionalTempPreIndustrial + s.regtmp[t, r]) / absoluteRegionalTempPreIndustrial, s.diamortnl) - 1.0))

                s.diasick[t, r] = (s.diayld[r] * s.population[t, r] * math.pow(ypc / ypc90, s.diayldel)
                                   * (math.pow((absoluteRegionalTempPreIndustrial + s.regtmp[t, r]) / absoluteRegionalTempPreIndustrial, s.diayldnl) - 1.0))

            else:

                s.diadead[t, r] = (0.0)
                s.diasick[t, r] = (0.0)


behavior_classes = [ImpactDiarrhoeaComponent]
