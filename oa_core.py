#!/usr/bin/env python
# -*- coding: utf8 -*-

import urllib.request
import urllib.parse
import os
import otfdlib
from collections import OrderedDict
import unicodedata
import re
import difflib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def normalize(_sentence):
    return convert_kanji_to_int(unicodedata.normalize("NFKC", _sentence.lower()).translate(str.maketrans("", "", " 　・_-\t\n\r")))


def convert_kanji_to_int(string):
    result = string.translate(str.maketrans("零〇一壱二弐三参四五六七八九", "00112233456789", ""))
    while re.search("(零|〇|一|壱|二|弐|三|参|四|五|六|七|八|九|十|百|千|万|億|兆|京)+", result):
        target = re.search("(零|〇|一|壱|二|弐|三|参|四|五|六|七|八|九|十|百|千|万|億|兆|京)+", string).group()
        if re.search("十|百|千|万|億|兆|京", result):
            result = result.replace("拾", "十")
            convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000", "億": "00000000", "兆": "000000000000", "京": "0000000000000000"}
            for index in convert_table.keys():
                unit = convert_table[index]
                for numbers in re.findall(f"(\d+){index}(\d+)", result):
                    result = result.replace(numbers[0] + index + numbers[1], numbers[0] + unit[len(numbers[1]):len(unit)] + numbers[1])
                for number in re.findall(f"(\d+){index}", result):
                    result = result.replace(number + index, number + unit)
                for number in re.findall(f"{index}(\d+)", result):
                    result = result.replace(index + number, "1" + unit[len(number):len(unit)] + number)
                result = result.replace(index, "1" + unit)
    return result


def load_dictionary(_path):
    root = otfdlib.Otfd()
    root.load(_path)
    root.parse()
    return root.to_string()


def judge(_input, _target, _matched_word=False):
    for _word in _target:
        if bool(re.search(_word, _input)):
            if _matched_word:
                return [True, _word]
            else:
                return True
    if _matched_word:
        return [False, ""]
    else:
        return False


def judge_with_intelligent_match(_input, _target, _threshold=0.75):
    for _content in _target:
        if intelligent_match(_input, _content) >= _threshold:
            return True
    return False


def respond(_dictionary, _query):
    root = otfdlib.Otfd()
    root.load_from_string(_dictionary)
    root.parse()
    _index_list = root.get_index_list()
    _similarity = {}
    for _index in _index_list:
        _splited_index = root.unescape(list(_index.split("/")))
        _similarity[max([intelligent_match(input, _query) for input in _splited_index])] = _index
        _judge_result = judge(_query, _index.split("/"), True)
        if _judge_result[0]:
            _response = root.get_value(_index).split("/")
            if len(_response) == 1:
                return root.unescape([_response[0], _response[0], _judge_result[1]])
            else:
                return root.unescape([_response[0], _response[1], _judge_result[1]])
    if os.path.exists("resource/dictionary/unknownQuestions.txt") is False:
        with open("resource/dictionary/unknownQuestions.txt", mode="w", newline="") as _f:
            pass
    _unknown_question = otfdlib.Otfd()
    _unknown_question.load("resource/dictionary/unknownQuestions.txt")
    _unknown_question.parse()
    _response = []
    _max_similarity = max(_similarity.keys())
    _most_similar_word = _similarity[_max_similarity]
    if _max_similarity >= 0.75:
        _response = list(root.get_value(_most_similar_word).split("/"))
    else:
        _response = ["そうですか。"]
    _unknown_question.add(_query, "/".join(_response))
    _unknown_question.write()
    if len(_response) == 1:
        return root.unescape([_response[0], _response[0], _most_similar_word])
    else:
        return root.unescape([_response[0], _response[1], _most_similar_word])


