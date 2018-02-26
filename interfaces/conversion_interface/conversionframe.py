#!/usr/bin/python2.7

""" Holds the Conversion interface and its methods """

import Tkinter as tk
import tkMessageBox
import os.path
import interfaces.conversion_interface.fileinputframe as fileinputframe
import interfaces.conversion_interface.advancedframe as advancedframe
import interfaces.conversion_interface.sheetsframe as sheetsframe
import tb_code.standart as std
import tb_code.convert as cvt


class ConversionFrame(tk.Frame):
    """ Implements the conversion frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)

        convert_labelframe = tk.LabelFrame(
            self, text='Arquivo', pady=10, padx=5)
        self.advanced_labelframe = tk.LabelFrame(
            self, text='Avancado', pady=10, padx=5)
        self.options_labelframe = tk.LabelFrame(
            self, text='Opcoes', pady=10, padx=5)
        self.sheets_labelframe = tk.LabelFrame(
            self, text='Multiplas Tabelas', pady=10, padx=5)

        self.file_frame = fileinputframe.FileInputFrame(
            convert_labelframe)
        self.advanced_frame = advancedframe.AdvancedFrame(
            self.advanced_labelframe)
        self.sheets_frame = sheetsframe.SheetsFrame(self.sheets_labelframe)

        convert_labelframe.pack(fill=tk.X)
        self.options_labelframe.pack(fill=tk.X)

        # Buttons
        tk.Button(self.options_labelframe, text='Mostrar avancado',
                  command=self.toggle_advanced).grid(row=0, column=0, padx=20, pady=10)
        tk.Button(self.options_labelframe, text='Converter arquivo',
                  command=self.convert).grid(row=0, column=1, padx=20, pady=10)

        self.options_labelframe.grid_columnconfigure(0, weight=1)
        self.options_labelframe.grid_columnconfigure(1, weight=1)

        self.file_frame.pack()
        self.advanced_frame.pack()
        self.sheets_frame.pack()

    def toggle_advanced(self):
        """ Toggles the advanced frame """

        if self.advanced_labelframe.winfo_ismapped() == 0:
            self.options_labelframe.pack_forget()
            self.advanced_labelframe.pack(fill='both')
            self.options_labelframe.pack(fill='both')
        else:
            self.advanced_labelframe.pack_forget()

    def show_sheet_frame(self, sh_list):
        """ Shows the sheet frame """

        self.options_labelframe.pack_forget()
        self.sheets_frame.fill_frame(sh_list)

        if self.advanced_labelframe.winfo_ismapped() == 1:
            self.advanced_labelframe.pack_forget()
            self.sheets_labelframe.pack()
            self.advanced_labelframe.pack()
        else:
            self.sheets_labelframe.pack()

        self.options_labelframe.pack()

    def hide_sheet_frame(self):
        """ Hides the sheet frame """

        self.sheets_frame.clear_frame()
        self.sheets_labelframe.pack_forget()

    def verify_input(self):
        """ Verifies the input typed by the user """

        filename = self.file_frame.get_filename()
        name = self.file_frame.get_rename()

        if filename == '' or (not os.path.isfile(filename)):
            tkMessageBox.showerror(
                'Error', 'Caminho Invalido, selecione um valido')
            return False

        if name.find('"') != -1 or name.find("'") != -1 or name == '':
            tkMessageBox.showerror(
                'Error', 'Nome invalido, nao pode conter "" ou \'\' ')
            return False

        if self.advanced_frame.get_standart_option() == 1 and self.advanced_frame.get_type() == '':
            tkMessageBox.showerror(
                'Error', 'Para usar o nome padrao e necessario informar um tipo')
            return False
        return True

    def convert(self):
        """ Converts the .csv or .xlrd file to a postgresql database table """

        self.verify_input()
        standart_name = self.advanced_frame.get_standart_option()
        # Gets the name, standart or not
        if standart_name == 1:
            try:
                name = self.__get_standart_name()
            except ValueError:
                tkMessageBox.showerror(
                    'Error', 'Mes ou ano informados da forma incorreta')
                return
        else:
            name = self.file_frame.get_rename()

        filename = self.file_frame.get_filename()

        # Converting multiple sheets
        if self.sheets_labelframe.winfo_ismapped() == 1:
            text = self.__convert_multiple(name)
        # Converting a csv file
        elif filename.split('.')[-1] == 'csv':
            text = self.__convert_csv(name)
        # Converting a xlrd file
        else:
            text = self.__convert_xlrd(name)

        if text == '':
            self.show_sheet_frame(cvt.get_sheet_names(filename))
            return
        elif self.sheets_labelframe.winfo_ismapped() == 1:
            self.hide_sheet_frame()

        tkMessageBox.showinfo('Info', text)

    def __convert_xlrd(self, name):
        """ Converts xlrd file """

        filename = self.file_frame.get_filename()
        text = ''

        sheets = cvt.get_sheet_names(filename)
        if len(sheets) > 1:
            return text

        final_name = final_name = self.file_frame.get_rename() if isinstance(
            name, str) else cvt.get_std_name(0, *name)
        final_csv = cvt.single_csv(filename, sheets[0], 'default')
        cvt.fileto_postgre(final_csv, final_name, std.DBNAME)
        text = final_name + ' adicionada com sucesso a base de dados'
        #text = final_name + ': problema ao criar a tabela na base de dados'

        return text

    def __convert_csv(self, name):
        """ Converts a csv file """

        filename = self.file_frame.get_filename()
        text = ''
        print "Trying to convert a csv file"
        # try:
        print "Will try to normalize"
        new_file = cvt.normalize_csv_file(filename)
        print "Normalized"
        final_name = final_name = self.file_frame.get_rename() if isinstance(
            name, str) else cvt.get_std_name(0, *name)
        cvt.fileto_postgre(new_file, final_name, std.DBNAME)
        text += final_name + ' adicionada com sucesso a base de dados'
        # except:
        #     text += final_name + ': problema ao criar a tabela na base de dados'
        return text

    def __convert_multiple(self, name):
        """ Converts multiple sheets """

        sheets = self.sheets_frame.get_checked_names()
        filename = self.file_frame.get_filename()
        text = ''

        if sheets == []:
            tkMessageBox.showerror('Error', 'Nenhuma planilha selecionda')
        for i, sheet in enumerate(sheets):
            csv_file = cvt.single_csv(filename, sheet, 'default')

            try:
                final_name = self.file_frame.get_rename() if isinstance(
                    name, str) else cvt.get_std_name(i, *name)
                cvt.fileto_postgre(csv_file, final_name, std.DBNAME)
                text += final_name + ' criada com sucesso na base de dados\n'
            except:
                text += 'Erro ao criar tabela ' + final_name

        return text

    def __get_standart_name(self):
        """ Gets the variables tb_type, year and month for standart name """

        year = self.advanced_frame.get_year()
        month = self.advanced_frame.get_month()
        tb_type = self.advanced_frame.get_type()

        year = None if year == '' else int(year)
        month = None if month == '' else int(month)

        return (tb_type, year, month)
