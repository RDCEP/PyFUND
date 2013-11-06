# This file was automatically generated by converter.py on
# 2013-11-05 21:16:17.610595. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactAgricultureState(Parameters):
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    income = IParameter2Dimensional(
        'income', ['Timestep', 'Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', ['Timestep', 'Region'], 'double', None)
    agrish = IVariable2Dimensional(
        'agrish', ['Timestep', 'Region'], 'double', None)
    agrish0 = IParameter1Dimensional('agrish0', ['Region'], 'double', None)
    agrate = IVariable2Dimensional(
        'agrate', ['Timestep', 'Region'], 'double', None)
    aglevel = IVariable2Dimensional(
        'aglevel', ['Timestep', 'Region'], 'double', None)
    agco2 = IVariable2Dimensional(
        'agco2', ['Timestep', 'Region'], 'double', None)
    agcost = IVariable2Dimensional(
        'agcost', ['Timestep', 'Region'], 'double', None)
    agrbm = IParameter1Dimensional('agrbm', ['Region'], 'double', None)
    agtime = IParameter1Dimensional('agtime', ['Region'], 'double', None)
    aglparl = IParameter1Dimensional('aglparl', ['Region'], 'double', None)
    aglparq = IParameter1Dimensional('aglparq', ['Region'], 'double', None)
    agcbm = IParameter1Dimensional('agcbm', ['Region'], 'double', None)
    temp = IParameter2Dimensional(
        'temp', ['Timestep', 'Region'], 'double', None)
    acco2 = IParameter1Dimensional('acco2', ['Timestep'], 'double', None)
    agel = ScalarVariable('agel', 'Double', None)
    agnl = ScalarVariable('agnl', 'Double', None)
    co2pre = ScalarVariable('co2pre', 'Double', None)

    options = [
        gdp90, income, pop90, population, agrish, agrish0, agrate, aglevel, agco2,
        agcost, agrbm, agtime, aglparl, aglparq, agcbm, temp, acco2, agel, agnl, co2pre]


class ImpactAgricultureComponent(Behaviors):
    state_class = IImpactAgricultureState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.agrate[t, r] = (
                    s.agrbm[r] * math.pow(0.005 / DBsT, s.agnl) * s.agtime[r])

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.agrish[t, r] = (
                    s.agrish0[r] * math.pow(ypc / ypc90, -s.agel))

            for r in dimensions.GetValuesOfRegion():

                dtemp = (abs(s.temp[t, r] - s.temp[t - 1, r]))

                if (math.isnan(math.pow(dtemp / 0.04, s.agnl))):
                    s.agrate[t, r] = (0.0)
                else:
                    s.agrate[t, r] = (s.agrbm[r] * math.pow(
                        dtemp / 0.04, s.agnl) + (1.0 - 1.0 / s.agtime[r]) * s.agrate[t - 1, r])

            for r in dimensions.GetValuesOfRegion():

                s.aglevel[t, r] = (s.aglparl[r] * s.temp[
                                   t, r] + s.aglparq[r] * math.pow(s.temp[t, r], 2.0))

            for r in dimensions.GetValuesOfRegion():

                s.agco2[t, r] = (s.agcbm[r] / math.log(
                    2.0) * math.log(s.acco2[t - 1] / s.co2pre))

            for r in dimensions.GetValuesOfRegion():

                s.agcost[t, r] = (
                    min(1.0, s.agrate[t, r] + s.aglevel[t, r] + s.agco2[t, r]) * s.agrish[t, r] * s.income[t, r])


behavior_classes = [ImpactAgricultureComponent]
