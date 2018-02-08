#!/usr/bin/env Python 2.7

""" Functions used for the analysis of the data """

import math
import tb_code.pypostgre as ppg
import tb_code.standart as std
import tb_code.typehandle as tph


def simple_exp(dbname, table, tblist, typename):
    """ Calculates the exponential smoothing """

    print 'tblist is ', tblist
    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, main_name)
    print 'STATIONS FETCHED '
    print stations

    ppg.add_column(dbname, table, std.PREDICTION)

    print 'END IT ALL'

    for i in stations:

        station = i
        prev = 0
        aux = []
        for j in range(len(tblist) + 1):

            if j is 0:
                prev = ppg.select_single_data(
                    dbname, tblist[0], target_name, main_name, station)
                aux.append(prev)
                continue

            real = ppg.select_single_data(
                dbname, tblist[j - 1], target_name, main_name, station)
            aux.append(real)
            prev = prev + std.SSE_ALPHA * (real - prev)

        real = ppg.select_single_data(
            dbname, table, target_name, main_name, station)
        prev = prev + std.SSE_ALPHA * (real - prev)
        aux.append(real)

        print "FOR {} -> ALPHA = {} -> PRED = {}".format(
            aux, std.SSE_ALPHA, prev)

        ppg.set_value(dbname, str(prev), table,
                      std.PREDICTION, main_name, station)


def avg_move(dbname, table, tblist, typename, weights=None):
    """ Calculates the average """

    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, main_name)
    ppg.add_column(dbname, table, std.PREDICTION)

    for i in stations:

        string = i
        data_db1 = ppg.select_single_data(
            dbname, table, target_name, main_name, string)
        data_db2 = ppg.select_single_data(
            dbname, tblist[0], target_name, main_name, string)
        data_db3 = ppg.select_single_data(
            dbname, tblist[1], target_name, main_name, string)

        avg = 0
        if weights is not None:
            data_db1 = data_db1 * weights[2]
            data_db2 = data_db2 * weights[1]
            data_db3 = data_db3 * weights[0]
            avg = (data_db1 + data_db2 + data_db3) / (1.0 * sum(weights))
        else:
            avg = (data_db1 + data_db2 + data_db3) / 3.0

        #print "FOR {} -> WEI = {} -> AVG = {}".format(s, weights, avg)

        ppg.set_value(dbname, str(avg), table,
                      std.PREDICTION, main_name, string)


def growth_rate(dbname, table, typename):
    """ Calculates the growth rate """

    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, main_name)
    ppg.add_column(dbname, table, std.GROWTH)

    for i in stations:

        ocp = ppg.select_single_data(
            std.DBNAME, table, target_name, main_name, i)
        pred = ppg.select_single_data(
            std.DBNAME, table, std.PREDICTION, main_name, i)

        if ocp == 0:
            grow = 0
        else:
            grow = (float(pred) - float(ocp)) / (float(ocp) * 1.0)

        ppg.set_value(dbname, str(grow), table, std.GROWTH, main_name, i)


def months_to_exhaustion(dbname, table, typename):
    """ Calculates the number os months to exhaustion """

    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)
    total_name = tph.get_total_col(typename)
    avial_name = tph.get_avail_col(typename)

    stations = ppg.select_single_distinct(dbname, table, main_name)
    ppg.add_column(dbname, table, std.EXHAUSTION)

    for i in stations:

        total = float(ppg.select_single_data(
            dbname, table, total_name, main_name, i)) * 1.0
        ocp = float(ppg.select_single_data(
            dbname, table, target_name, main_name, i)) * 1.0
        pred = float(ppg.select_single_data(
            dbname, table, std.PREDICTION, main_name, i)) * 1.0
        try:
            grow = ppg.select_single_data(
                dbname, table, std.GROWTH, main_name, i)
            grow = float(grow)
        except ppg.SQLException:
            grow = ''

        if avial_name is None:
            avail = total - ocp
        else:
            avail = ppg.select_single_data(
                dbname, table, avial_name, main_name, i) * 1.0

        if avail == 0:
            months = 'Esgotado'
        elif grow != '' and grow < 0:
            months = 'Decrescimento'
        elif ocp == 0 or total - avail == 0:
            months = 'Sem Previsao'
        else:
            try:
                months = str(
                    int(math.floor(math.log(total / (total - avail), pred / ocp)) + 1)) + ' Meses'
            except ZeroDivisionError:
                months = 'Sem previsao'
        # P.A.
        # months = avail/grow
        ppg.set_value(dbname, months, table, std.EXHAUSTION, main_name, i)
