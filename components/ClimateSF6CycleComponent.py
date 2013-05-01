class IClimateSF6CycleState(Parameters):
    globsf6 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Global SF6 emissions in kt of SF6')
    acsf6 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Atmospheric SF6 concentrations')


class ClimateSF6CycleComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.sf6decay = (1.0 / s.lifesf6)

            s.acsf6[t] = (s.sf6pre)

        else:

            s.acsf6[t] = (s.sf6pre + (s.acsf6[t - 1] - s.sf6pre) * (
                1 - s.sf6decay) + s.globsf6[t] / 25.1)

            if (s.acsf6[t] < 0):
                raise ApplicationException(
                    "sf6 atmospheric concentration out of range")
