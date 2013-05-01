class IPopulationState(Parameters):
    population = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    populationin1 = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    globalpopulation = IVariable1Dimensional(['Timestep', 'double'], None)
    pgrowth = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    enter = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    leave = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    dead = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    pop0 = IParameter1Dimensional(['Region', 'double'], None)


class PopulationComponent(Behaviors):
    state_class = IPopulationState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):
            globalpopulation = (0.0)

            for r in dimensions.GetValuesOfRegion():

                s.population[t, r] = (s.pop0[r])
                s.populationin1[t, r] = (s.population[t, r] * 1000000.0)

                globalpopulation = (globalpopulation + s.populationin1[t, r])

            s.globalpopulation[t] = (globalpopulation)

        else:

            globalPopulation = (0.0)

            for r in dimensions.GetValuesOfRegion():

                s.population[t, r] = ((1.0 + 0.01 * s.pgrowth[t - 1, r]) * (s.population[t - 1, r] +
                                     (
                                                                            (t >= Timestep.FromSimulationYear(40)) and not s.runwithoutpopulationperturbation and (s.enter[t - 1, r] / 1000000.0) - (
                                                                            s.leave[t - 1, r] / 1000000.0) - (s.dead[t - 1, r] >= 0 and s.dead[t - 1, r] / 1000000.0 or 0) or 0
                                                                            )
                                                                            ))

                if (s.population[t, r] < 0):
                    s.population[t, r] = (0.000001)

                s.populationin1[t, r] = (s.population[t, r] * 1000000.0)
                globalPopulation = (globalPopulation + s.populationin1[t, r])

            s.globalpopulation[t] = (globalPopulation)
