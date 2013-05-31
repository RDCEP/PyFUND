class IMarginalEmissionState(Parameters):
    emission = IParameter1Dimensional(['Timestep', 'Double'], None)
    modemission = IVariable1Dimensional(['Timestep', 'Double'], None)


class MarginalEmissionComponent(Behaviors):
    state_class = IMarginalEmissionState

    def run(state, clock):

        t = (clock.Current)
        s = (state)

        if (clock.IsFirstTimestep):

            pass

        else:

            if ((t.Value >= s.emissionperiod.Value) and (t.Value < (s.emissionperiod.Value + 10))):

                s.modemission[t] = (s.emission[t] + 1)

            else:
                s.modemission[t] = (s.emission[t])


behavior_classes = [MarginalEmissionComponent]
