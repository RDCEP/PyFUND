# This file was automatically generated by converter.py on
# 2013-05-31 17:48:36.588361. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IClimateSF6CycleState(Parameters):
    globsf6 = IParameter1Dimensional('globsf6', [
                                     'Timestep'], 'double', 'Global SF6 emissions in kt of SF6')
    acsf6 = IVariable1Dimensional('acsf6', [
                                  'Timestep'], 'double', 'Atmospheric SF6 concentrations')
    sf6pre = ScalarVariable('sf6pre', 'double', 'SF6 pre industrial')
    sf6decay = ScalarVariable('sf6decay', 'double', 'SF6 decay')
    lifesf6 = ScalarVariable('lifesf6', 'double', '')

    options = [globsf6, acsf6, sf6pre, sf6decay, lifesf6]


class ClimateSF6CycleComponent(Behaviors):
    state_class = IClimateSF6CycleState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.sf6decay = (1.0 / s.lifesf6)

            s.acsf6[t] = (s.sf6pre)

        else:

            s.acsf6[t] = (s.sf6pre + (s.acsf6[t - 1] - s.sf6pre) * (
                1 - s.sf6decay) + s.globsf6[t] / 25.1)

            if (s.acsf6[t] < 0):
                raise ApplicationException(
                    "sf6 atmospheric concentration out of range")


behavior_classes = [ClimateSF6CycleComponent]
