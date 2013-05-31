# This file was automatically generated by converter.py on
# 2013-05-31 17:03:13.968789. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IClimateCH4CycleState(Parameters):
    globch4 = IParameter1Dimensional('globch4', [
                                     'Timestep'], 'double', 'Global CH4 emissions in Mt of CH4')
    acch4 = IVariable1Dimensional('acch4', [
                                  'Timestep'], 'double', 'Atmospheric CH4 concentration')
    ch4decay = ScalarVariable('ch4decay', 'double', 'CH4 decay')
    lifech4 = ScalarVariable('lifech4', 'double', '')
    ch4pre = ScalarVariable('ch4pre', 'double', 'CH4 pre industrial')

    options = [globch4, acch4, ch4decay, lifech4, ch4pre]


class ClimateCH4CycleComponent(Behaviors):
    state_class = IClimateCH4CycleState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.ch4decay = (1.0 / s.lifech4)

            s.acch4[t] = (1222.0)

        else:

            s.acch4[t] = (s.acch4[t - 1] + 0.3597 * s.globch4[
                          t] - s.ch4decay * (s.acch4[t - 1] - s.ch4pre))

            if (s.acch4[t] < 0):
                raise ApplicationException(
                    "ch4 atmospheric concentration out of range")


behavior_classes = [ClimateCH4CycleComponent]
