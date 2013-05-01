class IImpactDiarrhoeaState(Parameters):
    diadead = IVariable2Dimensional(['Timestep', 'Region', 'Double'], None)
    diasick = IVariable2Dimensional(['Timestep', 'Region', 'Double'], None)
    diamort = IParameter1Dimensional(['Region', 'Double'], None)
    diayld = IParameter1Dimensional(['Region', 'Double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'Double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'Double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'Double'], None)
    pop90 = IParameter1Dimensional(['Region', 'Double'], None)
    temp90 = IParameter1Dimensional(['Region', 'Double'], None)
    bregtmp = IParameter1Dimensional(['Region', 'Double'], None)
    regtmp = IParameter2Dimensional(['Timestep', 'Region', 'Double'], None)


class ImpactDiarrhoeaComponent(Behaviors):
    state_class = IImpactDiarrhoeaState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        for r in dimensions.GetValuesOfRegion():

            ypc = (1000.0 * s.income[t, r] / s.population[t, r])
            ypc90 = (1000.0 * s.gdp90[r] / s.pop90[r])

            absoluteRegionalTempPreIndustrial = (
                s.temp90[r] - 0.49 * s.bregtmp[r])

            if (absoluteRegionalTempPreIndustrial > 0.0):

                s.diadead[t, r] = (s.diamort[r] * s.population[t, r] * math.pow(ypc / ypc90, s.diamortel)
                                   * (math.pow((absoluteRegionalTempPreIndustrial + s.regtmp[t, r]) / absoluteRegionalTempPreIndustrial, s.diamortnl) - 1.0))

                s.diasick[t, r] = (s.diayld[r] * s.population[t, r] * math.pow(ypc / ypc90, s.diayldel)
                                   * (math.pow((absoluteRegionalTempPreIndustrial + s.regtmp[t, r]) / absoluteRegionalTempPreIndustrial, s.diayldnl) - 1.0))

            else:

                s.diadead[t, r] = (0.0)
                s.diasick[t, r] = (0.0)
