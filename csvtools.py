#!/usr/bin/env Python 2.7

""" Useful functions to normalize .csv files """

from shutil import copyfile
import os
import csv


def convert_to_unicode(filename, newfile):

    if filename == newfile:
        copyfile(filename, 'temp')
        old_name = 'temp'
        new_name = filename
    else:
        old_name = filename
        new_name = newfile

    with open(old_name, 'r') as old_file, open(new_name, 'w') as new_file:
        
        indata = csv.reader(old_file)
        outdata = csv.writer(new_file)

        for row in indata:
            new_row = []
            for data in row:
                new_row.append(data.decode('latin1').encode('utf8'))
            #print new_row
            outdata.writerow(new_row)   

    

def semicolon_to_comma(filename, newfile):
    
    if filename == newfile:
        copyfile(filename, 'temp')
        f = open('temp', 'r')
        n = open(filename, 'w')
    else:
        f = open(filename, 'r')
        n = open(newfile, 'w')

    while True:
        s = f.read(1)
        if not s:
            break
        if s == ';':
            n.write(',')
        else:
            n.write(s)

    f.close()
    n.close()
    if filename == newfile:
        os.remove('temp')