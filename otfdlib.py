#!/usr/bin/env python
# -*- coding: utf8 -*-

from collections import OrderedDict


class Otfd():
    def __init__(self):
        self._otfd_file_path = ""
        self._otfd_content = ""
        self._index_list = []
        self._parsed_otfd = OrderedDict()

    def load(self, _otfd_file_path):
        self._otfd_file_path = _otfd_file_path
        with open(_otfd_file_path, mode="r", newline="", encoding="utf-8_sig") as _f:
            self._otfd_content = _f.read()
        return self._otfd_content

    def load_from_string(self, _otfd_string):
        self._otfd_content = _otfd_string
        return self._otfd_content
    
    def unescape(self, _target):
        if type(_target) is str:
            return _target.replace("&#47", ":").replace("&#58", "/")
        elif type(_target) is list:
            return list(map(lambda _string: _string.replace("&#47", ":").replace("&#58", "/"), _target))
        else:
            return _target
    
    def escape(self, _target):
        if type(_target) is str:
            return _target.replace(":", "&#47").replace("/", "&#58")
        elif type(_target) is list:
            return list(map(lambda _string: _string.replace(":", "&#47").replace("/", "&#58"), _target))
        else:
            return _target
    
    def parse(self):
        self._otfd_content = self._otfd_content.strip()
        _splited_with_line = self._otfd_content.splitlines()
        error_place = [_splited_with_line[num] for num in range(len(_splited_with_line)) if ":" not in _splited_with_line[num]]
        if error_place:
            raise Exception("otfdファイル内の:の数と改行の数が合いません。不正な値です。問題のある個所->\n" + "\n".join(error_place))
        self._parsed_otfd = OrderedDict([_line.split(":") for _line in _splited_with_line])
        return self._parsed_otfd

    def get_index_list(self):
        self._index_list = list(self._parsed_otfd.keys())
        return self._index_list
    
    def get_value_list(self, unescaping=True):
        if unescaping:
            return self.unescape(list(self._parsed_otfd.values()))
        else:
            return list(self._parsed_otfd.values())

    def get_value(self, _index):
        return self._parsed_otfd[_index]

    def add(self, _index, _value):
        self._parsed_otfd[_index] = _value
        return self._parsed_otfd
    
    def update(self, _otfd):
        return self._parsed_otfd.update(_otfd)
    
    def read(self):
        return self._parsed_otfd
    
    def read_list(self):
        _item = list(self._parsed_otfd.items())
        return [list(_item[num]) for num in range(len(_item))]
    
    def pop(self, _index):
        return self._parsed_otfd.pop(_index)
    
    def sort(self):
        _copy = self._parsed_otfd.items()
        return OrderedDict(sorted(_copy))
    
    def sort_list(self):
        return list(self.sort())
    
    def sorted(self):
        self._parsed_otfd = OrderedDict(sorted(self._parsed_otfd.items()))
        return self._parsed_otfd
    
    def to_string(self):
        _list = self.read_list()
        # _list = list(map(lambda _escape_target: self.escape(_escape_target), _list))
        # _list = [":".join(self.escape(_list[num])) for num in range(len(_list))]
        _list = [":".join(_list[num]) for num in range(len(_list))]
        return "\n".join(_list)
    
    def write(self, _file_path=None):
        if _file_path is None:
            _file_path = self._otfd_file_path
        _old_file = ""
        with open(_file_path, mode="r", newline="", encoding="utf-8_sig") as _f:
            _old_file = _f.read()
        _escaped_string = self.to_string()
        if _old_file != _escaped_string:
            with open(_file_path, mode="w", newline="", encoding="utf-8_sig") as _f:
                _f.write(_escaped_string)
        return
