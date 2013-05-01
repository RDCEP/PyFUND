class IClimateRegionalState(Parameters):
    inputtemp = IParameter1Dimensional(['Timestep', 'Double'], None)
    bregtmp = IParameter1Dimensional(['Region', 'Double'], None)
    bregstmp = IParameter1Dimensional(['Region', 'Double'], None)
    scentemp = IParameter2Dimensional(['Timestep', 'Region', 'Double'], None)
    temp = IVariable2Dimensional(['Timestep', 'Region', 'Double'], None)
    regtmp = IVariable2Dimensional(['Timestep', 'Region', 'Double'], None)
    regstmp = IVariable2Dimensional(['Timestep', 'Region', 'Double'], None)


class ClimateRegionalComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        for r in dimensions.GetValuesOfRegion():

            s.regtmp[t, r] = (s.inputtemp[t] * s.bregtmp[r] + s.scentemp[t, r])

        for r in dimensions.GetValuesOfRegion():

            s.temp[t, r] = (s.regtmp[t, r] / s.bregtmp[r])

        for r in dimensions.GetValuesOfRegion():

            s.regstmp[t, r] = (s.inputtemp[
                               t] * s.bregstmp[r] + s.scentemp[t, r])
