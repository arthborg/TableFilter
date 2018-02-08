#!/usr/bin/python2.7

""" Holds the rename table interface and its methods """

import Tkinter as tk
import tkMessageBox
import tb_code.standart as std
import tb_code.pypostgre as ppg


class RenameTableFrame(tk.Frame):
    """ Implements the rename table frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.table_entry = tk.Entry(self, text='')
        self.newname_entry = tk.Entry(self, text='')

        self.rename_label = tk.Label(self, text='Renomear: ')
        self.to_label = tk.Label(self, text='Para: ')

        self.rename_button = tk.Button(
            self, text='Renomear!', command=self.__rename)

        self.table_entry.grid(row=0, column=1, pady=10, padx=5)
        self.newname_entry.grid(row=0, column=3, pady=10, padx=5)
        self.rename_label.grid(row=0, column=0, pady=10, padx=5)
        self.to_label.grid(row=0, column=2, pady=10, padx=5)
        self.rename_button.grid(row=0, column=4, pady=10, padx=5)

    def __rename(self):

        new_name = self.newname_entry.get()
        if new_name == '':
            tkMessageBox.showerror('Error', 'Voce nao digitou um nome')
            return
        old_name = self.table_entry.get()

        ppg.rename_table(std.DBNAME, old_name, new_name)
        tkMessageBox.showinfo('Sucesso', 'Sua tabela foi renomeada')
        self.grid_forget()

    def set_table_name(self, name):
        """ Sets the table name for rename """

        self.table_entry.config(state='normal')
        self.table_entry.delete(0, tk.END)
        self.table_entry.insert(0, name)
        self.table_entry.config(state='disable')
