#!/usr/bin/python2.7

""" A useful library for postgresql """

import psycopg2 as psy
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Exceptions


class SQLException(Exception):
    """ Raised when there is an error with the sql command """
    pass


class InvalidInput(Exception):
    """ Raised when invalid input is found """
    pass


class FailedConnection(Exception):
    """ Raised when failed to connect to the database """
    pass


def format_string_sql(stm, str_type=0):
    """ Formats a string using sql rules "" for names and '' for values """

    if str_type == 0 and stm[0] != '"':
        return '"' + stm + '"'
    elif str_type == 1 and stm[0] != '\'':
        return '\'' + stm + '\''
    return stm


def get_columns(dbname, table):
    """ Returns the name of the columns of a database """

    table = format_string_sql(table)
    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    try:
        curs.execute('SELECT * FROM ' + table)
        columns = [i[0] for i in curs.description]
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        columns = []

    return columns


def select_data(dbname, table, wanted_cols, col_name, col_value):
    """ Selects raw data from the table """

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)
    col_value = format_string_sql(col_value, str_type=1)

    formated = []
    for i, item in enumerate(wanted_cols):
        formated.append(format_string_sql(item))

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    command = 'SELECT ' + formated[0]
    for i in range(1, len(formated)):
        command += ', ' + formated[i]
    command += ' FROM ' + table + ' WHERE ' + col_name + ' = ' + col_value

    try:
        curs.execute(command)
        data = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    conn.close()
    return data


def add_column(dbname, table, col_name):
    """ Adds a column to the table """

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)

    command = 'ALTER TABLE ' + table + \
        ' ADD COLUMN ' + col_name + 'VARCHAR(50)'
    try:
        curs.execute(command)
        conn.commit()
    except psy.ProgrammingError:
        conn.rollback()

    conn.close()


def rename_column(dbname, table, old_name, new_name):
    """ Renames a column on the table """

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    table = format_string_sql(table)
    old_name_ft = format_string_sql(old_name)
    new_name_ft = format_string_sql(new_name)

    command = 'ALTER TABLE ' + table + ' RENAME COLUMN ' + \
        old_name_ft + ' TO ' + new_name_ft

    try:
        curs.execute(command)
        conn.commit()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        if old_name not in get_columns(dbname, table):
            raise SQLException(
                'Column name {} not found on table {}'.format(old_name, table))

    conn.close()


def get_table_names(dbname):
    """ Gets the table names from the database """

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    command = 'SELECT table_name FROM information_schema.tables WHERE table_type = \
    \'BASE TABLE\' AND table_schema NOT IN (\'pg_catalog\', \'information_schema\')'
    curs.execute(command)

    tables = curs.fetchall()
    if tables == []:
        return tables

    final = []
    for i in tables:
        final.append(i[0])

    return final


def create_database(dbname, pswd):
    """ Creates a database """

    try:
        conn = psy.connect(user='postgres', host='localhost', password=pswd)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        curs.execute('CREATE DATABASE ' + dbname)

    except psy.InternalError:
        raise SQLException('Cannot create database! Do it manually')
    except psy.OperationalError:
        raise SQLException('Wrong password!')


def check_database(dbname):
    """ Checks if the database exists """

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        conn.close()
        return True
    except psy.OperationalError:
        return False


def validate_string_sql(stm):
    """ Checks if the user has typed a bad string """

    if stm.find('"') == -1:
        raise InvalidInput('Malicious input detected {}'.format(stm))


def select_single_data(dbname, table, wanted, col_name, col_value):
    """ Selects a single piece of data from the table """

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)
    col_value = format_string_sql(col_value, str_type=1)
    wanted = format_string_sql(wanted)

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    command = 'SELECT ' + wanted + ' FROM ' + table + \
        ' WHERE ' + col_name + ' = ' + col_value

    try:
        curs.execute(command)
        data = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    if len(data) > 1:
        return False

    data = data[0][0]
    conn.close()
    return data


def select_data_like(dbname, table, wanted_cols, col_name, col_value):
    """ Selects the data from the table using the like syntax """

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)
    col_value = format_string_sql(col_value, str_type=1)

    formated = []
    for i, item in enumerate(wanted_cols):
        formated.append(format_string_sql(item))

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    command = 'SELECT ' + formated[0]
    for i in range(1, len(formated)):
        command += ', ' + formated[i]
    command += ' FROM ' + table + ' WHERE ' + col_name + ' LIKE ' + col_value

    try:
        curs.execute(command)
        data = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    conn.close()
    return data


def create_table(dbname, table, col_names):
    """ Creates a new table on the database """

    table = format_string_sql(table)
    command = 'CREATE TABLE ' + table + ' ('

    for i in col_names:

        string = format_string_sql(i)

        command += string + ' VARCHAR(50)'
        if i is col_names[-1]:
            command += ')'
        else:
            command += ', '

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    print command

    try:
        curs.execute(command)
        conn.commit()
    except psy.ProgrammingError:
        conn.rollback()
        raise SQLException('Unable to create table!')

    conn.close()


