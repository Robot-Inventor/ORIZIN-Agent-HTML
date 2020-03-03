#!/usr/bin/env python
# -*- coding: utf8 -*-

import random
import webbrowser
import re
import urllib.request
import subprocess


def normalize(_sentence):
    return _sentence.translate(str.maketrans({" ": None, "　": None, "・": None, "_": None})).translate(str.maketrans("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")).lower()

def load_dictionary(_path):
    _f = open(_path, encoding="utf-8_sig")
    _dictionary = _f.read()
    _f.close()
    _number_of_items = _dictionary.count("\n") + 1
    if _number_of_items != _dictionary.count(":"):
        _bigger_num = max([_number_of_items, _dictionary.count(":")])
        _error_place = ""
        _dictionary_data_for_check = _dictionary
        for _num in range(_bigger_num):
            if _dictionary_data_for_check[:_dictionary_data_for_check.find("\n")].count(":") != 1:
                _error_place += '\n"' + _dictionary_data_for_check[0:_dictionary_data_for_check.find('\n')] + '"(' + str(_num + 1) + '行目)'
            _dictionary_data_for_check = _dictionary_data_for_check[_dictionary_data_for_check.find('\n') + 1:]
        raise Exception("エラー\n辞書ファイルの単語リストの数(" + str(_number_of_items) + "個）と応答の数(" + str(_dictionary.count(":")) + "個）が一致しません。正常に動作しない可能性があります。\n" + "問題のある箇所:" + _error_place)
    else:
        return _dictionary.strip()

def judge(_input, _target):
    for _num in range(len(_target)):
        if _target[_num] in _input:
            return True
    return False

def respond(_dictionary, _query):
    if judge(_query, ["じゃんけん", "ジャンケン"]):
        _random_int = random.randint(0, 2)
        if _random_int == 0:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はグーです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はグーです。"]
        elif _random_int == 1:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はチョキです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はチョキです。"]
        else:
            return ["ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はパーです。", "ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私はパーです。"]
    elif judge(_query, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen(["python", "resource/python/easter_egg.py"])
        return ["イースターエッグを起動します。", "イースターエッグを起動します。"]
    elif judge(_query, ["予定", "よてい", "カレンダ", "かれんだ", "calender", "リマインダ", "リマインド", "りまいんだ", "りまいんど", "remind", "メモ", "めも"]):
        webbrowser.open_new("https://calendar.google.com/")
        return ["Googleカレンダーを開きます", "Googleカレンダーを開きます。"]
    elif judge(_query, ["マップ", "まっぷ", "地図", "ちず", "場所", "ばしょ", "どこ", "何処", "行き方", "いきかた", "ゆきかた", "行きかた", "いき方", "ゆき方", "案内", "あんない", "道"]):
        webbrowser.open_new("https://google.com/maps/search/" + _query)
        return ["Googleマップで" + _query + "を検索します。", "Googleマップで" + _query + "を検索します。"]
    elif judge(_query, ["タイマ", "たいま"]):
        webbrowser.open_new("https://google.com/search?q=timer&hl=en")
        return ["タイマーを表示します。", "タイマーを表示します"]
    elif judge(_query, ["ストップウォッチ", "ストップウオッチ", "stopwatch"]):
        webbrowser.open_new("https://google.com/search?q=stopwatch&hl=en")
        return ["ストップウォッチを表示します。", "ストップウォッチを表示します。"]
    elif judge(_query, ["計算", "けいさん", "電卓", "でんたく"]):
        webbrowser.open_new("https://google.com/search?q=電卓")
        return ["電卓を開きます。", "電卓を開きます。"]
    elif judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ"]):
        webbrowser.open_new("https://google.com/search?q=" + _query)
        return ["Googleで「" + _query + "」を検索します。", "Googleで「" + _query + "」を検索します。"]
    else:
        _target_list = re.split("[\n:]", _dictionary)[::2]
        _response_list = re.split("[\n:]", _dictionary)[1::2]
        _number_of_items = _dictionary.count("\n") + 1
        for _num in range(_number_of_items):
            if judge(_query, _target_list[_num].split("/")):
                _response = _response_list[_num].split("/")
                if len(_response) != 2:
                    _response = [_response[0], _response[0]]
                return _response
        _f = open("resource/dictionary/unknownQuestions.txt", "a", encoding="utf-8_sig")
        _f.write(_query + "\n")
        _f.close()
        return ["そうですか。", "そうですか。"]

def get_version(_info_file_content):
    _result = _info_file_content[_info_file_content.find("Version : "):].replace("Version : ", "")
    return _result[:_result.find("\n")]

def check_update(_downloaded_file_path, _remote_file_url, _update_message_url):
    _remote_file_content = urllib.request.urlopen(_remote_file_url).read().decode()
    _update_message = urllib.request.urlopen(_update_message_url).read().decode()
    _f = open(_downloaded_file_path)
    _downloaded_file_content = _f.read()
    _f.close()
    _current_version = get_version(_downloaded_file_content)
    _remote_version = get_version(_remote_file_content)
    if _current_version == _remote_version:
        return ["false", _current_version, _remote_version, _update_message]
    else:
        return ["true", _current_version, _remote_version, _update_message]

def convert_to_bool(_value):
    _value = normalize(str(_value))
    _false_list = ["false", "f", "no", "n", "not", "none"]
    for _num in range(len(_false_list)):
        if _false_list[_num] in _value:
            return False
    if _value:
        return True
    else:
        return False
