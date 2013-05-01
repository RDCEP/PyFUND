class IClimateSO2CycleState(Parameters):
    globso2 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Global SO2 emissions')
    acso2 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Atmospheric SO2 concentration')


class ClimateSO2CycleComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            s.acso2[t] = (s.globso2[t])
