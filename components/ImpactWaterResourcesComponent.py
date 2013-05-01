class IImpactWaterResourcesState(Parameters):
    watech = IVariable1Dimensional(['Timestep', 'double'], None)
    water = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    wrbm = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactWaterResourcesComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (t > Timestep.FromYear(2000)):
            s.watech[t] = (math.pow(
                1.0 - s.watechrate, t.Value - Timestep.FromYear(2000).Value))
        else:
            s.watech[t] = (1.0)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            water = (s.wrbm[r] * s.gdp90[r] * s.watech[t] * math.pow(ypc / ypc90, s.wrel) * math.pow(
                s.population[t, r] / s.pop90[r], s.wrpl) * math.pow(s.temp[t, r], s.wrnl))

            if (water > 0.1 * s.income[t, r]):
                s.water[t, r] = (0.1 * s.income[t, r])
            else:
                s.water[t, r] = (water)
