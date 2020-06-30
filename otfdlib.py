#!/usr/bin/env python3
# -*- coding: utf8 -*-

from collections import OrderedDict
import typing


class Otfd:
    def __init__(self):
        self._otfd_file_path = ""
        self._otfd_content = ""
        self._index_list = []
        self._parsed_otfd = OrderedDict()

    def load(self, _otfd_file_path: str) -> str:
        self._otfd_file_path = _otfd_file_path
        with open(_otfd_file_path, mode="r", newline="", encoding="utf-8_sig") as _f:
            self._otfd_content = _f.read()
        return self._otfd_content

    def load_from_string(self, _otfd_string: str) -> str:
        self._otfd_content = _otfd_string
        return self._otfd_content
    
    @staticmethod
    def unescape(_target: typing.Union[str, list]) -> typing.Union[str, list]:
        if type(_target) is str:
            return _target.replace("&#47", ":").replace("&#58", "/")
        elif type(_target) is list:
            return [_string.replace("&#47", ":").replace("&#58", "/") for _string in _target]
        else:
            return _target
    
    @staticmethod
    def escape(_target: typing.Union[str, list]) -> typing.Union[str, list]:
        if type(_target) is str:
            return _target.replace(":", "&#47").replace("/", "&#58")
        elif type(_target) is list:
            return [_string.replace(":", "&#47").replace("/", "&#58") for _string in _target]
        else:
            return _target
    
    def parse(self) -> OrderedDict:
        self._otfd_content = self._otfd_content.strip()
        _splited_with_line = self._otfd_content.splitlines()
        error_place = [
            _splited_with_line[num] for num in range(len(_splited_with_line)) if _splited_with_line[num].count(":") != 1
        ]
        if error_place:
            raise Exception("otfdファイル内の:の数と改行の数が合いません。不正な値です。問題のある個所->\n" + "\n".join(error_place))
        self._parsed_otfd = OrderedDict([_line.split(":") for _line in _splited_with_line])
        return self._parsed_otfd

    def get_index_list(self) -> list:
        self._index_list = list(self._parsed_otfd.keys())
        return self._index_list
    
    def get_value_list(self, unescaping: bool = True) -> list:
        if unescaping:
            return self.unescape(list(self._parsed_otfd.values()))
        else:
            return list(self._parsed_otfd.values())

    def get_value(self, _index: str, unescaping: bool = True) -> str:
        if unescaping:
            return self.unescape(self._parsed_otfd.get(_index))
        else:
            return self._parsed_otfd.get(_index)

    def add(self, _index: str, _value: typing.Any) -> OrderedDict:
        self._parsed_otfd[self.escape(_index)] = self.escape(_value)
        return self._parsed_otfd
    
    def update(self, _otfd: typing.Union[dict, OrderedDict]) -> None:
        return self._parsed_otfd.update(_otfd)
    
    def read(self) -> OrderedDict:
        return self._parsed_otfd
    
    def read_list(self) -> typing.List[list]:
        _item = list(self._parsed_otfd.items())
        return [list(_item[num]) for num in range(len(_item))]
    
    def pop(self, _index: str) -> str:
        return self._parsed_otfd.pop(_index)
    
    def sort(self) -> OrderedDict:
        _copy = self._parsed_otfd.items()
        return OrderedDict(sorted(_copy))
    
    def sort_list(self) -> list:
        return list(self.sort())
    
    def sorted(self) -> OrderedDict:
        self._parsed_otfd = OrderedDict(sorted(self._parsed_otfd.items()))
        return self._parsed_otfd
    
    def to_string(self) -> str:
        _list = self.read_list()
        _list = [":".join(_list[num]) for num in range(len(_list))]
        return "\n".join(_list)
    
    def write(self, _file_path: str = None) -> None:
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
