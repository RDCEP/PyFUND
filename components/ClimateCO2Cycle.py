class IClimateCO2CycleState(Parameters):
    mco2 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Anthropogenic CO2 emissions in Mt of C')
    TerrestrialCO2 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Terrestrial biosphere CO2 emissions in Mt of C')
    globc = IVariable1Dimensional(
        ['Timestep', 'double'], 'Net CO2 emissions in Mt of C')
    cbox1 = IVariable1Dimensional(['Timestep', 'double'], 'Carbon box 1')
    cbox2 = IVariable1Dimensional(['Timestep', 'double'], 'Carbon box 2')
    cbox3 = IVariable1Dimensional(['Timestep', 'double'], 'Carbon box 3')
    cbox4 = IVariable1Dimensional(['Timestep', 'double'], 'Carbon box 4')
    cbox5 = IVariable1Dimensional(['Timestep', 'double'], 'Carbon box 5')
    acco2 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Atmospheric CO2 concentration')
    TerrCO2Stock = IVariable1Dimensional(
        ['Timestep', 'double'], 'Stock of CO2 in the terrestrial biosphere')
    temp = IParameter1Dimensional(['Timestep', 'double'], 'Temperature')


class ClimateCO2CycleComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            s.co2decay1 = (s.lifeco1)
            s.co2decay2 = (math.exp(-1.0 / s.lifeco2))
            s.co2decay3 = (math.exp(-1.0 / s.lifeco3))
            s.co2decay4 = (math.exp(-1.0 / s.lifeco4))
            s.co2decay5 = (math.exp(-1.0 / s.lifeco5))

            s.TerrCO2Stock[t] = (s.TerrCO2Stock0)

            s.cbox1[t] = (283.53)
            s.cbox2[t] = (5.62)
            s.cbox3[t] = (6.29)
            s.cbox4[t] = (2.19)
            s.cbox5[t] = (0.15)
            s.acco2[t] = (s.cbox1[t] + s.cbox2[
                          t] + s.cbox3[t] + s.cbox4[t] + s.cbox5[t])

        else:

            if (t == Timestep.FromYear(2011)):

                s.tempIn2010 = (s.temp[Timestep.FromYear(2010)])

            if (t > Timestep.FromYear(2010)):

                s.TerrestrialCO2[t] = ((s.temp[
                                       t - 1] - s.tempIn2010) * s.TerrCO2Sens * s.TerrCO2Stock[t - 1] / s.TerrCO2Stock0)

            else:
                s.TerrestrialCO2[t] = (0)

            s.TerrCO2Stock[t] = (math.max(s.TerrCO2Stock[
                                 t - 1] - s.TerrestrialCO2[t], 0.0))

            s.globc[t] = (s.mco2[t] + s.TerrestrialCO2[t])

            s.cbox1[t] = (s.cbox1[
                          t - 1] * s.co2decay1 + 0.000471 * s.co2frac1 * (s.globc[t]))
            s.cbox2[t] = (s.cbox2[
                          t - 1] * s.co2decay2 + 0.000471 * s.co2frac2 * (s.globc[t]))
            s.cbox3[t] = (s.cbox3[
                          t - 1] * s.co2decay3 + 0.000471 * s.co2frac3 * (s.globc[t]))
            s.cbox4[t] = (s.cbox4[
                          t - 1] * s.co2decay4 + 0.000471 * s.co2frac4 * (s.globc[t]))
            s.cbox5[t] = (s.cbox5[
                          t - 1] * s.co2decay5 + 0.000471 * s.co2frac5 * (s.globc[t]))

            s.acco2[t] = (s.cbox1[t] + s.cbox2[
                          t] + s.cbox3[t] + s.cbox4[t] + s.cbox5[t])
