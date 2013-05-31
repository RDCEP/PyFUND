class IImpactVectorBorneDiseasesState(Parameters):
    dengue = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    schisto = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    malaria = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    dfbs = IParameter1Dimensional(['Region', 'double'], None)
    dfch = IParameter1Dimensional(['Region', 'double'], None)
    smbs = IParameter1Dimensional(['Region', 'double'], None)
    smch = IParameter1Dimensional(['Region', 'double'], None)
    malbs = IParameter1Dimensional(['Region', 'double'], None)
    malch = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactVectorBorneDiseasesComponent(Behaviors):
    state_class = IImpactVectorBorneDiseasesState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        for r in dimensions.GetValuesOfRegion():
            ypc = (1000.0 * s.income[t, r] / s.population[t, r])
            ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

            s.dengue[t, r] = (s.dfbs[r] * s.population[t, r] * s.dfch[
                              r] * math.pow(s.temp[t, r], s.dfnl) * math.pow(ypc / ypc90, s.vbel))

            s.schisto[t, r] = (s.smbs[r] * s.population[t, r] * s.smch[
                               r] * math.pow(s.temp[t, r], s.smnl) * math.pow(ypc / ypc90, s.vbel))

            if (s.schisto[t, r] < -s.smbs[r] * s.population[t, r] * math.pow(ypc / ypc90, s.vbel)):
                s.schisto[t, r] = (-s.smbs[r] * s.population[
                                   t, r] * math.pow(ypc / ypc90, s.vbel))

            s.malaria[t, r] = (s.malbs[r] * s.population[t, r] * s.malch[
                               r] * math.pow(s.temp[t, r], s.malnl) * math.pow(ypc / ypc90, s.vbel))


behavior_classes = [ImpactVectorBorneDiseasesComponent]
