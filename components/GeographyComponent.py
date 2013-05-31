# This file was automatically generated by converter.py on
# 2013-05-31 17:03:20.545185. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IGeographyState(Parameters):
    area = IVariable2Dimensional('area', ['Timestep', 'Region'], 'double', '')
    landloss = IParameter2Dimensional('landloss', [
                                      'Timestep', 'Region'], 'double', None)
    area0 = IParameter1Dimensional('area0', ['Region'], 'double', None)

    options = [area, landloss, area0]


class GeographyComponent(Behaviors):
    state_class = IGeographyState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.area[t, r] = (s.area0[r])

        else:

            for r in dimensions.GetValuesOfRegion():

                s.area[t, r] = (s.area[t - 1, r] - s.landloss[t - 1, r])


behavior_classes = [GeographyComponent]
