#!/usr/bin/env python3

from collections import OrderedDict
import typing


class Otfd:
    def __init__(self):
        self.otfd_file_path = ""
        self.otfd_content = ""
        self.index_list = []
        self.parsed_otfd = OrderedDict()

    def load(self, otfd_file_path: str) -> str:
        self.otfd_file_path = otfd_file_path
        with open(otfd_file_path, mode="r", newline="", encoding="utf-8_sig") as f:
            self.otfd_content = f.read()
        return self.otfd_content
    
    def load_from_string(self, otfd_string: str) -> str:
        self.otfd_content = otfd_string
        return self.otfd_content
    
    def load_from_dictionary(self, otfd_dict: typing.Union[dict, OrderedDict]) -> typing.Union[dict, OrderedDict]:
        self.parsed_otfd = otfd_dict
        self.otfd_content = self.to_string()
        return self.parsed_otfd
    
    str_or_list_that_contains_str = typing.TypeVar("str_or_list_that_contains_str", str, list)

    @staticmethod
    def unescape(target: str_or_list_that_contains_str) -> str_or_list_that_contains_str:
        if type(target) is str:
            result = target.replace("&#47", ":").replace("&#58", "/")
        elif type(target) is list:
            result = [str(string).replace("&#47", ":").replace("&#58", "/") for string in target]
        else:
            result = str(target)
        return result
    
    @staticmethod
    def escape(target: str_or_list_that_contains_str) -> str_or_list_that_contains_str:
        if type(target) is str:
            result = target.replace(":", "&#47").replace("/", "&#58")
        elif type(target) is list:
            result = [string.replace(":", "&#47").replace("/", "&#58") for string in target]
        else:
            result = str(target)
        return result
    
    def parse(self) -> OrderedDict:
        self.otfd_content = self.otfd_content.strip()
        splited_with_line = self.otfd_content.splitlines()
        error_place = [
            splited_with_line[num] for num in range(len(splited_with_line)) if splited_with_line[num].count(":") != 1
        ]
        if error_place:
            raise Exception("otfdファイル内の:の数と改行の数が合いません。不正な値です。問題のある個所->\n" + "\n".join(error_place))
        self.parsed_otfd = OrderedDict([line.split(":") for line in splited_with_line])
        return self.parsed_otfd

    def get_index_list(self) -> list[str]:
        self.index_list = list(self.parsed_otfd.keys())
        return self.index_list
    
    def get_value_list(self, unescape: bool = True) -> list[str]:
        return self.unescape(list(self.parsed_otfd.values())) if unescape else list(self.parsed_otfd.values())

    def get_value(self, index: str, unescape: bool = True) -> str:
        return self.unescape(self.parsed_otfd.get(index)) if unescape else self.parsed_otfd.get(index)

    def add(self, index: str, value: typing.Any) -> OrderedDict:
        self.parsed_otfd[self.escape(index)] = self.escape(value)
        return self.parsed_otfd
    
    def update(self, otfd: typing.Union[dict, OrderedDict]) -> None:
        otfd = {index: self.escape(otfd[index]) for index in otfd.keys()}
        return self.parsed_otfd.update(otfd)
    
    def read(self) -> OrderedDict:
        return self.parsed_otfd
    
    def read_list(self) -> list[list]:
        item = list(self.parsed_otfd.items())
        return [list(item[num]) for num in range(len(item))]
    
    def pop(self, index: str) -> str:
        return self.parsed_otfd.pop(index)
    
    def sort(self) -> OrderedDict:
        copy = self.parsed_otfd.items()
        return OrderedDict(sorted(copy))
    
    def sort_list(self) -> list:
        return list(self.sort())
    
    def sorted(self) -> OrderedDict:
        self.parsed_otfd = OrderedDict(sorted(self.parsed_otfd.items()))
        return self.parsed_otfd
    
    def to_string(self) -> str:
        data_in_list = self.read_list()
        data_in_list = [":".join(data_in_list[num]) for num in range(len(data_in_list))]
        return "\n".join(data_in_list)
    
    def write(self, file_path: str = None) -> None:
        if file_path is None:
            file_path = self.otfd_file_path
        with open(file_path, mode="r", newline="", encoding="utf-8_sig") as f:
            old_file = f.read()
        escaped_string = self.to_string()
        if old_file != escaped_string:
            with open(file_path, mode="w", newline="", encoding="utf-8_sig") as f:
                f.write(escaped_string)
        return
