#!/usr/bin/env Python 2.7
""" Conversion interface class and methods """

import ttk
import os
import tkMessageBox
from tkFileDialog import askopenfilename
import Tkinter as tk
import standart as std
import typehandle as tph
import convert as cvt


class ConversionFrame(tk.Frame):
    """ Implements the Conversion frame and its widgets """

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.table_type = None
        self.advanced_flag = None
        self.filename = None
        self.sheets = None
        self.csv_files = None
        self.sheet_varlist = None
        self.checksheet_list = None

        self.pack()
        self.make_widgets()
        self.dispose_widgets()
    
    def make_widgets(self):
        """ Make the widgets of the conversion frame """

        #==============================================================================
        ###TOP FRAME
        self.topframe = tk.Frame(self)

        ###CHECKBOXES
        self.csvcheckboxvariable = tk.IntVar()
        self.csvcheckbox = tk.Checkbutton(self.topframe, text='Gerar arquivo ' +
        '.csv', variable=self.csvcheckboxvariable)

        ###ENTRYS
        self.filenameentry = tk.Entry(self.topframe)

        ###LABELS
        self.statuslabel = tk.Label(self.topframe, text='')
        self.filenamelabel = tk.Label(self.topframe, text='Arquivo')
        self.typelabel = tk.Label(self.topframe, text='Tipo do arquivo')

        ###COMBOBOXES
        self.typebox = ttk.Combobox(self.topframe, state='readonly')

        ###BUTTONS
        self.convertbutton = tk.Button(self.topframe, text='Adicionar planilha a base ' +
        'de dados', command=self.convert)
        self.findbutton = tk.Button(self.topframe, text='Procurar ' +
        'arquivo', command=self.get_filename)


        #==============================================================================
        ###SHEETS FRAME
        self.sheetsframe = tk.Frame(self)
        self.sheetstextframe = tk.Frame(self)

        ###BUTTONS
        self.corvertsheetsbutton = tk.Button(self.sheetsframe, text='Converter Planilhas\
         Selecionadas', command=self.convert_sheets)

        ###LABELS
        self.explanationlabel_1 = tk.Label(self.sheetsframe, text='Foram encontradas mais de ' +
        'uma planilha no arquivo!')
        self.explanationlabel_2 = tk.Label(self.sheetsframe, text='Selecione as planilhas que ' +
        'voce deseja converter')
        self.sheetstatuslabel = tk.Label(self.sheetstextframe, text='')


        #==============================================================================
        ###ADVANCED FRAME
        self.advframe = tk.Frame(self)
        self.advbuttonframe = tk.Frame(self)

        ###LABELS
        self.yearlabel = tk.Label(self.advframe, text='Ano da Consulta')
        self.monthlabel = tk.Label(self.advframe, text='Mes da Consulta')
        self.renamelabel = tk.Label(self.advframe, text='Nome da Planilha')

        ###ENTRYS
        self.renameentry = tk.Entry(self.advframe)

        ###SPINBOXES
        self.yearspinbox = tk.Spinbox(self.advframe, from_=2000, to=2100, state=tk.NORMAL)
        self.monthspinbox = tk.Spinbox(self.advframe, from_=1, to=12, state=tk.NORMAL)

        ###CHECKBOXES
        self.useadvcheckboxvariable = tk.IntVar()
        self.useadvcheckbox = tk.Checkbutton(self.advframe, text='Usar ano e ' +
        'mes informados', variable=self.useadvcheckboxvariable)
        self.renamecheckboxvariable = tk.IntVar()
        self.renamecheckbox = tk.Checkbutton(self.advframe, text='Usar nome ' +
        'informado', variable=self.renamecheckboxvariable)

        ###BUTTONS
        self.advbutton = tk.Button(self.advbuttonframe, text='Opcoes Avancadas De Conversao >')


    def dispose_widgets(self):
        """ Dispose the created widgets on the frame """

        #==============================================================================
        #TOP FRAME
        self.filenamelabel.grid(row=0, column=0)
        self.filenameentry.grid(row=0, column=1)
        self.findbutton.grid(row=0, column=2)

        self.typelabel.grid(row=1, column=0)
        self.typebox.grid(row=1, column=1)

        self.csvcheckbox.grid(row=2, column=0)
        self.convertbutton.grid(row=3, columnspan=3)

        self.statuslabel.grid(row=4, columnspan=3)

        #==============================================================================
        #SHEETS FRAME
        self.explanationlabel_1.grid(row=0, columnspan=2)
        self.explanationlabel_2.grid(row=1, columnspan=2)

        self.sheetstatuslabel.grid(row=0, column=0)

        #==============================================================================
        #ADVANCED FRAME
        self.advbutton.grid(row=0, column=0)

        self.yearlabel.grid(row=0, column=0)
        self.yearspinbox.grid(row=0, column=1)

        self.monthlabel.grid(row=1, column=0)
        self.monthspinbox.grid(row=1, column=1)

        self.useadvcheckbox.grid(row=2, columnspan=2)

        self.renamelabel.grid(row=3, column=0)
        self.renameentry.grid(row=3, column=1)
        self.renamecheckbox.grid(row=4, columnspan=2)

        #==============================================================================
        #DISPOSING FRAMES
        self.topframe.pack()
        #self.sheetsframe.grid(row=1, column=0)
        self.sheetstextframe.pack()
        self.advbuttonframe.pack()
        #self.advframe.grid(row=4, column=0)

        #==============================================================================
        #BINDINGS
        self.advbutton.bind('<Button-1>', self.toggle_advanced)
        self.typebox.bind('<<ComboboxSelected>>', self.alter_typebox)
        self.typebox['values'] = tph.get_type_names()
        self.typebox.current(0)
        self.table_type = self.typebox.get()
        self.filename = None
        self.advanced_flag = False



    def toggle_advanced(self, *_):
        """ Toggle the advanced frame """

        if self.advanced_flag is False:
            self.advframe.pack()
        else:
            self.advframe.pack_forget()

        self.advanced_flag = not self.advanced_flag



    def get_filename(self):
        """ Open a dialog window to get the filename """

        self.filename = askopenfilename()
        self.filenameentry.delete(0, tk.END)
        self.filenameentry.insert(0, self.filename)



    def alter_typebox(self, *_):
        """ Alter the value of the table_type variable """

        self.table_type = self.typebox.get()
        print 'mudei pra ' + self.table_type


    def convert(self):
        """ Method used to convert the especified file to a postgres table """

        self.filename = self.filenameentry.get()
        print self.filename

        if self.filename == '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um arquivo')
            return
        if os.path.isfile(self.filename) is False:
            tkMessageBox.showerror('Erro', 'O arquivo informado nao existe')
            return
        try:
            year = int(self.yearspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
            month = int(self.monthspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
        except ValueError:
            tkMessageBox.showerror('Erro', 'Os campos ano e mes devem conter apenas numeros')
            return
        
        name = self.filename 
        name = name.split('.')
        print 'NAME EXTENSION {}'.format(name[-1])
        if name[-1] == 'csv':
            self.convert_csv(year, month)
            return

        # EXCLUSIVE FOR EXCEL FILES
        self.sheets = cvt.get_sheet_names(self.filename)
        print 'SHEETS ARE {}'.format(self.sheets)
        self.csv_files = cvt.to_csv(self.filename, self.typebox.get(), year=year, month=month)

        if len(self.sheets) > 1:
            self.show_sheet_frame()
            text = ''
        else:
            sheet_name = self.sheets[0]
            csv_file = self.csv_files[0]

            print 'RENAME IS ', self.renamecheckboxvariable.get()
            if self.renamecheckboxvariable.get() is 0:
                table_name = cvt.get_std_name(self.typebox.get(), 0, year=year, month=month)
            else:
                table_name = self.renameentry.get()

            print 'TABLE NAME IS ' + table_name
            try:
                cvt.fileto_postgre(csv_file, table_name, std.DBNAME)
                text = 'A planilha "' + sheet_name + '" foi adicionada com o nome \
                ' + table_name + '!'
            except:
                text = 'Falha na criacao da planilha ' + sheet_name + ' com o nome \
                ' + table_name + '! Talvez ela ja tenha sido criada!'
            if self.csvcheckboxvariable.get() is 0:
                os.remove(csv_file)

        self.statuslabel['text'] = text


    def convert_csv(self, year, month):
        """ Converts a .csv file to a postgres database table """

        print 'MY TABLE TYPE IS {}'.format(self.typebox.get())
        if self.renamecheckboxvariable.get() is 0:
            table_name = cvt.get_std_name(self.typebox.get(), 0, year, month)
        else:
            table_name = self.renameentry.get()

        new_file = cvt.normalize_csv_file(self.filename)
        cvt.fileto_postgre(new_file, table_name, std.DBNAME)
        text = 'O arquivo "' + self.filename + '" foi adicionada com a base de dados ' + 'com o nome "' + table_name + '"!'
        self.statuslabel['text'] = text


    def show_sheet_frame(self):
        """ Show the sheet frame for the user to pick which sheet to convert to the database """

        count = 2
        self.sheet_varlist = []
        self.checksheet_list = []

        for name in self.sheets:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.sheetsframe, text=name, variable=var)

            chk.grid(row=count, column=0)
            count += 1

            self.sheet_varlist.append(var)
            self.checksheet_list.append(chk)

        self.corvertsheetsbutton.grid(row=count, column=0)

        self.advbuttonframe.pack_forget()
        self.sheetstextframe.pack_forget()
        self.sheetsframe.pack()

        if self.advanced_flag is True:
            self.advframe.pack_forget()

        self.sheetsframe.pack()
        self.sheetstextframe.pack()
        self.advbuttonframe.pack()

        if self.advanced_flag is True:
            self.advframe.pack()


    def convert_sheets(self):
        """ Convert all selected sheets to postgres tables """
        text = ''
        try:
            year = int(self.yearspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
            month = int(self.monthspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
        except ValueError:
            tkMessageBox.showerror('Erro', 'Os campos ano e mes devem conter apenas numeros')
            return

        for i in range(0, len(self.sheet_varlist)):

            if self.sheet_varlist[i].get() is 1:

                csvfile = self.csv_files[i]

                print 'RENAME IS '
                print self.renamecheckboxvariable.get()
                if self.renamecheckboxvariable.get() is 0:
                    table_name = cvt.get_std_name(self.typebox.get(), i, month=month, year=year)
                else:
                    table_name = self.renameentry.get() + '-' + str(i)
                print 'TABLE NAME IS ' + table_name
                try:
                    cvt.fileto_postgre(csvfile, table_name, std.DBNAME)
                    text += 'Planilha ' + self.sheets[i] + ' adicionada com o nome \
                    ' + table_name + '\n'
                except:
                    text += 'Falha na criacao da planilha ' + self.sheets[i] + ' com\
                     o nome ' + table_name + 'Talvez ela ja tenho sido criada!\n'

        if text == '':
            tkMessageBox.showerror('Erro', 'Nenhuma planilha selecionada')
            return

        self.sheetstatuslabel['text'] = text
        self.hide_sheet_frame()


    def hide_sheet_frame(self):
        """ Hides and clean the sheet frame """

        for chk in self.checksheet_list:
            chk.grid_forget()

        self.sheetsframe.grid_forget()

        if self.csvcheckboxvariable.get() is 0:
            for sfile in self.csv_files:
                os.remove(sfile)
