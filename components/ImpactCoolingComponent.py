class IImpactCoolingState(Parameters):
    cooling = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cebm = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    cumaeei = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactCoolingComponent(Behaviors):
    state_class = IImpactCoolingState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.cooling[t, r] = (s.cebm[r] * s.cumaeei[t, r] * s.gdp90[r] * math.pow(s.temp[
                                   t, r] / 1.0, s.cenl) * math.pow(ypc / ypc90, s.ceel) * s.population[t, r] / s.pop90[r])


behavior_classes = [ImpactCoolingComponent]
