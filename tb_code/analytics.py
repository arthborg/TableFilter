#!/usr/bin/env Python 2.7

""" Functions used for the analysis of the data """

import math
import tb_code.pypostgre as ppg
import tb_code.standart as std
import tb_code.typehandle as tph


def growth_average(dbname, table, tblist, typename):
    """ Calculates the growth average and apply it to the values """

    tblist = tblist[::-1]
    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)
    stations = ppg.select_single_distinct(dbname, table, main_name)

    ppg.add_column(dbname, table, std.PREDICTION)

    for i in stations:

        station = i

        growth_list = []
        for j in range(1, len(tblist)):

            data_prev = ppg.select_single_data(
                dbname, tblist[j - 1], target_name, main_name, station)
            data_cur = ppg.select_single_data(
                dbname, tblist[j], target_name, main_name, station)

            if data_prev != 0:
                growth_list.append(data_cur / data_prev)

        data_prev = ppg.select_single_data(
            dbname, tblist[-1], target_name, main_name, station)
        data_cur = ppg.select_single_data(
            dbname, table, target_name, main_name, station)

        if data_prev != 0:
            growth_list.append(data_cur / data_prev)

        if growth_list == []:
            prediction = 0
        else:
            prediction = sum(growth_list) / len(growth_list)

        ppg.set_value(dbname, str(prediction), table,
                      std.PREDICTION, main_name, station)


def simple_exp(dbname, table, tblist, typename):
    """ Calculates the exponential smoothing """
    tblist = tblist[::-1]
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

        print 'FOR ' + i
        for j in range(len(tblist) + 1):

            if j is 0:
                try:
                    prev = ppg.select_single_data(
                        dbname, tblist[0], target_name, main_name, station)
                except IndexError:
                    prev = 0
                print "\t ON {} REAL = {} AND PREV = {}".format(
                    tblist[0], prev, prev)
                continue

            try:
                real = ppg.select_single_data(
                    dbname, tblist[j - 1], target_name, main_name, station)
            except IndexError:
                real = prev

            prev = prev + std.SSE_ALPHA * (real - prev)
            print "\t ON {} REAL = {} AND PREV = {}".format(
                tblist[j - 1], real, prev)

        try:
            real = ppg.select_single_data(
                dbname, table, target_name, main_name, station)
        except IndexError:
            real = prev
        prev = prev + std.SSE_ALPHA * (real - prev)
        print "\t ON {} REAL = {} AND PREV = {}".format(table, real, prev)

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
        try:
            data_db2 = ppg.select_single_data(
                dbname, tblist[0], target_name, main_name, string)
        except IndexError:
            data_db2 = 0

        try:
            data_db3 = ppg.select_single_data(
                dbname, tblist[1], target_name, main_name, string)
        except IndexError:
            data_db3 = 0

        avg = 0
        if weights is not None:
            data_db1 = data_db1 * weights[2]
            data_db2 = data_db2 * weights[1]
            data_db3 = data_db3 * weights[0]
            avg = (data_db1 + data_db2 + data_db3) / (1.0 * sum(weights))
        else:
            avg = (data_db1 + data_db2 + data_db3) / 3.0

        print "FOR {} -> D1 = {} T={}, D2 = {} T={}, D3 = {} T={}, AND AVG = {}".format(
            string, data_db1, table, data_db2, tblist[0], data_db3, tblist[1], avg)
        #print "FOR {} -> WEI = {} -> AVG = {}".format(s, weights, avg)

        ppg.set_value(dbname, str(avg), table,
                      std.PREDICTION, main_name, string)


def growth_rate(dbname, table, previous, typename):
    """ Calculates the growth rate """

    print 'SELECTED TABLE IS ' + previous
    main_name = tph.get_main_col(typename)
    target_name = tph.get_target_col(typename)

    stations = ppg.select_single_distinct(dbname, table, main_name)
    ppg.add_column(dbname, table, std.GROWTH)

    for i in stations:

        try:
            old = ppg.select_single_data(
                std.DBNAME, previous, target_name, main_name, i)
        except (ppg.SQLException, IndexError):
            old = 0

        try:
            new = ppg.select_single_data(
                std.DBNAME, table, target_name, main_name, i)
        except (ppg.SQLException, IndexError):
            new = 0

        if old == 0:
            grow = 0
        else:
            grow = (float(new) * 1.0) / (1.0 * float(old))
            grow -= 1

        print "old = {} from {}, new = {} from {}, grow = {}".format(
            old, previous, new, table, grow)
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
        print "FOR {} TOTAL = {}, OCP = {}, PRED = {}, GROW = {}, AVAIL = {}".format(
            i, total, ocp, pred, grow, avail)
        if avail == 0:
            months = 'Esgotado'
        elif grow != '' and grow < 0:
            months = 'Decrescimento'
        elif ocp == 0 or total - avail == 0:
            months = 'Sem Previsao'
        else:
            count = 0
            total = ocp + avail
            if total < ocp:
                print 'fudeu'
            while ocp < total:
                ocp += ocp * grow
                count += 1
                if count > 10:
                    break

            months = str(count) + " Meses"
        # P.A.
        # months = avail/grow
        ppg.set_value(dbname, months, table, std.EXHAUSTION, main_name, i)
