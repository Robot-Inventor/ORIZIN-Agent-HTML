#!/usr/bin/env python3
# -*- coding: utf8 -*-


import otfdlib
import glob
import itertools
import difflib
from oa_core import normalize
from multiprocessing import Pool


different_words = []
errors = []


def return_words_setting(string: str, array: list) -> list:
    result = []
    for word in array:
        if string in word:
            result += word
    return result


def check(file_path: str) -> None:
    print(f"{file_path}　を検証中...", end="")
    result = []
    with open(file_path, mode="r", encoding="utf-8_sig") as f:
        content = f.read()
        invalid_syntax = ["\n/", "//", "/:", "\n:", ":/", "/\n", ":\n"]
        for syntax in invalid_syntax:
            if syntax in content:
                result.append(f"{file_path}　内に「{syntax}」が見つかりました。")
    root = otfdlib.Otfd()
    root.load(file_path)
    root.parse()
    for index in [index.split("/") for index in root.get_index_list()]:
        for index2 in list(reversed(index))[:]:
            index.pop(-1)
            for index3 in index:
                if index2 in index3 and index2 != "":
                    errors.append(
                        f"{file_path}　の「{index2}」は「{index3}」に含まれています。")
    indexes = list(itertools.chain.from_iterable(
        [index.split("/") for index in root.get_index_list()]))
    for index in indexes[:]:
        indexes.remove(index)
        if index != normalize(index):
            errors.append(
                f"{file_path}　の「{index}」は正規化によって「{normalize(index)}」になるため無効です。")
        if index in indexes:
            errors.append(f"{file_path}　の「{index}」が重複しています。")
        for index2 in indexes:
            if index not in return_words_setting(index2, different_words) and \
                    difflib.SequenceMatcher(None, index2, index).ratio() >= 0.9:
                errors.append(
                    f"{file_path}の「{index}」は「{index2}」と似ています。"
                    "正規化を検討するかdictionary_checker_words_setting.txtに追記して下さい。"
                )
            if index in index2 and index != index2 and index != "":
                errors.append(f"{file_path}　の「{index}」は「{index2}」に含まれています。")
    print("完了")
    return errors.extend(result)


if __name__ == "__main__":
    with open("dictionary_checker_ignore_files.txt", mode="r", encoding="utf-8_sig") as f:
        ignore_file_list = f.read().splitlines()
    with open("dictionary_checker_words_setting.txt", mode="r", encoding="utf-8_sig") as f:
        words_setting = f.read().splitlines()
        different_words = [word.split("!=") for word in words_setting]
    file_list = [file.replace(
        "\\", "/") for file in glob.glob("resource/dictionary/**/*.otfd", recursive=True)]
    file_list = [file for file in file_list if file not in ignore_file_list]
    with Pool() as p:
        p.map(check, file_list)
    print("すべてのファイルの検証が完了しました。")
    if errors:
        print(f"{len(errors)}個のエラーが見つかりました。")
        print("\n".join(errors))
    else:
        print("エラーは見つかりませんでした。")
