class IGeographyState(Parameters):
    area = IVariable2Dimensional(['Timestep', 'Region', 'double'], '')
    landloss = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    area0 = IParameter1Dimensional(['Region', 'double'], None)


class GeographyComponent(Behaviors):
    state_class = IGeographyState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.area[t, r] = (s.area0[r])

        else:

            for r in dimensions.GetValuesOfRegion():

                s.area[t, r] = (s.area[t - 1, r] - s.landloss[t - 1, r])


behavior_classes = [GeographyComponent]
