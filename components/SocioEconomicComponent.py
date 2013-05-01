class ISocioEconomicState(Parameters):
    income = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    consumption = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    ypc = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    ygrowth = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    plus = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    urbpop = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    popdens = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    globalconsumption = IVariable1Dimensional(['Timestep', 'double'], None)
    globalypc = IVariable1Dimensional(['Timestep', 'double'], None)
    globalincome = IVariable1Dimensional(['Timestep', 'double'], None)
    ypc90 = IVariable1Dimensional(['Region', 'double'], None)
    pgrowth = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    ypcgrowth = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    eloss = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    sloss = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    mitigationcost = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    area = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    globalpopulation = IParameter1Dimensional(['Timestep', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    populationin1 = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    plus90 = IParameter1Dimensional(['Region', 'double'], None)
    gdp90 = IParameter1Dimensional(['Region', 'double'], None)
    pop90 = IParameter1Dimensional(['Region', 'double'], None)
    urbcorr = IParameter1Dimensional(['Region', 'double'], None)
    gdp0 = IParameter1Dimensional(['Region', 'double'], None)


class SocioEconomicComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        savingsrate = (0.2)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.income[t, r] = (s.gdp0[r])
                s.ypc[t, r] = (s.income[t, r] / s.population[t, r] * 1000.0)
                s.consumption[t, r] = (s.income[
                                       t, r] * 1000000000.0 * (1.0 - savingsrate))

            s.globalconsumption[t] = (dimensions.GetValuesOfRegion().Select(
                lambda r: s.consumption[t, r]).Sum())

            for r in dimensions.GetValuesOfRegion():

                s.ypc90[r] = (s.gdp90[r] / s.pop90[r] * 1000)

        else:

            for r in dimensions.GetValuesOfRegion():

                s.ygrowth[t, r] = ((1 + 0.01 * s.pgrowth[
                                   t - 1, r]) * (1 + 0.01 * s.ypcgrowth[t - 1, r]) - 1)

            for r in dimensions.GetValuesOfRegion():
                oldincome = (s.income[t - 1, r] - ((t >= Timestep.FromSimulationYear(
                    40)) and not s.runwithoutdamage and s.consleak * s.eloss[t - 1, r] / 10.0 or 0))

                s.income[t, r] = ((1 + s.ygrowth[
                                  t, r]) * oldincome - s.mitigationcost[t - 1, r])

            for r in dimensions.GetValuesOfRegion():

                if (s.income[t, r] < 0.01 * s.population[t, r]):
                    s.income[t, r] = (0.1 * s.population[t, r])

            for r in dimensions.GetValuesOfRegion():

                s.ypc[t, r] = (s.income[t, r] / s.population[t, r] * 1000.0)

            totalConsumption = (0.0)
            for r in dimensions.GetValuesOfRegion():

                s.consumption[t, r] = (math.max(
                    s.income[t, r] * 1000000000.0 * (1.0 - savingsrate) - (s.runwithoutdamage and 0.0 or (
                        s.eloss[t - 1, r] + s.sloss[t - 1, r]) * 1000000000.0),
                    0.0))

                totalConsumption = (totalConsumption + s.consumption[t, r])

            s.globalconsumption[t] = (totalConsumption)

            for r in dimensions.GetValuesOfRegion():

                s.plus[t, r] = (s.plus90[r] * math.pow(
                    s.ypc[t, r] / s.ypc90[r], s.plusel))

                if (s.plus[t, r] > 1):
                    s.plus[t, r] = (1.0)

            for r in dimensions.GetValuesOfRegion():

                s.popdens[t, r] = (s.population[
                                   t, r] / s.area[t, r] * 1000000.0)

            for r in dimensions.GetValuesOfRegion():

                s.urbpop[t, r] = ((0.031 * math.sqrt(s.ypc[t, r]) - 0.011 * math.sqrt(s.popdens[t, r])) / (1.0 + 0.031 * math.sqrt(s.ypc[t, r]) - 0.011 * math.sqrt(s.popdens[t, r]))
                                  / (1 + s.urbcorr[r] / (1 + 0.001 * math.pow(Convert.ToDouble(t.Value) - 40.0, 2))))

            s.globalincome[t] = (dimensions.GetValuesOfRegion().Select(
                lambda r: s.income[t, r]).Sum())

            s.globalypc[t] = (dimensions.GetValuesOfRegion().Select(lambda r: s.income[t, r] * 1000000000.0).Sum() /
                              dimensions.GetValuesOfRegion().Select(lambda r: s.populationin1[t, r]).Sum())
