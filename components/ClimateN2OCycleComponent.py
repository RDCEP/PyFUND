class IClimateN2OCycleState(Parameters):
    globn2o = IParameter1Dimensional(
        ['Timestep', 'double'], 'Global N2O emissions in Mt of N')
    acn2o = IVariable1Dimensional(
        ['Timestep', 'double'], 'Atmospheric N2O concentration')


class ClimateN2OCycleComponent(Behaviors):
    state_class = IClimateN2OCycleState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.n2odecay = (1.0 / s.lifen2o)

            s.acn2o[t] = (296)

        else:

            s.acn2o[t] = (s.acn2o[t - 1] + 0.2079 * s.globn2o[
                          t] - s.n2odecay * (s.acn2o[t - 1] - s.n2opre))

            if (s.acn2o[t] < 0):
                raise ApplicationException(
                    "n2o atmospheric concentration out of range")


behavior_classes = [ClimateN2OCycleComponent]
