#!/usr/bin/env python3

from collections import OrderedDict
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
import pathlib
import shutil
import json


def normalize(sentence: str) -> str:
    result = normalize_with_dictionary("resource/dictionary/normalize_dictionary.otfd",
                                       convert_kanji_to_int(unicodedata.normalize("NFKC", sentence.lower()).translate(
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


def normalize_with_dictionary(file_path: str, sentence: str) -> str:
    root = otfdlib.Otfd()
    root.load(file_path)
    root.parse()
    result = sentence
    for element in root.get_index_list():
        result = re.sub(element.replace("/", "|"),
                        root.get_value(element), sentence)
    return result


def convert_kanji_to_int(string: str) -> str:
    result = string.translate(str.maketrans(
        "零〇一壱二弐三参四五六七八九拾", "00112233456789十", ""))
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
                result = result.replace(
                    unit + number, "1" + zeros[len(number):len(zeros)] + number)
            result = result.replace(unit, "1" + zeros)
    return result


def load_dictionary(path: str) -> OrderedDict:
    root = otfdlib.Otfd()
    root.load(path)
    root.parse()
    return root.read()


bool_and_str_type_var = typing.TypeVar("bool_and_str_type_var", bool, str)


def judge(query: str, dictionary: typing.Union[str, list], matched_word: bool = False) ->\
        typing.Union[bool, list[bool_and_str_type_var]]:
    if type(dictionary) == str:
        dictionary = [dictionary]
    for word in dictionary:
        if bool(re.search(word, query)):
            if matched_word:
                return [True, word]
            else:
                return True
    if matched_word:
        return [False, ""]
    else:
        return False


def judge_with_intelligent_match(input_str: str, target: list, threshold: typing.Union[int, float] = 0.75) -> bool:
    for content in target:
        if intelligent_match(input_str, content) >= threshold:
            return True
    return False


def add_unknown_question(question: str, response: typing.Union[str, list]) -> None:
    unknown_questions = otfdlib.Otfd()
    unknown_questions.load("resource/dictionary/unknownQuestions.txt")
    unknown_questions.parse()
    if type(response) == str:
        unknown_questions.add(question, response)
    else:
        unknown_questions.add(question, "/".join(response))
    unknown_questions.write()
    return


def respond(dictionary: dict, query: str) -> list[str]:
    root = otfdlib.Otfd()
    root.load_from_dictionary(dictionary)
    root.parse()
    index_list = root.get_index_list()
    most_similar_word = ""
    most_similar_value = 0
    for index in index_list:
        splited_index = root.unescape(list(index.split("/")))
        similarity = max([intelligent_match(string, query)
                          for string in splited_index])
        if similarity >= most_similar_value:
            most_similar_value = similarity
            most_similar_word = index
        judge_result = judge(query, index.split("/"), True)
        if judge_result[0]:
            response = root.get_value(index, unescape=False).split("/")
            if len(response) == 1:
                return root.unescape([response[0], response[0], judge_result[1]])
            else:
                return root.unescape([response[0], response[1], judge_result[1]])
    if os.path.exists("resource/dictionary/unknownQuestions.txt") is False:
        pathlib.Path("resource/dictionary/unknownQuestions.txt").touch()
    if most_similar_value >= 0.75:
        response = root.unescape(
            list(root.get_value(most_similar_word, unescape=False).split("/")))
    else:
        response = ["そうですか。"]
    add_unknown_question(query, response)
    if len(response) == 1:
        return root.unescape([response[0], response[0], most_similar_word])
    else:
        return root.unescape([response[0], response[1], most_similar_word])


def respond_fast(dictionary: dict, query: str) -> list[str]:
    root = otfdlib.Otfd()
    root.load_from_dictionary(dictionary)
    root.parse()
    index_list = root.get_index_list()
    for index in index_list:
        judge_result = judge(query, index.split("/"), True)
        if judge_result[0]:
            response = root.get_value(index, unescape=False).split("/")
            if len(response) == 1:
                return root.unescape([response[0], response[0], judge_result[1]])
            else:
                return root.unescape([response[0], response[1], judge_result[1]])
    if os.path.exists("resource/dictionary/unknownQuestions.txt") is False:
        pathlib.Path("resource/dictionary/unknownQuestions.txt").touch()
    add_unknown_question(query, "そうですか。")
    return ["そうですか。", "そうですか。", ""]


def convert_to_bool(value: typing.Any) -> bool:
    if value:
        value = normalize(str(value))
        if value.isdigit():
            return int(value) != 0
        else:
            true_level = max(list(difflib.SequenceMatcher(
                None, value, target).ratio() for target in ["yes", "true", "y"]))
            false_level = max(list(difflib.SequenceMatcher(
                None, value, target).ratio() for target in ["no", "false", "none", "n", "not"]))
            if true_level == false_level:
                return False
            else:
                return false_level < true_level
    else:
        return False


def read_setting(_setting_file_path: str, setting_name: str = "") -> typing.Any:
    if os.path.exists(_setting_file_path) is False:
        return
    else:
        with open(_setting_file_path, encoding="utf-8_sig", mode="r") as f:
            json_dictionary = json.load(f)
            if setting_name:
                return json_dictionary[setting_name]
            else:
                return json_dictionary


def write_setting(_setting_file_path: str, setting_name: str, setting_value: typing.Any) -> None:
    if os.path.exists(_setting_file_path) is False:
        with open(_setting_file_path, mode="w", encoding="utf-8_sig") as f:
            json.dump({}, f)
    with open(_setting_file_path, encoding="utf-8_sig", mode="r") as f:
        json_dictionary = json.load(f)
    json_dictionary[setting_name] = setting_value
    with open(_setting_file_path, encoding="utf-8_sig", mode="w") as f:
        json.dump(json_dictionary, f, indent=4)


def read_flag(_flag_file_path: str, flag_name: str) -> bool:
    return read_setting(_flag_file_path, flag_name)


def set_flag(_flag_file_path: str, flag_name: str, flag_value: bool) -> None:
    write_setting(_flag_file_path, flag_name, flag_value)
    return


def solve_setting_conflict(default_setting_file_path: str, current_setting_file_path: str) -> None:
    if os.path.exists(default_setting_file_path) is False:
        raise Exception(f"{default_setting_file_path}にデフォルト設定ファイルがありません。")
    if os.path.exists(current_setting_file_path) is False:
        with open(current_setting_file_path, mode="w", encoding="utf-8_sig") as current:
            with open(default_setting_file_path, mode="r", encoding="utf-8_sig") as default:
                current.write(default.read())
                return
    else:
        default_setting = read_setting(default_setting_file_path)
        current_setting = read_setting(current_setting_file_path)
        need_to_delete = list(
            set(current_setting.keys()) - set(default_setting.keys()))
        for index in need_to_delete:
            current_setting.pop(index)
        solved_setting = default_setting | current_setting
        with open(current_setting_file_path, encoding="utf-8_sig", mode="w") as f:
            json.dump(solved_setting, f, indent=4)


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


def show_error(message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("ORIZIN Agent HTML　エラー", message)
    root.destroy()
    return


def show_info(message: str) -> None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("ORIZIN Agent HTML", message)
    root.destroy()
    return


def get_google_news(number_of_items: int = 3) -> list[dict[str, str]]:
    root = ET.fromstring(urllib.request.urlopen(
        "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja").read().decode())
    items = root.iter("item")
    result = []
    for num in range(number_of_items):
        one_item = next(items)
        result.append({
            "title": html.unescape(next(one_item.iter("title")).text),
            "description": html.unescape(next(one_item.iter("description")).text)
        })
    return result


def print_log(function_name: str, description: str, log_content: OrderedDict):
    print()
    print(function_name + "=" *
          (shutil.get_terminal_size().columns - len(function_name)))
    print()
    print(description)
    print()
    for key in log_content.keys():
        print(f"{key}: {log_content[key]}")
    print()
    print("=" * shutil.get_terminal_size().columns)
    return
