#!/usr/bin/python2.7

""" Holds the AdvancedFrame interface and its methods """

import Tkinter as tk
import ttk

try:
    import tb_code.typehandle as tph
except ImportError:
    import os
    import sys
    import inspect
    CUR = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    PAR = os.path.dirname(CUR)
    GRAND = os.path.dirname(PAR)
    sys.path.insert(0, GRAND)
    import tb_code.typehandle as tph

import tb_code.standart as std


class AdvancedFrame(tk.Frame):
    """ Implements the advanced frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Tipo*: ').grid(row=0, column=0, pady=5, padx=10)
        tk.Label(self, text='Mes: ').grid(row=1, column=0, pady=5, padx=10)
        tk.Label(self, text='Ano: ').grid(row=2, column=0, pady=5, padx=10)

        self.month_entry = tk.Entry(self)
        self.year_entry = tk.Entry(self)

        self.standart_var = tk.IntVar()
        tk.Checkbutton(self, text='Usar nome padrao').grid(
            row=3, columnspan=3, pady=5)
        tk.Label(self, text='* Necessario caso deseje usar' +
                 ' o nome padrao').grid(row=4, columnspan=3, pady=5)

        self.update_button = tk.Button(self, text='Atualizar Tipos')
        self.type_combobox = ttk.Combobox(self, state='readonly')

        self.__grid_all()
        self.update_types()

    def __grid_all(self):
        """ Grid all the frame widgets """

        self.type_combobox.grid(row=0, column=1, pady=5)
        self.update_button.grid(row=0, column=2, pady=5, padx=10)

        self.month_entry.grid(row=1, column=1, pady=5)
        self.year_entry.grid(row=2, column=1, pady=5)

    def update_types(self):
        """ Update the type list """

        tph.initialize_types(std.TYPE_FILENAME)
        all_types = tph.get_type_names()
        std.print_log('Trying to update all types is ' + ''.join(all_types))
        self.type_combobox['values'] = all_types

    def get_year(self):
        """ Gets the year from the year_entry """

        return self.year_entry.get()

    def get_month(self):
        """ Gets the month from the month_entry """

        return self.month_entry.get()

    def get_type(self):
        """ Gets the selected type """

        return self.type_combobox.get()

    def get_standart_option(self):
        """ Returns the status of the standart name checkbox """

        return self.standart_var.get()
