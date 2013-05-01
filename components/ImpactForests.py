class IImpactForestsState(Parameters):
    forests = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    forbm = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    acco2 = IParameter1Dimensional(['Timestep', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactForests(Behaviors):
    state_class = IImpactForestsState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (1000.0 * s.income[t, r] / s.population[t, r])
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.forests[t, r] = (s.forbm[r] * s.income[t, r] * math.pow(ypc / ypc90, s.forel) * (
                    0.5 * math.pow(s.temp[t, r], s.fornl) + 0.5 * math.log(s.acco2[t - 1] / s.co2pre) * s.forco2))

                if (s.forests[t, r] > 0.1 * s.income[t, r]):
                    s.forests[t, r] = (0.1 * s.income[t, r])
