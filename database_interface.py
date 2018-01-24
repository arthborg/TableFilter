import Tkinter as tk
import convert as cvt
import standart as std
import pypostgre as ppg
import tkMessageBox
import ttk


#==============================================================================
###DATABASE INTERFACE

class DatabaseFrame(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()
        self.dispose_widgets()


    def make_widgets(self):

        #==============================================================================
        ###MAIN FRAME
        self.mainframe = tk.Frame(self)

        ###LABELS
        self.titlelabel = tk.Label(self.mainframe, text='Tabelas presentes na sua base de dados')
        self.statuslabel = tk.Label(self.mainframe, text='')
    
        ###LISTBOX
        self.databaselistbox = tk.Listbox(self.mainframe)

        ###BUTTONS
        #self.vizualizebutton = tk.Button(self, text='Vizualizar', command = self.vizualize)
        self.deletebutton = tk.Button(self.mainframe, text='Excluir', command=self.delete)
        self.renamebutton = tk.Button(self.mainframe, text='Renomear tabela', command=self.show_rename_frame)
        self.renamecolumn = tk.Button(self.mainframe, text='Renomear coluna', command=self.show_rename_column)
        self.convertexcel = tk.Button(self.mainframe, text='Gerar excel', command=self.show_excel)
        
        ###BINDS
        self.databaselistbox.bind('<<ListboxSelected>>', self.clear_grid)

        #==============================================================================
        ###RENAME FRAME
        self.renameframe = tk.Frame(self)
        self.finalrenamebutton = tk.Button(self.renameframe, text='Renomear', command=self.rename_command)
        
        self.tablenameentry = tk.Entry(self.renameframe, state='normal')
        self.newnameentry = tk.Entry(self.renameframe)

        self.renamelabel = tk.Label(self.renameframe, text='Renomear')
        self.tolabel = tk.Label(self.renameframe, text=' Para ')


        #==============================================================================
        ###RENAME COLUMN FRAME
        self.renamecolumnframe = tk.Frame(self)
        self.columnlistbox = tk.Listbox(self.renamecolumnframe)
        self.renamecolumnlabel = tk.Label(self.renamecolumnframe, text='Escolha a coluna que deseja renomear')
        self.renamecolumnto = tk.Label(self.renamecolumnframe, text='Renomear')
        self.renamecolumnfrom = tk.Label(self.renamecolumnframe, text='Para ')
        self.newcolumnentry = tk.Entry(self.renamecolumnframe)
        self.columnnameentry = tk.Entry(self.renamecolumnframe)
        self.renamecolumnbutton = tk.Button(self.renamecolumnframe, text='Renomear', state='disabled', command=self.rename_column)

        ###EXCEL FRAME
        self.excelframe = tk.Frame(self)
        self.makefilebutton = tk.Button(self.excelframe, text='Criar arquivo', command=self.make_excel)
        self.filenamelabel = tk.Label(self.excelframe, text='Nome do arquivo')
        self.filenameentry = tk.Entry(self.excelframe)

        self.update_database_listbox()

    def dispose_widgets(self):
        
        #==============================================================================
        ###MAIN FRAME
        self.mainframe.grid(row=0, column=0)
        self.titlelabel.grid(row=0, column=0)
        self.databaselistbox.grid(row=1, column=0)
        self.deletebutton.grid(row = 2, column=0)
        self.renamebutton.grid(row = 3, column=0)
        self.renamecolumn.grid(row=4, column=0)
        self.convertexcel.grid(row=5, column=0)
        self.statuslabel.grid(row=6, column=0)

        #==============================================================================
        ###RENAME FRAME
        self.renamelabel.grid(row=0, column=0)
        self.tablenameentry.grid(row=0, column=1)
        self.tolabel.grid(row=1, column=0)
        self.newnameentry.grid(row=1, column=1)
        self.finalrenamebutton.grid(row=2, columnspan=2)

        #==============================================================================
        ###RENAME COLUMN FRAME
        self.renamecolumnlabel.grid(row=0, columnspan=2)
        self.columnlistbox.grid(row=1, columnspan=2)
        self.renamecolumnto.grid(row=2, column=0)
        self.columnnameentry.grid(row=2, column=1)
        self.renamecolumnfrom.grid(row=3, column=0)
        self.newcolumnentry.grid(row=3, column=1)
        self.renamecolumnbutton.grid(row=4, columnspan=2)

        #==============================================================================
        ###EXCEL FRAME
        self.filenamelabel.grid(row=0, column=0)
        self.filenameentry.grid(row=0, column=1)
        self.makefilebutton.grid(row=1, columnspan=2)

        ###COMMON VARIABLES
        self.SELECTEDTABLE = None

        #BINDS
        self.columnlistbox.bind('<<ListboxSelect>>', self.column_selected)


    def make_excel(self):
        name = self.filenameentry.get()
        if name is '':
            tkMessageBox.showerror('Erro', 'Voce nao digitou um novo nome para a coluna!')
            return

        cvt.to_table(name, std.DBNAME, self.SELECTEDTABLE)
        self.clear_grid()
        self.statuslabel['text'] = 'Arquivo criado com sucesso'


    def show_excel(self):
        if self.verify_selected() is False:
            return
        self.clear_grid()
        self.excelframe.grid(row=1, column=0)
        index = self.databaselistbox.curselection()[0]

        self.filenameentry.delete(0, tk.END)
        self.filenameentry.insert(0, self.databaselistbox.get(index)+'.xlsx')
        self.SELECTEDTABLE = self.databaselistbox.get(index)


    def column_selected(self, event):
        
        self.columnnameentry.delete(0, tk.END)
        index = self.columnlistbox.curselection()
        print 'index is'
        print index
        self.columnnameentry.insert(0, self.columnlistbox.get(index))

        self.columnnameentry['state'] = 'readonly'
        self.renamecolumnbutton['state'] = 'normal'


    def rename_column(self):
        new_name = self.newcolumnentry.get()
        if new_name is '':
            tkMessageBox.showerror('Erro', 'Voce nao digitou um novo nome para a coluna!')
            return

        index = self.columnlistbox.curselection()
        if index == ():
            tkMessageBox.showerror('Erro', 'Voce nao selecionou uma coluna para renomear')
            return
        index = index[0]
        
        ppg.rename_column(std.DBNAME, self.SELECTEDTABLE, self.columnnameentry.get(), new_name)
        self.SELECTEDTABLE = None
        self.clear_grid()
        self.statuslabel['text'] = 'Coluna renomeada com sucesso!'


    def show_rename_column(self):
        if self.verify_selected() is False:
            return
        self.clear_grid()
        self.renamecolumnframe.grid(row=1, column=0)
        index = self.databaselistbox.curselection()[0]
        self.SELECTEDTABLE = self.databaselistbox.get(index)
        self.columnlistbox.delete(0, tk.END)

        column_names = ppg.get_columns(std.DBNAME, self.databaselistbox.get(index))
        for col in column_names:
            self.columnlistbox.insert(tk.END, col)


    def rename_command(self):
        new_name = self.newnameentry.get()
        if new_name is '':
            tkMessageBox.showerror('Erro', 'Voce nao escreveu um nome para a tabela')
            return

        ppg.rename_table(std.DBNAME, self.tablenameentry.get(), new_name)
        self.clear_grid()
        self.statuslabel['text'] = 'Tabela renomeada com sucesso!'


    def show_rename_frame(self):
        if self.verify_selected() is False:
            return
        self.clear_grid()
        self.renameframe.grid(row=1, column=0)
        index = self.databaselistbox.curselection()[0]
        
        self.tablenameentry.delete(0, tk.END)
        self.tablenameentry.insert(0, self.databaselistbox.get(index))
        self.tablenameentry['state'] = 'readonly'


    def delete(self):
        
        if self.verify_selected() is False:
            return
        index = self.databaselistbox.curselection()[0]

        text = 'Tem certeza que deseja excluir a tabela ' + self.databaselistbox.get(index)
        text += ' da sua base de dados?'
        answer = tkMessageBox.askquestion("Excluir", text)

        if answer == 'yes':
            ppg.delete_table(std.DBNAME, self.databaselistbox.get(index))
            self.update_database_listbox()

        self.statuslabel['text'] = 'Tabela excluida com sucesso!'



    def clear_grid(self):

        self.renamecolumnframe.grid_forget()
        self.renameframe.grid_forget()
        self.excelframe.grid_forget()
        self.statuslabel['text'] = ''


    def verify_selected(self):
        
        index = self.databaselistbox.curselection()
        if index == ():
            tkMessageBox.showerror('Erro', 'Voce nao selecionou uma planilha')
            return False
        return True


    def update_database_listbox(self):
        
        self.databaselistbox.delete(0, tk.END)
        tables = ppg.get_table_names(std.DBNAME)

        for table in tables:
            self.databaselistbox.insert(tk.END, table)