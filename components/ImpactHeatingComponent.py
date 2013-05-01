class IImpactHeatingState(Parameters):
    heating = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    hebm = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    cumaeei = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactHeatingComponent(Behaviors):
    state_class = IImpactHeatingState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.heating[t, r] = (s.hebm[r] * s.cumaeei[t, r] * s.gdp90[r] * math.atan(s.temp[
                                   t, r]) / math.atan(1.0) * math.pow(ypc / ypc90, s.heel) * s.population[t, r] / s.pop90[r])
