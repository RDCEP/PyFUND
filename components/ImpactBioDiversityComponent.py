# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactBioDiversityState(Parameters):
    biodiv = IVariable1Dimensional('biodiv',['Timestep'],'double','Change in number of species in relation to the year 2000')
    species = IVariable2Dimensional('species', ['Timestep', 'Region'], 'double', None)
    nospecies = IParameter1Dimensional('nospecies',['Timestep'],'double',None)
    temp = IParameter2Dimensional('temp', ['Timestep', 'Region'], 'double', None)
    income = IParameter2Dimensional('income', ['Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional('population', ['Timestep', 'Region'], 'double', None)
    valinc = IParameter1Dimensional('valinc', ['Region'], 'double', None)
    nospecbase = ScalarVariable('nospecbase', 'double','Number of species in the year 2000')
    bioshare = ScalarVariable('bioshare', 'double', None)
    spbm = ScalarVariable('spbm', 'double', None)
    valbase = ScalarVariable('valbase', 'double', None)
    dbsta = ScalarVariable('dbsta', 'double', None)

    options = [
        biodiv,
        species,
        nospecies,
        temp,
        income,
        population,
        valinc,
        nospecbase,
        bioshare,
        spbm,
        valbase,
        dbsta]


class ImpactBioDiversityComponent(Behaviors):
    state_class = IImpactBioDiversityState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            s.biodiv[t] = (s.nospecbase / s.nospecies[t])

            for r in dimensions.GetValuesOfRegion():
                ypc = (1000.0 * s.income[t, r] / s.population[t, r])

                dt = (abs(s.temp[t, r] - s.temp[t - 1, r]))

                valadj = (s.valbase / s.valinc[r] / (1 + s.valbase / s.valinc[r]))

                s.species[t, r] = (s.spbm /s.valbase * ypc / s.valinc[r] / (1.0 + ypc / s.valinc[r]) /
                                    valadj * ypc * s.population[t, r] / 1000.0 * dt / s.dbsta / (1.0 + dt /
                                    s.dbsta) * (1.0 - s.bioshare + s.bioshare * s.biodiv[t]))


behavior_classes = [ImpactBioDiversityComponent]
