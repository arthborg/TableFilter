#!/usr/bin/python2.7

""" Holds the configuration frame class and its methods """

import Tkinter as tk


class ConfigurationFrame(tk.Frame):
    """ Implements the configuration frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Tipo de Analise').grid(
            row=0, columnspan=2, padx=5, pady=5)
        tk.Label(self, text='O que analisar').grid(
            row=2, columnspan=2, padx=5, pady=10)

        self.exp_smooth = tk.IntVar()
        self.exponential_checkbox = tk.Checkbutton(
            self, text='Suavizacao Exponencial', variable=self.exp_smooth)
        self.exponential_checkbox.grid(row=1, column=0, padx=5, pady=5)

        self.mov_avg = tk.IntVar()
        self.average_checkbox = tk.Checkbutton(
            self, text='Media Movel', variable=self.mov_avg)
        self.average_checkbox.grid(row=1, column=1, padx=5, pady=5)

        self.growth = tk.IntVar()
        tk.Checkbutton(self, text='Taxa de Crescimento', variable=self.growth).grid(
            row=3, column=0, padx=5, pady=5)

        self.exhaustion = tk.IntVar()
        tk.Checkbutton(self, text='Esgotamento (em meses)', variable=self.exhaustion).grid(
            row=3, column=1, padx=5, pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.average_checkbox.bind('<Button-1>', self.__unmark_exponential)
        self.exponential_checkbox.bind('<Button-1>', self.__unmark_average)

    def __unmark_exponential(self, *_):
        """ Unmarks the exponential_checkbox """

        self.exp_smooth.set(0)

    def __unmark_average(self, *_):
        """ Unmarks the average_checkbox """

        self.mov_avg.set(0)

    def get_selected(self):
        """ Gets the selected analysis """

        if self.exp_smooth.get() == 1:
            return 'sse'
        elif self.mov_avg.get() == 1:
            return 'avg'
        return ''

    def get_growth(self):
        """ Returns the value of the growth checkbox """

        return self.growth.get()

    def get_exhaustion(self):
        """ Returns the value of the exhaustion checkbox """

        return self.exhaustion.get()
