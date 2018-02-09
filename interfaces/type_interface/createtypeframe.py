#!/usr/bin/python2.7

""" Holds the create type frame class and its methods """

import Tkinter as tk
import tkMessageBox
import tb_code.typehandle as tph
import tb_code.standart as std
from interfaces.type_interface.filtertypeframe import FilterTypeFrame
from interfaces.type_interface.analysistypeframe import AnalysisTypeFrame


class CreateTypeFrame(tk.Frame):
    """ Implements the create type frame interface """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        self.filter_labelframe = tk.LabelFrame(
            self, text='Configuracoes de Filtragem')
        self.analysis_labelframe = tk.LabelFrame(
            self, text='Configuracoes de Analise')

        self.filter_frame = FilterTypeFrame(self.filter_labelframe)
        self.filter_labelframe.pack()
        self.filter_frame.pack()

        self.analysis_frame = AnalysisTypeFrame(self.analysis_labelframe)
        self.analysis_labelframe.pack(fill=tk.BOTH)
        self.analysis_frame.pack()

        tk.Label(self, text='Nome do tipo').pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.create_button = tk.Button(
            self, text='Criar novo tipo', command=self.__create_type)

        self.create_button.pack()

    def __create_type(self):

        name = self.name_entry.get()
        if name == '':
            tkMessageBox.showerror('Error', 'Voce nao digitou um nome')
            return

        grlist = self.filter_frame.get_group_names()
        final_group = []
        for data in grlist:

            if data[0] == '':
                continue
            final_group.append(data)

        ctlist = self.filter_frame.get_count_names()
        final_count = []
        for data in ctlist:

            if data[0] == '':
                continue
            final_count.append(data)

        if final_count == [] and final_group == []:
            tkMessageBox.showerror('Error', 'Voce nao informou nenhuma coluna')
            return

        main_name = self.analysis_frame.get_main()
        target_name = self.analysis_frame.get_target()
        total_name = self.analysis_frame.get_total()
        avail_name = self.analysis_frame.get_avail()

        if main_name == '' and target_name == '' and total_name == '' and avail_name == '':
            answer = tkMessageBox.askquestion('Atencao', 'Nenhuma coluna de analize informada! ' +
                                              'Prosseguir mesmo assim? Obs.: Nao sera possivel ' +
                                              'fazer analizes estatisticas!')
            if answer == 'no':
                return
        elif main_name == '' or target_name == '':
            tkMessageBox.showerror(
                'Erro', 'Para analize e preciso que as colunas marcadas em ** sejam preenchidas')
            return
        elif avail_name != '' and total_name == '':
            tkMessageBox.showerror('Erro', 'Para calculo de esgotamento e preciso que as colunas' +
                                   ' marcadas em *** sejam preenchidas')
            return

        tph.write_new_type(std.TYPE_FILENAME, name, final_count,
                           final_group, main_name, target_name, total_name, avail_name)

        tkMessageBox.showinfo('Sucesso', 'Seu novo tipo foi cadastrado!')
        self.grid_forget()
        self.filter_frame.clear()
