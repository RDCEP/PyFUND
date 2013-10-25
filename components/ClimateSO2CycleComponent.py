# This file was automatically generated by converter.py on
# 2013-10-25 13:47:53.406541. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IClimateSO2CycleState(Parameters):
    globso2 = IParameter1Dimensional(
        'globso2', ['Timestep'], 'double', 'Global SO2 emissions')
    acso2 = IVariable1Dimensional(
        'acso2', ['Timestep'], 'double', 'Atmospheric SO2 concentration')

    options = [globso2, acso2]


class ClimateSO2CycleComponent(Behaviors):
    state_class = IClimateSO2CycleState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            s.acso2[t] = (s.globso2[t])


behavior_classes = [ClimateSO2CycleComponent]
