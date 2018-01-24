import os
import xlrd
import pandas as pd
import psycopg2 as psy
import standart as std
import pypostgre as ppg


#==============================================================================
### TO_CSV


def n_sheets(filename):
    excel_table = pd.ExcelFile(filename)
    sheets = excel_table.sheet_names
    return len(sheets)


def get_sheet_names(filename):

    excel_table = xlrd.open_workbook(filename, on_demand=True)
    sheets = excel_table.sheet_names()
    return sheets

def to_csv(filename, tb_type, yy = None, mm = None, state = None):

    excel_table = pd.ExcelFile(filename)
    sheets = excel_table.sheet_names
    final_names = []

    for i in range(0, len(sheets)):

        sheet = excel_table.parse(i)
        if state is None:
            name = std.standardize_name('B', i, tb_type, yy, mm)
        else:
            name = std.standardize_name(state, i, tb_type, yy, mm)

        path = std.get_path(filename) + name
        final_names.append(path+'.csv')
        sheet.to_csv(path_or_buf = path+'.csv', sep=',', index = False, encoding='utf-8')

    return final_names



def get_std_name(tb_type, num, yy = None, mm = None, state = 'B'):
    
    name = std.standardize_name(state, num, tb_type, yy, mm)
    
    return name


def fileto_postgre(filename, tablename, dbname):

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

    data = ppg.select_all(dbname, table)
    myfile = open(path, 'w')

    for row in data:

        s = ''
        for col in row:
            s += col
            if col is not row[-1]:
                s += ','
        s += '\n'
        myfile.write(s)

    myfile.close()
            
