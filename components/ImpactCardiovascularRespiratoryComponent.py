# This file was automatically generated by converter.py.
# Think long and hard before attempting to modify it.

import math
from components.helpers import *
from components._patches import *


class IImpactCardiovascularRespiratoryState(Parameters):
    basecardvasc = IVariable2Dimensional(
        'basecardvasc', [
            'Timestep', 'Region'], 'double', None)
    baseresp = IVariable2Dimensional(
        'baseresp', [
            'Timestep', 'Region'], 'double', None)
    cardheat = IVariable2Dimensional(
        'cardheat', [
            'Timestep', 'Region'], 'double', None)
    resp = IVariable2Dimensional(
        'resp', [
            'Timestep', 'Region'], 'double', None)
    cardcold = IVariable2Dimensional(
        'cardcold', [
            'Timestep', 'Region'], 'double', None)
    cardvasc90 = IParameter1Dimensional(
        'cardvasc90',
        ['Region'],
        'double',
        None)
    plus90 = IParameter1Dimensional('plus90', ['Region'], 'double', None)
    resp90 = IParameter1Dimensional('resp90', ['Region'], 'double', None)
    chplbm = IParameter1Dimensional('chplbm', ['Region'], 'double', None)
    chmlbm = IParameter1Dimensional('chmlbm', ['Region'], 'double', None)
    chpqbm = IParameter1Dimensional('chpqbm', ['Region'], 'double', None)
    chmqbm = IParameter1Dimensional('chmqbm', ['Region'], 'double', None)
    rlbm = IParameter1Dimensional('rlbm', ['Region'], 'double', None)
    rqbm = IParameter1Dimensional('rqbm', ['Region'], 'double', None)
    ccplbm = IParameter1Dimensional('ccplbm', ['Region'], 'double', None)
    ccmlbm = IParameter1Dimensional('ccmlbm', ['Region'], 'double', None)
    ccpqbm = IParameter1Dimensional('ccpqbm', ['Region'], 'double', None)
    ccmqbm = IParameter1Dimensional('ccmqbm', ['Region'], 'double', None)
    plus = IParameter2Dimensional(
        'plus', [
            'Timestep', 'Region'], 'double', None)
    temp = IParameter2Dimensional(
        'temp', [
            'Timestep', 'Region'], 'double', None)
    urbpop = IParameter2Dimensional(
        'urbpop', [
            'Timestep', 'Region'], 'double', None)
    population = IParameter2Dimensional(
        'population', [
            'Timestep', 'Region'], 'double', None)
    cvlin = ScalarVariable('cvlin', 'double', None)
    rlin = ScalarVariable('rlin', 'double', None)
    maxcardvasc = ScalarVariable('maxcardvasc', 'double', None)

    options = [
        basecardvasc,
        baseresp,
        cardheat,
        resp,
        cardcold,
        cardvasc90,
        plus90,
        resp90,
        chplbm,
        chmlbm,
        chpqbm,
        chmqbm,
        rlbm,
        rqbm,
        ccplbm,
        ccmlbm,
        ccpqbm,
        ccmqbm,
        plus,
        temp,
        urbpop,
        population,
        cvlin,
        rlin,
        maxcardvasc]


class ImpactCardiovascularRespiratoryComponent(Behaviors):
    state_class = IImpactCardiovascularRespiratoryState

    def run(self, state, clock, dimensions):

        s = (state)
        t = (clock.Current)

        if (clock.IsFirstTimestep):

            pass

        else:

            for r in dimensions.GetValuesOfRegion():

                s.basecardvasc[t, r] = (
                    s.cardvasc90[r] + s.cvlin * (s.plus[t, r] - s.plus90[r]))
                if (s.basecardvasc[t, r] > 1.0):
                    s.basecardvasc[t, r] = (1.0)

                s.baseresp[t, r] = (
                    s.resp90[r] + s.rlin * (s.plus[t, r] - s.plus90[r]))
                if (s.baseresp[t, r] > 1.0):
                    s.baseresp[t, r] = (1.0)

                s.cardheat[t, r] = ((s.chplbm[r] * s.plus[t, r] + s.chmlbm[r] * (1.0 - s.plus[t, r])) * s.temp[t, r] +
                                    (s.chpqbm[r] * s.plus[t, r] + s.chmqbm[r] * (1.0 - s.plus[t, r])) * math.pow(s.temp[t, r], 2))
                s.cardheat[
                    t,
                    r] = (
                    s.cardheat[
                        t,
                        r] *
                    s.urbpop[
                        t,
                        r] *
                    s.population[
                        t,
                        r] *
                    10)
                if (s.cardheat[t, r] > 1000.0 * s.maxcardvasc *
                        s.basecardvasc[t, r] * s.urbpop[t, r] * s.population[t, r]):
                    s.cardheat[
                        t,
                        r] = (
                        1000 *
                        s.maxcardvasc *
                        s.basecardvasc[
                            t,
                            r] *
                        s.urbpop[
                            t,
                            r] *
                        s.population[
                            t,
                            r])
                if (s.cardheat[t, r] < 0.0):
                    s.cardheat[t, r] = (0)

                s.resp[
                    t,
                    r] = (
                    s.rlbm[r] *
                    s.temp[
                        t,
                        r] +
                    s.rqbm[r] *
                    math.pow(
                        s.temp[
                            t,
                            r],
                        2))
                s.resp[
                    t,
                    r] = (
                    s.resp[
                        t,
                        r] *
                    s.urbpop[
                        t,
                        r] *
                    s.population[
                        t,
                        r] *
                    10)
                if (s.resp[t, r] > 1000 * s.maxcardvasc *
                        s.baseresp[t, r] * s.urbpop[t, r] * s.population[t, r]):
                    s.resp[
                        t,
                        r] = (
                        1000 *
                        s.maxcardvasc *
                        s.baseresp[
                            t,
                            r] *
                        s.urbpop[
                            t,
                            r] *
                        s.population[
                            t,
                            r])
                if (s.resp[t, r] < 0):
                    s.resp[t, r] = (0)

                s.cardcold[t, r] = ((s.ccplbm[r] * s.plus[t, r] + s.ccmlbm[r] * (1.0 - s.plus[t, r])) * s.temp[t, r] +
                                    (s.ccpqbm[r] * s.plus[t, r] + s.ccmqbm[r] * (1.0 - s.plus[t, r])) * math.pow(s.temp[t, r], 2))
                s.cardcold[t, r] = (s.cardcold[t, r] * s.population[t, r] * 10)
                if (s.cardcold[t, r] < -1000 * s.maxcardvasc *
                        s.basecardvasc[t, r] * s.population[t, r]):
                    s.cardcold[t, r] = (-
                                        1000 *
                                        s.maxcardvasc *
                                        s.basecardvasc[t, r] *
                                        s.population[t, r])
                if (s.cardcold[t, r] > 0):
                    s.cardcold[t, r] = (0)


behavior_classes = [ImpactCardiovascularRespiratoryComponent]
