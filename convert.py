#!/usr/bin/env Python 2.7
""" Implements the functions needed for converting tables to .csv files
    and put them on the users database
"""

import xlrd
import pandas as pd
import standart as std
import pypostgre as ppg
import csvtools as cts

def normalize_csv_file(filename):
    """ Normalizes the csv file for future use """

    comma_text = std.get_path(filename)+'commatext.csv'
    cts.semicolon_to_comma(filename, comma_text)

    unicode_text = std.get_path(filename)+'unicodetext.csv'
    cts.convert_to_unicode(comma_text, unicode_text)
    print 'finished unicode'

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

def to_csv(filename, tb_type, year=None, month=None, state=None):
    """ Converts an excel table to .csv file """

    excel_table = pd.ExcelFile(filename)
    sheets = excel_table.sheet_names
    final_names = []

    for i in range(0, len(sheets)):

        sheet = excel_table.parse(i)
        if state is None:
            name = std.standardize_name('B', i, tb_type, year, month)
        else:
            name = std.standardize_name(state, i, tb_type, year, month)

        path = std.get_path(filename) + name
        final_names.append(path+'.csv')
        sheet.to_csv(path_or_buf=path+'.csv', sep=',', index=False, encoding='latin-1')

    return final_names


def get_std_name(tb_type, num, year=None, month=None, state='B'):
    """ Get the standart name for tables """
    name = std.standardize_name(state, num, tb_type, year, month)
    return name


def fileto_postgre(filename, tablename, dbname):
    """ Converts a .csv file to a postgres database table """
    myfile = open(filename, 'r')
    header = myfile.readline()
    print header
    col_list = header.split(',')
    col_list[-1] = col_list[-1].rstrip()

    for i in  col_list:
        print i

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
    print string

    for row in data:

        string = ''
        for col in row:
            string += col
            string += ','
        string += '\n'
        myfile.write(string)

    myfile.close()
            