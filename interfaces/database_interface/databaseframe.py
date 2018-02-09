#!/usr/bin/python2.7

""" Holds the database interface """

import Tkinter as tk
import tkMessageBox
import tb_code.pypostgre as ppg
import tb_code.standart as std
from interfaces.database_interface.renametableframe import RenameTableFrame
from interfaces.database_interface.excelframe import ExcelFrame
from interfaces.database_interface.renamecolumnframe import RenameColumnFrame


class DatabseFrame(tk.Frame):
    """ Implements the database frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.database_listbox = tk.Listbox(self)

        tk.Button(self, text='Excluir', command=self.__delete,
                  width=20).grid(row=2, column=0, pady=5, padx=5)

        tk.Button(self, text='Renomear tabela', command=self.__show_rename_frame,
                  width=20).grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self, text='Renomear coluna', command=self.__show_rename_column,
                  width=20).grid(row=3, column=0, pady=5, padx=5)

        tk.Button(self, text='Gerar excel', command=self.__show_excel,
                  width=20).grid(row=3, column=1, pady=5, padx=5)

        tk.Label(self, text='Tabelas armazenadas na sua base de dados').grid(
            row=0, columnspan=2, pady=10, padx=10)

        self.rename_frame = RenameTableFrame(self)
        self.column_frame = RenameColumnFrame(self)
        self.excel_frame = ExcelFrame(self)

        self.database_listbox.grid(row=1, columnspan=2, pady=5, padx=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.__update_listbox()

    def __update_listbox(self):
        """ Updates the database listbox """

        self.database_listbox.delete(0, tk.END)
        tables = ppg.get_table_names(std.DBNAME)

        for table in tables:
            self.database_listbox.insert(tk.END, table)

    def __delete(self):
        """ Delets a table from the databse """

        name = self.__get_listbox_value()
        if name == '':
            return
        answer = tkMessageBox.askquestion(
            'Deletar', 'Deseja realmente excluir a tabela' + name)
        if answer == 'no':
            return
        else:
            ppg.delete_table(std.DBNAME, name)

        self.__forget()

    def __show_rename_frame(self):
        """ Show the rename frame """

        name = self.__get_listbox_value()
        if name == '':
            return

        self.rename_frame.grid(row=4, columnspan=2, padx=5, pady=10)
        self.rename_frame.set_table_name(name)

    def __show_rename_column(self):
        """ Shows the frame for rename columns """

        name = self.__get_listbox_value()
        if name == '':
            return
        self.column_frame.grid(row=4, columnspan=2, padx=5, pady=10)
        self.column_frame.selected_table(name)

    def __show_excel(self):
        """ Shows the frame to generate excel files """

        name = self.__get_listbox_value()
        if name == '':
            return
        self.excel_frame.grid(row=4, columnspan=2, padx=5, pady=10)
        self.excel_frame.selected_file(name)

    def __forget(self):
        """ Forgets all the frames on the grid """
        self.column_frame.grid_forget()
        self.rename_frame.grid_forget()
        self.excel_frame.grid_forget()

    def __get_listbox_value(self):
        """ Gets the listbox selected value """

        selected = self.database_listbox.curselection()
        if selected == ():
            tkMessageBox.showerror('Error', 'Nenhuma tabela selecionada')
            return ''

        selected = selected[0]
        return self.database_listbox.get(selected)
