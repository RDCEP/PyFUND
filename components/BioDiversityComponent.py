# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IBioDiversityState(Parameters):
    nospecies = IVariable1Dimensional(
        'nospecies',
        ['Timestep'],
        'double',
        'Number of species')
    temp = IParameter1Dimensional(
        'temp',
        ['Timestep'],
        'double',
        'Temperature')
    bioloss = ScalarVariable('bioloss', 'double', 'additive parameter')
    biosens = ScalarVariable('biosens', 'double', 'multiplicative parameter')
    dbsta = ScalarVariable('dbsta', 'double', 'benchmark temperature change')
    nospecbase = ScalarVariable(
        'nospecbase',
        'double',
        'Number of species in the year 2000')

    options = [nospecies, temp, bioloss, biosens, dbsta, nospecbase]


class BioDiversityComponent(Behaviors):
    state_class = IBioDiversityState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (t > Timestep.FromYear(2000)):

            dt = (abs(s.temp[t] - s.temp[t - 1]))

            s.nospecies[t] = (max(
                s.nospecbase / 100,
                s.nospecies[
                    t - 1] * (1.0 - s.bioloss - s.biosens * dt * dt / s.dbsta / s.dbsta)
            ))

        else:
            s.nospecies[t] = (s.nospecbase)


behavior_classes = [BioDiversityComponent]
