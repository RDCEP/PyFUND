class IImpactExtratropicalStormsState(Parameters):
    extratropicalstormsdam = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    extratropicalstormsdead = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    extratropicalstormsbasedam = IParameter1Dimensional(
        ['Region', 'double'], None)
    extratropicalstormspar = IParameter1Dimensional(['Region', 'double'], None)
    extratropicalstormsbasedead = IParameter1Dimensional(
        ['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    acco2 = IParameter1Dimensional(['Timestep', 'double'], None)


class ImpactExtratropicalStormsComponent(Behaviors):
    state_class = IImpactExtratropicalStormsState

    def run(state, clock):

        t = (clock.Current)
        s = (state)

        for r in dimensions.GetValuesOfRegion():
            ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.extratropicalstormsdam[t, r] = (s.extratropicalstormsbasedam[r] * s.income[t, r] * math.pow(ypc / ypc90, s.extratropicalstormsdamel) * (
                math.pow(1.0 + (s.extratropicalstormspar[r] * (s.acco2[t] / s.co2pre)), s.extratropicalstormsnl) - 1.0))
            s.extratropicalstormsdead[t, r] = (1000.0 * s.extratropicalstormsbasedead[r] * s.population[t, r] * math.pow(
                ypc / ypc90, s.extratropicalstormsdeadel) * (math.pow(1.0 + (s.extratropicalstormspar[r] * (s.acco2[t] / s.co2pre)), s.extratropicalstormsnl) - 1.0))
