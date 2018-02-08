#!/usr/bin/python2.7

""" Holds the type interface and methods """

import Tkinter as tk
import tkMessageBox


class TypeFrame(tk.Frame):
    """ Implements the type frame """

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
