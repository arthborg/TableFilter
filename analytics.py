#!/usr/bin/env Python 2.7

import pypostgre  as ppg
import standart   as std
import typehandle as tph


class NotEnoughDataException(Exception):
    pass


def simple_exp(dbname, table, tblist, typename):

    MAINNAME = tph.get_main_col(typename)
    TARGETNAME = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, MAINNAME)
    print 'STATIONS FETCHED '
    print stations

    ppg.add_column(dbname, table, std.PREDICTION)

    print 'END IT ALL'

    for i in stations:

        s = i
        pred = 0

        for j in range(len(tblist)+1):

            if j is 0:
                prev = ppg.select_single_data(dbname, tblist[0], TARGETNAME, MAINNAME, s)
                continue
            
            real = ppg.get_single_data(dbname, tblist[j-1], TARGETNAME, MAINNAME, s)
            prev = prev + std.SSE_ALPHA * (real - prev)
        
        real = ppg.get_single_data(dbname, table, TARGETNAME, MAINNAME, s)
        prev = prev + std.SSE_ALPHA * (real - prev)

        if std.DEBUG_CONST is True:
            print "FOR {} -> ALPHA = {} -> PRED = {}".format(s, std.SSE_ALPHA, prev)
        
        ppg.set_value(dbname, str(prev), table, std.PREDICTION, MAINNAME, s)

    if std.DEBUG_CONST is True:
        print 'SSE OK'


def avg_move(dbname, table, tblist, typename, weights=None):

    MAINNAME = tph.get_main_col(typename)
    TARGETNAME = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, MAINNAME)
    ppg.add_column(dbname, table, std.PREDICTION)

    for i in stations:

        s = i
        data_db1 = single_single_data(dbname, table, TARGETNAME, MAINNAME, s)
        data_db2 = single_single_data(dbname, tblist[0], TARGETNAME, MAINNAME, s)
        data_db3 = single_single_data(dbname, tblist[1], TARGETNAME, MAINNAME, s)

        avg = 0
        if weights is not None:
            data_db1 = data_db1 * weights[2]
            data_db2 = data_db2 * weights[1]
            data_db3 = data_db3 * weights[0]
            avg = (data_db1+data_db2+data_db3)/(1.0*sum(weights))
        else:
            avg = (data_db1+data_db2+data_db3)/3.0

        if std.DEBUG_CONST is True:
            print "FOR {} -> WEI = {} -> AVG = {}".format(s, weights, avg)

        ppg.set_value(dbname, str(avg), table, std.PREDICTION, MAINNAME, s)

    if std.DEBUG_CONST is True:
        print 'AVG OK'


def growth_rate(dbname, table, typename):

    MAINNAME = tph.get_main_col(typename)
    TARGETNAME = tph.get_target_col(typename)
    
    stations = ppg.select_single_distinct(dbname, table, MAINNAME)
    ppg.add_column(dbname, table, std.GROWTH)

    for i in stations:
        
        ocp = ppg.get_single_data(dbname, table, TARGETNAME, MAINNAME, i)
        pred = ppg.get_single_data(dbnaem, table, std.PREDICTION, MAINNAME, i)

        if ocp is 0:
            gr = 0
        else:
            gr = (pred - ocp)/(ocp*1.0)

        ppg.set_value(dbname, str(gr), table, std.GROWTH, MAINNAME, s)

    
def months_to_exhaustion(dbname, table, typename):

    MAINNAME = tph.get_main_col(typename)
    TARGETNAME = tph.get_target_col(typename)
    TOTALNAME = tph.get_total_col(typename)
    AVAILNAME = tph.get_avail_col(typename)

    stations = ppg.select_single_distinct(dbname, table, MAINNAME)
    ppg.add_column(dbname, table, std.EXHAUSTION)

    for i in stations:

        total = ppg.get_single_data(dbname, table, TOTALNAME, MAINNAME, i)*1.0
        ocp = ppg.get_single_data(dbname, table, TARGETNAME, MAINNAME, i)*1.0
        pred = ppg.get_single_data(dbname, table, std.PREDICTION, MAINNAME, i)*1.0
        if AVAILNAME is None:
            avail = total-ocp
        else:
            avail = ppg.get_single_data(dbname, table, AVAILNAME, MAINNAME, i)*1.0

        if avail is 0:
            months = 'Esgotado'
        elif gr < 0:
            months = 'Decrescimento'
        elif ocp is 0:
            months = 'Sem Previsao'
        else:
            months = str(int(math.floor(math.log( total/(total-avail), pred/ocp)) +1)) + ' Meses'

        ppg.set_value(dbname, months, table, std.EXHAUSTION, MAINNAME, s)
