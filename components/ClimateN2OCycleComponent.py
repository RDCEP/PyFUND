# This file was automatically generated by converter.py on
# 2013-11-05 21:16:11.546499. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IClimateN2OCycleState(Parameters):
    globn2o = IParameter1Dimensional(
        'globn2o', ['Timestep'], 'double', 'Global N2O emissions in Mt of N')
    acn2o = IVariable1Dimensional(
        'acn2o', ['Timestep'], 'double', 'Atmospheric N2O concentration')
    n2odecay = ScalarVariable('n2odecay', 'double', 'N2O decay')
    lifen2o = ScalarVariable('lifen2o', 'Double', '')
    n2opre = ScalarVariable('n2opre', 'double', 'N2o pre industrial')

    options = [globn2o, acn2o, n2odecay, lifen2o, n2opre]


class ClimateN2OCycleComponent(Behaviors):
    state_class = IClimateN2OCycleState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.n2odecay = (1.0 / s.lifen2o)

            s.acn2o[t] = (296)

        else:

            s.acn2o[t] = (s.acn2o[t - 1] + 0.2079 * s.globn2o[
                          t] - s.n2odecay * (s.acn2o[t - 1] - s.n2opre))

            if (s.acn2o[t] < 0):
                raise ApplicationException(
                    "n2o atmospheric concentration out of range")


behavior_classes = [ClimateN2OCycleComponent]
