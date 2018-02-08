""" Init module of tb_code package """

import os
import inspect
import tb_code.standart as std

CUR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PAR = os.path.dirname(CUR)

std.LOG_FILE = PAR + '/files/.log'
std.TYPE_FILENAME = PAR + '/files/types.dat'
std.EXCEL_STD_PATH = PAR + '/files/excel_files'
std.CSV_STD_PATH = PAR + '/files/csv_files'