#                 str         str     str      list of tup  list of trip -> 3rd is also list (or)
def agroup_table(dbname, table_from, table_to, wanted_cols, count_cols=None, order=None):
    """ Group a table based on the parameters passed """

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))

    table_from = format_string_sql(table_from)
    table_to = format_string_sql(table_to)

    command = 'SELECT '
    for i in wanted_cols:
        command += format_string_sql(i[0])
        if i[1] != '' and i[1] != None:
            command += ' AS ' + format_string_sql(i[1])
        command += ', '

    if count_cols != None and count_cols != []:
        for i in count_cols:

            if i[2] == [''] or i[2] is None or i[2] == []:
                command += 'COUNT (' + format_string_sql(i[0]) + ')'
            else:
                command += 'COUNT ( CASE '
                for cond in i[2]:
                    command += 'WHEN ' + \
                        format_string_sql(i[0]) + ' = ' + \
                        format_string_sql(cond, 1) + ' THEN 1 '
                command += 'ELSE Null END )'

            if i[1] == '' or i[1] is None:
                command += ' AS "COUNT ' + format_string_sql(i[0]) + '"'
            else:
                command += ' AS ' + format_string_sql(i[1])

            if i is not count_cols[-1]:
                command += ', '

    command += ' INTO ' + table_to + ' FROM ' + table_from + ' GROUP BY '

    for i in wanted_cols:
        command += format_string_sql(i[0])
        if i is not wanted_cols[-1]:
            command += ', '

    if order is not None:
        command += ' ORDER BY ' + format_string_sql(order)

    print command

    try:
        curs.execute(command)
        conn.commit()
        conn.close()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to execute command')


def select_single_distinct(dbname, table, col_name):
    """ Select distincts pieces of data from the table """

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)

    try:
        conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
        curs = conn.cursor()
    except psy.OperationalError:
        raise FailedConnection('Unable to connect to {}'.format(dbname))
    command = 'SELECT DISTINCT ' + col_name + ' FROM ' + table

    print command
    try:
        curs.execute(command)
        cols = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    if cols == []:
        return cols

    final = []
    for i in cols:
        final.append(i[0])

    conn.close()
    return final


def set_value(dbname, data, table, wanted, col_name, col_value):
    """ Sets the value of a specified row """

    table = format_string_sql(table)
    col_name = format_string_sql(col_name)
    col_value = format_string_sql(col_value, str_type=1)
    wanted = format_string_sql(wanted)

    if isinstance(data, str):
        data = str(data)

    data = format_string_sql(data, str_type=1)

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    command = 'UPDATE ' + table + ' SET ' + wanted + ' = ' + data + ' WHERE ' + \
        col_name + ' = ' + col_value

    print command

    try:
        curs.execute(command)
        conn.commit()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to execute command')

    conn.close()


def get_data_type(dbname, table, col_name):
    """ Gets the data type of a column """

    table = format_string_sql(table, str_type=1)
    col_name = format_string_sql(col_name, str_type=1)

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    command = 'SELECT data_type FROM information_schema.columns WHERE table_name \
    = ' + table + ' AND column_name = ' + col_name

    try:
        curs.execute(command)
        data = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    conn.close()

    if data[0][0] == 'character varying':
        return 'string'
    elif data[0][0].find('int') != -1:
        return 'int'
    return data[0][0]


def select_all(dbname, table):
    """ Selects all the data from the table """

    table = format_string_sql(table)

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    command = 'SELECT * FROM ' + table

    try:
        curs.execute(command)
        data = curs.fetchall()
    except psy.ProgrammingError:
        conn.rollback()
        conn.close()
        raise SQLException('Unable to fetch or failure on command execution')

    conn.close()
    return data


def copy_data(dbname, table, filename, header=True):
    """ Copy data of a csv file into a table """

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    csv_file = open(filename, 'r')

    if header is True:
        csv_file.readline()

    table = format_string_sql(table)

    curs.copy_from(csv_file, table, sep=',')
    conn.commit()
    csv_file.close()


def check_column(dbname, table, column_name, column_list=None):
    """ Checks if a column or a list of columns is in the especified table """

    if column_list is None:
        column_list = get_columns(dbname, table)

    if isinstance(column_name, str):
        return column_name in column_list

    for i in column_name:
        if i not in column_list:
            return False

    return True


def delete_table(dbname, table):
    """ Deletes the table """

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    table = format_string_sql(table)

    command = 'DROP TABLE ' + table
    print command

    curs.execute(command)
    conn.commit()
    conn.close()


def rename_table(dbname, oldname, newname):
    """ Renames the table """

    conn = psy.connect(dbname=dbname, user='postgres', host='localhost')
    curs = conn.cursor()

    oldname = format_string_sql(oldname)
    newname = format_string_sql(newname)

    command = 'ALTER TABLE ' + oldname + ' RENAME TO ' + newname

    try:
        curs.execute(command)
        conn.commit()
    except psy.ProgrammingError:
        conn.close()
        raise SQLException('Failed on command execution {}'.format(command))

    conn.close()
