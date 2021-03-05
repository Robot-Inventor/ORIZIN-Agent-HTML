#!/usr/bin/env python3

import os
import glob
import pathlib
import oa_core as core
import re
import otfdlib
from collections import OrderedDict


def change(css_theme_path: str) -> None:
    if os.path.exists(f"resource/css/{css_theme_path}") is False:
        with open("resource/css/theme/light_theme.css", mode="r", encoding="utf-8_sig") as light_theme_file:
            light_theme = light_theme_file.read()
        with open(f"resource/css/{css_theme_path}", mode="w", encoding="utf-8_sig") as new_theme:
            new_theme.write(light_theme)
    with open("resource/css/theme_setting.css", mode="w", encoding="utf-8_sig") as css_file:
        css_file.write(f"@import url('{css_theme_path}');")
    core.write_setting("resource/setting/setting.otfd",
                       "theme", css_theme_path)
    return


def return_dict() -> dict[str, str]:
    result = {}
    for file_path in glob.glob("resource/css/theme/**/*.css", recursive=True):
        with open(file_path, mode="r", encoding="utf-8_sig") as f:
            css_file = f.read()
            p = pathlib.Path(file_path)
            file_path = str(p.resolve().relative_to(
                f"{p.cwd()}/resource/css")).replace("\\", "/")
            result[file_path] = css_file.splitlines()[0].replace(
                "/*", "").replace("*/", "").strip()
    return result


def write_custom(theme_dictionary: dict[str, str]) -> None:
    value = ""
    for key in theme_dictionary:
        value += f"    {key}: {theme_dictionary[key]};\n"
    content = "/* カスタムテーマ */\n\n:root {\n" + value + "}"
    with open("resource/css/theme/user/custom_theme.css", mode="w", encoding="utf-8_sig") as f:
        f.write(content)
    return


def current() -> OrderedDict:
    css_file_path = core.read_setting("resource/setting/setting.otfd", "theme")
    with open(f"resource/css/{css_file_path}", mode="r", encoding="utf-8_sig") as f:
        css = f.read()
        pattern = re.compile(r"( *?--.*?:.*?;(\n|))+",
                             re.MULTILINE | re.DOTALL)
        value = re.search(pattern, css).group()
        delete_space_pattern = re.compile(r"^ *", re.MULTILINE | re.DOTALL)
        value = re.sub(delete_space_pattern, "", value)
        delete_semicolon_pattern = re.compile(r";$", re.MULTILINE | re.DOTALL)
        value = re.sub(delete_semicolon_pattern, "", value)
        value = re.sub(r" *: *", ":", value)
        root = otfdlib.Otfd()
        root.load_from_string(value)
        root.parse()
    result = root.read()
    return result
