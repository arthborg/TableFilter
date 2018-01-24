from tkFileDialog import askopenfilename
import Tkinter as tk
import standart as std
import pypostgre as ppg
import typehandle as tph
import convert as cvt
import ttk
import os
import tkMessageBox

#==============================================================================
###CONVERSION INTERFACE


class ConversionFrame(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()
        self.dispose_widgets()

    
    def make_widgets(self):
        
        #==============================================================================
        ###TOP FRAME
        self.topframe = tk.Frame(self)

        ###CHECKBOXES
        self.csvcheckboxvariable = tk.IntVar()
        self.csvcheckbox = tk.Checkbutton(self.topframe, text='Gerar arquivo .csv', variable=self.csvcheckboxvariable)

        ###ENTRYS
        self.filenameentry = tk.Entry(self.topframe)

        ###LABELS
        self.statuslabel = tk.Label(self.topframe, text = '')
        self.filenamelabel = tk.Label(self.topframe, text='Arquivo')
        self.typelabel = tk.Label(self.topframe, text='Tipo do arquivo')

        ###COMBOBOXES
        self.typebox = ttk.Combobox(self.topframe, state='readonly')

        ###BUTTONS
        self.convertbutton = tk.Button(self.topframe, text='Adicionar planilha a base de dados', command=self.convert)
        self.findbutton = tk.Button(self.topframe, text='Procurar arquivo', command=self.get_filename)


        #==============================================================================
        ###SHEETS FRAME
        self.sheetsframe = tk.Frame(self)
        self.sheetstextframe = tk.Frame(self)

        ###BUTTONS
        self.corvertsheetsbutton = tk.Button(self.sheetsframe, text='Converter Planilhas Selecionadas', command = self.convert_sheets)

        ###LABELS
        self.explanationlabel_1 = tk.Label(self.sheetsframe, text='Foram encontradas mais de uma planilha no arquivo!')
        self.explanationlabel_2 = tk.Label(self.sheetsframe, text='Selecione as planilhas que voce deseja converter')
        self.sheetstatuslabel = tk.Label(self.sheetstextframe, text='')


        #==============================================================================
        ###ADVANCED FRAME
        self.advframe = tk.Frame(self)
        self.advbuttonframe = tk.Frame(self)

        ###LABELS
        self.yearlabel = tk.Label(self.advframe, text = 'Ano da Consulta')
        self.monthlabel = tk.Label(self.advframe, text = 'Mes da Consulta')
        self.renamelabel = tk.Label(self.advframe, text = 'Nome da Planilha')

        ###ENTRYS
        self.renameentry = tk.Entry(self.advframe)

        ###SPINBOXES
        self.yearspinbox = tk.Spinbox(self.advframe, from_=2000, to=2100, state=tk.NORMAL)
        self.monthspinbox = tk.Spinbox(self.advframe, from_=1, to=12, state=tk.NORMAL)

        ###CHECKBOXES
        self.useadvcheckboxvariable = tk.IntVar()
        self.useadvcheckbox = tk.Checkbutton(self.advframe, text = 'Usar ano e mes informados', variable=self.useadvcheckboxvariable)
        self.renamecheckboxvariable = tk.IntVar()
        self.renamecheckbox = tk.Checkbutton(self.advframe, text = 'Usar nome informado', variable=self.renamecheckboxvariable)

        ###BUTTONS
        self.advbutton = tk.Button(self.advbuttonframe, text='Opcoes Avancadas De Conversao >')


    def dispose_widgets(self):
        
        #==============================================================================
        #TOP FRAME
        self.filenamelabel.grid(row=0, column=0)
        self.filenameentry.grid(row=0, column=1)
        self.findbutton.grid(row=0, column=2)

        self.typelabel.grid(row=1, column=0)
        self.typebox.grid(row=1, column=1)

        self.csvcheckbox.grid(row=2, column=0)
        self.convertbutton.grid(row=3, columnspan = 3)

        self.statuslabel.grid(row=4, columnspan=3)

        #==============================================================================
        #SHEETS FRAME
        self.explanationlabel_1.grid(row=0, columnspan=2)
        self.explanationlabel_2.grid(row=1, columnspan=2)

        self.sheetstatuslabel.grid(row=0, column=0)

        #==============================================================================
        #ADVANCED FRAME
        self.advbutton.grid(row=0, column=0)

        self.yearlabel.grid(row=0,column=0)
        self.yearspinbox.grid(row=0, column=1)

        self.monthlabel.grid(row=1, column=0)
        self.monthspinbox.grid(row=1, column=1)

        self.useadvcheckbox.grid(row=2, columnspan = 2)

        self.renamelabel.grid(row=3,column=0)
        self.renameentry.grid(row=3,column=1)
        self.renamecheckbox.grid(row=4, columnspan=2)

        #==============================================================================
        #DISPOSING FRAMES
        self.topframe.grid(row=0, column=0)
        #self.sheetsframe.grid(row=1, column=0)
        self.sheetstextframe.grid(row=2, column=0)
        self.advbuttonframe.grid(row=3, column=0)
        #self.advframe.grid(row=4, column=0)

        #==============================================================================
        #BINDINGS
        self.advbutton.bind('<Button-1>', self.toggle_advanced)
        self.typebox.bind('<<ComboboxSelected>>', self.alter_typebox)
        self.typebox['values'] = tph.get_type_names()
        self.typebox.current(0)
        self.TABLE_TYPE = self.typebox.get()
        self.FILENAME = None
        self.ADVANCED_FLAG = False



    def toggle_advanced(self, event):
        
        if self.ADVANCED_FLAG is False:
            self.advframe.grid(row=4, column=0)
        else:
            self.advframe.grid_forget()

        self.ADVANCED_FLAG = not self.ADVANCED_FLAG



    def get_filename(self):
        
        self.FILENAME = askopenfilename()

        self.filenameentry.delete(0,tk.END)
        self.filenameentry.insert(0,self.FILENAME)



    def alter_typebox(self, event):
        
        self.TABLE_TYPE = self.typebox.get()
        print 'mudei pra ' + self.TABLE_TYPE


    def convert(self):

        self.FILENAME = self.filenameentry.get()
        print self.FILENAME

        if self.FILENAME is '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um arquivo')
            return
        if os.path.isfile(self.FILENAME) is False:
            tkMessageBox.showerror('Erro', 'O arquivo informado nao existe')
            return
        try:        
            year = int(self.yearspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
            month = int(self.monthspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
        except ValueError:
            tkMessageBox.showerror('Erro', 'Os campos ano e mes devem conter apenas numeros')
            return

        self.SHEETS = cvt.get_sheet_names(self.FILENAME)
        self.CSV_FILES = cvt.to_csv(self.FILENAME, self.TABLE_TYPE, yy=year, mm=month)

        if len(self.SHEETS) > 1:
            self.show_sheet_frame()
            text = ''
        else:
            sheet_name = self.SHEETS[0]
            csv_file = self.CSV_FILES[0]

            print 'RENAME IS '
            print self.renamecheckboxvariable.get()
            if self.renamecheckboxvariable.get() is 0:
                table_name = cvt.get_std_name(self.TABLE_TYPE, 0, yy=year, mm=month)
            else:
                table_name = self.renameentry.get() 

            print 'TABLE NAME IS ' + table_name 
            try:
                cvt.fileto_postgre(csv_file, table_name, std.DBNAME)
                text = 'A planilha "' + sheet_name + '" foi adicionada com o nome ' + table_name + '!'
            except:
                text = 'Falha na criacao da planilha ' + sheet_name + ' com o nome ' + table_name + '! Talvez ela ja tenha sido criada!'
            if self.csvcheckboxvariable.get() is 0:
                os.remove(csv_file)

        self.statuslabel['text'] = text


    def show_sheet_frame(self):
        count = 2
        self.SHEET_VARLIST = []
        self.CHECKSHEET_LIST = []

        for name in self.SHEETS:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.sheetsframe, text = name, variable=var)

            chk.grid(row=count, column=0)
            count += 1

            self.SHEET_VARLIST.append(var)
            self.CHECKSHEET_LIST.append(chk)

        self.corvertsheetsbutton.grid(row=count, column=0)
        self.sheetsframe.grid(row=1, column=0)


    def convert_sheets(self):
        
        text = ''
        try:        
            year = int(self.yearspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
            month = int(self.monthspinbox.get()) if self.useadvcheckboxvariable.get() is 1 else None
        except ValueError:
            tkMessageBox.showerror('Erro', 'Os campos ano e mes devem conter apenas numeros')
            return
            
        for i in range(0, len(self.SHEET_VARLIST)):

            if self.SHEET_VARLIST[i].get() is 1:

                csvfile = self.CSV_FILES[i]

                print 'RENAME IS '
                print self.renamecheckboxvariable.get()
                if self.renamecheckboxvariable.get() is 0:
                    table_name = cvt.get_std_name(self.TABLE_TYPE, i, mm=month, yy=year)
                else:
                    table_name = self.renameentry.get() + '-' + str(i)
                print 'TABLE NAME IS ' + table_name
                try:
                    cvt.fileto_postgre(csvfile, table_name, std.DBNAME)
                    text += 'Planilha ' + self.SHEETS[i] + ' adicionada com o nome ' + table_name + '\n'
                except:
                    text += 'Falha na criacao da planilha ' + self.SHEETS[i] + ' com o nome ' + table_name + 'Talvez ela ja tenho sido criada!\n'

        if text is '':
            tkMessageBox.showerror('Erro', 'Nenhuma planilha selecionada')
            return

        self.sheetstatuslabel['text'] = text
        self.hide_sheet_frame()


    #HIDES AND CLEANS THE SHEET FRAME
    def hide_sheet_frame(self):
        
        for chk in self.CHECKSHEET_LIST:
            chk.grid_forget()
        
        self.sheetsframe.grid_forget()

        if self.csvcheckboxvariable.get() is 0:
            for s in self.CSV_FILES:
                os.remove(s)