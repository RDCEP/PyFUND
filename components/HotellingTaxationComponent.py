# This file was automatically generated by converter.py on
# 2013-05-31 15:40:31.860449. Think long and hard before
# attempting to modify it.

import math
from components.helpers import *


class IGlobalHotellingTaxationState(Parameters):
    population = IParameter1Dimensional(
        'population', ['Timestep'], 'double', None)
    consumption = IParameter1Dimensional(
        'consumption', ['Timestep'], 'double', None)
    currtax = IVariable2Dimensional('currtax', [
                                    'Timestep', 'Region'], 'double', None)
    currtaxch4 = IVariable2Dimensional('currtaxch4', [
                                       'Timestep', 'Region'], 'double', None)
    currtaxn2o = IVariable2Dimensional('currtaxn2o', [
                                       'Timestep', 'Region'], 'double', None)
    basetax = ScalarVariable('basetax', 'double', None)
    baseyear = ScalarVariable('baseyear', 'Timestep', None)
    prtp = ScalarVariable('prtp', 'Double', None)
    elasticityofmarginalutility = ScalarVariable(
        'elasticityofmarginalutility', 'Double', None)

    options = [population, consumption, currtax, currtaxch4,
               currtaxn2o, basetax, baseyear, prtp, elasticityofmarginalutility]


class IRegionalHotellingTaxationState(Parameters):
    basetax = IParameter1Dimensional('basetax', ['Region'], 'double', None)
    population = IParameter2Dimensional('population', [
                                        'Timestep', 'Region'], 'double', None)
    consumption = IParameter2Dimensional('consumption', [
                                         'Timestep', 'Region'], 'double', None)
    currtax = IVariable2Dimensional('currtax', [
                                    'Timestep', 'Region'], 'double', None)
    currtaxch4 = IVariable2Dimensional('currtaxch4', [
                                       'Timestep', 'Region'], 'double', None)
    currtaxn2o = IVariable2Dimensional('currtaxn2o', [
                                       'Timestep', 'Region'], 'double', None)
    baseyear = ScalarVariable('baseyear', 'Timestep', None)
    prtp = ScalarVariable('prtp', 'Double', None)
    elasticityofmarginalutility = ScalarVariable(
        'elasticityofmarginalutility', 'Double', None)

    options = [basetax, population, consumption, currtax, currtaxch4,
               currtaxn2o, baseyear, prtp, elasticityofmarginalutility]


class GlobalHotellingTaxationComponent(Behaviors):
    state_class = IGlobalHotellingTaxationState

    def run(self, state, clock):

        t = (clock.Current)
        s = (state)

        perCapitaConsumptionNow = (s.consumption[t] / s.population[t])
        perCapitaConsumptionPrevious = (
            s.consumption[t - 1] / s.population[t - 1])

        perCapitaGrowthRate = (
            perCapitaConsumptionNow / perCapitaConsumptionPrevious - 1.0)

        if (perCapitaConsumptionNow == 0.0 and perCapitaConsumptionPrevious == 0.0):
            perCapitaGrowthRate = (0.0)

        discountrate = (
            perCapitaGrowthRate * s.elasticityofmarginalutility + s.prtp)

        for r in dimensions.GetValuesOfRegion():

            if (t < s.baseyear):
                s.currtax[t, r] = (0.0)
            elif (t == s.baseyear):
                s.currtax[t, r] = (s.basetax)
            else:
                s.currtax[t, r] = (s.currtax[t - 1, r] * (1.0 + discountrate))

            s.currtaxn2o[t, r] = (s.currtax[t, r])
            s.currtaxch4[t, r] = (s.currtax[t, r])


class RegionalHotellingTaxationComponent(Behaviors):
    state_class = IRegionalHotellingTaxationState

    def run(self, state, clock):

        t = (clock.Current)
        s = (state)

        for r in dimensions.GetValuesOfRegion():

            perCapitaConsumptionNow = (s.consumption[
                                       t, r] / s.population[t, r])
            perCapitaConsumptionPrevious = (s.consumption[
                                            t - 1, r] / s.population[t - 1, r])

            perCapitaGrowthRate = (
                perCapitaConsumptionNow / perCapitaConsumptionPrevious - 1.0)

            discountrate = (
                perCapitaGrowthRate * s.elasticityofmarginalutility + s.prtp)

            if (t < s.baseyear):
                s.currtax[t, r] = (0.0)
            elif (t == s.baseyear):
                s.currtax[t, r] = (s.basetax[r])
            else:
                s.currtax[t, r] = (s.currtax[t - 1, r] * (1.0 + discountrate))

            s.currtaxn2o[t, r] = (s.currtax[t, r])
            s.currtaxch4[t, r] = (s.currtax[t, r])


behavior_classes = [
    GlobalHotellingTaxationComponent, RegionalHotellingTaxationComponent]
