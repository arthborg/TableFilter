#!/usr/bin/env python 2.7

import Tkinter as tk
import standart as std
import pypostgre as ppg
import typehandle as tph
import tkMessageBox
import ttk


#==============================================================================
###FILTER INTERFACE


class FilterFrame(tk.Frame):
    
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()
        self.dispose_widgets()


    def make_widgets(self):

        ###COMBOBOXES
        self.tablebox = ttk.Combobox(self, state='readonly')
        self.typebox = ttk.Combobox(self, state='readonly')
        self.orderbox = ttk.Combobox(self, state='readonly')

        ###LABELS
        self.selectlabel = tk.Label(self, text='Selecione a planilha: ')
        self.obsselectlabel = tk.Label(self, text='OBS.: Se sua planilha nao estiver presente clique no botao para atualizar')
        self.selecttypelabel = tk.Label(self, text='Selecione o tipo da planilha')
        self.obslabel = tk.Label(self, text='OBS.: A filtragem e feita com base no tipo da planilha')
        self.renamelabel = tk.Label(self, text='(Opcional) Renomear para ')
        self.resultlabel = tk.Label(self, text='')
        self.orderlabel = tk.Label(self, text='(Opcional) Ordenar por ')

        ###BUTTONS
        self.updatevalues = tk.Button(self, text='Atualizar Planilhas', command=self.update_tablebox)
        self.filterbutton = tk.Button(self, text='Filtrar Planilha', command=self.filter)

        #ENTRYS
        self.renameentry = tk.Entry(self)

        #CHECKBOXES
        self.renamecheckboxvariable = tk.IntVar()
        self.renamecheckbox = tk.Checkbutton(self, text='Usar nome informado', variable=self.renamecheckboxvariable)


    def dispose_widgets(self):
        self.selectlabel.grid(row=0,column=0)
        self.tablebox.grid(row=0,column=1)
        self.selecttypelabel.grid(row=1,column=0)
        self.typebox.grid(row=1,column=1)

        self.obsselectlabel.grid(row=2,columnspan=2)
        self.updatevalues.grid(row=3,column=1)
        self.renamelabel.grid(row=4, column=0)
        self.renameentry.grid(row=4, column=1)
        self.renamecheckbox.grid(row=5, columnspan=2)

        self.orderlabel.grid(row=6, column=0)
        self.orderbox.grid(row=6, column=1)

        self.obslabel.grid(row=7,columnspan=2)
        self.filterbutton.grid(row=8,column=1)
        self.resultlabel.grid(row=9, columnspan=2)

        #UPDATE COMBOBOXES VALUES
        self.update_tablebox()

        #BINDS
        self.typebox.bind('<<ComboboxSelected>>', self.update_orderbox)


    def update_orderbox(self, event):
        self.orderbox['values'] = tph.get_group_cols(self.typebox.get())
        
    def update_tablebox(self):
        self.tablebox['values'] = ppg.get_table_names(std.DBNAME)
        self.typebox['values'] = tph.get_type_names()

        self.resultlabel['text'] = 'Atualizado com sucesso!'

    def filter(self):
        if self.tablebox.get() is '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou uma planilha')
            return
        if self.typebox.get() is '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um tipo')
            return

        old_name = self.tablebox.get()
        type_name = self.typebox.get()

        if self.renamecheckboxvariable.get() is 1:
            new_name = self.renameentry.get()
        else:
            new_name = 'F-' + old_name

        wanted = tph.get_group_list(type_name)
        count_dict = tph.get_count_list(type_name)

        if self.orderbox.get() is '':
            order = None
        else:
            order = self.orderbox.get()

        try:
            ppg.agroup_table(std.DBNAME, old_name, new_name, wanted, count_dict, order)
            self.resultlabel['text'] = 'Operacao concluida'
        except:
            self.resultlabel['text'] = 'Erro! Houve uma falha na operacao'

