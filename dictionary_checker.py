#!/usr/bin/env python
# -*- coding: utf8 -*-


import otfdlib
import glob
import itertools


if __name__ == "__main__":
    errors = []
    for file in glob.glob("resource/dictionary/**/*.otfd", recursive=True):
        with open(file, mode="r", encoding="utf-8_sig") as f:
            content = f.read()
            invalid_syntax = ["\n/", "//", "/:", "\n:", ":/", "/\n"]
            for syntax in invalid_syntax:
                if syntax in content:
                    errors.append(f"\033[31mINVALID SYNTAX: In {file}, '{syntax}' was found.\033[0m")
        root = otfdlib.Otfd()
        root.load(file)
        root.parse()
        indexes = root.get_index_list()
        indexes = list(itertools.chain.from_iterable([index.split("/") for index in indexes]))
        for index in indexes:
            indexes.pop(0)
            if indexes.count(index) >= 2:
                errors.append(f"\033[31mINVALID SYNTAX: In {file}, '{index}' was duplicated.\033[0m")
        print(f"{file} was checked!")
    print("All files were checked!")
    if errors:
        print(f"{len(errors)} errors were found.")
        print("\n".join(errors))
    else:
        print("There were no errors.")
