#!/usr/bin/env python

""" Main interface for the program """

import Tkinter as tk
import os
import ttk
import sys
import inspect

try:
    import interfaces.conversion_interface.conversionframe as cvt_interface
except ImportError:
    CUR = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    sys.path.insert(0, CUR)
    import interfaces.conversion_interface.conversionframe as cvt_interface

import interfaces.database_interface.databaseframe as db_interface
import interfaces.filter_interface.filterframe as flt_interface
import interfaces.analysis_interface.analysisframe as anl_interface
import interfaces.type_interface.typeframe as tp_interface

import tb_code.typehandle as tph
import tb_code.standart as std


def main():
    """ Main program function """

    window = tk.Tk()
    window.title('TableFilter')
    notebook = ttk.Notebook(window)

    tph.initialize_types(std.TYPE_FILENAME)
    std.clean_log_file()

    cvt_frame = cvt_interface.ConversionFrame(notebook)
    notebook.add(cvt_frame, text='Conversao')

    flt_frame = flt_interface.FilterFrame(notebook)
    notebook.add(flt_frame, text='Filtragem')

    anl_frame = anl_interface.AnalysisFrame(notebook)
    notebook.add(anl_frame, text='Analise')

    db_frame = db_interface.DatabseFrame(notebook)
    notebook.add(db_frame, text='Base de Dados')

    tp_frame = tp_interface.TypeFrame(notebook)
    notebook.add(tp_frame, text='Tipos')

    notebook.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
