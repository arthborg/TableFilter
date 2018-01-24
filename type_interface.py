import Tkinter as tk
import standart as std
import typehandle as tph
import tkMessageBox


#==============================================================================
###TYPE INTERFACE
#==============================================================================


class TypeFrame(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()
        self.dispose_widgets()

    
    def make_widgets(self):
        
        ###MAIN FRAME
        self.mainframe = tk.Frame(self)
        self.typelabel = tk.Label(self.mainframe, text='Tipos cadastrados')
        self.typelistbox = tk.Listbox(self.mainframe)
        self.newbutton = tk.Button(self.mainframe, text='Adicionar novo tipo', command = self.show_addframe)
        self.visualbutton = tk.Button(self.mainframe, text='Detalhes', command=self.show_details)
        self.deletebutton = tk.Button(self.mainframe, text='Excluir', command=self.delete_type)
        self.statuslabel = tk.Label(self.mainframe, text='')

        ###ADD FRAME - FILTER
        self.addframe = tk.Frame(self)
        self.addbuttonframe = tk.Frame(self)
        self.grouplabel = tk.Label(self.addframe, text='Colunas de agrupamento: ')
        self.countlabel = tk.Label(self.addframe, text='Colunas de contagem:')
        
        self.plusgroupbutton = tk.Button(self.addframe, text='+', command=self.add_group_entry)
        self.minusgroupbutton = tk.Button(self.addframe, text='-', command=self.sub_group_entry)
        self.pluscountbutton = tk.Button(self.addframe, text='+', command=self.add_count_entry)
        self.minuscountbutton = tk.Button(self.addframe, text='-', command=self.sub_count_entry)
        self.newtypebutton = tk.Button(self.addbuttonframe, text='Cadastrar Tipo', command=self.add_new_type)

        self.brutegrouplabel = tk.Label(self.addframe, text='Nome Bruto*')
        self.newgrouplabel = tk.Label(self.addframe, text='Novo Nome')

        self.brutecountlabel = tk.Label(self.addframe, text='Nome Bruto*')
        self.newcountlabel = tk.Label(self.addframe, text='Novo Nome')
        self.conditionallabel = tk.Label(self.addframe, text='Condicao')

        self.namelabel = tk.Label(self.addframe, text='Nome do novo tipo: ')
        self.nameentry = tk.Entry(self.addframe)
        self.filterlabel = tk.Label(self.addframe, text='CONFIGURACOES DE FILTRAGEM')

        ###ADD FRAME - ANALYTICS
        self.analyticsframe = tk.Frame(self)
        self.analyticslabel = tk.Label(self.analyticsframe, text='CONFIGURACOES DE ANALIZE')

        self.mainnamelabel = tk.Label(self.analyticsframe, text='Fazer analize pela coluna**: ')
        self.analizedlabel = tk.Label(self.analyticsframe, text='Analizar coluna**: ')
        self.monthslabel = tk.Label(self.analyticsframe, text='Para calculo de esgotamento ')
        self.totallabel = tk.Label(self.analyticsframe, text='Coluna que guarda o total***: ')
        self.availlabel = tk.Label(self.analyticsframe, text='Coluna que guarda disponibilidade')

        self.analizedentry = tk.Entry(self.analyticsframe)
        self.columnentry = tk.Entry(self.analyticsframe)
        self.totalentry = tk.Entry(self.analyticsframe)
        self.availentry = tk.Entry(self.analyticsframe)


        ### STATUS FRAME
        self.statusframe = tk.Frame(self)
        self.asterisk1 = tk.Label(self.statusframe, text='* Necessario e obrigratorio para fazer a filtragem.')
        self.asterisk2 = tk.Label(self.statusframe, text='** Necessario e obrigratorio caso se deseje fazer analize estatistica.')
        self.asterisk3 = tk.Label(self.statusframe, text='*** Necessario e obrigratorio caso se deseje fazer o calculo de esgotamentos.')

        ###COMMON VARIABLES
        self.GROUPENTRYSLIST = []
        self.COUNTENTRYSLIST = []
        self.GROUPROWCOUNT = 4
        self.COUNTROWCOUNT = 4

    def dispose_widgets(self):

        ###MAIN FRAME
        self.mainframe.pack()
        self.typelabel.grid(row=0, column=0)
        self.typelistbox.grid(row=1, columnspan=3)
        self.visualbutton.grid(row=2, column=0)
        self.newbutton.grid(row=2, column=1)
        self.deletebutton.grid(row=2, column=2)
        self.statuslabel.grid(row=3, columnspan=3)


        ###ADD FRAME
        self.filterlabel.grid(row=0, columnspan=7)
        self.namelabel.grid(row=1, columnspan=3)
        self.nameentry.grid(row=1, column=3, columnspan=4)
        
        self.minusgroupbutton.grid(row=2, column=0)
        self.grouplabel.grid(row=2, column=1, columnspan=2)
        self.plusgroupbutton.grid(row=2, column=3)

        self.minuscountbutton.grid(row=2, column=4)
        self.countlabel.grid(row=2, column=5, columnspan=2)
        self.pluscountbutton.grid(row=2, column=7)

        self.brutegrouplabel.grid(row=3, column=0, columnspan = 2)
        self.newgrouplabel.grid(row=3, column=2, columnspan=2)

        self.brutecountlabel.grid(row=3, column=4)
        self.newcountlabel.grid(row=3, column=5)
        self.conditionallabel.grid(row=3, column=6, columnspan=2)
        self.newtypebutton.grid(row=0, column=0)

        ###ADD FRAME - ANALYTICS
        self.analyticslabel.grid(row=0, columnspan=2)

        self.mainnamelabel.grid(row=1, column=0)
        self.analizedentry.grid(row=1, column=1)

        self.analizedlabel.grid(row=2, column=0)
        self.columnentry.grid(row=2, column=1)

        self.monthslabel.grid(row=3, columnspan=2)

        self.totallabel.grid(row=4, column=0)
        self.totalentry.grid(row=4, column=1)

        self.availlabel.grid(row=5, column=0)
        self.availentry.grid(row=5, column=1)

        self.update_listbox()

    def add_new_type(self):

        ### NAME VERIFICATION
        count = []
        group = []
        name = self.nameentry.get()
        if name == '':
            tkMessageBox.showerror('Erro', 'Nome do tipo nao informado!')
            return

        ### GROUP VERIFICATION
        for g in self.GROUPENTRYSLIST:
            e1 = g[0].get()
            e2 = g[1].get()
            if e2 != '' and e1 == '':
                tkMessageBox.showerror('Erro', 'Novo nome ' + e2 + ' sem padrao Nome Bruto obrigratorio')
                self.forget_lists()
                return
            if e1 == '':
                continue
            group.append([e1,e2])

        ### COUNT VERIFICATION
        for c in self.COUNTENTRYSLIST:
            e1 = c[0].get()
            e2 = c[1].get()
            e3 = c[2].get()
            if (e2 != '' or e3 != '') and e1 == '':
                tkMessageBox.showerror('Erro', 'Novo nome '+e2+' e Condicao '+e3+' sem padrao Nome Bruto obrigratorio')
                self.forget_lists()
                return
            if e1 == '':
                continue
            count.append([e1,e2,e3])

        if count == [] and group == []:
            tkMessageBox.showerror('Erro', 'Nenhuma coluna informada - Impossivel cadastrar tipo')
            return
        if count == []:
            answer = tkMessageBox.askquestion('Atencao', 'Nenhuma coluna de contagem informada! Prosseguir mesmo assim?')
            if answer == 'no':
                return
        if group == []:
            answer = tkMessageBox.askquestion('Atencao', 'Nenhuma coluna de agrupamento informada! Prosseguir mesmo assim?')
            if answer == 'no':
                return

        
        ###ANALYSIS VERIFICATION
        main = self.analizedentry.get()
        target = self.columnentry.get()
        total = self.totalentry.get()
        avail = self.availentry.get()

        if main == '' and target == '' and total == '' and avail == '':
            answer = tkMessageBox.askquestion('Atencao', 'Nenhuma coluna de analize informada! Prosseguir mesmo assim? Obs.: Nao sera possivel fazer analizes estatisticas!')
            if answer == 'no':
                self.forget_lists()
                return
        elif main == '' or target == '':
            tkMessageBox.showerror('Erro', 'Para analize e preciso que as colunas marcadas em ** sejam preenchidas')
            self.forget_lists()
            return
        elif avail != '' and total == '':
            tkMessageBox.showerror('Erro', 'Para calculo de esgotamento e preciso que as colunas marcadas em *** sejam preenchidas')
            self.forget_lists()
            return

        self.forget()
        tph.write_new_type(std.TYPE_FILENAME, name, count, group, main, target, total, avail)
        self.update_listbox()



    def forget_lists(self):
        self.GROUPENTRYSLIST = []
        self.COUNTENTRYSLIST = []


    def forget(self):

        for c in self.COUNTENTRYSLIST:
            c[0].grid_forget()
            c[1].grid_forget()
            c[2].grid_forget()

        for g in self.GROUPENTRYSLIST:
            g[0].grid_forget()
            g[1].grid_forget()

        self.analyticsframe.pack_forget()
        self.addbuttonframe.pack_forget()
        self.addframe.pack_forget()
        self.nameentry.delete(0, tk.END)
        self.columnentry.delete(0, tk.END)
        self.analizedentry.delete(0, tk.END)
        self.totalentry.delete(0, tk.END)
        self.availentry.delete(0, tk.END)


    def delete_type(self):
        
        index = self.typelistbox.curselection()
        if index == ():
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um tipo')
            return
        
        index = index[0]
        name = self.typelistbox.get(index)
        tph.purge_type(std.TYPE_FILENAME, name)
        self.update_listbox()


    def show_details(self):

        index = self.typelistbox.curselection()
        if index == ():
            tkMessageBox.showerror('Erro', 'Voce nao selecionou um tipo')
            return
        
        index = index[0]
        name = self.typelistbox.get(index)

        print tph.get_details(name)


    def add_group_entry(self):

        new_entry1 = tk.Entry(self.addframe)
        new_entry1.grid(row=self.GROUPROWCOUNT, column=0, columnspan=2)
        
        new_entry2 = tk.Entry(self.addframe)
        new_entry2.grid(row=self.GROUPROWCOUNT, column=2, columnspan=2)
        
        self.GROUPENTRYSLIST.append([new_entry1, new_entry2])
        self.GROUPROWCOUNT += 1


    def add_count_entry(self):
        
        new_entry1 = tk.Entry(self.addframe)
        new_entry1.grid(row=self.COUNTROWCOUNT, column=4)
                
        new_entry2 = tk.Entry(self.addframe)
        new_entry2.grid(row=self.COUNTROWCOUNT, column=5, columnspan=1)
        
        new_entry3 = tk.Entry(self.addframe)
        new_entry3.grid(row=self.COUNTROWCOUNT, column=6, columnspan=2)

        self.COUNTENTRYSLIST.append([new_entry1, new_entry2, new_entry3])
        self.COUNTROWCOUNT += 1


    def sub_group_entry(self):

        if self.GROUPENTRYSLIST == []:
            return

        entry1 = self.GROUPENTRYSLIST[-1][0]
        entry2 = self.GROUPENTRYSLIST[-1][1]

        entry1.grid_forget()
        entry2.grid_forget()

        self.GROUPROWCOUNT -= 1
        self.GROUPENTRYSLIST.pop()
        

    def sub_count_entry(self):
        
        if self.COUNTENTRYSLIST == []:
            return

        entry1 = self.COUNTENTRYSLIST[-1][0]
        entry2 = self.COUNTENTRYSLIST[-1][1]
        entry3 = self.COUNTENTRYSLIST[-1][2]
        
        entry1.grid_forget()
        entry2.grid_forget()
        entry3.grid_forget()

        self.COUNTROWCOUNT -= 1
        self.COUNTENTRYSLIST.pop()


    def show_addframe(self):

        self.addframe.pack()
        if len(self.COUNTENTRYSLIST) is 0:
            self.add_count_entry()
        if len(self.GROUPENTRYSLIST) is 0:
            self.add_group_entry()
        self.analyticsframe.pack()
        self.addbuttonframe.pack()

    def update_listbox(self):

        names = tph.get_type_names()
        self.typelistbox.delete(0, tk.END)

        for name in names:
            self.typelistbox.insert(tk.END, name)
        