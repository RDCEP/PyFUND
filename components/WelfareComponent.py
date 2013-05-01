class IGlobalWelfareState(Parameters):
    population = IParameter1Dimensional(['Timestep', 'double'], None)
    consumption = IParameter1Dimensional(['Timestep', 'double'], None)
    cummulativewelfare = IVariable1Dimensional(['Timestep', 'double'], None)
    marginalwelfare = IVariable1Dimensional(['Timestep', 'double'], None)


class IUtilitarianWelfareState(Parameters):
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    consumption = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    welfareweight = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    cummulativewelfare = IVariable1Dimensional(['Timestep', 'double'], None)
    marginalwelfare = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)


class IRegionalWelfareState(Parameters):
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    consumption = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    cummulativewelfare = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    marginalwelfare = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    totalwelfare = IVariable1Dimensional(['Region', 'double'], None)


class GlobalWelfareComponent(Behaviors):
    state_class = IGlobalWelfareState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.cummulativewelfare[t] = (0)

        else:

            if (t >= s.starttimestep):

                def U(consumption):

                    if (s.elasticityofmarginalutility == 1.0):
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.log(consumption)
                    else:
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.pow(consumption, 1.0 - s.elasticityofmarginalutility) / (1.0 - s.elasticityofmarginalutility)

                def DF(year):

                    return math.pow(1.0 + s.prtp, -(year.Value - s.starttimestep.Value))

                perCapitaConsumption = (s.consumption[t] / s.population[t])

                if (perCapitaConsumption <= 0.0):
                    perCapitaConsumption = (1.0)

                s.cummulativewelfare[t] = (s.cummulativewelfare[t - 1] + (
                    U(perCapitaConsumption) * s.population[t] * DF(t)))
                s.marginalwelfare[t] = (DF(t) * s.utilitycalibrationmultiplicative / math.pow(
                    perCapitaConsumption, s.elasticityofmarginalutility))

                if (t == s.stoptimestep):

                    s.totalwelfare = (s.cummulativewelfare[t])

            else:
                s.cummulativewelfare[t] = (0)


class UtilitarianWelfareComponent(Behaviors):
    state_class = IUtilitarianWelfareState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.cummulativewelfare[t] = (0)

        else:

            if (t >= s.starttimestep):

                w = (s.cummulativewelfare[t - 1])

                def U(consumption):

                    if (s.elasticityofmarginalutility == 1.0):
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.log(consumption)
                    else:
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.pow(consumption, 1.0 - s.elasticityofmarginalutility) / (1.0 - s.elasticityofmarginalutility)

                def DF(year):

                    return math.pow(1.0 + s.prtp, -(year.Value - s.starttimestep.Value))

                for r in dimensions.GetValuesOfRegion():

                    perCapitaConsumption = (s.consumption[
                                            t, r] / s.population[t, r])

                    if (perCapitaConsumption <= 0.0):
                        perCapitaConsumption = (1.0)

                    w = (w + (s.welfareweight[t, r] * U(
                        perCapitaConsumption) * s.population[t, r] * DF(t)))
                    s.marginalwelfare[t, r] = (DF(t) * s.welfareweight[t, r] * s.utilitycalibrationmultiplicative / math.pow(
                        perCapitaConsumption, s.elasticityofmarginalutility))

                s.cummulativewelfare[t] = (w)

                if (t == s.stoptimestep):
                    s.totalwelfare = (s.cummulativewelfare[t])

            else:
                s.cummulativewelfare[t] = (0)


class RegionalWelfareComponent(Behaviors):
    state_class = IRegionalWelfareState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.cummulativewelfare[t, r] = (0)

        else:

            if (t >= s.starttimestep):

                def U(consumption):

                    if (s.elasticityofmarginalutility == 1.0):
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.log(consumption)
                    else:
                        return s.utilitycalibrationadditive + s.utilitycalibrationmultiplicative * math.pow(consumption, 1.0 - s.elasticityofmarginalutility) / (1.0 - s.elasticityofmarginalutility)

                def DF(year):

                    return math.pow(1.0 + s.prtp, -(year.Value - s.starttimestep.Value))

                for r in dimensions.GetValuesOfRegion():

                    w = (s.cummulativewelfare[t - 1, r])

                    perCapitaConsumption = (s.consumption[
                                            t, r] / s.population[t, r])

                    if (perCapitaConsumption <= 0.0):
                        perCapitaConsumption = (1.0)

                    w = (w + (U(perCapitaConsumption) * s.population[
                         t, r] * DF(t)))
                    s.marginalwelfare[t, r] = (DF(t) * s.utilitycalibrationmultiplicative / math.pow(
                        perCapitaConsumption, s.elasticityofmarginalutility))

                    s.cummulativewelfare[t, r] = (w)

                    if (t == s.stoptimestep):
                        s.totalwelfare[r] = (s.cummulativewelfare[t, r])

            else:

                for r in dimensions.GetValuesOfRegion():

                    s.cummulativewelfare[t, r] = (0)
