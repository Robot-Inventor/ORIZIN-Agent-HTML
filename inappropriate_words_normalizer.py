#!/usr/bin/env python3
# -*- coding: utf8 -*-


import oa_core
import glob


if __name__ == "__main__":
    for file_path in glob.glob("resource/dictionary/inappropriate_words_ja_dictionary/*.txt"):
        with open(file_path, mode="r", encoding="utf-8") as f:
            content = f.read()
        result = "\n".join(sorted(list(set([oa_core.normalize(word) for word in content.splitlines()]))))
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(result)
    print("Finished.")
