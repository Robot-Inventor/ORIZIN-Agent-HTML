#!/usr/bin/env python
# -*- coding: utf8 -*-

import urllib.request
import os
import otfdlib
from collections import OrderedDict


def normalize(_sentence):
    return _sentence.translate(str.maketrans({" ": None, "　": None, "・": None, "_": None})).translate(str.maketrans("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")).lower()


def load_dictionary(_path):
    root = otfdlib.Otfd()
    root.load(_path)
    root.parse()
    return root.to_string()


def judge(_input, _target):
    return True in [_target[_num] in _input for _num in range(len(_target))]


def respond(_dictionary, _query):
    root = otfdlib.Otfd()
    root.load_from_string(_dictionary)
    root.parse()
    _index_list = root.get_index_list()
    for num in range(len(_index_list)):
        if judge(_query, _index_list[num].split("/")):
            _response = root.get_value(_index_list[num]).split("/")
            if len(_response) == 1:
                return [_response[0], _response[0]]
            else:
                return [_response[0], _response[1]]
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
        _f = open(_setting_file_path, mode="w")
        _f.close()
        return None
    else:
        root = otfdlib.Otfd()
        root.load(_setting_file_path)
        root.parse()
        if _setting_name in root.get_index_list():
            return root.get_value(_setting_name)
        return None


def write_setting(_setting_file_path, _setting_name, _setting_value):
    if os.path.exists(_setting_file_path) is False:
        _f = open(_setting_file_path, mode="w")
        _f.close()
    root = otfdlib.Otfd()
    root.load(_setting_file_path)
    root.parse()
    root.add(_setting_name, _setting_value)
    root.write()
    return


def read_flag(_flag_file_path, _flag_name):
    return convert_to_bool(read_setting(_flag_file_path, _flag_name))


def set_flag(_flag_file_path, _flag_name, _flag_value):
    write_setting(_flag_file_path, _flag_name, str(convert_to_bool(_flag_value)))
    return


def solve_setting_conflict(_default_setting_file_path, _current_setting_file_path):
    if os.path.exists(_default_setting_file_path) is False:
        raise Exception(_default_setting_file_path + "にデフォルト設定ファイルがありません。")
    if os.path.exists(_current_setting_file_path) is False:
        _f = open(_current_setting_file_path, mode="w")
        _f.close()
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
    map(current_setting.pop, _need_to_delete)
    default_setting.sorted()
    current_setting.sorted()
    default_setting.write()
    current_setting.write()
