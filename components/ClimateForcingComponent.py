class IClimateForcingState(Parameters):
    acco2 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Atmospheric CO2 concentration')
    acch4 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Atmospheric CH4 concentration')
    acn2o = IParameter1Dimensional(
        ['Timestep', 'double'], 'Atmospheric N2O concentration')
    acsf6 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Atmospheric SF6 concentrations')
    acso2 = IParameter1Dimensional(
        ['Timestep', 'double'], 'Atmospheric SO2 concentration')
    rfCO2 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing from CO2')
    rfCH4 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing from CH4')
    rfN2O = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing from N2O')
    rfSF6 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing from N2O')
    rfSO2 = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing from SO2')
    radforc = IVariable1Dimensional(
        ['Timestep', 'double'], 'Radiative forcing')
    rfEMF22 = IVariable1Dimensional(
        ['Timestep', 'double'], 'EMF22 radiative forcing')


class ClimateForcingComponent(Behaviors):
    def run(state, clock):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:
            ch4n2o = (Interact(s.ch4pre, s.n2opre))

            s.rfCO2[t] = (5.35 * math.log(s.acco2[t] / s.co2pre))

            s.rfCH4[t] = (0.036 * (1.0 + s.ch4ind) * (math.sqrt(s.acch4[
                          t]) - math.sqrt(s.ch4pre)) - Interact(s.acch4[t], s.n2opre) + ch4n2o)

            s.rfN2O[t] = (0.12 * (math.sqrt(s.acn2o[t]) - math.sqrt(
                s.n2opre)) - Interact(s.ch4pre, s.acn2o[t]) + ch4n2o)

            s.rfSF6[t] = (0.00052 * (s.acsf6[t] - s.sf6pre))

            s.rfSO2[t] = (s.so2dir * s.acso2[t] / 14.6 + s.so2ind * math.log(
                1.0 + s.acso2[t] / 34.4) / math.log(1 + 14.6 / 34.4) - 0.9)

            s.radforc[t] = (s.rfCO2[t] + s.rfCH4[
                            t] + s.rfN2O[t] + s.rfSF6[t] - s.rfSO2[t])

            s.rfEMF22[t] = (s.rfCO2[t] + s.rfCH4[t] + s.rfN2O[t])
