#!/usr/bin/env Python 2.7
""" Main Program Interface for TableFilter """

import ttk
import Tkinter as tk
import standart as std
import typehandle as tph
import filter_interface
import conversion_interface
import analysis_interface
import database_interface
import type_interface


def main():

    """ Implements and show the main window and it's modules to the user """

    ### MAIN WINDOW CONFIGURATIONS
    root = tk.Tk()
    root.geometry('800x600')
    root.update()
    notebook = ttk.Notebook(root)


    ### TYPE INITIALIZATION
    tph.initialize_types(std.TYPE_FILENAME)


    ### CONVERSION FRAME
    cvtframe = conversion_interface.ConversionFrame(notebook)
    notebook.add(cvtframe, text='Conversao')


    ### FILTER FRAME
    filterframe = filter_interface.FilterFrame(notebook)
    notebook.add(filterframe, text='Filtragem')


    ### ANALYSIS FRAME
    anlframe = analysis_interface.AnalysisFrame(notebook)
    notebook.add(anlframe, text='Analize Estatistica')


    ### DATABASE FRAME
    dbframe = database_interface.DatabaseFrame(notebook)
    notebook.add(dbframe, text='Base de Dados')


    ### TYPE FRAME
    typeframe = type_interface.TypeFrame(notebook)
    notebook.add(typeframe, text='Configuracoes de Tipos')


    notebook.pack(expand=True, fill='both')
    root.mainloop()


if __name__ == '__main__':
    main()
