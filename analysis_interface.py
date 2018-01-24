import Tkinter as tk
import standart as std
import analytics as anl
import pypostgre as ppg
import typehandle as tph
import tkMessageBox
import ttk


#==============================================================================
### ANALYSIS INTERFACE
#==============================================================================

class AnalysisFrame(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()
        self.dispose_widgets()


    def make_widgets(self):

        #==============================================================================
        ###MAINFRAME        
        self.mainframe = tk.Frame(self)

        ###LABELS
        self.targettablelabel = tk.Label(self.mainframe, text='Planilha para a analize')
        self.typelabel = tk.Label(self.mainframe, text='Tipo da planilha')
        self.databaselabel = tk.Label(self.mainframe, text='Planilhas na base de dados: ')
        self.selectedlabel = tk.Label(self.mainframe, text='Planilhas selecionadas: ')
        self.auxtablelabel = tk.Label(self.mainframe, text='Selecione as planilha de forma que observacao mais recente\n\
        seja a primeira e a mais antiga seja a ultima')
        
        ###COMBOBOXES
        self.targettablecombobox = ttk.Combobox(self.mainframe, state='readonly')
        self.typecombobox = ttk.Combobox(self.mainframe, state='readonly')

        ###LISTBOX
        self.databaselistbox = tk.Listbox(self.mainframe)
        self.selectedlistbox = tk.Listbox(self.mainframe)

        #==============================================================================
        ###OPTIONSFRAME
        self.optionsframe = tk.Frame(self)

        ###LABELS
        self.anltypelabel = tk.Label(self.optionsframe, text='Tipo de analise')
        self.analysislabel = tk.Label(self.optionsframe, text='O que analizar ')

        ###CHECKBOXES
        self.ssevar = tk.IntVar()
        self.ssecheckbox = tk.Checkbutton(self.optionsframe, text='Suavizacao Exponencial', variable=self.ssevar, command=self.check_type_sse)
        self.mmvar = tk.IntVar()
        self.mmcheckbox = tk.Checkbutton(self.optionsframe, text='Media movel', variable=self.mmvar, command=self.check_type_mm)
        self.predictionvar = tk.IntVar()
        self.predictioncheckbox = tk.Checkbutton(self.optionsframe, text='Predicao', variable=self.predictionvar, command=self.check_growth)
        self.growthvar = tk.IntVar()
        self.growthcheckbox = tk.Checkbutton(self.optionsframe, text='Taxa de Crescimento', variable=self.growthvar, state=tk.DISABLED)
        self.exhaustionvar = tk.IntVar()
        self.exhaustioncheckbox = tk.Checkbutton(self.optionsframe, text='Esgotamento (em meses)', variable=self.exhaustionvar, state=tk.DISABLED)

        ###BUTTONS
        self.analysisbutton = tk.Button(self.optionsframe, text='Fazer analize!', command=self.analize)



    def dispose_widgets(self):

        #==============================================================================
        ### MAIN FRAME        
        self.mainframe.pack()
        self.targettablelabel.grid(row=0, column =0)
        self.targettablecombobox.grid(row=0, column=1)

        self.typelabel.grid(row=1, column=0)
        self.typecombobox.grid(row=1, column=1)

        self.auxtablelabel.grid(row=2, columnspan = 2)
        self.databaselabel.grid(row=3, column=0)
        self.selectedlabel.grid(row=3, column=1)

        self.databaselistbox.grid(row=4, column=0)
        self.selectedlistbox.grid(row=4, column=1)

        ### BINDS
        self.databaselistbox.bind('<Double-Button-1>', self.dbtoselected)
        self.selectedlistbox.bind('<Double-Button-1>', self.selectedtodb)
        self.targettablecombobox.bind('<<ComboboxSelected>>', self.update_database_tables)
        self.typecombobox.bind('<<ComboboxSelected>>', self.check_types)

        ### COMMON VARIABLES
        self.table_names = ppg.get_table_names(std.DBNAME)

        #==============================================================================
        ### OPTIONS FRAME
        self.optionsframe.pack()
        self.anltypelabel.grid(row=0, column=0)
        self.ssecheckbox.grid(row=1, column=0)
        self.mmcheckbox.grid(row=2, column=0)

        self.analysislabel.grid(row=3, column=0)
        self.predictioncheckbox.grid(row=4, column=0)
        self.growthcheckbox.grid(row=5, column=0)
        self.exhaustioncheckbox.grid(row=6, column=0)

        self.analysisbutton.grid(row=7, column=0)

        #==============================================================================
        ### UPDATES
        self.update_tablebox()
        self.update_database_tables()

    
    def check_growth(self):
        if self.predictionvar.get() is 1:
            self.growthcheckbox['state'] = tk.NORMAL

            if tph.get_exhaustion_flag(self.typecombobox.get()) is True:
                self.exhaustioncheckbox['state'] = tk.NORMAL
        else:
            self.exhaustioncheckbox.deselect()
            self.growthcheckbox.deselect()
            self.exhaustioncheckbox['state'] = tk.DISABLED
            self.growthcheckbox['state'] = tk.DISABLED  


    def check_types(self, event):

        if self.predictionvar.get() is 1:
            if tph.get_exhaustion_flag(self.typecombobox.get()) is True:
                self.exhaustioncheckbox['state'] = tk.NORMAL


    def check_type_mm(self):
        
        if self.ssevar.get() is 1:
            self.ssecheckbox.deselect()


    def check_type_sse(self):
        
        if self.mmvar.get() is 1:
            self.mmcheckbox.deselect()


    def update_database_tables(self, event=None):
    
        self.databaselistbox.delete(0, tk.END)
        targettable = self.targettablecombobox.get()
        selectedtables = self.selectedlistbox.get(0,tk.END)

        for table in self.table_names:
            if table != targettable and table not in selectedtables:
                self.databaselistbox.insert(tk.END, table)

        if targettable in selectedtables:
            
            index = selectedtables.index(targettable)
            self.selectedlistbox.delete(index)


    def dbtoselected(self, event):

        try:
            selected = self.databaselistbox.curselection()[0]
        except IndexError:
            return

        selected = self.databaselistbox.get(selected)
        self.selectedlistbox.insert(tk.END, selected)
        self.update_database_tables()


    def selectedtodb(self, event):

        try:
            index = self.selectedlistbox.curselection()[0]
        except IndexError:
            return

        selected = self.selectedlistbox.get(index)
        self.databaselistbox.insert(tk.END, selected)
        self.selectedlistbox.delete(index)


    def update_tablebox(self):
        self.targettablecombobox['values'] = ppg.get_table_names(std.DBNAME)
        self.typecombobox['values'] = tph.get_analysis_type_names()


    def analize(self):

        if self.targettablecombobox.get() is '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou uma planilha')
            return
        if self.typecombobox.get() is '':
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um tipo')
            return

        selected_tables = self.selectedlistbox.get(0, tk.END)

        if len(selected_tables) < 2:
            tkMessageBox.showerror('Erro', 'Para fazer uma analize estatistica \
            relevante eh necessario que 2 ou mais planilhas sejam selecionadas!')
            return

        if (self.ssevar.get() is 0) and (self.mmvar.get() is 0):
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um tipo de analize')
            return
        
        if self.predictionvar.get() is 0:
            tkMessageBox.showerror('Erro', 'Voce nao selecionou o que analizar')
            return

        print 'TUDO OK SELECTED TABLES ARE '
        print selected_tables
        print 'TARGET TABLE IS ' + self.targettablecombobox.get()

        if self.ssevar.get() is 1:
            anl.simple_exp(std.DBNAME, self.targettablecombobox.get(), selected_tables, self.typecombobox.get())
        elif self.mmvar.get() is 1:
            anl.avg_move(std.DBNAME, self.targettablecombobox.get(), selected_tables, self.typecombobox.get())

        if self.growthvar.get() is 1:
            anl.growth_rate(std.DBNAME, self.targettablecombobox.get(), self.typecombobox.get())
        
        if self.exhaustionvar.get() is 1:
            anl.months_to_exhaustion(std.DBNAME, self.targettablecombobox.get(), self.typecombobox.get())

        print 'END'