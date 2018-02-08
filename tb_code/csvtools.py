#!/usr/bin/python2.7

""" Useful functions to normalize .csv files """

from shutil import copyfile
import os
import csv


def convert_to_unicode(filename, newfile):
    """ Encodes a csv file on UTF-8 """

    # Sets the new and old filenames
    if filename == newfile:
        copyfile(filename, 'temp')
        old_name = 'temp'
        new_name = filename
    else:
        old_name = filename
        new_name = newfile

    # Opens the files for the operation
    with open(old_name, 'r') as old_file, open(new_name, 'w') as new_file:

        indata = csv.reader(old_file)
        outdata = csv.writer(new_file)

        # Converts the string on the old file to a UTF-8 string, and prints it cn the new file
        for row in indata:
            new_row = []
            for data in row:
                new_row.append(data.decode('latin1').encode('utf8'))
            outdata.writerow(new_row)

    # Deletes the temporary files created
    if filename == newfile:
        os.remove('temp')


def semicolon_to_comma(filename, newfile):
    """ Converts a csv file with ';' separators to ',' separators """

    if filename == newfile:
        copyfile(filename, 'temp')
        old_file = open('temp', 'r')
        new_file = open(filename, 'w')
    else:
        old_file = open(filename, 'r')
        new_file = open(newfile, 'w')

    while True:
        char = old_file.read(1)
        if not char:
            break
        if char == ';':
            new_file.write(',')
        else:
            new_file.write(char)

    old_file.close()
    new_file.close()
    if filename == newfile:
        os.remove('temp')
