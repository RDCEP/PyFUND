# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactDeathMorbidityState(Parameters):
    dead = IVariable2Dimensional(
        'dead', [
            'Timestep', 'Region'], 'double', None)
    yll = IVariable2Dimensional('yll', ['Timestep', 'Region'], 'double', None)
    yld = IVariable2Dimensional('yld', ['Timestep', 'Region'], 'double', None)
    deadcost = IVariable2Dimensional(
        'deadcost', [
            'Timestep', 'Region'], 'double', None)
    morbcost = IVariable2Dimensional(
        'morbcost', [
            'Timestep', 'Region'], 'double', None)
    vsl = IVariable2Dimensional('vsl', ['Timestep', 'Region'], 'double', None)
    vmorb = IVariable2Dimensional(
        'vmorb', [
            'Timestep', 'Region'], 'double', None)
    d2ld = IParameter1Dimensional('d2ld', ['Region'], 'double', None)
    d2ls = IParameter1Dimensional('d2ls', ['Region'], 'double', None)
    d2lm = IParameter1Dimensional('d2lm', ['Region'], 'double', None)
    d2lc = IParameter1Dimensional('d2lc', ['Region'], 'double', None)
    d2lr = IParameter1Dimensional('d2lr', ['Region'], 'double', None)
    d2dd = IParameter1Dimensional('d2dd', ['Region'], 'double', None)
    d2ds = IParameter1Dimensional('d2ds', ['Region'], 'double', None)
    d2dm = IParameter1Dimensional('d2dm', ['Region'], 'double', None)
    d2dc = IParameter1Dimensional('d2dc', ['Region'], 'double', None)
    d2dr = IParameter1Dimensional('d2dr', ['Region'], 'double', None)
    dengue = IParameter2Dimensional(
        'dengue', [
            'Timestep', 'Region'], 'double', None)
    schisto = IParameter2Dimensional(
        'schisto', [
            'Timestep', 'Region'], 'double', None)
    malaria = IParameter2Dimensional(
        'malaria', [
            'Timestep', 'Region'], 'double', None)
    cardheat = IParameter2Dimensional(
        'cardheat', [
            'Timestep', 'Region'], 'double', None)
    cardcold = IParameter2Dimensional(
        'cardcold', [
            'Timestep', 'Region'], 'double', None)
    resp = IParameter2Dimensional(
        'resp', [
            'Timestep', 'Region'], 'double', None)
    diadead = IParameter2Dimensional(
        'diadead', [
            'Timestep', 'Region'], 'double', None)
    hurrdead = IParameter2Dimensional(
        'hurrdead', [
            'Timestep', 'Region'], 'double', None)
    extratropicalstormsdead = IParameter2Dimensional(
        'extratropicalstormsdead', [
            'Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', [
            'Timestep', 'Region'], 'double', None)
    diasick = IParameter2Dimensional(
        'diasick', [
            'Timestep', 'Region'], 'double', None)
    income = IParameter2Dimensional(
        'income', [
            'Timestep', 'Region'], 'double', None)
    vslbm = ScalarVariable('vslbm', 'double', None)
    vslel = ScalarVariable('vslel', 'double', None)
    vmorbbm = ScalarVariable('vmorbbm', 'double', None)
    vmorbel = ScalarVariable('vmorbel', 'double', None)
    vslypc0 = ScalarVariable('vslypc0', 'double', None)
    vmorbypc0 = ScalarVariable('vmorbypc0', 'double', None)

    options = [
        dead,
        yll,
        yld,
        deadcost,
        morbcost,
        vsl,
        vmorb,
        d2ld,
        d2ls,
        d2lm,
        d2lc,
        d2lr,
        d2dd,
        d2ds,
        d2dm,
        d2dc,
        d2dr,
        dengue,
        schisto,
        malaria,
        cardheat,
        cardcold,
        resp,
        diadead,
        hurrdead,
        extratropicalstormsdead,
        population,
        diasick,
        income,
        vslbm,
        vslel,
        vmorbbm,
        vmorbel,
        vslypc0,
        vmorbypc0]


class ImpactDeathMorbidityComponent(Behaviors):
    state_class = IImpactDeathMorbidityState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)

                s.dead[t, r] = (s.dengue[t, r] +
                                s.schisto[t, r] +
                                s.malaria[t, r] +
                                s.cardheat[t, r] +
                                s.cardcold[t, r] +
                                s.resp[t, r] +
                                s.diadead[t, r] +
                                s.hurrdead[t, r] +
                                s.extratropicalstormsdead[t, r])
                if (s.dead[t, r] > s.population[t, r] * 1000000.0):
                    s.dead[t, r] = (s.population[t, r] / 1000000.0)

                s.yll[
                    t,
                    r] = (
                    s.d2ld[r] *
                    s.dengue[
                        t,
                        r] +
                    s.d2ls[r] *
                    s.schisto[
                        t,
                        r] +
                    s.d2lm[r] *
                    s.malaria[
                        t,
                        r] +
                    s.d2lc[r] *
                    s.cardheat[
                        t,
                        r] +
                    s.d2lc[r] *
                    s.cardcold[
                        t,
                        r] +
                    s.d2lr[r] *
                    s.resp[
                        t,
                        r])

                s.yld[t, r] = (s.d2dd[r] *
                               s.dengue[t, r] +
                               s.d2ds[r] *
                               s.schisto[t, r] +
                               s.d2dm[r] *
                               s.malaria[t, r] +
                               s.d2dc[r] *
                               s.cardheat[t, r] +
                               s.d2dc[r] *
                               s.cardcold[t, r] +
                               s.d2dr[r] *
                               s.resp[t, r] +
                               s.diasick[t, r])

                s.vsl[t, r] = (s.vslbm * math.pow(ypc / s.vslypc0, s.vslel))
                s.deadcost[t, r] = (s.vsl[t, r] * s.dead[t, r] / 1000000000.0)

                s.vmorb[
                    t,
                    r] = (
                    s.vmorbbm *
                    math.pow(
                        ypc /
                        s.vmorbypc0,
                        s.vmorbel))
                s.morbcost[t, r] = (s.vmorb[t, r] * s.yld[t, r] / 1000000000.0)


behavior_classes = [ImpactDeathMorbidityComponent]
