#!/usr/bin/env python
# -*- coding: utf8 -*-

import eel
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import oa_core as core
import re
import webbrowser
import os
import pathlib

@eel.expose
def change_theme(_css_theme_path):
    _css_file_path = "resource/css/layout.css"
    _css_file = open(_css_file_path, mode="r")
    _old_css = _css_file.read()
    _css_file.close()
    if os.path.exists("resource/css/" + _css_theme_path) == False:
        _light_theme_file = open("resource/css/theme/light_theme.css", mode="r")
        _light_theme = _light_theme_file.read()
        _light_theme_file.close()
        _new_theme = open("resource/css/" + _css_theme_path, mode="w")
        _new_theme.write(_light_theme)
        _new_theme.close()
    _new_css = '@import url("' + _css_theme_path + '");' + _old_css[_old_css.find(";") + 1:]
    _css_file = open(_css_file_path, mode="w")
    _css_file.write(_new_css)
    _css_file.close()
    write_setting("theme", _css_theme_path)
    return

@eel.expose
def write_custom_css_theme(_value):
    if len(_value) == 5:
        _custom_css_data = ":root {\n    --bg: " + _value[0] + ";\n    --card_bg: " + _value[1] + ";\n    --text: " + _value[2] + ";\n    --shadow: " + _value[3] +";\n    --theme_color: " + _value[4] + ";\n}"
        _f = open("resource/css/theme/custom_theme.css", mode="w")
        _f.write(_custom_css_data)
        _f.close()
        return
    else:
        root = tk.Tk()
        root.withdraw()
        error = messagebox.showerror("ORIZIN Agent　エラー", "カスタムCSSテーマに不正な値を書き込もうとしています。")
        root.destroy()
        return

@eel.expose
def ask_css_theme_file():
    root = tk.Tk()
    root.withdraw()
    _css_theme_path = filedialog.askopenfilename(filetypes=[("css", ".css")], initialdir="resource/css/theme/")
    if os.path.exists(_css_theme_path) == False:
        return ""
    return pathlib.Path(_css_theme_path).relative_to(pathlib.Path("resource/css/").resolve())

@eel.expose
def read_setting(_setting_name):
    return core.read_setting("resource/setting/setting.otfd", _setting_name)

def write_setting(_setting_name, _setting_value):
    return core.write_setting("resource/setting/setting.otfd", _setting_name, _setting_value)

@eel.expose
def read_flag(_flag_name):
    return core.read_flag("resource/setting/flag.otfd", _flag_name)

@eel.expose
def set_flag(_flag_name, _flag_value):
    core.set_flag("resource/setting/flag.otfd", _flag_name, _flag_value)
    return

@eel.expose
def make_response(_not_normalized_query):
    _query = core.normalize(_not_normalized_query)
    if core.judge(_query, ["じゃんけん", "ジャンケン"]):
        _random_int = random.randint(0, 2)
        if _random_int == 0:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はグーです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はグーです。"]
        elif _random_int == 1:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はチョキです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はチョキです。"]
        else:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はパーです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はパーです。"]
    elif core.judge(_query, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen(["python", "resource/python/easter_egg.py"])
        return ["イースターエッグを起動します。", "イースターエッグを起動します。"]
    elif core.judge(_query, ["予定", "よてい", "カレンダ", "かれんだ", "calender", "リマインダ", "リマインド", "りまいんだ", "りまいんど", "remind", "メモ", "めも"]):
        webbrowser.open_new("https://calendar.google.com/")
        return ["Googleカレンダーを開きます", "Googleカレンダーを開きます。"]
    elif core.judge(_query, ["マップ", "まっぷ", "地図", "ちず", "場所", "ばしょ", "どこ", "何処", "行き方", "いきかた", "ゆきかた", "行きかた", "いき方", "ゆき方", "案内", "あんない", "道"]):
        webbrowser.open_new("https://google.com/maps/search/" + _query)
        return ["Googleマップで" + _query + "を検索します。", "Googleマップで" + _query + "を検索します。"]
    elif core.judge(_query, ["タイマ", "たいま"]):
        webbrowser.open_new("https://google.com/search?q=timer&hl=en")
        return ["タイマーを表示します。", "タイマーを表示します"]
    elif core.judge(_query, ["ストップウォッチ", "ストップウオッチ", "stopwatch"]):
        webbrowser.open_new("https://google.com/search?q=stopwatch&hl=en")
        return ["ストップウォッチを表示します。", "ストップウォッチを表示します。"]
    elif core.judge(_query, ["計算", "けいさん", "電卓", "でんたく"]):
        webbrowser.open_new("https://google.com/search?q=電卓")
        return ["電卓を開きます。", "電卓を開きます。"]
    elif core.judge(_query, ["何時", "時間", "時刻", "時計", "なんじ", "じかん", "じこく", "とけい"]) and read_flag("search_time_with_google") == True:
        webbrowser.open_new("https://google.com/search?q=今何時")
        return ["Googleで現在の時刻を検索します。", "Googleで現在の時刻を検索します。"]
    elif core.judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ"]):
        webbrowser.open_new("https://google.com/search?q=" + _query)
        return ["Googleで「" + _query + "」を検索します。", "Googleで「" + _query + "」を検索します。"]
    else:
        return core.respond(dictionary, _query)

@eel.expose
def check_update():
    return core.check_update("resource/information.txt", "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/resource/information.txt", "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/update_message.txt")


if __name__ == "__main__":
    try:
        dictionary = core.load_dictionary("resource/dictionary/dictionary.otfd")
    except Exception as error_message:
        root = tk.Tk()
        root.withdraw()
        dictionary_error = messagebox.showerror("ORIZIN Agent　エラー", error_message)
        sys.exit()
    if os.path.exists("resource/setting/setting.otfd") == False:
        change_theme("theme/light_theme.css")
    core.solve_setting_conflict("resource/setting/default_setting.otfd", "resource/setting/setting.otfd")
    core.solve_setting_conflict("resource/setting/default_flag.otfd", "resource/setting/flag.otfd")
    eel.init("resource")
    eel.start("/html/splash.html")
