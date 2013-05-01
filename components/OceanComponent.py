class IOceanState(Parameters):
    sea = IVariable1Dimensional(['Timestep', 'double'], 'Sea-level rise in cm')
    temp = IParameter1Dimensional(
        ['Timestep', 'double'], 'Temperature incrase in C\xc2\xb0')


class OceanComponent(Behaviors):
    state_class = IOceanState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.delaysea = (1.0 / s.lifesea)
            s.sea[t] = (0.0)

        else:

            ds = (s.delaysea * s.seas * s.temp[t] - s.delaysea * s.sea[t - 1])

            s.sea[t] = (s.sea[t - 1] + ds)
