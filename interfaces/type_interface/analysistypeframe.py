#!/usr/bin/python3

""" Analysis frame for the create type interface """

import Tkinter as tk


class AnalysisTypeFrame(tk.Frame):
    """ Implements the analysis type interface """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Analise Geral').grid(
            row=0, columnspan=2, padx=5)
        tk.Label(self, text='Fazer analise pela coluna**: ').grid(
            row=1, column=0, padx=5)
        tk.Label(self, text='Analisar coluna**: ').grid(
            row=2, column=0, padx=5)
        tk.Label(self, text='Calculo de Esgotamento').grid(
            row=3, columnspan=2, padx=5)
        tk.Label(self, text='Coluna correspondente ao Total***').grid(
            row=4, column=0, padx=5)
        tk.Label(self, text='Coluna correspondente a disponibilidade').grid(
            row=5, column=0, padx=5)

        tk.Label(self, text='**Necessario e obrigratorio para fazer a analise').grid(
            row=6, columnspan=2, padx=5)
        tk.Label(self, text='***Necessario e obrigratorio para fazer calculo de esgotamento').grid(
            row=7, columnspan=2, padx=5)

        self.main_entry = tk.Entry(self)
        self.target_entry = tk.Entry(self)
        self.total_entry = tk.Entry(self)
        self.avial_entry = tk.Entry(self)

        self.main_entry.grid(row=1, column=1, padx=5)
        self.target_entry.grid(row=2, column=1, padx=5)
        self.total_entry.grid(row=4, column=1, padx=5)
        self.avial_entry.grid(row=5, column=1, padx=5)

    def get_main(self):
        """ Gets the value of the main entry """
        return self.main_entry.get()

    def get_target(self):
        """ Gets the value of the target entry """
        return self.target_entry.get()

    def get_total(self):
        """ Gets the value of the total entry """
        return self.total_entry.get()

    def get_avail(self):
        """ Gets the value of the available entry """
        return self.avial_entry.get()
