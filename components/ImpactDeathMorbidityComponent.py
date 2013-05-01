class IImpactDeathMorbidityState(Parameters):
    dead = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    yll = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    yld = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    deadcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    morbcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    vsl = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    vmorb = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    d2ld = IParameter1Dimensional(['Region', 'double'], None)
    d2ls = IParameter1Dimensional(['Region', 'double'], None)
    d2lm = IParameter1Dimensional(['Region', 'double'], None)
    d2lc = IParameter1Dimensional(['Region', 'double'], None)
    d2lr = IParameter1Dimensional(['Region', 'double'], None)
    d2dd = IParameter1Dimensional(['Region', 'double'], None)
    d2ds = IParameter1Dimensional(['Region', 'double'], None)
    d2dm = IParameter1Dimensional(['Region', 'double'], None)
    d2dc = IParameter1Dimensional(['Region', 'double'], None)
    d2dr = IParameter1Dimensional(['Region', 'double'], None)
    dengue = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    schisto = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    malaria = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    cardheat = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    cardcold = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    resp = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    diadead = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    hurrdead = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    extratropicalstormsdead = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    diasick = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactDeathMorbidityComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)

                s.dead[t, r] = (s.dengue[t, r] + s.schisto[t, r] + s.malaria[t, r] + s.cardheat[t, r] + s.cardcold[
                                t, r] + s.resp[t, r] + s.diadead[t, r] + s.hurrdead[t, r] + s.extratropicalstormsdead[t, r])
                if (s.dead[t, r] > s.population[t, r] * 1000000.0):
                    s.dead[t, r] = (s.population[t, r] / 1000000.0)

                s.yll[t, r] = (s.d2ld[r] * s.dengue[t, r] + s.d2ls[r] * s.schisto[t, r] + s.d2lm[r] * s.malaria[
                               t, r] + s.d2lc[r] * s.cardheat[t, r] + s.d2lc[r] * s.cardcold[t, r] + s.d2lr[r] * s.resp[t, r])

                s.yld[t, r] = (s.d2dd[r] * s.dengue[t, r] + s.d2ds[r] * s.schisto[t, r] + s.d2dm[r] * s.malaria[t, r] + s.d2dc[
                               r] * s.cardheat[t, r] + s.d2dc[r] * s.cardcold[t, r] + s.d2dr[r] * s.resp[t, r] + s.diasick[t, r])

                s.vsl[t, r] = (s.vslbm * math.pow(ypc / s.vslypc0, s.vslel))
                s.deadcost[t, r] = (s.vsl[t, r] * s.dead[t, r] / 1000000000.0)

                s.vmorb[t, r] = (s.vmorbbm * math.pow(
                    ypc / s.vmorbypc0, s.vmorbel))
                s.morbcost[t, r] = (s.vmorb[t, r] * s.yld[t, r] / 1000000000.0)
