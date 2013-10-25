# This file was automatically generated by converter.py on
# 2013-10-25 13:47:53.502960. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IEmissionsState(Parameters):
    mitigationcost = IVariable2Dimensional(
        'mitigationcost', ['Timestep', 'Region'], 'double', None)
    ch4cost = IVariable2Dimensional(
        'ch4cost', ['Timestep', 'Region'], 'double', None)
    ch4costindollar = IVariable2Dimensional(
        'ch4costindollar', ['Timestep', 'Region'], 'double', None)
    n2ocost = IVariable2Dimensional(
        'n2ocost', ['Timestep', 'Region'], 'double', None)
    ryg = IVariable2Dimensional('ryg', ['Timestep', 'Region'], 'double', None)
    energint = IVariable2Dimensional(
        'energint', ['Timestep', 'Region'], 'double', None)
    emissint = IVariable2Dimensional(
        'emissint', ['Timestep', 'Region'], 'double', None)
    emission = IVariable2Dimensional(
        'emission', ['Timestep', 'Region'], 'double', None)
    emissionwithforestry = IVariable2Dimensional(
        'emissionwithforestry', ['Timestep', 'Region'], 'double', None)
    so2WithSeeiAndScei = IVariable2Dimensional(
        'so2WithSeeiAndScei', ['Timestep', 'Region'], 'double', None)
    so2 = IVariable2Dimensional('so2', ['Timestep', 'Region'], 'double', None)
    sf6 = IVariable2Dimensional('sf6', ['Timestep', 'Region'], 'double', None)
    reei = IVariable2Dimensional(
        'reei', ['Timestep', 'Region'], 'double', None)
    rcei = IVariable2Dimensional(
        'rcei', ['Timestep', 'Region'], 'double', None)
    energuse = IVariable2Dimensional(
        'energuse', ['Timestep', 'Region'], 'double', None)
    seei = IVariable2Dimensional(
        'seei', ['Timestep', 'Region'], 'double', None)
    scei = IVariable2Dimensional(
        'scei', ['Timestep', 'Region'], 'double', None)
    ch4 = IVariable2Dimensional('ch4', ['Timestep', 'Region'], 'double', None)
    n2o = IVariable2Dimensional('n2o', ['Timestep', 'Region'], 'double', None)
    n2ored = IVariable2Dimensional(
        'n2ored', ['Timestep', 'Region'], 'double', None)
    taxpar = IVariable2Dimensional(
        'taxpar', ['Timestep', 'Region'], 'double', None)
    co2red = IVariable2Dimensional(
        'co2red', ['Timestep', 'Region'], 'double', None)
    know = IVariable2Dimensional(
        'know', ['Timestep', 'Region'], 'double', None)
    perm = IVariable2Dimensional(
        'perm', ['Timestep', 'Region'], 'double', None)
    cumaeei = IVariable2Dimensional(
        'cumaeei', ['Timestep', 'Region'], 'double', None)
    ch4red = IVariable2Dimensional(
        'ch4red', ['Timestep', 'Region'], 'double', None)
    minint = IVariable1Dimensional('minint', ['Timestep'], 'double', None)
    globknow = IVariable1Dimensional('globknow', ['Timestep'], 'double', None)
    mco2 = IVariable1Dimensional('mco2', ['Timestep'], 'double', None)
    globch4 = IVariable1Dimensional('globch4', ['Timestep'], 'double', None)
    globn2o = IVariable1Dimensional('globn2o', ['Timestep'], 'double', None)
    globsf6 = IVariable1Dimensional('globsf6', ['Timestep'], 'double', None)
    globso2 = IVariable1Dimensional('globso2', ['Timestep'], 'double', None)
    cumglobco2 = IVariable1Dimensional(
        'cumglobco2', ['Timestep'], 'double', None)
    cumglobch4 = IVariable1Dimensional(
        'cumglobch4', ['Timestep'], 'double', None)
    cumglobn2o = IVariable1Dimensional(
        'cumglobn2o', ['Timestep'], 'double', None)
    cumglobsf6 = IVariable1Dimensional(
        'cumglobsf6', ['Timestep'], 'double', None)
    cumglobso2 = IVariable1Dimensional(
        'cumglobso2', ['Timestep'], 'double', None)
    taxmp = IParameter1Dimensional('taxmp', ['Region'], 'double', None)
    sf60 = IParameter1Dimensional('sf60', ['Region'], 'double', None)
    GDP90 = IParameter1Dimensional('GDP90', ['Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    ch4par1 = IParameter1Dimensional('ch4par1', ['Region'], 'double', None)
    ch4par2 = IParameter1Dimensional('ch4par2', ['Region'], 'double', None)
    n2opar1 = IParameter1Dimensional('n2opar1', ['Region'], 'double', None)
    n2opar2 = IParameter1Dimensional('n2opar2', ['Region'], 'double', None)
    gdp0 = IParameter1Dimensional('gdp0', ['Region'], 'double', None)
    emissint0 = IParameter1Dimensional('emissint0', ['Region'], 'double', None)
    so20 = IParameter1Dimensional('so20', ['Region'], 'double', None)
    forestemm = IParameter2Dimensional(
        'forestemm', ['Timestep', 'Region'], 'double', None)
    aeei = IParameter2Dimensional(
        'aeei', ['Timestep', 'Region'], 'double', None)
    acei = IParameter2Dimensional(
        'acei', ['Timestep', 'Region'], 'double', None)
    ch4em = IParameter2Dimensional(
        'ch4em', ['Timestep', 'Region'], 'double', None)
    n2oem = IParameter2Dimensional(
        'n2oem', ['Timestep', 'Region'], 'double', None)
    currtax = IParameter2Dimensional(
        'currtax', ['Timestep', 'Region'], 'double', None)
    currtaxch4 = IParameter2Dimensional(
        'currtaxch4', ['Timestep', 'Region'], 'double', None)
    currtaxn2o = IParameter2Dimensional(
        'currtaxn2o', ['Timestep', 'Region'], 'double', None)
    pgrowth = IParameter2Dimensional(
        'pgrowth', ['Timestep', 'Region'], 'double', None)
    ypcgrowth = IParameter2Dimensional(
        'ypcgrowth', ['Timestep', 'Region'], 'double', None)
    income = IParameter2Dimensional(
        'income', ['Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', ['Timestep', 'Region'], 'double', None)
    so2pop = ScalarVariable('so2pop', 'double', None)
    so2inc = ScalarVariable('so2inc', 'double', None)
    so2carb = ScalarVariable('so2carb', 'double', None)
    sf6gdp = ScalarVariable('sf6gdp', 'double', None)
    sf6ypc = ScalarVariable('sf6ypc', 'double', None)
    knowpar = ScalarVariable('knowpar', 'double', None)
    knowgpar = ScalarVariable('knowgpar', 'double', None)
    gwpch4 = ScalarVariable('gwpch4', 'double', None)
    gwpn2o = ScalarVariable('gwpn2o', 'double', None)
    TaxConstant = ScalarVariable('TaxConstant', 'double', None)
    TaxEmInt = ScalarVariable('TaxEmInt', 'double', None)
    TaxThreshold = ScalarVariable('TaxThreshold', 'double', None)
    TaxDepreciation = ScalarVariable('TaxDepreciation', 'double', None)
    MaxCostFall = ScalarVariable('MaxCostFall', 'double', None)
    ch4add = ScalarVariable('ch4add', 'double', None)
    n2oadd = ScalarVariable('n2oadd', 'double', None)
    sf6add = ScalarVariable('sf6add', 'double', None)

    options = [
        mitigationcost, ch4cost, ch4costindollar, n2ocost, ryg, energint, emissint, emission, emissionwithforestry, so2WithSeeiAndScei, so2, sf6, reei, rcei, energuse, seei, scei, ch4, n2o, n2ored, taxpar, co2red, know, perm, cumaeei, ch4red, minint, globknow, mco2, globch4, globn2o, globsf6, globso2, cumglobco2, cumglobch4, cumglobn2o, cumglobsf6, cumglobso2,
        taxmp, sf60, GDP90, pop90, ch4par1, ch4par2, n2opar1, n2opar2, gdp0, emissint0, so20, forestemm, aeei, acei, ch4em, n2oem, currtax, currtaxch4, currtaxn2o, pgrowth, ypcgrowth, income, population, so2pop, so2inc, so2carb, sf6gdp, sf6ypc, knowpar, knowgpar, gwpch4, gwpn2o, TaxConstant, TaxEmInt, TaxThreshold, TaxDepreciation, MaxCostFall, ch4add, n2oadd, sf6add]


class EmissionsComponent(Behaviors):
    state_class = IEmissionsState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            t0 = (Timestep.FromSimulationYear(0))

            for r in dimensions.GetValuesOfRegion():

                s.energint[t0, r] = (1)
                s.energuse[t0, r] = (s.gdp0[r])
                s.emissint[t0, r] = (s.emissint0[r])
                s.so2[t0, r] = (s.so20[r])
                s.emission[t0, r] = (s.emissint[t0, r] / s.energuse[t0, r])
                s.ch4cost[t0, r] = (0)
                s.n2ocost[t0, r] = (0)
                s.ryg[t0, r] = (0)
                s.reei[t0, r] = (0)
                s.rcei[t0, r] = (0)
                s.seei[t0, r] = (0)
                s.scei[t0, r] = (0)
                s.co2red[t0, r] = (0)
                s.know[t0, r] = (1)
                s.ch4red[t0, r] = (0)
                s.n2ored[t0, r] = (0)
                s.mitigationcost[t0, r] = (0)

            s.globknow[t0] = (1)
            s.cumglobco2[t0] = (0.0)
            s.cumglobch4[t0] = (0.0)
            s.cumglobn2o[t0] = (0.0)
            s.cumglobsf6[t0] = (0.0)
            s.cumglobso2[t0] = (0.0)

            minint = (float('+inf'))
            for r in dimensions.GetValuesOfRegion():

                if (s.emission[t0, r] / s.income[t0, r] < minint):
                    minint = (s.emission[t0, r] / s.income[t0, r])

            s.minint[t0] = (0)

        else:

            for r in dimensions.GetValuesOfRegion():

                s.energint[t, r] = (
                    (1.0 - 0.01 * s.aeei[t, r] - s.reei[t - 1, r]) * s.energint[t - 1, r])
                s.emissint[t, r] = (
                    (1.0 - 0.01 * s.acei[t, r] - s.rcei[t - 1, r]) * s.emissint[t - 1, r])

            for r in dimensions.GetValuesOfRegion():

                s.so2[t, r] = (s.so2[t - 1, r] *
                               math.pow(1 + 0.01 * s.pgrowth[t - 1, r], s.so2pop) *
                               math.pow(1 + 0.01 * s.ypcgrowth[t - 1, r], s.so2inc) *
                               math.pow(1 - 0.01 * s.aeei[t, r] - s.reei[t - 1, r] - 0.01 * s.acei[t, r] - s.rcei[t - 1, r], s.so2carb))

                s.so2WithSeeiAndScei[t, r] = (
                    s.so2[t, r] * (1 - s.seei[t - 1, r] - s.scei[t - 1, r]))

            for r in dimensions.GetValuesOfRegion():

                s.sf6[t, r] = ((s.sf60[r] + s.sf6gdp * (s.income[t, r] - s.GDP90[r]) + s.sf6ypc * (s.income[t - 1, r] / s.population[t - 1, r] - s.GDP90[r] / s.pop90[r])) *
                               (t <= Timestep.FromSimulationYear(60) and 1 + (t.Value - 40.0) / 40.0 or 1.0 + (60.0 - 40.0) / 40.0) * (t > Timestep.FromSimulationYear(60) and math.pow(0.99, t.Value - 60.0) or 1.0))

            for r in dimensions.GetValuesOfRegion():

                if (s.sf6[t, r] < 0.0):
                    s.sf6[t, r] = (0)

            for r in dimensions.GetValuesOfRegion():

                s.energuse[t, r] = (
                    (1 - s.seei[t - 1, r]) * s.energint[t, r] * s.income[t, r])

            for r in dimensions.GetValuesOfRegion():

                s.emission[t, r] = (
                    (1 - s.scei[t - 1, r]) * s.emissint[t, r] * s.energuse[t, r])
                s.emissionwithforestry[t, r] = (
                    s.emission[t, r] + s.forestemm[t, r])

            for r in dimensions.GetValuesOfRegion():

                s.ch4[t, r] = (s.ch4em[t, r] * (1 - s.ch4red[t - 1, r]))

            for r in dimensions.GetValuesOfRegion():

                s.n2o[t, r] = (s.n2oem[t, r] * (1 - s.n2ored[t - 1, r]))

            for r in dimensions.GetValuesOfRegion():

                if (s.emission[t, r] / s.income[t, r] - s.minint[t - 1] <= 0):
                    s.taxpar[t, r] = (s.TaxConstant)
                else:
                    s.taxpar[t, r] = (s.TaxConstant - s.TaxEmInt * math.sqrt(
                        s.emission[t, r] / s.income[t, r] - s.minint[t - 1]))

            for r in dimensions.GetValuesOfRegion():

                s.co2red[t, r] = (s.currtax[t, r] * s.emission[t, r] * s.know[
                                  t - 1, r] * s.globknow[t - 1] / 2 / s.taxpar[t, r] / s.income[t, r] / 1000)

                if (s.co2red[t, r] < 0):
                    s.co2red[t, r] = (0)
                elif (s.co2red[t, r] > 0.99):
                    s.co2red[t, r] = (0.99)

            for r in dimensions.GetValuesOfRegion():

                s.ryg[t, r] = (s.taxpar[t, r] * math.pow(
                    s.co2red[t, r], 2) / s.know[t - 1, r] / s.globknow[t - 1])

            for r in dimensions.GetValuesOfRegion():

                s.perm[t, r] = (1.0 - 1.0 / s.TaxThreshold * s.currtax[
                                t, r] / (1 + 1.0 / s.TaxThreshold * s.currtax[t, r]))

            for r in dimensions.GetValuesOfRegion():

                s.reei[t, r] = (s.perm[t, r] * 0.5 * s.co2red[t, r])

            for r in dimensions.GetValuesOfRegion():

                if (s.currtax[t, r] < s.TaxThreshold):
                    s.rcei[t, r] = (
                        s.perm[t, r] * 0.5 * math.pow(s.co2red[t, r], 2))
                else:
                    s.rcei[t, r] = (s.perm[t, r] * 0.5 * s.co2red[t, r])

            for r in dimensions.GetValuesOfRegion():

                s.seei[t, r] = ((1.0 - s.TaxDepreciation) * s.seei[
                                t - 1, r] + (1.0 - s.perm[t, r]) * 0.5 * s.co2red[t, r] * 1.7)

            for r in dimensions.GetValuesOfRegion():

                if (s.currtax[t, r] < 100):
                    s.scei[t, r] = (
                        0.9 * s.scei[t - 1, r] + (1 - s.perm[t, r]) * 0.5 * math.pow(s.co2red[t, r], 2))
                else:
                    s.scei[t, r] = (
                        0.9 * s.scei[t - 1, r] + (1 - s.perm[t, r]) * 0.5 * s.co2red[t, r] * 1.7)

            for r in dimensions.GetValuesOfRegion():

                s.know[t, r] = (
                    s.know[t - 1, r] * math.sqrt(1 + s.knowpar * s.co2red[t, r]))

                if (s.know[t, r] > math.sqrt(s.MaxCostFall)):
                    s.know[t, r] = (math.sqrt(s.MaxCostFall))

            s.globknow[t] = (s.globknow[t - 1])
            for r in dimensions.GetValuesOfRegion():

                s.globknow[t] = (
                    s.globknow[t] * math.sqrt(1 + s.knowgpar * s.co2red[t, r]))

            if (s.globknow[t] > 3.16):
                s.globknow[t] = (3.16)

            for r in dimensions.GetValuesOfRegion():

                s.ch4red[t, r] = (s.currtaxch4[t, r] * s.ch4em[t, r] / 2 / s.ch4par1[
                                  r] / s.ch4par2[r] / s.ch4par2[r] / s.income[t, r] / 1000)

                if (s.ch4red[t, r] < 0):
                    s.ch4red[t, r] = (0)
                elif (s.ch4red[t, r] > 0.99):
                    s.ch4red[t, r] = (0.99)

            for r in dimensions.GetValuesOfRegion():

                s.n2ored[t, r] = (s.gwpn2o * s.currtaxn2o[t, r] * s.n2oem[
                                  t, r] / 2 / s.n2opar1[r] / s.n2opar2[r] / s.n2opar2[r] / s.income[t, r] / 1000)

                if (s.n2ored[t, r] < 0):
                    s.n2ored[t, r] = (0)
                elif (s.n2ored[t, r] > 0.99):
                    s.n2ored[t, r] = (0.99)

            for r in dimensions.GetValuesOfRegion():

                s.ch4cost[t, r] = (s.ch4par1[r] * math.pow(
                    s.ch4par2[r], 2) * math.pow(s.ch4red[t, r], 2))
                s.ch4costindollar[t, r] = (s.ch4cost[t, r] * s.income[t, r])

            for r in dimensions.GetValuesOfRegion():

                s.n2ocost[t, r] = (s.n2opar1[r] * math.pow(
                    s.n2opar2[r], 2) * math.pow(s.n2ored[t, r], 2))

            minint = (float('+inf'))
            for r in dimensions.GetValuesOfRegion():

                if (s.emission[t, r] / s.income[t, r] < minint):
                    minint = (s.emission[t, r] / s.income[t, r])

            s.minint[t] = (minint)

            for r in dimensions.GetValuesOfRegion():

                if (t > Timestep.FromYear(2000)):
                    s.cumaeei[t, r] = (
                        s.cumaeei[t - 1, r] * (1.0 - 0.01 * s.aeei[t, r] - s.reei[t, r] + s.seei[t - 1, r] - s.seei[t, r]))
                else:
                    s.cumaeei[t, r] = (1.0)

            for r in dimensions.GetValuesOfRegion():

                s.mitigationcost[t, r] = (
                    (s.taxmp[r] * s.ryg[t, r] + s.n2ocost[t, r]) * s.income[t, r])

            globco2 = (0)
            globch4 = (0)
            globn2o = (0)
            globsf6 = (0)
            globso2 = (34.4)

            for r in dimensions.GetValuesOfRegion():

                globco2 = (globco2 + s.emissionwithforestry[t, r])
                globch4 = (globch4 + s.ch4[t, r])
                globn2o = (globn2o + s.n2o[t, r])
                globsf6 = (globsf6 + s.sf6[t, r])
                globso2 = (globso2 + s.so2WithSeeiAndScei[t, r])

            s.mco2[t] = (globco2)
            s.globch4[t] = (
                max(0.0, globch4 + (t.Value > 50 and s.ch4add * (t.Value - 50) or 0.0)))
            s.globn2o[t] = (
                max(0.0, globn2o + (t.Value > 50 and s.n2oadd * (t.Value - 50) or 0)))
            s.globsf6[t] = (
                max(0.0, globsf6 + (t.Value > 50 and s.sf6add * (t.Value - 50) or 0.0)))
            s.globso2[t] = (globso2)

            s.cumglobco2[t] = (s.cumglobco2[t - 1] + s.mco2[t])
            s.cumglobch4[t] = (s.cumglobch4[t - 1] + s.globch4[t])
            s.cumglobn2o[t] = (s.cumglobn2o[t - 1] + s.globn2o[t])
            s.cumglobsf6[t] = (s.cumglobsf6[t - 1] + s.globsf6[t])
            s.cumglobso2[t] = (s.cumglobso2[t - 1] + s.globso2[t])


behavior_classes = [EmissionsComponent]
