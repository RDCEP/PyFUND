class IImpactTropicalStormsState(Parameters):
    hurrdam = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    hurrdead = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    hurrbasedam = IParameter1Dimensional(['Region', 'double'], None)
    hurrbasedead = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    regstmp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactTropicalStormsComponent(Behaviors):
    state_class = IImpactTropicalStormsState

    def run(state, clock):

        t = (clock.Current)
        s = (state)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.hurrdam[t, r] = (0.001 * s.hurrbasedam[r] * s.income[t, r] * math.pow(
                ypc / ypc90, s.hurrdamel) * (math.pow(1.0 + s.hurrpar * s.regstmp[t, r], s.hurrnl) - 1.0))

            s.hurrdead[t, r] = (1000.0 * s.hurrbasedead[r] * s.population[t, r] * math.pow(
                ypc / ypc90, s.hurrdeadel) * (math.pow(1.0 + s.hurrpar * s.regstmp[t, r], s.hurrnl) - 1.0))


behavior_classes = [ImpactTropicalStormsComponent]
