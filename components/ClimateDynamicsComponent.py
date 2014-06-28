# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IClimateDynamicsState(Parameters):
    radforc = IParameter1Dimensional(
        'radforc',
        ['Timestep'],
        'double',
        'Total radiative forcing')
    temp = IVariable1Dimensional(
        'temp',
        ['Timestep'],
        'double',
        'Average global temperature')
    LifeTempConst = ScalarVariable('LifeTempConst', 'double', 'LifeTempConst')
    LifeTempLin = ScalarVariable('LifeTempLin', 'double', 'LifeTempLin')
    LifeTempQd = ScalarVariable('LifeTempQd', 'double', 'LifeTempQd')
    ClimateSensitivity = ScalarVariable(
        'ClimateSensitivity',
        'double',
        'Climate sensitivity')

    options = [
        radforc,
        temp,
        LifeTempConst,
        LifeTempLin,
        LifeTempQd,
        ClimateSensitivity]


class ClimateDynamicsComponent(Behaviors):
    state_class = IClimateDynamicsState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        #print "ClimateDynamicsComponent;", t
        if (clock.IsFirstTimestep):

            s.temp[t] = (0.20)
            #print "temp;", t, ";global;", s.temp[t]
            #print "LifeTemp;", t, ";global;None"
            #print "LifeTempConst;", t, ";global;None"
            #print "LifeTempLin;", t, ";global;None"
            #print "ClimateSensitivity;", t, ";global;None"
            #print "LifeTempQd;", t, ";global;None"
            #print "delaytemp;", t, ";global;None"
            #print "temps;", t, ";global;None"
            #print "dtemp;", t, ";global;None"
            #print "radforc;", t, ";global;None"



        else:

            LifeTemp = (max(s.LifeTempConst + s.LifeTempLin * s.ClimateSensitivity + s.LifeTempQd *
                            math.pow(s.ClimateSensitivity, 2.0), 1.0))

            delaytemp = (1.0 / LifeTemp)

            temps = (s.ClimateSensitivity / 5.35 / math.log(2.0))

            dtemp = (delaytemp *temps *s.radforc[t] -delaytemp *s.temp[t -1])

            s.temp[t] = (s.temp[t - 1] + dtemp)

            #print "temp;", t, ";global;", s.temp[t]
            #print "LifeTemp;", t, ";global;", LifeTemp
            #print "LifeTempConst;", t, ";global;", s.LifeTempConst
            #print "LifeTempLin;", t, ";global;", s.LifeTempLin
            #print "ClimateSensitivity;", t, ";global;", s.ClimateSensitivity
            #print "LifeTempQd;", t, ";global;", s.LifeTempQd
            #print "delaytemp;", t, ";global;", delaytemp
            #print "temps;", t, ";global;", temps
            #print "dtemp;", t, ";global;", dtemp
            #print "radforc;", t, ";global;", s.radforc[t]




behavior_classes = [ClimateDynamicsComponent]
