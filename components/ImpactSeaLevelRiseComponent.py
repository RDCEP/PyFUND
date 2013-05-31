class IImpactSeaLevelRiseState(Parameters):
    wetval = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    wetlandloss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cumwetlandloss = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    wetlandgrowth = IVariable2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    wetcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    dryval = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    landloss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    cumlandloss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    drycost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    npprotcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    npwetcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    npdrycost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    protlev = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    protcost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    enter = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    leave = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    entercost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    leavecost = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    imigrate = IVariable2Dimensional(['Region', 'Region', 'double'], None)
    pc = IParameter1Dimensional(['Region', 'double'], None)
    slrprtp = IParameter1Dimensional(['Region', 'double'], None)
    wmbm = IParameter1Dimensional(['Region', 'double'], None)
    dlbm = IParameter1Dimensional(['Region', 'double'], None)
    drylandlossparam = IParameter1Dimensional(['Region', 'double'], None)
    wlbm = IParameter1Dimensional(['Region', 'double'], None)
    coastpd = IParameter1Dimensional(['Region', 'double'], None)
    wetmax = IParameter1Dimensional(['Region', 'double'], None)
    wetland90 = IParameter1Dimensional(['Region', 'double'], None)
    maxlandloss = IParameter1Dimensional(['Region', 'double'], None)
    sea = IParameter1Dimensional(['Timestep', 'double'], None)
    migrate = IParameter2Dimensional(['Region', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    population = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    area = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactSeaLevelRiseComponent(Behaviors):
    state_class = IImpactSeaLevelRiseState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r1 in dimensions.GetValuesOfRegion():

                for r2 in dimensions.GetValuesOfRegion():
                    immsumm = (0)
                    for i in dimensions.GetValuesOfRegion():

                        immsumm += s.migrate[i, r1]

                    s.imigrate[r1, r2] = (s.migrate[r2, r1] / immsumm)

                t0 = (clock.StartTime)
                s.landloss[t0, r1] = (0.0)
                s.cumlandloss[t0, r1] = (0.0)
                s.cumwetlandloss[t0, r1] = (0.0)
                s.wetlandgrowth[t0, r1] = (0.0)

        else:

            ds = (s.sea[t] - s.sea[t - 1])

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                ypcprev = (s.income[
                           t - 1, r] / s.population[t - 1, r] * 1000.0)
                ypcgrowth = (ypc / ypcprev - 1.0)

                if (t == Timestep.FromYear(1951)):
                    ypcgrowth = (0)

                incomedens = (s.income[t, r] / s.area[t, r])

                incomedensprev = (s.income[t - 1, r] / s.area[t - 1, r])

                incomedensgrowth = (incomedens / incomedensprev - 1.0)

                popdens = (s.population[t, r] / s.area[t, r] * 1000000.0)
                popdensprev = (s.population[
                               t - 1, r] / s.area[t - 1, r] * 1000000.0)
                popdensgrowth = (popdens / popdensprev - 1.0)

                s.dryval[t, r] = (s.dvbm * math.pow(
                    incomedens / s.incdens, s.dvydl))

                s.wetval[t, r] = (s.wvbm *
                                  math.pow(ypc / s.slrwvypc0, s.wvel) *
                                  math.pow(popdens / s.slrwvpopdens0, s.wvpdl) *
                                  math.pow((s.wetland90[r] - s.cumwetlandloss[t - 1, r]) / s.wetland90[r], s.wvsl))

                potCumLandloss = (math.min(s.maxlandloss[r], s.cumlandloss[
                                  t - 1, r] + s.dlbm[r] * math.pow(s.sea[t], s.drylandlossparam[r])))

                potLandloss = (potCumLandloss - s.cumlandloss[t - 1, r])

                if (ds < 0):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (0)

                elif ((1.0 + s.slrprtp[r] + ypcgrowth) < 0.0):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (0)

                elif (((1.0 + s.dvydl * incomedensgrowth) < 0.0)):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (0)

                elif ((1.0 / (1.0 + s.slrprtp[r] + ypcgrowth)) >= 1):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (0)

                elif (((1.0 + s.dvydl * incomedensgrowth) / (1.0 + s.slrprtp[r] + ypcgrowth)) >= 1.0):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (1)

                elif (((1.0 + s.wvel * ypcgrowth + s.wvpdl * popdensgrowth + s.wvsl * s.wetlandgrowth[t - 1, r]) / (1.0 + s.slrprtp[r] + ypcgrowth)) >= 1.0):

                    s.npprotcost[t, r] = (0)
                    s.npwetcost[t, r] = (0)
                    s.npdrycost[t, r] = (0)
                    s.protlev[t, r] = (0)

                else:

                    s.npprotcost[t, r] = (s.pc[r] * ds * (1.0 + s.slrprtp[
                                          r] + ypcgrowth) / (s.slrprtp[r] + ypcgrowth))

                    if ((1.0 + s.wvel * ypcgrowth + s.wvpdl * popdensgrowth + s.wvsl * s.wetlandgrowth[t - 1, r]) < 0.0):
                        s.npwetcost[t, r] = (0)
                    else:
                        s.npwetcost[t, r] = (s.wmbm[r] * ds * s.wetval[t, r] * (1.0 + s.slrprtp[r] + ypcgrowth) / (s.slrprtp[
                                             r] + ypcgrowth - s.wvel * ypcgrowth - s.wvpdl * popdensgrowth - s.wvsl * s.wetlandgrowth[t - 1, r]))

                    if ((1.0 + s.dvydl * incomedensgrowth) < 0.0):
                        s.npdrycost[t, r] = (0)
                    else:
                        s.npdrycost[t, r] = (potLandloss * s.dryval[t, r] * (1 + s.slrprtp[
                                             r] + ypcgrowth) / (s.slrprtp[r] + ypcgrowth - s.dvydl * incomedensgrowth))

                    s.protlev[t, r] = (math.max(0.0, 1.0 - 0.5 * (s.npprotcost[
                                       t, r] + s.npwetcost[t, r]) / s.npdrycost[t, r]))

                    if (s.protlev[t, r] > 1):
                        raise Exception("protlevel >1 should not happen")

                s.wetlandloss[t, r] = (math.min(
                    s.wlbm[r] * ds + s.protlev[t, r] * s.wmbm[r] * ds,
                    s.wetmax[r] - s.cumwetlandloss[t - 1, r]))

                s.cumwetlandloss[t, r] = (s.cumwetlandloss[
                                          t - 1, r] + s.wetlandloss[t, r])

                s.wetlandgrowth[t, r] = ((s.wetland90[r] - s.cumwetlandloss[
                                         t, r]) / (s.wetland90[r] - s.cumwetlandloss[t - 1, r]) - 1.0)

                s.wetcost[t, r] = (s.wetval[t, r] * s.wetlandloss[t, r])

                s.landloss[t, r] = ((1.0 - s.protlev[t, r]) * potLandloss)

                s.cumlandloss[t, r] = (s.cumlandloss[
                                       t - 1, r] + s.landloss[t, r])
                s.drycost[t, r] = (s.dryval[t, r] * s.landloss[t, r])

                s.protcost[t, r] = (s.protlev[t, r] * s.pc[r] * ds)

                if (s.landloss[t, r] < 0):
                    s.leave[t, r] = (0)
                else:
                    s.leave[t, r] = (s.coastpd[r] * popdens * s.landloss[t, r])

                s.leavecost[t, r] = (
                    s.emcst * ypc * s.leave[t, r] / 1000000000)

            for destination in dimensions.GetValuesOfRegion():
                enter = (0.0)
                for source in dimensions.GetValuesOfRegion():

                    enter += s.leave[t, source] * s.imigrate[
                        source, destination]

                s.enter[t, destination] = (enter)

            for r in dimensions.GetValuesOfRegion():
                ypc = (s.income[t, r] / s.population[t, r] * 1000.0)
                s.entercost[t, r] = (
                    s.immcst * ypc * s.enter[t, r] / 1000000000)


behavior_classes = [ImpactSeaLevelRiseComponent]
