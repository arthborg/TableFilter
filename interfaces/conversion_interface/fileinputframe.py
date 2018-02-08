#!/usr/bin/python2.7

""" Holds the FileInputFrame interface and its methods """

import Tkinter as tk
from tkFileDialog import askopenfilename


class FileInputFrame(tk.Frame):
    """ Implements the file input frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.file_label = tk.Label(self, text='Arquivo: ')
        self.name_label = tk.Label(self, text='Novo nome: ')

        self.search_button = tk.Button(
            self, text='Procurar', command=self.search_file)

        self.file_entry = tk.Entry(self, width=50)
        self.name_entry = tk.Entry(self)

        self.csv_variable = tk.IntVar()
        self.csv_checkbox = tk.Checkbutton(
            self, text='Gerar arquivo .csv', variable=self.csv_variable)

        self.__grid_all()

    def __grid_all(self):

        self.file_label.grid(row=0, column=0, pady=5, padx=10)
        self.file_entry.grid(row=0, column=1, pady=5)
        self.search_button.grid(row=0, column=2, pady=5, padx=10)

        self.csv_checkbox.grid(row=1, columnspan=3, pady=5)

        self.name_label.grid(row=2, column=0, pady=5, padx=10)
        self.name_entry.grid(row=2, column=1, pady=5)

    def get_filename(self):
        """ Gets the filename """

        return self.file_entry.get()

    def get_rename(self):
        """ Gets the new name """

        return self.name_entry.get()

    def search_file(self):
        """ Opens a window so the user can search for the file """

        filename = askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def get_csv_status(self):
        """ Gets the status of the csv_variable """

        if self.csv_variable.get() == 1:
            return True
        return False
