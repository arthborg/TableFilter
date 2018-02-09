#!/usr/bin/python3

""" Filter frame for the create type interface """

import Tkinter as tk


class FilterTypeFrame(tk.Frame):
    """ Implements the filter type frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Colunas de Agrupamento').grid(
            row=0, column=1, padx=5)
        tk.Label(self, text='Colunas de Contagem').grid(
            row=0, column=4, padx=5)

        self.info = tk.Label(self, text='* Campos Obrigatorios, Obs.: Para informar mais de um ' +
                             'valor condicional utilize "|", exemplo: disponivel|disponivel ngn')

        tk.Label(self, text='Nome Original*').grid(
            row=1, column=0, padx=5)
        tk.Label(self, text='Novo Nome').grid(
            row=1, column=1, padx=5)
        tk.Label(self, text='Nome Original*').grid(
            row=1, column=3, padx=5)
        tk.Label(self, text='Novo Nome').grid(
            row=1, column=4, padx=5)
        tk.Label(self, text='Condicao').grid(
            row=1, column=5, padx=5)

        self.info.grid(row=3, columnspan=5, padx=5)

        tk.Button(self, text='+', command=self.__add_group).grid(row=0,
                                                                 column=2, padx=5)
        tk.Button(self, text='+', command=self.__add_count).grid(row=0,
                                                                 column=5, padx=5)
        tk.Button(self, text='-', command=self.__sub_group).grid(row=0,
                                                                 column=0, padx=5)
        tk.Button(self, text='-', command=self.__sub_count).grid(row=0,
                                                                 column=3, padx=5)
        self.count_row = 2
        self.group_row = 2
        self.group_entrys = []
        self.count_entrys = []
        self.__add_count()
        self.__add_group()

    def clear(self):
        """ Clears all the entrys from the frame """

        for raw_entry, new_entry in self.group_entrys:
            raw_entry.grid_forget()
            new_entry.grid_forget()
            self.group_row -= 1

        for raw_entry, new_entry, con_entry in self.count_entrys:
            raw_entry.grid_forget()
            new_entry.grid_forget()
            con_entry.grid_forget()
            self.count_row -= 1

        self.__add_count()
        self.__add_group()

    def get_group_names(self):
        """ Gets the names of the group columns typed """

        group = []
        for raw_entry, new_entry in self.group_entrys:
            raw = raw_entry.get()
            new = new_entry.get()

            if raw == '':
                continue
            if new == '':
                new = raw
            group.append([raw, new])

        return group

    def get_count_names(self):
        """ Gets the names of the count columns typed """

        count = []
        for raw_entry, new_entry, con_entry in self.count_entrys:
            raw = raw_entry.get()
            new = new_entry.get()
            con = con_entry.get()

            if raw == '':
                continue
            if new == '':
                new = raw

            count.append([raw, new, con])

        return count

    def __add_count(self):

        raw = tk.Entry(self)
        new = tk.Entry(self)
        con = tk.Entry(self)

        raw.grid(row=self.count_row, column=3, padx=5)
        new.grid(row=self.count_row, column=4, padx=5)
        con.grid(row=self.count_row, column=5, padx=5)

        self.count_entrys.append((raw, new, con))

        self.count_row += 1
        self.info.grid_forget()
        self.info.grid(row=max(self.count_row, self.group_row),
                       columnspan=5, padx=5)

    def __add_group(self):
        raw = tk.Entry(self)
        new = tk.Entry(self)

        raw.grid(row=self.group_row, column=0, padx=5)
        new.grid(row=self.group_row, column=1, padx=5)

        self.group_entrys.append((raw, new))

        self.group_row += 1
        self.info.grid_forget()
        self.info.grid(row=max(self.count_row, self.group_row),
                       columnspan=5, padx=5)

    def __sub_count(self):

        try:
            raw, new, con = self.count_entrys[-1]
        except IndexError:
            return
        raw.grid_forget()
        new.grid_forget()
        con.grid_forget()

        self.count_entrys.pop(-1)
        self.count_row -= 1

    def __sub_group(self):

        try:
            raw, new = self.group_entrys[-1]
        except IndexError:
            return
        raw.grid_forget()
        new.grid_forget()

        self.group_entrys.pop(-1)
        self.group_row -= 1
