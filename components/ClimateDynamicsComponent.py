class IClimateDynamicsState(Parameters):
    radforc = IParameter1Dimensional(
        ['Timestep', 'double'], 'Total radiative forcing')
    temp = IVariable1Dimensional(
        ['Timestep', 'double'], 'Average global temperature')


class ClimateDynamicsComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.temp[t] = (0.20)

        else:

            LifeTemp = (math.max(s.LifeTempConst + s.LifeTempLin * s.ClimateSensitivity + s.LifeTempQd * math.pow(
                s.ClimateSensitivity, 2.0), 1.0))

            delaytemp = (1.0 / LifeTemp)

            temps = (s.ClimateSensitivity / 5.35 / math.log(2.0))

            dtemp = (delaytemp * temps * s.radforc[
                     t] - delaytemp * s.temp[t - 1])

            s.temp[t] = (s.temp[t - 1] + dtemp)
