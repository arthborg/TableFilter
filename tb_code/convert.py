#!/usr/bin/python2.7

""" Implements the functions needed for converting tables to .csv files
    and put them on the users database
"""

import xlrd
import pandas as pd
import tb_code.standart as std
import tb_code.pypostgre as ppg
import tb_code.csvtools as cts


def normalize_csv_file(filename):
    """ Normalizes the csv file for future use """

    comma_text = std.CSV_STD_PATH + '/commatext.csv'
    cts.semicolon_to_comma(filename, comma_text)

    unicode_text = std.CSV_STD_PATH + '/unicodetext.csv'
    cts.convert_to_unicode(comma_text, unicode_text)
    std.print_log('finished unicode on file ' + unicode_text)

    return unicode_text


def n_sheets(filename):
    """ Returns the number of sheets of an excel file """
    excel_table = pd.ExcelFile(filename)
    sheets = excel_table.sheet_names
    return len(sheets)


def get_sheet_names(filename):
    """ Returns the sheets names of an excel file """
    excel_table = xlrd.open_workbook(filename, on_demand=True)
    sheets = excel_table.sheet_names()
    return sheets


def to_csv(filename, tb_type, year=None, month=None):
    """ Converts an excel table to .csv files """

    excel_table = pd.ExcelFile(filename)
    sheets = excel_table.sheet_names
    final_names = []

    for i in range(0, len(sheets)):

        sheet = excel_table.parse(i)
        name = std.standardize_name(i, tb_type, year, month)

        path = std.get_path(filename) + name
        final_names.append(path + '.csv')
        sheet.to_csv(path_or_buf=path + '.csv', sep=',',
                     index=False, encoding='utf-8')

    return final_names


def single_csv(filename, sheet_name, tb_type, year=None, month=None):
    """ Converts an excel file to one csv file """

    excel_table = pd.ExcelFile(filename)
    sheet = excel_table.parse(sheet_name)

    name = std.standardize_name(0, tb_type, year, month)
    final = std.CSV_STD_PATH + '/' + name + '.csv'

    sheet.to_csv(path_or_buf=final, sep=',', index=False, encoding='utf-8')
    return final


def get_std_name(num, tb_type, year=None, month=None):
    """ Get the standart name for tables """
    name = std.standardize_name(num, tb_type, year, month)
    return name


def fileto_postgre(filename, tablename, dbname):
    """ Converts a .csv file to a postgres database table """

    myfile = open(filename, 'r')
    header = myfile.readline()
    std.print_log('header is ' + header)
    col_list = header.split(',')
    col_list[-1] = col_list[-1].rstrip()

    std.print_log('COLUMNS ARE')
    for i in col_list:
        std.print_log(i)

    ppg.create_table(dbname, tablename, col_list)
    ppg.copy_data(dbname, tablename, filename)
    myfile.close()


def to_table(path, dbname, table):
    """ Converts the data on the database to an excel file """

    data = ppg.select_all(dbname, table)
    myfile = open(path, 'w')
    headerdata = ppg.get_columns(dbname, table)

    string = ''
    for dat in headerdata:
        string += dat
        if dat is not headerdata:
            string += ','
    string += '\n'
    myfile.write(string)

    for row in data:

        string = ''
        for col in row:
            string += str(col)
            string += ','
        string += '\n'
        myfile.write(string)

    myfile.close()
