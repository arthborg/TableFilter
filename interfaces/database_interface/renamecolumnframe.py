#!/usr/bin/python2.7

""" Holds the Column rename frame class and its methods """

import Tkinter as tk
import tkMessageBox
import ttk
import tb_code.pypostgre as ppg
import tb_code.standart as std


class RenameColumnFrame(tk.Frame):
    """ Implements the rename column interface """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Selecione a coluna que deseja renomear').grid(
            row=0, columnspan=2, padx=5, pady=5)
        tk.Label(self, text='Coluna: ').grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text='Renomear para: ').grid(
            row=2, column=0, padx=5, pady=5)

        self.column_combobox = ttk.Combobox(self, state='readonly')
        self.rename_entry = tk.Entry(self, text='')

        self.rename_button = tk.Button(
            self, text='Renomear!', command=self.__rename_column)
        self.table_name = None

        self.column_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.rename_entry.grid(row=2, column=1, padx=5, pady=5)
        self.rename_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def __rename_column(self):
        """ Renames the column """

        column_selected = self.column_combobox.get()
        new_name = self.rename_entry.get()

        if column_selected == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou uma coluna')
            return
        if new_name == '':
            tkMessageBox.showerror('Error', 'Voce nao digitou um nome')
            return

        ppg.rename_column(std.DBNAME, self.table_name,
                          column_selected, new_name)
        tkMessageBox.showinfo('Sucesso', 'A coluna foi renomeada!')

    def selected_table(self, table):
        """ Sets the selected table and the column rename options """

        self.rename_entry.delete(0, tk.END)
        self.table_name = table
        columns = ppg.get_columns(std.DBNAME, self.table_name)
        self.column_combobox['values'] = columns
