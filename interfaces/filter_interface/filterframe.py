#!/usr/bin/python2.7

""" Holds the filter interface class and its methods """

import Tkinter as tk
import tkMessageBox
import tb_code.typehandle as tph
import tb_code.pypostgre as ppg
import tb_code.standart as std
from interfaces.filter_interface.selectionframe import SelectionFrame
from interfaces.filter_interface.optionframe import OptionFrame


class FilterFrame(tk.Frame):
    """ Implements the filter frame interface """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.selection_labelframe = tk.LabelFrame(
            self, text='Selecao', pady=10, padx=10)
        self.options_labelframe = tk.LabelFrame(
            self, text='Opcional', pady=10, padx=10)
        self.filter_button = tk.Button(
            self, text='Filtrar Tabela', command=self.__filter_table)

        self.selection_frame = SelectionFrame(self.selection_labelframe, self)
        self.options_frame = OptionFrame(self.options_labelframe, self)
        self.selected_type = None

        self.selection_frame.pack()
        self.options_frame.pack()

        self.selection_labelframe.pack(fill='both')
        self.options_labelframe.pack(fill='both')
        self.filter_button.pack(pady=10, padx=10)

    """
    def get_selected_type(self):
        return self.selected_type
    """

    def __filter_table(self):

        table_name = self.selection_frame.get_table()
        table_type = self.selection_frame.get_type()

        if table_name == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou uma tabela!')
            return
        if table_type == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou um tipo!')
            return

        if self.options_frame.get_rename_value() == 1:
            name = self.options_frame.get_rename()
            if name == '':
                tkMessageBox.showerror('Error', 'Voce nao digitou um nome')
                return
            elif name.find('"') != -1 or name.find("'") != -1:
                tkMessageBox.showerror(
                    'Error', 'O nome nao pode conter "" ou \'\'!')
                return
        else:
            name = table_name + '-FILTERED'

        order = self.options_frame.get_order()
        if order == '':
            order = None

        tkMessageBox.showinfo(
            'Processando', 'Sua tabela esta sendo filtrada, isso pode demorar alguns minutos!')

        wanted_list = tph.get_group_list(table_type)
        count_list = tph.get_count_list(table_type)

        # print 'all ', tph.get_type_names()
        # print 'wanted ', wanted_list
        # print 'counte ', count_list

        ppg.agroup_table(std.DBNAME, table_name, name,
                         wanted_list, count_list, order)

        tkMessageBox.showinfo(
            'Sucesso', 'Sua tabela foi filtrada e adicionada a base de dados com o nome ' + name)
