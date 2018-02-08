#!/usr/bin/python2.7

""" Holds the SheetsFrame interface and its methods """

import Tkinter as tk


class SheetsFrame(tk.Frame):
    """ Implements the the Sheet Frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.sheet_list = []
        self.varlist = []
        self.checkboxes = []

        tk.Label(self, text='Existem multiplas planilhas no seu arquivo!' +
                 '\nMarque aquelas que voce deseja converter.').pack()

    def fill_frame(self, sh_list):
        """ Fills the frame with the given argument """
        self.sheet_list = sh_list

        for sheet in self.sheet_list:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=sheet, variable=var)
            chk.pack()
            self.checkboxes.append(chk)
            self.varlist.append(var)

    def get_checked_names(self):
        """ Get the checked names """

        new_vars = []
        for i, var in enumerate(self.varlist):

            if var == 0:
                continue
            new_vars.append(self.sheet_list[i])

        return new_vars

    def clear_frame(self):
        """ Clears the frame """

        for chk in self.checkboxes:
            chk.pack_forget()

        self.varlist = []
        self.checkboxes = []
        self.sheet_list = []
