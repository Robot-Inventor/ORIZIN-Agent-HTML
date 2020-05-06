#!/usr/bin/env python3
# -*- coding: utf8 -*-


import otfdlib
import glob
import itertools
import difflib
from oa_core import normalize


def return_words_setting(string, array):
    result = []
    for word in array:
        if string in word:
            result += word
    return result


if __name__ == "__main__":
    errors = []
    with open("dictionary_checker_ignore_files.txt", mode="r", encoding="utf-8_sig") as f:
        ignore_file_list = f.read().splitlines()
    with open("dictionary_checker_words_setting.txt", mode="r", encoding="utf-8_sig") as f:
        words_setting = f.read().splitlines()
        different_words = [word.split("!=") for word in [word for word in words_setting if "!=" in word]]
    for file in glob.glob("resource/dictionary/**/*.otfd", recursive=True):
        if file.replace("\\", "/") in ignore_file_list:
            continue
        print(f"{file}　を検証中...", end="")
        with open(file, mode="r", encoding="utf-8_sig") as f:
            content = f.read()
            invalid_syntax = ["\n/", "//", "/:", "\n:", ":/", "/\n"]
            for syntax in invalid_syntax:
                if syntax in content:
                    errors.append(f"{file}　内に'{syntax}'が見つかりました。")
        root = otfdlib.Otfd()
        root.load(file)
        root.parse()
        indexes = root.get_index_list()
        indexes = [index.split("/") for index in indexes]
        for num in range(len(indexes)):
            if type(indexes[num]) == str:
                indexes[num] = [indexes[num]]
        for index in indexes:
            for index2 in list(reversed(index))[:]:
                index.remove(index2)
                for index3 in index:
                    if index2 in index3 and index2 != "":
                        errors.append(f"{file}　の「{index2}」は「{index3}」に含まれています。")
        indexes = root.get_index_list()
        indexes = list(itertools.chain.from_iterable([index.split("/") for index in indexes]))
        for index in indexes[:]:
            indexes.remove(index)
            if index != normalize(index):
                errors.append(f"{file}　の「{index}」は正規化によって「{normalize(index)}」になるため無効です。")
            if index in indexes:
                errors.append(f"{file}　の「{index}」が重複しています。")
            for index2 in indexes:
                if index not in return_words_setting(index2, different_words) and \
                        difflib.SequenceMatcher(None, index2, index).ratio() >= 0.9:
                    errors.append(
                        f"{file}の「{index}」は「{index2}」と似ています。"
                        "正規化を検討するかdictionary_checker_words_setting.txtに追記して下さい。"
                    )
                if index in index2 and index != index2 and index != "":
                    errors.append(f"{file}　の「{index}」は「{index2}」に含まれています。")
        print("完了")
    print("すべてのファイルの検証が完了しました。")
    if errors:
        print(f"{len(errors)}個のエラーが見つかりました。")
        print("\n".join(errors))
    else:
        print("エラーは見つかりませんでした。")
