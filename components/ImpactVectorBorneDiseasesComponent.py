# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactVectorBorneDiseasesState(Parameters):
    dengue = IVariable2Dimensional(
        'dengue', [
            'Timestep', 'Region'], 'double', None)
    schisto = IVariable2Dimensional(
        'schisto', [
            'Timestep', 'Region'], 'double', None)
    malaria = IVariable2Dimensional(
        'malaria', [
            'Timestep', 'Region'], 'double', None)
    dfbs = IParameter1Dimensional('dfbs', ['Region'], 'double', None)
    dfch = IParameter1Dimensional('dfch', ['Region'], 'double', None)
    smbs = IParameter1Dimensional('smbs', ['Region'], 'double', None)
    smch = IParameter1Dimensional('smch', ['Region'], 'double', None)
    malbs = IParameter1Dimensional('malbs', ['Region'], 'double', None)
    malch = IParameter1Dimensional('malch', ['Region'], 'double', None)
    gdp90 = IParameter1Dimensional('gdp90', ['Region'], 'double', None)
    pop90 = IParameter1Dimensional('pop90', ['Region'], 'double', None)
    income = IParameter2Dimensional(
        'income', [
            'Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', [
            'Timestep', 'Region'], 'double', None)
    temp = IParameter2Dimensional(
        'temp', [
            'Timestep', 'Region'], 'double', None)
    dfnl = ScalarVariable('dfnl', 'double', None)
    vbel = ScalarVariable('vbel', 'double', None)
    smnl = ScalarVariable('smnl', 'double', None)
    malnl = ScalarVariable('malnl', 'double', None)

    options = [
        dengue,
        schisto,
        malaria,
        dfbs,
        dfch,
        smbs,
        smch,
        malbs,
        malch,
        gdp90,
        pop90,
        income,
        population,
        temp,
        dfnl,
        vbel,
        smnl,
        malnl]


class ImpactVectorBorneDiseasesComponent(Behaviors):
    state_class = IImpactVectorBorneDiseasesState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        for r in dimensions.GetValuesOfRegion():
            ypc = (1000.0 * s.income[t, r] / s.population[t, r])
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.dengue[
                t,
                r] = (
                s.dfbs[r] *
                s.population[
                    t,
                    r] *
                s.dfch[r] *
                math.pow(
                    s.temp[
                        t,
                        r],
                    s.dfnl) *
                math.pow(
                    ypc /
                    ypc90,
                    s.vbel))

            s.schisto[
                t,
                r] = (
                s.smbs[r] *
                s.population[
                    t,
                    r] *
                s.smch[r] *
                math.pow(
                    s.temp[
                        t,
                        r],
                    s.smnl) *
                math.pow(
                    ypc /
                    ypc90,
                    s.vbel))

            if (s.schisto[t, r] < -s.smbs[r] * s.population[t, r] * math.pow(ypc / ypc90, s.vbel)):
                s.schisto[t, r] = (-
                                   s.smbs[r] *
                                   s.population[t, r] *
                                   math.pow(ypc /
                                            ypc90, s.vbel))

            s.malaria[
                t,
                r] = (
                s.malbs[r] *
                s.population[
                    t,
                    r] *
                s.malch[r] *
                math.pow(
                    s.temp[
                        t,
                        r],
                    s.malnl) *
                math.pow(
                    ypc /
                    ypc90,
                    s.vbel))


behavior_classes = [ImpactVectorBorneDiseasesComponent]
