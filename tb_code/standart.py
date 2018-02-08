#!/usr/bin/env python 2.7
""" Standart functions and constants useful on the program """

import datetime

# Defining common names

GROWTH = 'TAXA DE CRESCIMENTO'
PREDICTION = 'PREVISAO PROXIMO MES'
EXHAUSTION = 'PREVISAO DE ESGOTAMENTO'

# Defining programming constants

SSE_ALPHA = 0.5
DBNAME = 'capacidade'
TYPE_FILENAME = '../files/types.dat'
LOG_FILE = '../files/.log'
EXCEL_STD_PATH = ''
CSV_STD_PATH = ''

# Defining Exceptions


class WrongNameException(Exception):
    """ Raised when there are problem with names """
    pass


def get_path(filename):
    """ Gets the path of a certain file """

    string = filename.split('/')
    final = ''

    for i in range(0, len(string) - 1):
        final += string[i] + '/'

    return final


def standardize_name(num, tb_type, year=None, month=None):
    """ Standardize name on fomat 'YY-MM-TYPE-NUM' - Rarely used """

    if not isinstance(tb_type, str):
        raise WrongNameException('Invalid Table Type Name {}.'.format(tb_type))

    if not isinstance(num, int):
        raise WrongNameException('Invalid Table Number {}.'.format(tb_type))

    now = datetime.datetime.now()

    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if year > 99:
        year = year % 100

    if year < 0 or month <= 0 or month > 12:
        raise WrongNameException('Invalid Date {}/{}.'.format(month, year))

    final_year = str(year).rjust(2, '0')
    final_month = str(month).rjust(2, '0')
    final_num = str(num)

    name = final_year + '-' + final_month + '-' + tb_type + '-' + final_num

    print_log('Standardize Name called - Final name is ' + name)

    return name


def print_log(message):
    """ Prints a message on the log file """

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')


def clean_log_file():
    """ Cleans the log file """

    open(LOG_FILE, 'w').close()
