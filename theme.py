#!/usr/bin/env python3

import os
import glob
import pathlib
import oa_core as core
import re
import otfdlib


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


def write_custom(value: list[str]) -> None:
    if len(value) == 5:
        custom_css_data = "/* カスタムテーマ */\n\n:root {\n    --bg: " + value[0] + ";\n    --card_bg: " + value[1] + ";\n    --text: " + \
                          value[2] + ";\n    --shadow: " + value[3] + \
            ";\n    --theme_color: " + value[4] + ";\n    --header_background_color: " + \
            value[5] + ";\n    --error_text_color: " + value[6] + ";\n}"
        with open("resource/css/theme/user/custom_theme.css", mode="w", encoding="utf-8_sig") as f:
            f.write(custom_css_data)
        return
    else:
        core.show_error("カスタムCSSテーマに不正な値を書き込もうとしています。")
        return


def current() -> list[str]:
    css_file_path = core.read_setting("resource/setting/setting.otfd", "theme")
    with open(f"resource/css/{css_file_path}", mode="r", encoding="utf-8_sig") as f:
        css = f.read()
        pattern = re.compile(r":root {.*?}", re.MULTILINE | re.DOTALL)
        value = re.sub(r"(:root {)|}|( *)|-|;", "",
                       re.search(pattern, css).group())
        root = otfdlib.Otfd()
        root.load_from_string(value)
        root.parse()
    result = root.get_value_list()
    return result
