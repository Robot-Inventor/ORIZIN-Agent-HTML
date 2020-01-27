# -*- coding: utf8 -*-

import eel
import random
import re
import subprocess
import webbrowser
import urllib.request
import sys
import tkinter as tk
from tkinter import messagebox

@eel.expose
def load_dictionary():
    f = open("resource/dictionary/dictionary.odic", encoding="utf-8_sig")
    global dictionary
    global index
    dictionary_file = f.read()
    index = dictionary_file.count("\n") + 1
    if index != dictionary_file.count(":"):
        bigger_num = 0
        if index > dictionary_file.count(":"):
            bigger_num = index
        else:
            bigger_num = dictionary_file.count(":")
        dictionary_checker = dictionary_file
        bad_point = ""
        for num in range(bigger_num):
            if dictionary_checker[0:dictionary_checker.find("\n")].count(":") != 1:
                bad_point += '\n"' + dictionary_checker[0:dictionary_checker.find('\n')] + '"(' + str(num + 1) + '行目)'
            dictionary_checker = dictionary_checker[dictionary_checker.find('\n') + 1:]
        root = tk.Tk()
        root.withdraw()
        dictionary_error = messagebox.showerror("ORIZIN Agent　エラー", "エラー\n辞書ファイルの単語リストの数(" + str(index) + "個）と応答の数(" + str(dictionary_file.count(":")) + "個）が一致しません。正常に動作しない可能性があります。\n" + "問題のある箇所:" + bad_point)
        sys.exit()
    dictionary = dictionary_file
    f.close()


@eel.expose
def change_theme(theme):
    cssFilePath = "resource/css/layout.css"
    cssFile = open(cssFilePath, mode="r")
    oldCss = cssFile.read()
    cssFile.close
    if theme == "dark":
        newCss = '@import url("dark_theme.css");' + oldCss[oldCss.find(";") + 1:]
    else:
        newCss = '@import url("light_theme.css");' + oldCss[oldCss.find(";") + 1:]
    cssFile = open(cssFilePath, mode="w")
    cssFile.write(newCss)
    cssFile.close()
    return

def remove_unnecessary(sentence):
    return sentence.translate(str.maketrans({" ": None, "　": None, "・": None, "_": None}))

def fullpitch_to_highpitch(sentence):
    return sentence.translate(str.maketrans("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))

def adjust_question(sentence):
    return remove_unnecessary(fullpitch_to_highpitch(sentence.lower()))

def judge(character, array):
    for num in range(len(array)):
        if array[num] in character:
            return True
    return False

def search_response(request):
    global response
    global knownQuestion
    knownQuestion = False
    candidate_for_dictionary = re.split("[\n:]", dictionary)[::2]
    candidate_for_response = re.split("[\n:]", dictionary)[1::2]
    for num in range(index):
        if judge(request, candidate_for_dictionary[num].split("/")):
            response_and_insert_content = candidate_for_response[num].split("/")
            return response_and_insert_content[0]
            knownQuestion = True
            break
    if knownQuestion == False:
        f = open("resource/dictionary/unknownQuestions.txt", "a", encoding="utf-8_sig")
        f.write(request + "\n")
        f.close()
        return "そうですか。"

@eel.expose
def make_response(not_adjusted_question):
    question = adjust_question(not_adjusted_question)
    if judge(question, ["じゃんけん", "ジャンケン"]):
        randomInt = random.randint(0, 2)
        if randomInt == 0:
            return "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はグーです。"
        elif randomInt == 1:
            return "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はチョキです。"
        else:
            return "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はパーです。"
    elif judge(question, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen(["python", "resource/python/easter_egg.py"])
        return "イースターエッグを起動します。"
    elif judge(question, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ"]):
        webbrowser.open_new("https://google.com/search?q=" + question)
        return question + "を検索します。"
    else:
        return search_response(question)

def check_version_from_info(file):
    result = file[file.find("Version : "):].replace("Version : ", "")
    return result[:result.find("\n")]
 
@eel.expose
def check_update():
    info_file = urllib.request.urlopen("https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML-Based/master/resource/information.txt").read().decode()
    update_message = urllib.request.urlopen("https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML-Based/master/update_message.txt").read().decode()
    f = open("resource/information.txt")
    local_info_file = f.read()
    f.close()
    current_version = check_version_from_info(local_info_file)
    new_version = check_version_from_info(info_file)
    if info_file != local_info_file:
        return ["true", current_version, new_version, update_message]
    else:
        return ["false", current_version, new_version, update_message]


load_dictionary()
eel.init("resource")
eel.start("/html/splash.html")
