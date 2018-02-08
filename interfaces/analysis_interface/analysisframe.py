#!/usr/bin/python2.7

""" Holds the analysis frame class and its methods """


import Tkinter as tk
import tkMessageBox
from interfaces.analysis_interface.tableframe import TableFrame
from interfaces.analysis_interface.selectionframe import SelectionFrame
from interfaces.analysis_interface.configurationframe import ConfigurationFrame
import tb_code.standart as std
import tb_code.analytics as anl
import tb_code.typehandle as tph


class AnalysisFrame(tk.Frame):
    """ Implements the analysis frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.table_labelframe = tk.LabelFrame(self, text='Tabela')
        self.selection_labelframe = tk.LabelFrame(self, text='Selecao')
        self.config_labelframe = tk.LabelFrame(self, text='Configuracoes')

        self.table_frame = TableFrame(self.table_labelframe)
        self.selection_frame = SelectionFrame(self.selection_labelframe)
        self.config_frame = ConfigurationFrame(self.config_labelframe)

        self.analysis_button = tk.Button(
            self, text='Fazer Analise', command=self.__analize)

        self.table_labelframe.pack(fill=tk.BOTH)
        self.selection_labelframe.pack(fill=tk.BOTH)
        self.config_labelframe.pack(fill=tk.BOTH)

        self.table_frame.pack(fill=tk.BOTH)
        self.selection_frame.pack(fill=tk.BOTH)
        self.config_frame.pack(fill=tk.BOTH)

        self.analysis_button.pack()

    def __analize(self):
        """ Analyses the table """

        table_name = self.table_frame.get_table()
        if table_name == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou uma tabela')
            return

        table_type = self.table_frame.get_type()
        if table_type == '':
            tkMessageBox.showerror('Error', 'Voce nao selecionou um tipo')
            return

        selected = self.selection_frame.get_selected()
        if len(selected) < 2:
            tkMessageBox.showerror(
                'Error', 'Voce precisa selecionar no minino 2 tabelas')
            return

        analysis_type = self.config_frame.get_selected()
        if analysis_type == '':
            tkMessageBox.showerror(
                'Error', 'Voce precisa escolher um tipo de analise')
            return

        growth = self.config_frame.get_growth()
        exhaustion = self.config_frame.get_exhaustion()

        if exhaustion == 1 and (tph.get_exhaustion_flag(table_type) is False):
            tkMessageBox.showerror(
                'Error', 'O tipo ' + table_type + ' nao pode ter seu esgotamento analisado!')
            return

        selected = selected[::-1]

        if analysis_type == 'sse':
            anl.simple_exp(std.DBNAME, table_name, selected, table_type)
        elif analysis_type == 'avg':
            anl.avg_move(std.DBNAME, table_name, selected, table_type)

        if growth == 1:
            anl.growth_rate(std.DBNAME, table_name, table_type)
        if exhaustion == 1:
            anl.months_to_exhaustion(std.DBNAME, table_name, table_type)
