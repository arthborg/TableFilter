#!/usr/bin/python2.7

""" Holds the excel frame class """

import Tkinter as tk
import tkMessageBox
import tkFileDialog
import tb_code.standart as std
import tb_code.convert as cvt


class ExcelFrame(tk.Frame):
    """ Implements the excel frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Digite ou procure o caminho onde o arquivo sera criado\n').grid(
            row=0, columnspan=2, pady=10, padx=5)

        self.file_label = tk.Label(self, text='')
        self.filename_entry = tk.Entry(self, text='', width=20)

        self.create_button = tk.Button(
            self, text='Gerar Excel', command=self.__to_excel)
        self.search_button = tk.Button(
            self, text='Procurar', command=self.__search_file)

        self.table_name = None

        self.file_label.grid(row=1, columnspan=2, pady=5, padx=10)
        self.filename_entry.grid(row=2, column=0, pady=5, padx=10)
        self.search_button.grid(row=2, column=1, pady=5, padx=10)

        self.create_button.grid(row=3, columnspan=2, pady=5, padx=10)

    def selected_file(self, name):
        """ Sets the selected file """

        self.file_label['text'] = 'Arquivo selecionado: ' + name
        self.table_name = name

    def __to_excel(self):
        """ Generates the excel file """

        directory = self.filename_entry.get()
        if directory == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou um diretorio')
            return
        directory += '/' + self.table_name + '.xlrd'

        tkMessageBox.showinfo('Gerando arquivo', 'Isso pode demorar um pouco!')
        cvt.to_table(directory, std.DBNAME, self.table_name)

        tkMessageBox.showinfo(
            'Concluido', 'O arquivo foi criado com sucesso')
        self.grid_forget()

    def __search_file(self):
        """ Searches a directory for the file """

        directory = tkFileDialog.askdirectory()
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, directory)
