#!/usr/bin/env python
# -*- coding: utf8 -*-

import eel
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import oa_core as core
import distutils.util
import re

@eel.expose
def change_theme(_theme):
    _css_file_path = "resource/css/layout.css"
    _css_file = open(_css_file_path, mode="r")
    _old_css = _css_file.read()
    _css_file.close
    if _theme == "dark":
        _new_css = '@import url("dark_theme.css");' + _old_css[_old_css.find(";") + 1:]
    else:
        _new_css = '@import url("light_theme.css");' + _old_css[_old_css.find(";") + 1:]
    _css_file = open(_css_file_path, mode="w")
    _css_file.write(_new_css)
    _css_file.close()
    return

@eel.expose
def load_flag(_flag_name):
    _f = open("resource/setting/flag.oflg")
    _flag_file = _f.read()
    _f.close()
    if _flag_name in _flag_file:
        _flag_file = _flag_file[_flag_file.find(_flag_name):]
        return core.convert_to_bool(re.split(":", _flag_file[:_flag_file.find("\n")])[1])
    else:
        return False

@eel.expose
def set_flag(_flag_name, _flag_value):
    _f = open("resource/setting/flag.oflg", mode="r")
    _flag_file = _f.read()
    _f.close()
    if _flag_name in _flag_file:
        _rewriting_place = _flag_file[_flag_file.find(_flag_name):].strip() + "\n"
        _rewriting_place = _rewriting_place[:_rewriting_place.find("\n") + 1]
        _f = open("resource/setting/flag.oflg", mode="w")
        _f.write(_flag_file.replace(_rewriting_place.strip(), _rewriting_place[:_rewriting_place.find(":") + 1] + str(_flag_value)))
        _f.close()
        return
    else:
        _new_flag_file = _flag_file.strip() + "\n" + _flag_name + ":" + str(_flag_value)
        _f = open("resource/setting/flag.oflg", mode="w")
        _f.write(_new_flag_file.strip())
        _f.close()
        return

@eel.expose
def make_response(_not_normalized_query):
    return core.respond(dictionary, core.normalize(_not_normalized_query))

@eel.expose
def check_update():
    return core.check_update("resource/information.txt", "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML-Based/master/resource/information.txt", "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML-Based/master/update_message.txt")

try:
    dictionary = core.load_dictionary("resource/dictionary/dictionary.odic")
except Exception as error_message:
    root = tk.Tk()
    root.withdraw()
    dictionary_error = messagebox.showerror("ORIZIN Agent　エラー", error_message)
    sys.exit()
eel.init("resource")
eel.start("/html/splash.html")
