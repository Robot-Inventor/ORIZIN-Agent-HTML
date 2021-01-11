#!/usr/bin/env python3

import oa_core as core
import theme


def setting() -> None:
    with open("resource/setting/default_setting.otfd", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/setting.otfd", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    core.write_setting("resource/setting/setting.otfd",
                       "setup_finished", "True")
    theme.change("theme/auto_theme.css")
    return


def flag() -> None:
    with open("resource/setting/default_flag.otfd", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/flag.otfd", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    return


def all() -> None:
    setting()
    flag()
