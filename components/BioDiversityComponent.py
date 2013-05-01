class IBioDiversityState(Parameters):
    nospecies = IVariable1Dimensional(
        ['Timestep', 'double'], 'Number of species')
    temp = IParameter1Dimensional(['Timestep', 'double'], 'Temperature')


class BioDiversityComponent(Behaviors):
    state_class = IBioDiversityState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (t > Timestep.FromYear(2000)):

            dt = (math.abs(s.temp[t] - s.temp[t - 1]))

            s.nospecies[t] = (math.max(
                              s.nospecbase / 100,
                              s.nospecies[t - 1] * (
                              1.0 - s.bioloss - s.biosens * dt * dt / s.dbsta / s.dbsta)
                              ))

        else:
            s.nospecies[t] = (s.nospecbase)
