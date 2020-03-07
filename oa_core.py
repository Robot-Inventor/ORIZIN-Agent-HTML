#!/usr/bin/env python
# -*- coding: utf8 -*-

import random
import re
import urllib.request
import subprocess
import os


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

def read_setting(_setting_file_path, _setting_name):
    if os.path.exists(_setting_file_path) == False:
        _f = open(_setting_file_path, mode="w")
        return None
    else:
        _f = open(_setting_file_path, mode="r")
        _setting_file = _f.read()
        _f.close()
        if _setting_name in _setting_file:
            _setting_file = _setting_file[_setting_file.find(_setting_name):]
            return (re.split(":", _setting_file[:_setting_file.find("\n")])[1]).replace("&#47", ":").replace("&#58", "/")
        else:
            return None

def write_setting(_setting_file_path, _setting_name, _setting_value):
    _f = open(_setting_file_path, mode="r")
    _setting_file = _f.read()
    _f.close()
    if _setting_name in _setting_file:
        _rewriting_place = _setting_file[_setting_file.find(_setting_name):].strip() + "\n"
        _rewriting_place = _rewriting_place[:_rewriting_place.find("\n") + 1]
        _f = open(_setting_file_path, mode="w")
        _f.write(_setting_file.replace(_rewriting_place.strip(), _rewriting_place[:_rewriting_place.find(":") + 1] + str(_setting_value).replace(":", "&#47").replace("/", "&#58")))
        _f.close()
        return
    else:
        _new_setting_file = _setting_file.strip() + "\n" + _setting_name + ":" + str(_setting_value).replace(":", "&#47").replace("/", "&#58")
        _f = open(_setting_file_path, mode="w")
        _f.write(_new_setting_file.strip())
        _f.close()
        return

def read_flag(_flag_file_path, _flag_name):
    return convert_to_bool(read_setting(_flag_file_path, _flag_name))

def set_flag(_flag_file_path, _flag_name, _flag_value):
    write_setting(_flag_file_path, _flag_name, str(convert_to_bool(_flag_value)))
    return
