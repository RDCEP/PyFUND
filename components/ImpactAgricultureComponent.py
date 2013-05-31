class IImpactAgricultureState(Parameters):
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    agrish = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    agrish0 = IParameter1Dimensional(['Region', 'double'], None)
    agrate = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    aglevel = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    agco2 = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    agcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    agrbm = IParameter1Dimensional(['Region', 'double'], None)
    agtime = IParameter1Dimensional(['Region', 'double'], None)
    aglparl = IParameter1Dimensional(['Region', 'double'], None)
    aglparq = IParameter1Dimensional(['Region', 'double'], None)
    agcbm = IParameter1Dimensional(['Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    acco2 = IParameter1Dimensional(['Timestep', 'double'], None)


class ImpactAgricultureComponent(Behaviors):
    state_class = IImpactAgricultureState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.agrate[t, r] = (s.agrbm[r] * math.pow(
                    0.005 / DBsT, s.agnl) * s.agtime[r])

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                ypc90 = (s.gdp90[r] / s.pop90[r] * 1000.0)

                s.agrish[t, r] = (s.agrish0[
                                  r] * math.pow(ypc / ypc90, -s.agel))

            for r in dimensions.GetValuesOfRegion():

                dtemp = (math.abs(s.temp[t, r] - s.temp[t - 1, r]))

                if (double.IsNaN(math.pow(dtemp / 0.04, s.agnl))):
                    s.agrate[t, r] = (0.0)
                else:
                    s.agrate[t, r] = (s.agrbm[r] * math.pow(dtemp / 0.04, s.agnl) + (
                        1.0 - 1.0 / s.agtime[r]) * s.agrate[t - 1, r])

            for r in dimensions.GetValuesOfRegion():

                s.aglevel[t, r] = (s.aglparl[r] * s.temp[
                                   t, r] + s.aglparq[r] * math.pow(s.temp[t, r], 2.0))

            for r in dimensions.GetValuesOfRegion():

                s.agco2[t, r] = (s.agcbm[r] / math.log(
                    2.0) * math.log(s.acco2[t - 1] / s.co2pre))

            for r in dimensions.GetValuesOfRegion():

                s.agcost[t, r] = (math.min(1.0, s.agrate[t, r] + s.aglevel[
                                  t, r] + s.agco2[t, r]) * s.agrish[t, r] * s.income[t, r])


behavior_classes = [ImpactAgricultureComponent]
