class IImpactBioDiversityState(Parameters):
    biodiv = IVariable1Dimensional(
        ['Timestep', 'double'], 'Change in number of species in relation to the year 2000')
    species = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    nospecies = IParameter1Dimensional(['Timestep', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    valinc = IParameter1Dimensional(['Region', 'double'], None)


class ImpactBioDiversityComponent(Behaviors):
    state_class = IImpactBioDiversityState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            s.biodiv[t] = (s.nospecbase / s.nospecies[t])

            for r in dimensions.GetValuesOfRegion():
                ypc = (1000.0 * s.income[t, r] / s.population[t, r])

                dt = (math.abs(s.temp[t, r] - s.temp[t - 1, r]))

                valadj = (s.valbase / s.valinc[
                          r] / (1 + s.valbase / s.valinc[r]))

                s.species[t, r] = (s.spbm /
                                   s.valbase * ypc / s.valinc[r] / (1.0 + ypc / s.valinc[r]) / valadj * ypc *
                                   s.population[t, r] / 1000.0 *
                                   dt / s.dbsta / (1.0 + dt / s.dbsta) *
                                   (1.0 - s.bioshare + s.bioshare * s.biodiv[t]))


behavior_classes = [ImpactBioDiversityComponent]
