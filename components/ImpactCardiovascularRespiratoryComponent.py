class IImpactCardiovascularRespiratoryState(Parameters):
    basecardvasc = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    baseresp = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cardheat = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    resp = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cardcold = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cardvasc90 = IParameter1Dimensional(['Region', 'double'], None)
    plus90 = IParameter1Dimensional(['Region', 'double'], None)
    resp90 = IParameter1Dimensional(['Region', 'double'], None)
    chplbm = IParameter1Dimensional(['Region', 'double'], None)
    chmlbm = IParameter1Dimensional(['Region', 'double'], None)
    chpqbm = IParameter1Dimensional(['Region', 'double'], None)
    chmqbm = IParameter1Dimensional(['Region', 'double'], None)
    rlbm = IParameter1Dimensional(['Region', 'double'], None)
    rqbm = IParameter1Dimensional(['Region', 'double'], None)
    ccplbm = IParameter1Dimensional(['Region', 'double'], None)
    ccmlbm = IParameter1Dimensional(['Region', 'double'], None)
    ccpqbm = IParameter1Dimensional(['Region', 'double'], None)
    ccmqbm = IParameter1Dimensional(['Region', 'double'], None)
    plus = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    temp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    urbpop = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactCardiovascularRespiratoryComponent(Behaviors):
    state_class = IImpactCardiovascularRespiratoryState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():

                s.basecardvasc[t, r] = (s.cardvasc90[
                                        r] + s.cvlin * (s.plus[t, r] - s.plus90[r]))
                if (s.basecardvasc[t, r] > 1.0):
                    s.basecardvasc[t, r] = (1.0)

                s.baseresp[t, r] = (s.resp90[
                                    r] + s.rlin * (s.plus[t, r] - s.plus90[r]))
                if (s.baseresp[t, r] > 1.0):
                    s.baseresp[t, r] = (1.0)

                s.cardheat[t, r] = ((s.chplbm[r] * s.plus[t, r] + s.chmlbm[r] * (1.0 - s.plus[t, r])) * s.temp[t, r] +
                                    (s.chpqbm[r] * s.plus[t, r] + s.chmqbm[r] * (1.0 - s.plus[t, r])) * math.pow(s.temp[t, r], 2))
                s.cardheat[t, r] = (s.cardheat[t, r] * s.urbpop[
                                    t, r] * s.population[t, r] * 10)
                if (s.cardheat[t, r] > 1000.0 * s.maxcardvasc * s.basecardvasc[t, r] * s.urbpop[t, r] * s.population[t, r]):
                    s.cardheat[t, r] = (1000 * s.maxcardvasc * s.basecardvasc[
                                        t, r] * s.urbpop[t, r] * s.population[t, r])
                if (s.cardheat[t, r] < 0.0):
                    s.cardheat[t, r] = (0)

                s.resp[t, r] = (s.rlbm[r] * s.temp[
                                t, r] + s.rqbm[r] * math.pow(s.temp[t, r], 2))
                s.resp[t, r] = (s.resp[t, r] * s.urbpop[
                                t, r] * s.population[t, r] * 10)
                if (s.resp[t, r] > 1000 * s.maxcardvasc * s.baseresp[t, r] * s.urbpop[t, r] * s.population[t, r]):
                    s.resp[t, r] = (1000 * s.maxcardvasc * s.baseresp[
                                    t, r] * s.urbpop[t, r] * s.population[t, r])
                if (s.resp[t, r] < 0):
                    s.resp[t, r] = (0)

                s.cardcold[t, r] = ((s.ccplbm[r] * s.plus[t, r] + s.ccmlbm[r] * (1.0 - s.plus[t, r])) * s.temp[t, r] +
                                    (s.ccpqbm[r] * s.plus[t, r] + s.ccmqbm[r] * (1.0 - s.plus[t, r])) * math.pow(s.temp[t, r], 2))
                s.cardcold[t, r] = (s.cardcold[t, r] * s.population[t, r] * 10)
                if (s.cardcold[t, r] < -1000 * s.maxcardvasc * s.basecardvasc[t, r] * s.population[t, r]):
                    s.cardcold[t, r] = (-1000 * s.maxcardvasc * s.basecardvasc[
                                        t, r] * s.population[t, r])
                if (s.cardcold[t, r] > 0):
                    s.cardcold[t, r] = (0)


behavior_classes = [ImpactCardiovascularRespiratoryComponent]
