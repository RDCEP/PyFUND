# This file was automatically generated by converter.py on
# 2013-05-31 17:03:14.883823. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IClimateDynamicsState(Parameters):
    radforc = IParameter1Dimensional('radforc', [
                                     'Timestep'], 'double', 'Total radiative forcing')
    temp = IVariable1Dimensional('temp', [
                                 'Timestep'], 'double', 'Average global temperature')
    LifeTempConst = ScalarVariable('LifeTempConst', 'double', 'LifeTempConst')
    LifeTempLin = ScalarVariable('LifeTempLin', 'double', 'LifeTempLin')
    LifeTempQd = ScalarVariable('LifeTempQd', 'double', 'LifeTempQd')
    ClimateSensitivity = ScalarVariable(
        'ClimateSensitivity', 'double', 'Climate sensitivity')

    options = [radforc, temp, LifeTempConst,
               LifeTempLin, LifeTempQd, ClimateSensitivity]


class ClimateDynamicsComponent(Behaviors):
    state_class = IClimateDynamicsState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.temp[t] = (0.20)

        else:

            LifeTemp = (max(s.LifeTempConst + s.LifeTempLin * s.ClimateSensitivity + s.LifeTempQd * math.pow(
                s.ClimateSensitivity, 2.0), 1.0))

            delaytemp = (1.0 / LifeTemp)

            temps = (s.ClimateSensitivity / 5.35 / math.log(2.0))

            dtemp = (delaytemp * temps * s.radforc[
                     t] - delaytemp * s.temp[t - 1])

            s.temp[t] = (s.temp[t - 1] + dtemp)


behavior_classes = [ClimateDynamicsComponent]
