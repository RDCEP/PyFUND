class IImpactAggregationState(Parameters):
    eloss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    sloss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    loss = IVariable2Dimensional(['Timestep', 'Region', 'double'], None)
    income = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    water = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    forests = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    heating = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    cooling = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    agcost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    drycost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    protcost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    entercost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    hurrdam = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    extratropicalstormsdam = IParameter2Dimensional(
        ['Timestep', 'Region', 'double'], None)
    species = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    deadcost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    morbcost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    wetcost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)
    leavecost = IParameter2Dimensional(['Timestep', 'Region', 'double'], None)


class ImpactAggregationComponent(Behaviors):
    state_class = IImpactAggregationState

    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            for r in dimensions.GetValuesOfRegion():

                s.eloss[t, r] = (0.0)
                s.sloss[t, r] = (0.0)

        else:

            for r in dimensions.GetValuesOfRegion():

                s.eloss[t, r] = (math.min(
                    0.0
                    - (s.switchoffwater and 0.0 or s.water[t, r])
                    - (s.switchoffforests and 0.0 or s.forests[t, r])
                    - (s.switchoffheating and 0.0 or s.heating[t, r])
                    - (s.switchoffcooling and 0.0 or s.cooling[t, r])
                    - (s.switchoffagcost and 0.0 or s.agcost[t, r])
                    + (s.switchoffdrycost and 0.0 or s.drycost[t, r])
                    + (s.switchoffprotcost and 0.0 or s.protcost[t, r])
                    + (s.switchoffentercost and 0.0 or s.entercost[t, r])
                    + (s.switchoffhurrdam and 0.0 or s.hurrdam[t, r])
                    + (s.switchoffextratropicalstormsdam and 0.0 or s.extratropicalstormsdam[
                       t, r]),
                    s.income[t, r]))

            for r in dimensions.GetValuesOfRegion():

                s.sloss[t, r] = (0.0
                                 + (s.switchoffspecies and 0.0 or s.species[
                                    t, r])
                                 + (s.switchoffdeadcost and 0.0 or s.deadcost[
                                    t, r])
                                 + (s.switchoffmorbcost and 0.0 or s.morbcost[
                                    t, r])
                                 + (s.switchoffwetcost and 0.0 or s.wetcost[
                                    t, r])
                                 + (s.switchoffleavecost and 0.0 or s.leavecost[t, r]))

            for r in dimensions.GetValuesOfRegion():

                s.loss[t, r] = ((s.eloss[t, r] + s.sloss[t, r]) * 1000000000.0)
