class IClimateCH4CycleState(Parameters):
    globch4 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Global CH4 emissions in Mt of CH4')
    acch4 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Atmospheric CH4 concentration')


class ClimateCH4CycleComponent(Behaviors):
    state_class = IClimateCH4CycleState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.ch4decay = (1.0 / s.lifech4)

            s.acch4[t] = (1222.0)

        else:

            s.acch4[t] = (s.acch4[t - 1] + 0.3597 * s.globch4[
                          t] - s.ch4decay * (s.acch4[t - 1] - s.ch4pre))

            if (s.acch4[t] < 0):
                raise ApplicationException(
                    "ch4 atmospheric concentration out of range")


behavior_classes = [ClimateCH4CycleComponent]
