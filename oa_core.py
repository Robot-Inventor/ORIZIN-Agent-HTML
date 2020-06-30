#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib.request
import urllib.parse
import os
import otfdlib
import unicodedata
import re
import difflib
import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import html
import typing


def normalize(_sentence: str) -> str:
    result = normalize_with_dictionary("resource/dictionary/normalize_dictionary.otfd",
                                       convert_kanji_to_int(unicodedata.normalize("NFKC", _sentence.lower()).translate(
                                           str.maketrans(
                                               "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろ"
                                               "わをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっぁぃぅぇぉゔ",
                                               "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロ"
                                               "ワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッァィゥェォブ",
                                               " 　・_-\t\n\r"))))
    replace_table = {"ヴァ": "バ", "ヴィ": "ビ", "ヴゥ": "ブ", "ヴェ": "ベ", "ヴォ": "ボ"}
    for string in replace_table.keys():
        result.replace(string, replace_table[string])
    return result


def normalize_with_dictionary(_file_path: str, _sentence: str) -> str:
    root = otfdlib.Otfd()
    root.load(_file_path)
    root.parse()
    result = _sentence
    for element in root.get_index_list():
        result = re.sub(element.replace("/", "|"), root.get_value(element), _sentence)
    return result


def convert_kanji_to_int(string: str) -> str:
    result = string.translate(str.maketrans("零〇一壱二弐三参四五六七八九拾", "00112233456789十", ""))
    convert_table = {
        "十": "0", "百": "00", "千": "000", "万": "0000", "億": "00000000", "兆": "000000000000", "京": "0000000000000000"
    }
    unit_list = "|".join(convert_table.keys())
    while re.search(unit_list, result):
        for unit in convert_table.keys():
            zeros = convert_table[unit]
            for numbers in re.findall(r"(\d+)" + unit + r"(\d+)", result):
                result = result.replace(
                    numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
            for number in re.findall(r"(\d+)" + unit, result):
                result = result.replace(number + unit, number + zeros)
            for number in re.findall(unit + r"(\d+)", result):
                result = result.replace(unit + number, "1" + zeros[len(number):len(zeros)] + number)
            result = result.replace(unit, "1" + zeros)
    return result


def load_dictionary(_path: str) -> dict:
    root = otfdlib.Otfd()
    root.load(_path)
    root.parse()
    return root.read()


bool_and_str_type_var = typing.TypeVar("bool_and_str_type_var", bool, str)


def judge(_query: str, _dictionary: typing.Union[str, list], _matched_word: bool = False) ->\
        typing.Union[bool, typing.List[bool_and_str_type_var]]:
    if type(_dictionary) == str:
        _dictionary = [_dictionary]
    for _word in _dictionary:
        if bool(re.search(_word, _query)):
            if _matched_word:
                return [True, _word]
            else:
                return True
    if _matched_word:
        return [False, ""]
    else:
        return False


def judge_with_intelligent_match(_input: str, _target: list, _threshold: typing.Union[int, float] = 0.75) -> bool:
    for _content in _target:
        if intelligent_match(_input, _content) >= _threshold:
            return True
    return False


def respond(_dictionary: dict, _query: str) -> typing.List[str]:
    root = otfdlib.Otfd()
    root.load_from_string("")
    root.parse()
    root.update(_dictionary)
    _index_list = root.get_index_list()
    _most_similar_word = ""
    _most_similar_value = 0
    for _index in _index_list:
        _splited_index = root.unescape(list(_index.split("/")))
        _similarity = max([intelligent_match(_input, _query) for _input in _splited_index])
        if _similarity >= _most_similar_value:
            _most_similar_value = _similarity
            _most_similar_word = _index
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
    if _most_similar_value >= 0.75:
        _response = list(root.get_value(_most_similar_word).split("/"))
    else:
        _response = ["そうですか。"]
    _unknown_question.add(_query, "/".join(_response))
    _unknown_question.write()
    if len(_response) == 1:
        return root.unescape([_response[0], _response[0], _most_similar_word])
    else:
        return root.unescape([_response[0], _response[1], _most_similar_word])


def check_update(_downloaded_file_path: str, _remote_file_url: str, _update_message_url: str) ->\
        typing.List[str]:
    _current = otfdlib.Otfd()
    _current.load(_downloaded_file_path)
    _current.parse()
    _current_version = _current.get_value("Version")
    _remote = otfdlib.Otfd()
    _remote.load_from_string(urllib.request.urlopen(_remote_file_url).read().decode())
    _remote.parse()
    _remote_version = _remote.get_value("Version")
    _update_status = "false"
    if _current_version != _remote_version:
        _current_version_numbers = _current_version.split(".")
        _remote_version_numbers = _remote_version.split(".")
        if int(_current_version_numbers[2]) < int(_remote_version_numbers[2]):
            _update_status = "true"
        elif _current_version_numbers[2] == _remote_version_numbers[2]:
            if (int(_current_version_numbers[3].replace("dev", "")) <
                    int(_remote_version_numbers[3].replace("dev", ""))) or \
                    ("dev" in _current_version_numbers[3] and "dev" not in _remote_version_numbers[3]):
                _update_status = "true"
    return [_update_status, _current_version, _remote_version,
            urllib.request.urlopen(_update_message_url).read().decode()]


def convert_to_bool(_value: typing.Any) -> bool:
    if _value:
        _value = normalize(str(_value))
        if _value.isdigit():
            return int(_value) != 0
        else:
            _true_level = max(list(difflib.SequenceMatcher(
                None, _value, _target).ratio() for _target in ["yes", "true", "y"]))
            _false_level = max(list(difflib.SequenceMatcher(
                None, _value, _target).ratio() for _target in ["no", "false", "none", "n", "not"]))
            if _true_level == _false_level:
                return False
            else:
                return _false_level < _true_level
    else:
        return False


def read_setting(_setting_file_path: str, _setting_name: typing.Any) -> typing.Optional[str]:
    if os.path.exists(_setting_file_path) is False:
        return
    else:
        root = otfdlib.Otfd()
        root.load(_setting_file_path)
        root.parse()
        return root.get_value(_setting_name)


def write_setting(_setting_file_path: str, _setting_name: typing.Any, _setting_value: typing.Any) -> None:
    if os.path.exists(_setting_file_path) is False:
        with open(_setting_file_path, mode="w", encoding="utf-8_sig") as f:
            f.write("")
    root = otfdlib.Otfd()
    root.load(_setting_file_path)
    root.parse()
    root.add(str(_setting_name), str(_setting_value))
    root.write()
    return


def read_flag(_flag_file_path: str, _flag_name: typing.Any) -> bool:
    return convert_to_bool(read_setting(_flag_file_path, _flag_name))


def set_flag(_flag_file_path: str, _flag_name: typing.Any, _flag_value: typing.Any) -> None:
    write_setting(_flag_file_path, str(_flag_name), convert_to_bool(_flag_value))
    return


def solve_setting_conflict(_default_setting_file_path: str, _current_setting_file_path: str) -> None:
    if os.path.exists(_default_setting_file_path) is False:
        raise Exception(f"{_default_setting_file_path}にデフォルト設定ファイルがありません。")
    if os.path.exists(_current_setting_file_path) is False:
        with open(_current_setting_file_path, mode="w", encoding="utf-8_sig") as _current:
            with open(_default_setting_file_path, mode="r", encoding="utf-8_sig") as _default:
                _current.write(_default.read())
                return
    else:
        default_setting = otfdlib.Otfd()
        default_setting.load(_default_setting_file_path)
        default_setting.parse()
        _default_index_list = default_setting.get_index_list()
        current_setting = otfdlib.Otfd()
        current_setting.load(_current_setting_file_path)
        current_setting.parse()
        _current_index_list = current_setting.get_index_list()
        _need_to_add = list(set(_default_index_list) - set(_current_index_list))
        current_setting.update({_index: default_setting.get_value(_index) for _index in _need_to_add})
        _need_to_delete = list(set(_current_index_list) - set(_default_index_list))
        for _index in _need_to_delete:
            current_setting.pop(_index)
        default_setting.sorted()
        current_setting.sorted()
        default_setting.write()
        current_setting.write()
        return


def generate_search_engine_url(search_engine: str = "google", keyword: str = None, define: bool = False) -> str:
    if keyword:
        keyword = urllib.parse.quote(keyword)
    if define:
        return search_engine + keyword
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
            similarity = {
                intelligent_match(engine_name, search_engine):
                    engine_name for engine_name in search_engine_url_table.keys()
            }
            search_engine = similarity[max(similarity.keys())]
        if keyword:
            return search_engine_url_table[search_engine] + keyword
        else:
            url = search_engine_url_table[search_engine]
            return url[:url.rfind("/") + 1]


def intelligent_match(a: str, b: str) -> float:
    if len(a) > len(b):
        a, b = b, a
    if bool(re.search(a, b)):
        return 1.0
    else:
        a_length = len(a)
        return max(list(
            difflib.SequenceMatcher(None, target, a).ratio() for target in [
                b[num:num + a_length] for num in range(len(b) - a_length + 1)
            ]))


def showerror(_message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("ORIZIN Agent HTML　エラー", _message)
    root.destroy()
    return


def showinfo(_message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("ORIZIN Agent HTML", _message)
    root.destroy()
    return


def get_google_news(number_of_items: int = 3) -> typing.List[typing.Dict[str, str]]:
    root = ET.fromstring(urllib.request.urlopen("https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja").read().decode())
    items = root.iter("item")
    result = []
    for num in range(number_of_items):
        one_item = next(items)
        result.append({
            "title": html.unescape(next(one_item.iter("title")).text),
            "description": html.unescape(next(one_item.iter("description")).text)
        })
    return result
