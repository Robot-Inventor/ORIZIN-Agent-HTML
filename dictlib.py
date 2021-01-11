#!/usr/bin/env python3

import pickle
import hashlib
import os
import typing
import oa_core as core
from collections import OrderedDict


def load(file_path: str) -> OrderedDict:
    FILE_PATH_WITHOUT_EXTENSION = os.path.join(os.path.dirname(
        file_path), os.path.splitext(os.path.basename(file_path))[0])
    HASH_FILE_PATH = FILE_PATH_WITHOUT_EXTENSION + "_hash.txt"
    BINARY_FILE_PATH = FILE_PATH_WITHOUT_EXTENSION + ".bin"

    dict_hash = _calc_hash(_read_text(file_path).encode())

    if os.path.exists(HASH_FILE_PATH):
        hash_value = _read_text(HASH_FILE_PATH)
    else:
        _write_text(HASH_FILE_PATH, dict_hash)
        hash_value = 0

    if os.path.exists(BINARY_FILE_PATH):
        if hash_value == dict_hash:
            dictionary_data = _read_cache(BINARY_FILE_PATH)
        else:
            _write_text(HASH_FILE_PATH, dict_hash)
            dictionary_data = core.load_dictionary(file_path)
            _cache(dictionary_data, BINARY_FILE_PATH)
    else:
        dictionary_data = core.load_dictionary(file_path)
        _cache(dictionary_data, BINARY_FILE_PATH)

    return dictionary_data


def _cache(binary_file_path: str, object: typing.Any) -> None:
    with open(binary_file_path, mode="wb") as f:
        pickle.dump(object, f)


def _read_cache(binary_file_path: str) -> typing.Any:
    with open(binary_file_path, mode="rb") as f:
        result = pickle.load(f)
    return result


def _write_text(file_path: str, content: str) -> None:
    with open(file_path, mode="w", encoding="utf-8_sig") as f:
        f.write(content)


def _read_text(file_path: str) -> str:
    with open(file_path, mode="r", encoding="utf-8_sig") as f:
        result = f.read()
    return result


def _calc_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
