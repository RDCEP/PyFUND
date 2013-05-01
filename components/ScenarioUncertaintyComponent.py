class IScenarioUncertaintyState(Parameters):
    pgrowth = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    ypcgrowth = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    aeei = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    acei = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    forestemm = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    scenpgrowth = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    scenypcgrowth = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    scenaeei = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    scenacei = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    scenforestemm = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    ecgradd = IParameter1Dimensional(['Region', 'double'], None)
    pgadd = IParameter1Dimensional(['Region', 'double'], None)
    aeeiadd = IParameter1Dimensional(['Region', 'double'], None)
    aceiadd = IParameter1Dimensional(['Region', 'double'], None)
    foremadd = IParameter1Dimensional(['Region', 'double'], None)


class ScenarioUncertaintyComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        yearsFromUncertaintyStart = (t.Value - s.timeofuncertaintystart.Value)
        sdTimeFactor = ((yearsFromUncertaintyStart / 50.0) / (
            1.0 + (yearsFromUncertaintyStart / 50.0)))

        for r in dimensions.GetValuesOfRegion():

            s.ypcgrowth[t, r] = (s.scenypcgrowth[t, r] + (
                t >= s.timeofuncertaintystart and s.ecgradd[r] * sdTimeFactor or 0.0))
            s.pgrowth[t, r] = (s.scenpgrowth[t, r] + (
                t >= s.timeofuncertaintystart and s.pgadd[r] * sdTimeFactor or 0.0))
            s.aeei[t, r] = (s.scenaeei[t, r] + (
                t >= s.timeofuncertaintystart and s.aeeiadd[r] * sdTimeFactor or 0.0))
            s.acei[t, r] = (s.scenacei[t, r] + (
                t >= s.timeofuncertaintystart and s.aceiadd[r] * sdTimeFactor or 0.0))
            s.forestemm[t, r] = (s.scenforestemm[t, r] + (
                t >= s.timeofuncertaintystart and s.foremadd[r] * sdTimeFactor or 0.0))
