# This file was automatically generated by converter.py on
# 2013-05-31 13:51:10.745417. Think long and hard before
# attempting to modify it.

from components.helpers import *


class IMarginalEmissionState(Parameters):
    emission = IParameter1Dimensional('emission', ['Timestep'], 'Double', None)
    modemission = IVariable1Dimensional(
        'modemission', ['Timestep'], 'Double', None)

    options = [emission, modemission]


class MarginalEmissionComponent(Behaviors):
    state_class = IMarginalEmissionState

    def run(self, state, clock):

        t = (clock.Current)
        s = (state)

        if (clock.IsFirstclock):

            pass

        else:

            if ((t.Value >= s.emissionperiod.Value) and (t.Value < (s.emissionperiod.Value + 10))):

                s.modemission[t] = (s.emission[t] + 1)

            else:
                s.modemission[t] = (s.emission[t])


behavior_classes = [MarginalEmissionComponent]
