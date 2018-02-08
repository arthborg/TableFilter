#!/usr/bin/python2.7

""" Holds the selection interface and its methods """

import Tkinter as tk
import ttk
import tb_code.pypostgre as ppg
import tb_code.typehandle as tph
import tb_code.standart as std


class SelectionFrame(tk.Frame):
    """ Implements the selection frame interface """

    def __init__(self, parent, mainframe):

        tk.Frame.__init__(self, parent)
        self.father = mainframe

        tk.Label(self, text='Tabela: ').grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text='Tipo :').grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text='Obs: A filtragem e feita com base no tipo da planilha').grid(
            row=2, columnspan=2, padx=5, pady=5)

        self.update_button = tk.Button(
            self, text='Atualizar dados', command=self.__update_comboboxes)

        self.table_combobox = ttk.Combobox(self, state='readonly')
        self.type_combobox = ttk.Combobox(self, state='readonly')

        self.update_button.grid(row=3, columnspan=2, padx=5, pady=5)
        self.table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.type_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.type_combobox.bind("<<ComboboxSelected>>", self.__update_type)

        self.__update_comboboxes()

    def __update_type(self, *_):
        """ Update the value of the type name on the parent frame """
        pass
        #self.father.selected_type = self.type_combobox.get()

    def __update_comboboxes(self):
        """ Updates the value of the comboboxes """

        all_types = tph.get_type_names()
        all_tables = ppg.get_table_names(std.DBNAME)

        self.table_combobox['values'] = all_tables
        self.type_combobox['values'] = all_types

    def get_table(self):
        """ Returns the value of the table combobox """

        return self.table_combobox.get()

    def get_type(self):
        """ Returns the value of the type combobox """

        return self.type_combobox.get()
