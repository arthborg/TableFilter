#!/usr/bin/python2.7

""" Holds the type interface and methods """

import Tkinter as tk
import tkMessageBox
import tb_code.standart as std
import tb_code.typehandle as tph
from interfaces.type_interface.createtypeframe import CreateTypeFrame


class TypeFrame(tk.Frame):
    """ Implements the type frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Tipos Cadastrados').grid(
            row=0, columnspan=2, padx=5, pady=5)

        self.type_listbox = tk.Listbox(self)
        self.type_listbox.grid(row=1, columnspan=2, padx=5, pady=5)

        tk.Button(self, text='Excluir Tipo', command=self.__delete_type).grid(
            row=2, column=0, padx=5, pady=5)
        tk.Button(self, text='Novo Tipo', command=self.__show_create).grid(
            row=2, column=1, padx=5, pady=5)
        tk.Button(self, text='Detalhar Tipo', command=self.__details).grid(
            row=3, column=0, padx=5, pady=5)
        tk.Button(self, text='Atualizar Tipos', command=self.__update_type).grid(
            row=3, column=1, padx=5, pady=5)

        self.create_frame = CreateTypeFrame(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.__update_type()

    def __update_type(self):
        """ Updates the type listbox """

        all_types = tph.get_type_names()
        self.type_listbox.delete(0, tk.END)
        self.type_listbox.insert(tk.END, *all_types)

    def __delete_type(self):
        """ Deletes a type """

        name = self.__get_selected_type()
        if name == '':
            return
        tph.purge_type(std.TYPE_FILENAME, name)

    def __show_create(self):
        """ Shows the create type frame """

        self.create_frame.grid(row=4, columnspan=2, padx=5, pady=5)

    def __details(self):
        """ Shows the selected type details """

        name = self.__get_selected_type()
        if name == '':
            return
        detail = tph.get_details(name)
        tkMessageBox.showinfo('Detalhes', detail)

    def __get_selected_type(self):
        """ Gets the selected type """

        selected = self.type_listbox.curselection()
        if selected == ():
            tkMessageBox.showerror('Error', 'Nenhum tipo selecionada')
            return ''

        selected = selected[0]
        return self.type_listbox.get(selected)
