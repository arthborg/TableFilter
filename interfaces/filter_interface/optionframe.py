#!/usr/bin/python2.7

""" Holds the options frame class and its methods """

import Tkinter as tk
import ttk
import tb_code.typehandle as tph


class OptionFrame(tk.Frame):
    """ Implements the options frame interface """

    def __init__(self, parent, mainframe):

        tk.Frame.__init__(self, parent)

        self.parent = mainframe
        tk.Label(self, text='Renomear para: ').grid(
            row=0, column=0, padx=5, pady=5)
        tk.Label(self, text='Ordenar por: ').grid(
            row=2, column=0, padx=5, pady=5)

        self.rename_variable = tk.IntVar()
        tk.Checkbutton(self, text='Usar nome informado', variable=self.rename_variable).grid(
            row=1, columnspan=2, padx=5, pady=5)

        self.rename_entry = tk.Entry(self, text='')
        self.update_button = tk.Button(
            self, text='Atualizar!', command=self.__update_orders())
        self.order_combobox = ttk.Combobox(self, state='readonly')

        self.rename_entry.grid(row=0, column=1, padx=5, pady=5)
        self.update_button.grid(row=3, column=1, padx=5, pady=5)
        self.order_combobox.grid(row=2, column=1, padx=5, pady=5)

    def __update_orders(self):
        """ Updates the order combobox """
        pass
        """
        if self.parent.get_selected_type() is None:
            return
        all_columns = tph.get_group_cols(self.parent.get_selected_type())
        self.order_combobox['values'] = all_columns
        """

    def get_rename_value(self):
        """ Gets the value of the renaem checkbox """

        return self.rename_variable.get()

    def get_rename(self):
        """ Gets the new name """

        return self.rename_entry.get()

    def get_order(self):
        """ Gets the value of the order combobox """

        return self.order_combobox.get()
