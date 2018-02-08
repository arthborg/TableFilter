#!/usr/bin/python2.7

""" Holds the table frame class and its methods """

import Tkinter as tk
import ttk
import tb_code.typehandle as tph
import tb_code.pypostgre as ppg
import tb_code.standart as std


class TableFrame(tk.Frame):
    """ Implements the table frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Tabela: ').grid(row=0, column=0, pady=5, padx=5)
        tk.Label(self, text='Tipo: ').grid(row=1, column=0, pady=5, padx=5)

        self.type_combobox = ttk.Combobox(self, state='readonly')
        self.table_combobox = ttk.Combobox(self, state='readonly')

        self.update_button = tk.Button(
            self, text='Atualizar Dados', command=self.__update_comboboxes)

        self.type_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.table_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.update_button.grid(row=2, column=1, pady=5, padx=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.__update_comboboxes()

    def __update_comboboxes(self):
        """ Updates the values of the comboboxes """

        all_tables = ppg.get_table_names(std.DBNAME)
        all_types = tph.get_analysis_type_names()

        self.table_combobox['values'] = all_tables
        self.type_combobox['values'] = all_types

    def get_type(self):
        """ Returns the value of the type combobox """

        return self.type_combobox.get()

    def get_table(self):
        """ Returns the value of the table combobox """

        return self.table_combobox.get()
