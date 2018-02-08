#!/usr/bin/python2.7

""" Holds the selection frame class and its methods """

import Tkinter as tk
import tb_code.pypostgre as ppg
import tb_code.standart as std


class SelectionFrame(tk.Frame):
    """ Implements the selection frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Selecione as tabelas de forma que a observacao mais recente seja a ' +
                 'primeira e a mais antiga seja a ultima').grid(row=0, columnspan=2, padx=5, pady=5)
        tk.Label(self, text='Tabelas na base de dados').grid(
            row=1, column=0, padx=10, pady=5)
        tk.Label(self, text='Tabelas selecionadas').grid(
            row=1, column=1, padx=10, pady=5)
        tk.Label(self, text='* Necessario selecionar no ' +
                 'minimo 2 tabelas').grid(row=3, columnspan=2, padx=5, pady=10)
        tk.Button(self, text='Atualizar Tabelas', command=self.__update_tables).grid(
            row=4, columnspan=2, padx=5, pady=5)

        self.database_listbox = tk.Listbox(self)
        self.selected_listbox = tk.Listbox(self)

        self.database_listbox.grid(row=2, column=0, padx=5, pady=5)
        self.selected_listbox.grid(row=2, column=1, padx=5, pady=5)

        self.database_listbox.bind('<Double-Button-1>', self.__double_database)
        self.selected_listbox.bind('<Double-Button-1>', self.__double_selected)

        self.__update_tables()
        self.get_selected()

    def get_selected(self):
        """ Gets the selected tables """

        selected = self.selected_listbox.get(0, tk.END)
        return selected

    def __update_tables(self):
        """ Updates the database tables on the listbox """

        self.database_listbox.delete(0, tk.END)
        selected_tables = self.selected_listbox.get(0, tk.END)

        table_names = ppg.get_table_names(std.DBNAME)
        for table in table_names:
            if table not in selected_tables:
                self.database_listbox.insert(tk.END, table)

    def __double_selected(self, *_):
        """ Executed when the user double clicks a table on the selected listbox """

        try:
            selected = self.selected_listbox.curselection()[0]
        except IndexError:
            return

        data = self.selected_listbox.get(selected)
        self.selected_listbox.delete(selected)
        self.database_listbox.insert(tk.END, data)
        self.__update_tables()

    def __double_database(self, *_):
        """ Executed when the user double clicks a table on the database listbox """

        try:
            selected = self.database_listbox.curselection()[0]
        except IndexError:
            return

        selected = self.database_listbox.get(selected)
        self.selected_listbox.insert(tk.END, selected)
        self.__update_tables()
