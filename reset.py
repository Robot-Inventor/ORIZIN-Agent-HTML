#!/usr/bin/env python3

import oa_core as core
import theme


def setting(skip_setup: bool = True) -> None:
    with open("resource/setting/default_setting.json", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/setting.json", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    if skip_setup:
        core.write_setting("resource/setting/setting.json",
                           "setup_finished", True)
    theme.change("theme/auto_theme.css")
    return


def flag() -> None:
    with open("resource/setting/default_flag.json", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/flag.json", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    return


def factory_reset() -> None:
    setting(False)
    flag()