def check_update(_downloaded_file_path, _remote_file_url, _update_message_url):
    _update_message = urllib.request.urlopen(_update_message_url).read().decode()
    _current = otfdlib.Otfd()
    _current.load(_downloaded_file_path)
    _current.parse()
    _current_version = _current.get_value("Version")
    _remote = otfdlib.Otfd()
    _remote.load_from_string(urllib.request.urlopen(_remote_file_url).read().decode().replace(" : ", ":"))
    _remote.parse()
    _remote_version = _remote.get_value("Version")
    if _current_version == _remote_version:
        return ["false", _current_version, _remote_version, _update_message]
    else:
        _versions = [_current_version, _remote_version]
        _versions.sort()
        if _versions[0] == _current_version:
            return ["true", _current_version, _remote_version, _update_message]
        else:
            return ["false", _current_version, _remote_version, _update_message]


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
    if os.path.exists(_setting_file_path) is False:
        with open(_setting_file_path, mode="w") as _f:
            pass
        return None
    else:
        root = otfdlib.Otfd()
        root.load(_setting_file_path)
        root.parse()
        if _setting_name in root.get_index_list():
            return root.unescape(root.get_value(_setting_name))
        return None


def write_setting(_setting_file_path, _setting_name, _setting_value):
    if os.path.exists(_setting_file_path) is False:
        with open(_setting_file_path, mode="w") as _f:
            pass
    root = otfdlib.Otfd()
    root.load(_setting_file_path)
    root.parse()
    root.add(_setting_name, root.escape(_setting_value))
    root.write()
    return


def read_flag(_flag_file_path, _flag_name):
    return convert_to_bool(read_setting(_flag_file_path, _flag_name))


def set_flag(_flag_file_path, _flag_name, _flag_value):
    write_setting(_flag_file_path, _flag_name, str(convert_to_bool(_flag_value)))
    return


def solve_setting_conflict(_default_setting_file_path, _current_setting_file_path):
    if os.path.exists(_default_setting_file_path) is False:
        raise Exception(f"{_default_setting_file_path}にデフォルト設定ファイルがありません。")
    if os.path.exists(_current_setting_file_path) is False:
        with open(_current_setting_file_path, mode="w") as _f:
            pass
    default_setting = otfdlib.Otfd()
    default_setting.load(_default_setting_file_path)
    default_setting.parse()
    _default_index_list = default_setting.get_index_list()
    current_setting = otfdlib.Otfd()
    current_setting.load(_current_setting_file_path)
    current_setting.parse()
    _current_index_list = current_setting.get_index_list()
    _need_to_add = list(set(_default_index_list) - set(_current_index_list))
    current_setting.update(OrderedDict(map(lambda _index: [_index, default_setting.get_value(_index)], _need_to_add)))
    _need_to_delete = list(set(_current_index_list) - set(_default_index_list))
    for _index in _need_to_delete:
        current_setting.pop(_index)
    default_setting.sorted()
    current_setting.sorted()
    default_setting.write()
    current_setting.write()


def generate_search_engine_url(search_engine="google", keyword=None, define=False):
    if keyword:
        keyword = urllib.parse.quote(keyword)
    if define:
        if keyword:
            return search_engine + keyword
        else:
            return re.search(r".*?", search_engine)
    else:
        search_engine = normalize(search_engine)
        search_engine_url_table = {
            "google": "https://google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "yahoo": "https://search.yahoo.com/search?p=",
            "yahoojapan": "https://search.yahoo.co.jp/search?p=",
            "duckduckgo": "https://duckduckgo.com/?q="
            }
        if search_engine not in search_engine_url_table:
            similarity = {intelligent_match(engine_name, search_engine): engine_name for engine_name in search_engine_url_table.keys()}
            search_engine = similarity[max(similarity.keys())]
        if keyword:
            return search_engine_url_table[search_engine] + keyword
        else:
            url = search_engine_url_table[search_engine]
            return url[:url.rfind("/") + 1]


def intelligent_match(a, b):
    if len(a) > len(b):
        a_cache = a
        a = b
        b = a_cache
    if bool(re.search(a, b)):
        return 1.0
    else:
        a_length = len(a)
        return max(list(map(lambda target: difflib.SequenceMatcher(None, target, a).ratio(), [b[num:num + a_length] for num in range(len(b) - a_length + 1)])))


def showerror(_message):
    root = tk.Tk()
    root.withdraw()
    error_window = messagebox.showerror("ORIZIN Agent　エラー", _message)
    error_window.wm_attributes("-topmost", True)
    root.destroy()
    return


def showinfo(_message):
    root = tk.Tk()
    root.withdraw()
    message_window = messagebox.showinfo("ORIZIN Agent", _message)
    message_window.wm_attributes("-topmost", True)
    root.destroy()
    return
