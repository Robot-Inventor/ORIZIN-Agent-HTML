#!/usr/bin/env python3
# -*- coding: utf8 -*-

import eel
import oa_core as core
import random
import subprocess
import webbrowser
import os
import datetime
import re
import urllib.request
import urllib.parse
import html
import otfdlib
import hashlib
import pickle
import typing
import unicodedata
import pathlib
import argparse
from collections import OrderedDict
import inspect
import glob


@eel.expose
def change_theme(css_theme_path: str) -> None:
    css_file_path = "resource/css/layout.css"
    if os.path.exists(f"resource/css/{css_theme_path}") is False:
        with open("resource/css/theme/light_theme.css", mode="r", encoding="utf-8_sig") as light_theme_file:
            light_theme = light_theme_file.read()
        with open(f"resource/css/{css_theme_path}", mode="w", encoding="utf-8_sig") as new_theme:
            new_theme.write(light_theme)
    with open(css_file_path, mode="r", encoding="utf-8_sig") as css_file:
        old_css = css_file.read()
    new_css = f'@import url("{css_theme_path}");{old_css[old_css.find(";") + 1:]}'
    with open(css_file_path, mode="w", encoding="utf-8_sig") as css_file:
        css_file.write(new_css)
    write_setting("theme", css_theme_path)
    print_log_if_dev_mode("Change theme setting.", OrderedDict(Theme=css_theme_path))
    return


@eel.expose
def return_theme_dict() -> typing.Dict[str, str]:
    result = {}
    for file_path in glob.glob("resource/css/theme/**/*.css", recursive=True):
        with open(file_path, mode="r", encoding="utf-8_sig") as f:
            css_file = f.read()
            p = pathlib.Path(file_path)
            file_path = str(p.resolve().relative_to(f"{p.cwd()}/resource/css")).replace("\\", "/")
            result[file_path] = css_file.splitlines()[0].replace("/*", "").replace("*/", "").strip()
    return result


@eel.expose
def write_custom_css_theme(value: typing.Any) -> None:
    if len(value) == 5:
        custom_css_data = "/* カスタムテーマ */\n\n:root {\n    --bg: " + value[0] + ";\n    --card_bg: " + value[1] + ";\n    --text: " + \
                          value[2] + ";\n    --shadow: " + value[3] + ";\n    --theme_color: " + value[4] + ";\n}"
        with open("resource/css/theme/user/custom_theme.css", mode="w", encoding="utf-8_sig") as f:
            f.write(custom_css_data)
        print_log_if_dev_mode("Write custom css theme.", OrderedDict(Values=value))
        return
    else:
        core.show_error("カスタムCSSテーマに不正な値を書き込もうとしています。")
        print_log_if_dev_mode("Error happened when writing custom css theme.", OrderedDict(Status="ERROR"))
        return


@eel.expose
def check_current_css_theme_information() -> typing.List[str]:
    css_file_path = read_setting("theme")
    with open(f"resource/css/{css_file_path}", mode="r", encoding="utf-8_sig") as f:
        css = f.read()
        pattern = re.compile(r":root {.*?}", re.MULTILINE | re.DOTALL)
        value = re.sub(r"(:root {)|}|( *)|-|;", "", re.search(pattern, css).group())
        root = otfdlib.Otfd()
        root.load_from_string(value)
        root.parse()
    result = root.get_value_list()
    print_log_if_dev_mode("Check current css theme information.", OrderedDict(Information=result))
    return result


@eel.expose
def read_setting(setting_name: typing.Any) -> str:
    value = core.read_setting("resource/setting/setting.otfd", setting_name)
    print_log_if_dev_mode("Read setting.", OrderedDict(SettingName=setting_name, SettingValue=value))
    return value


@eel.expose
def write_setting(setting_name: typing.Any, setting_value: typing.Any) -> None:
    print_log_if_dev_mode("Write setting.", OrderedDict(SettingName=setting_name, SettingValue=setting_value))
    core.write_setting("resource/setting/setting.otfd", setting_name, setting_value)
    return


@eel.expose
def read_flag(flag_name: typing.Any) -> bool:
    value = core.read_flag("resource/setting/flag.otfd", flag_name)
    print_log_if_dev_mode("Read flag.", OrderedDict(FlagName=flag_name, FlagValue=value))
    return value


@eel.expose
def set_flag(flag_name: typing.Any, flag_value: typing.Any) -> None:
    core.set_flag("resource/setting/flag.otfd", flag_name, flag_value)
    print_log_if_dev_mode("Set flag.", OrderedDict(FlagName=flag_name, FlagValue=flag_value))
    return


@eel.expose
def reset_setting() -> None:
    with open("resource/setting/default_setting.otfd", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/setting.otfd", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    write_setting("setup_finished", "True")
    change_theme("theme/auto_theme.css")
    print_log_if_dev_mode("Reset settings.", OrderedDict(Status="OK"))
    return


@eel.expose
def reset_flag() -> None:
    with open("resource/setting/default_flag.otfd", encoding="utf-8_sig") as f:
        default_setting = f.read()
    with open("resource/setting/flag.otfd", mode="w", encoding="utf-8_sig") as f:
        f.write(default_setting)
    print_log_if_dev_mode("Reset flag.", OrderedDict(Status="OK"))
    return


def add_chat(content: str) -> None:
    if IS_CUI_MODE:
        print()
        print(content)
        return
    else:
        eel.add_chat(content)
        print_log_if_dev_mode("Add chat at index.html by Python.", OrderedDict(Content=content))
        return


def start_speak(content: str) -> None:
    if IS_CUI_MODE:
        print()
        print(content)
        return
    else:
        eel.start_speak(content, True, False)
        print_log_if_dev_mode("Start speak at index.html by Python.", OrderedDict(Content=content))
        return


@eel.expose
def print_log_if_dev_mode(description: str, log_content: OrderedDict):
    if IS_DEV_MODE:
        core.print_log(inspect.stack()[1].function, description, log_content)
    return


YOUTUBE_MUSIC_VIDEOS = {
    "(白|ハク)(日|ジツ)": ["白日", "はくじつ", "King Gnu", "キングヌー", "ony539T074w"],
    "マリーゴールド": ["マリーゴールド", "マリーゴールド", "あいみょん", "あいみょん", "0xSiBpUdW4E"],
    "(pretender)|(プリテンダー)": ["Pretender", "プリテンダー", "Official髭男dism", "おふぃしゃるひげだんでぃずむ", "TQ8WlA2GXbk"],
    "(lemon)|(レモン)": ["Lemon", "レモン", "米津玄師", "よねづけんし", "SX_ViT4Ra7k"],
    "パプリカ": ["パプリカ", "パプリカ", "米津玄師", "よねづけんし", "s582L3gujnw"],
    "(負|マ)ケナイデ": ["負けないで", "まけないで", "ZARD", "ザード", "NCPH9JUFESA"],
    "(前|ゼン)(前|ゼン)(前|ゼン)(世|セ)": ["前前前世", "ぜんぜんぜんせ", "RADWIMPS", "ラッドウィンプス", "PDSkFeMVNFs"],
    "(LOSER)|(ルーザー)": ["LOSER", "ルーザー", "米津玄師", "よねづけんし", "Dx_fKPBPYUI"],
    "(紅蓮華)|(グレンゲ)": ["紅蓮華", "ぐれんげ", "LiSA", "リサ", "CwkzK-F0Y00"],
    "(馬|ウマ)ト(鹿|シカ)": ["馬と鹿", "うまとしか", "米津玄師", "よねづけんし", "ptnYBctoexk"],
    "(間|マ)(違|チガ)イ(探|サガ)シ": ["まちがいさがし", "まちがいさがし", "菅田将暉", "すだまさき", "7940nuwCEYA"],
    "(happy|ハッピー)(birthday|バースデー)": ["HAPPY BIRTHDAY", "ハッピーバースデー", "back number", "バックナンバー", "ZIn20Rmj030"],
    "(flamingo|フラミンゴ)": ["Flamingo", "フラミンゴ", "米津玄師", "よねづけんし", "Uh6dkL1M9DM"],
    "(アイ|愛)ノ(カタチ|形)": ["アイノカタチ", "アイノカタチ", "GReeeeN", "グリーン", "ra4gQV_V1-Q"],
    "(milk|ミルク)": ["Milk", "ミルク", "WANIMA", "ワニマ", "_Qsp6N54TnU"],
    "(夜|ヨル)ニ(駆|カ)ケル": ["夜に駆ける", "よるにかける", "YOASOBI", "よあそび", "x8VYWazR5mE"],
    "(裸|ハダカ)ノ(心|ココロ)": ["裸の心", "はだかのこころ", "あいみょん", "あいみょん", "dbczJ1vQxtQ"],
    "(香|コウ)(水|スイ)": ["香水", "こうすい", "瑛人", "えいと", "9MjAJSoaoSo"],
    "(星|ホシ)(影|カゲ)ノエール": ["星影のエール", "ほしかげのえーる", "GReeeeN", "グリーン", "D5pQLK2bpns"]
}


@eel.expose
def make_response(not_normalized_query: str) -> typing.List[typing.Union[str, bool]]:
    def print_log_if_dev_mode_template():
        if IS_DEV_MODE:
            core.print_log(inspect.stack()[1].function, "Generate response.", OrderedDict(
                Query=not_normalized_query,
                NormalizedQuery=query,
                ResponseToRead=response[0],
                ResponseToDisplay=response[1],
                MatchedWord="Untracked"))
        return
    not_normalized_query = not_normalized_query.replace("\n", "").replace("\r", "")
    query = core.normalize(not_normalized_query)
    user_name = read_setting("user_name")
    if query == "":
        response = [
            "私はオープンソースのAIアシスタント、オリジンエージェントです。気軽に話しかけてくださいね。",
            "私はオープンソースのAIアシスタント、ORIZIN Agentです。気軽に話しかけてくださいね。"]
        print_log_if_dev_mode_template()
        return response
    if core.judge(query, "ジャンケン"):
        hand_shapes = ["グー", "チョキ", "パー"]
        selected_hand_shape = hand_shapes[random.randint(0, 2)]
        response = [f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。",
                    f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen([read_setting("python_interpreter"), "resource/python/easter_egg.py"])
        response = ["イースターエッグを起動します。", "イースターエッグを起動します。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, [".*ノ(面積|メンセキ|広サ|ヒロサ|大キサ|オオキサ)"]):
        area_value = core.respond(core.load_dictionary(
            "resource/dictionary/country_information_dictionary/area_dictionary.otfd"), query)
        if area_value[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
            response = ["面積を検索します。", "面積を検索します。", False]
        else:
            response = [f"{area_value[2]}の面積は{area_value[0]}です。", f"{area_value[2]}の面積は{area_value[1]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, [".*(ノ|ニアル)(首都|シュト)"]):
        capital_name = core.respond(core.load_dictionary(
            "resource/dictionary/country_information_dictionary/capital_dictionary.otfd"), query)
        if capital_name[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
            response = ["首都を検索します。", "首都を検索します。", False]
        else:
            response = [f"{capital_name[2]}の首都は{capital_name[0]}です。", f"{capital_name[2]}の首都は{capital_name[1]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, [".*(ノ|使.*?イル)(言語|ゲンゴ|言葉|コトバ|公用語|コウヨウゴ)"]):
        language = core.respond(core.load_dictionary(
            "resource/dictionary/country_information_dictionary/language_dictionary.otfd"), query)
        if language[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
            response = ["言語を検索します。", "言語を検索します。", False]
        else:
            response = [f"{language[2]}の言語は{language[0]}です。", f"{language[2]}の言語は{language[1]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, [".*(ノ|ニ.*?(イル|デル))(人口|人口|(人|ヒト)(ノ|)(数|カズ))"]):
        population = core.respond(core.load_dictionary(
            "resource/dictionary/country_information_dictionary/population_dictionary.otfd"), query)
        if population[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
            response = ["人口を検索します。", "人口を検索します。", False]
        else:
            response = [f"{population[2]}の人口は{population[0]}です。", f"{population[2]}の人口は{population[1]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, [".*(ノ|デ)(宗教|シュウキョウ|信仰|シンコウ|国教|コッキョウ)"]):
        religion = core.respond(core.load_dictionary(
            "resource/dictionary/country_information_dictionary/religion_dictionary.otfd"), query)
        if religion[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
            response = ["宗教を検索します。", "宗教を検索します。", False]
        else:
            response = [f"{religion[2]}の宗教は{religion[0]}です。", f"{religion[2]}の宗教は{religion[1]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["予定", "ヨテイ", "カレンダ", "calender", "リマイン", "remind"]):
        webbrowser.open_new("https://calendar.google.com/")
        response = ["Googleカレンダーを開きます", "Googleカレンダーを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query,
                    [
                        "マップ", "地図", "チズ", "場所", "バショ", "ドコ", "何処", "行キ方", "イキカタ",
                        "ユキカタ", "行キカタ", "イキ方", "ユキ方", "案内", "アンナイ", "道", "ミチ"
                    ]):
        webbrowser.open_new("https://google.com/maps/search/" + urllib.parse.quote(not_normalized_query))
        response = [f"Googleマップで「{not_normalized_query}」を検索します。", f"Googleマップで「{not_normalized_query}」を検索します。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["ストップウォッチ", "ストップウオッチ", "stopwatch"]):
        webbrowser.open_new("https://google.com/search?q=stopwatch&hl=en")
        response = ["ストップウォッチを表示します。", "ストップウォッチを表示します。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(計|ケイ)(算|サン)", "(電|デン)(卓|タク)"]):
        webbrowser.open_new(core.generate_search_engine_url("google", "電卓"))
        response = ["電卓を開きます。", "電卓を開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["タイマ", "(砂|スナ)(時|ト|ド)(計|ケイ)"]) and \
            core.judge(query, ["(設|セッ)(定|テイ)", "セット", "(鳴|ナ)ラ", "(掛|カ)ケ"]):
        time = set_intelligent_timer(query)
        response = [f"{time}後にタイマーを設定しました。スタートボタンを押して下さい。タイマーアプリを閉じるとタイマーは破棄されます。また、画面を最小化すると音が鳴りません。ご注意下さい。",
                    f"{time}後にタイマーを設定しました。スタートボタンを押して下さい。タイマーアプリを閉じるとタイマーは破棄されます。また、画面を最小化すると音が鳴りません。ご注意下さい。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query,
                    ["(時|ジ)(刻|間|カン|コク)", "(時|ト)(計|ケイ)", "(何|ナン)(時|ジ|日|ニチ)", "(日|ヒ)(付|ヅケ|ズケ|ニチ)"]):
        time = datetime.datetime.now()
        time = time.strftime('%Y年%m月%d日 %H:%M:%S')
        response = [f"現在は{time}です。", f"現在は{time}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["twitter", "ツイッタ", "tweet", "ツイート"]):
        if core.judge(unicodedata.normalize("NFKC", not_normalized_query.replace(" ", "").lower()), [
            "(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(|(|内容|ないよう)([でをの]))"
            "(twitter|tweet|ツイッター|ツイート)(|を|で|に)(|(お願い|おねがい)(|する|します|です)|(頼|たの(む|みます)))"
            "((|投稿|とうこう|アップ|tweet|ツイート|送信|そうしん)((てお|と|て)"
            "(いて|け|ろ|ください|下さい)|し(て(|下さい|ください)|てお"
            "(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))(|よ|や)|ろ|)|)|)(|。|.)$"
        ]):
            tweet_content = html.escape(re.sub("(| )(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(|(|内容|ないよう)([でをの]))"
                                               "(| )([tT]witter|[tT]weet|ツイッター|ツイート)(| )(|を|で|に)(|(お願い|おねがい)"
                                               "(|する|します|です)|(頼|たの(む|みます)))((|投稿|とうこう|アップ|[tT]weet|ツイート|送信|そうしん)"
                                               "((てお|と|て)(いて|け|ろ|ください|下さい)|し(て(|下さい|ください)|てお"
                                               "(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))(|よ|や)|ろ|)|)|)(|。|.)$",
                                               "", not_normalized_query))
            webbrowser.open_new(f"https://twitter.com/intent/tweet?text={tweet_content}")
            response = [
                f"「{tweet_content}」という内容でTwitterの投稿画面を開きます。",
                f"「{tweet_content}」という内容でTwitterの投稿画面を開きます。",
                False]
        else:
            webbrowser.open_new("https://twitter.com/")
            response = ["Twitterを開きます。", "Twitterを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(接|セッ)(触|ショク)(確|カク)(認|ニン)アプリ", "cocoa", "ココア", "contactconfirmingapplication"]):
        webbrowser.open_new("https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/cocoa_00138.html")
        response = ["新型コロナウイルス接触確認アプリ（ココア）についての厚生労働省のページを開きます。", "新型コロナウイルス接触確認アプリ（COCOA）についての厚生労働省のページを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["コロナ", "corona", "covid19", "sarscov2", "(感|カン)(染|セン)", "(肺|ハイ)(炎|エン)"]):
        webbrowser.open_new("https://corona.go.jp/")
        response = ["内閣官房の新型コロナウイルスに関するページを表示します。", "内閣官房の新型コロナウイルスに関するページを表示します。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["facebook", "フェースブック"]):
        webbrowser.open_new("https://www.facebook.com/")
        response = ["Facebookを開きます。", "Facebookを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["テレビ", "tv", "(番|バン)(組|グミ|クミ)", "tver", "ティーバ"]):
        webbrowser.open_new("https://tver.jp/")
        response = ["ティーバーを開きます。", "TVerを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["youtube", "ユーチューブ", "ヨ(ウ|ー)ツベ"]) and\
            core.judge(query, [
                "テ(何|ナニ)", "(意|イ)(味|ミ)", "トハ", "(教|オシ)エ", "(検|ケン)(索|サク)", "(調|シラ)ベ",
                "(調|チョウ)(査|サ)", "(再|サイ)(生|セイ)", "(見|観|ミ)(セ|タイ)"
            ]):
        webbrowser.open_new(
            core.generate_search_engine_url("https://www.youtube.com/results?search_query=",
                                            not_normalized_query, True))
        response = [f"YouTubeで「{not_normalized_query}」を検索します。", f"YouTubeで「{not_normalized_query}」を検索します。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["youtube", "ユーチューブ", "ヨ(ウ|ー)ツベ"]):
        webbrowser.open_new("https://www.youtube.com/")
        response = ["YouTubeを開きます。", "YouTubeを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["instagram", "インスタ"]):
        webbrowser.open_new("https://www.instagram.com/")
        response = ["Instagramを開きます。", "Instagramを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["github", "ギットハブ"]):
        webbrowser.open_new("https://github.com/")
        response = ["GitHubを開きます。", "GitHubを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(地|ジ)(震|シン)"]):
        webbrowser.open_new("https://www.jma.go.jp/jp/quake/")
        response = ["気象庁の地震情報のページを開きます。", "気象庁の地震情報のページを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["トレンド", "trend"]):
        webbrowser.open_new("https://trends.google.com/trends/trendingsearches/daily?geo=JP")
        response = ["Googleトレンドを開きます。", "Googleトレンドを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["news", "ニュース"]):
        if read_flag("get_news_from_google_news"):
            news_data = core.get_google_news()
            str_to_read = ""
            str_to_display = ""
            for content in news_data:
                title = content["title"]
                str_to_read += title + "。"
                str_to_display += title + content["description"]
            add_chat("最新のニュースを3件、Googleニュースから取得しました。")
            response = []
            if IS_CUI_MODE:
                response = [str_to_read, str_to_read]
            if IS_CUI_MODE is False:
                start_speak("最新のニュースを3件、Googleニュースから取得しました。")
                response = [str_to_read, str_to_display]
        else:
            webbrowser.open_new(read_setting("news_site_url"))
            response = ["ニュースを開きます。", "ニュースを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(翻|ホン)(訳|ヤク)"]):
        webbrowser.open_new("https://translate.google.co.jp/?hl=ja")
        response = ["Google翻訳を開きます。", "Google翻訳を開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["メール", "mail"]):
        if core.judge(unicodedata.normalize("NFKC", not_normalized_query.replace(" ", "").lower()), [
            "(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(|(|内容|ないよう)([でをの]))"
            "((|g)mail|(|g|ジー)メール)(|を|で)(|((送|おく)(って(|(くだ|下)さい)|れ))|(お願い|おねがい)(|する|します|です)|(頼|たの(む|みます)))"
            "((|投稿|とうこう|アップ|送信|そうしん)((てお|と|て)(いて|け|ろ|ください|下さい)|し(て(|下さい|ください)|てお"
            "(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))(|よ|や)|ろ|)|)|)(|。|.)$"
        ]):
            message_content = html.escape(re.sub(
                "(| )(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(|(|内容|ないよう)([でをの]))"
                "((| )(|G|g|ジー)(メール|[mM]ail))( |)(|を|で)(|((送|おく)(って(|(くだ|下)さい)|れ))|(お願い|おねがい)"
                "(|する|します|です)|(頼|たの(む|みます)))((|投稿|とうこう|アップ|送信|そうしん)((てお|と|て)"
                "(いて|け|ろ|ください|下さい)|し(て(|下さい|ください)|てお"
                "(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))(|よ|や)|ろ|)|)|)(|。|.)$", "", not_normalized_query))
            webbrowser.open_new(f"https://mail.google.com/mail/?view=cm&body={message_content}")
            response = [f"「{message_content}」という内容でGmailの送信画面を開きます", f"「{message_content}」という内容でGmailの送信画面を開きます", False]
        else:
            webbrowser.open_new("https://mail.google.com/")
            response = ["Gmailを開きます。", "Gmailを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["ラジオ", "radio"]):
        webbrowser.open_new("http://radiko.jp/")
        response = ["radikoを開きます。", "radikoを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(写|シャ)(真|シン)", "(画|ガ)(像|ゾウ)", "フォト", "photo", "ピクチャ", "picture"]):
        webbrowser.open_new("https://photos.google.com/")
        response = ["Googleフォトを開きます。", "Googleフォトを開きます。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["メモ", "memo", "(記|キ)(憶|オク|録|ロク)"]) and \
            core.judge(query, [
                "(削|サク)(除|ジョ)", "(消|ショウ)(去|キョ)", "クリア", "clear",
                "(消|ケ)シ", "(忘|ワス)レ", "(破|ハ|放|ホウ)(棄|キ)"
            ]):
        if os.path.exists("memo.txt") is False:
            response = ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            with open("memo.txt", mode="r", newline="") as f:
                memo = f.read()
            if memo.strip() == "":
                response = ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                if core.judge(query, [r"\d+?((ツ|個|コ|番|バン)(|メ|目))"]):
                    splited_memo = memo.splitlines()
                    memo_index = int(re.search(
                        r"\d+?", (re.search(r"\d+?((ツ|個|コ|番|バン)(|メ|目))", query).group())
                    ).group())
                    if memo_index > len(splited_memo) or memo_index < 1:
                        response = ["削除するメモの番号が正しくありません。", "削除するメモの番号が正しくありません。"]
                    else:
                        splited_memo.pop(memo_index - 1)
                        with open("memo.txt", mode="w", newline="") as f:
                            f.write("\n".join(splited_memo))
                        response = [f"{memo_index}つ目のメモを削除しました。", f"{memo_index}つ目のメモを削除しました。"]
                else:
                    with open("memo.txt", mode="w", newline="") as f:
                        f.write("")
                    response = ["覚えているメモをすべて消去しました。", "覚えているメモをすべて消去しました。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["メモ", "memo", "何", "ナニ", "(内|ナイ)(容|ヨウ)"]) and \
            core.judge(query, [
                "(覚|オボ)エテ(イ|)ル", "(記|キ)(憶|オク|録|ロク)", "(教|オシ)エ", "(読|ヨ)(メ|ミ|ン)"
            ]):
        if os.path.exists("memo.txt") is False:
            response = ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            with open("memo.txt", mode="r", newline="") as f:
                memo = f.read()
            if memo.strip() == "":
                response = ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                memo_list = memo.strip().split("\n")
                memo_list = [f"{num + 1}つ目は、「{memo_list[num]}」です。" for num in range(len(memo_list))]
                memo_content_to_read = "".join(memo_list)
                response = [f"覚えているメモを読み上げます。{memo_content_to_read}以上が、覚えているメモです。",
                            f"覚えているメモを読み上げます。{memo_content_to_read}以上が、覚えているメモです。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["メモ", "memo", "(覚|オボ)エ", "(記|キ)(憶|オク|録|ロク)"]):
        if os.path.exists("memo.txt") is False:
            pathlib.Path("memo.txt").touch()
        memo_content = re.sub(
            "(| )(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(|(|内容|ないよう)([でをの]))(メモ|memo|めも|記憶|きおく|記録|きろく)"
            "(|を|で)(|(お願い|おねがい)(|する|します|です)|(頼|たの(む|みます)))((覚え|おぼえ|残し|のこし)(てお|と|て)(いて|け|ろ|ください|下さい)|し"
            "(て(|下さい|ください)|てお(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))(|よ|や)|ろ|)|)(|。|.)$",
            "", not_normalized_query)
        with open("memo.txt", mode="a", newline="") as f:
            f.write(f"{memo_content}\n")
        if memo_content == "":
            response = ["申し訳ありません。処理に失敗しました。別の言い方をお試し下さい。", "申し訳ありません。処理に失敗しました。別の言い方をお試し下さい。"]
        else:
            response = [f"「{memo_content}」とメモしました。", f"「{memo_content}」とメモしました。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(何|ナニ|ナン)ノ[日ヒ]"]):
        now = datetime.datetime.now()
        day_point = "今日"
        if core.judge(query, ["一昨[々昨]日", "サキオトトイ"]):
            now -= datetime.timedelta(days=3)
            day_point = "一昨々日"
        elif core.judge(query, ["一昨日", "オトトイ"]):
            now -= datetime.timedelta(days=2)
            day_point = "一昨日"
        elif core.judge(query, ["(昨|サク)(日|ジツ)", "キノウ"]):
            now -= datetime.timedelta(days=1)
            day_point = "昨日"
        elif core.judge(query, ["明日", "アス", "アシタ"]):
            now += datetime.timedelta(days=1)
            day_point = "明日"
        elif core.judge(query, ["明後日", "アサッテ"]):
            now += datetime.timedelta(days=2)
            day_point = "明後日"
        elif core.judge(query, ["明[々明]後日", "シアサッテ"]):
            now += datetime.timedelta(days=3)
            day_point = "明々後日"
        webbrowser.open_new(f"https://ja.wikipedia.org/wiki/Wikipedia:今日は何の日_{now.month}月#{now.month}月{now.day}日")
        response = [f"Wikipediaの「今日は何の日」の{day_point}のページを開きます。", f"Wikipediaの「今日は何の日」の{day_point}のページを開きます。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["トリビア", "trivia", "(豆|マメ)(知|チ)(識|シキ)"]):
        with open("resource/dictionary/trivia_dictionary.txt", encoding="utf-8_sig") as trivia_file:
            trivias = trivia_file.read().splitlines()
            chosen_trivia = trivias[random.randint(0, len(trivias) - 1)]
            chosen_trivia = otfdlib.Otfd().unescape(chosen_trivia.split("/"))
            if len(chosen_trivia) == 1:
                chosen_trivia = [chosen_trivia[0], chosen_trivia[0]]
            response = [f"{user_name}さん、知っていましたか？{chosen_trivia[0]}", f"{user_name}さん、知っていましたか？{chosen_trivia[1]}"]
            print_log_if_dev_mode_template()
            return response
    elif core.judge(query, ["テ(何|ナニ)", "(意|イ)(味|ミ)", "トハ", "(教|オシ)エ", "(検|ケン)(索|サク)", "(調|シラ)ベ", "(調|チョウ)(査|サ)"]):
        search_engine = read_setting("search_engine")
        webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), not_normalized_query))
        response = [f"{search_engine}で「{not_normalized_query}」を検索します。",
                    f"{search_engine}で「{not_normalized_query}」を検索します。", False]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["サイコロ", "ダイス", "dice"]):
        max_number = 6
        if core.judge(query, [r"\d(面|メン)"]):
            max_number = re.sub("(面|メン)", "", re.search(r"\d*(面|メン)", query).group())
        if int(max_number) <= 0:
            max_number = 6
        dice_result = random.randint(1, int(max_number))
        max_number_message = ""
        if max_number != 6:
            max_number_message = f"{max_number}面"
        response = [f"{max_number_message}サイコロを振りますね。{dice_result}が出ました。",
                    f"{max_number_message}サイコロを振りますね。{dice_result}が出ました。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["コイン", "coin"]) and core.judge(query, ["トス", "toss", "(投|ナ)ゲ"]):
        coin = ["表", "裏"]
        result = coin[random.randint(0, 1)]
        response = [f"コイントスをしますね。{result}が出ました。", f"コイントスをしますね。{result}が出ました。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["(御|神|ミ)(籤|クジ)"]):
        fortune_repertoire = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
        result = fortune_repertoire[random.randint(0, len(fortune_repertoire) - 1)]
        response = [f"おみくじをします。ガラガラ...。結果は・・・{result}です。", f"おみくじをします。ガラガラ...。結果は・・・{result}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, list(YOUTUBE_MUSIC_VIDEOS.keys())):
        music_data = YOUTUBE_MUSIC_VIDEOS[core.judge(query, list(YOUTUBE_MUSIC_VIDEOS.keys()), True)[1]]
        if IS_CUI_MODE is False:
            eel.add_chat(music_data[4], False, True)
        response = [f"{music_data[3]}の{music_data[1]}です。", f"{music_data[2]}の{music_data[0]}です。"]
        print_log_if_dev_mode_template()
        return response
    elif core.judge(query, ["blackouttuesday", "ブラックアウトチューズデー", "blacklivesmatter", "ブラックリブズマター", "blm"]):
        eel.blm()
        response = ["人種差別に反対します。", "人種差別に反対します。"]
        print_log_if_dev_mode_template()
        return response
    else:
        if read_flag("use_fast_response_mode"):
            response = core.respond_fast(dictionary, query)
        else:
            response = core.respond(dictionary, query)
        response_to_read = response[0].format(user_name=user_name)
        response_to_display = response[1].format(user_name=user_name)
        if response_to_read == response_to_display == "そうですか。":
            for file_path in glob.glob("resource/dictionary/inappropriate_words_ja_dictionary/*.txt"):
                with open(file_path, mode="r", encoding="utf-8") as f:
                    content = f.read().splitlines()
            for word in content:
                if word in query:
                    response = [
                        "不適切な可能性がある単語を検出しました。別の表現を試してみてください。",
                        "不適切な可能性がある単語を検出しました。別の表現を試してみてください。"
                    ]
                    print_log_if_dev_mode_template()
                    return response
        else:
            if IS_DEV_MODE:
                print_log_if_dev_mode("Generate response.", OrderedDict(
                    Query=not_normalized_query,
                    NormalizedQuery=query,
                    ResponseToRead=response_to_read,
                    ResponseToDisplay=response_to_display,
                    MatchedWord=response[2]
                ))
            return [response_to_read, response_to_display]


def set_intelligent_timer(query: str) -> str:
    hours = minutes = seconds = 0
    query = re.sub(r"ジカン|hour", "時間", query)
    query = re.sub(r"フン|プン|minute", "分", query)
    query = re.sub(r"ビョウ|second", "秒", query)
    query = query.replace("半", "30")
    if '時間' in query:
        hours = int(re.search(r'\d*', re.search(r'\d*時間', query).group()).group())
    if '分' in query:
        minutes = int(re.search(r'\d*', re.search(r'\d*分', query).group()).group())
    if '秒' in query:
        seconds = int(re.search(r'\d*', re.search(r'\d*秒', query).group()).group())
    time = ""
    if hours:
        time = f"{hours}時間"
    if minutes:
        time += f"{minutes}分"
    if seconds:
        time += f"{seconds}秒"
    if not time:
        time = "0秒"
    subprocess.Popen(f"{read_setting('python_interpreter')} timer.py {hours} {minutes} {seconds}")
    print_log_if_dev_mode("Start timer app.", OrderedDict(Hours=hours, Minutes=minutes, Seconds=seconds))
    return time


IS_DEV_MODE = False
IS_CUI_MODE = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="オープンソースの会話を目的としたAIアシスタント「ORIZIN Agent HTML」です。")
    parser.add_argument("-D", "--dev_mode", action="store_true", help="enable development mode")
    parser.add_argument("-C", "--cui_mode", action="store_true", help="enable CUI mode")
    args = parser.parse_args()
    IS_DEV_MODE = args.dev_mode
    IS_CUI_MODE = args.cui_mode
    print_log_if_dev_mode("Program start.", OrderedDict(Status="OK"))
    with open("resource/dictionary/dictionary.otfd", mode="r", encoding="utf-8_sig") as dict_file:
        dict_hash = hashlib.sha256(dict_file.read().encode()).hexdigest()
        print_log_if_dev_mode("Calculate dictionary hash.", OrderedDict(Hash=dict_hash))
    if os.path.exists("resource/dictionary/dictionary_hash.txt"):
        with open("resource/dictionary/dictionary_hash.txt", mode="r", encoding="utf-8_sig") as hash_file:
            hash_value = hash_file.read()
            print_log_if_dev_mode("Read cached dictionary hash.", OrderedDict(Hash=hash_value))
    else:
        with open("resource/dictionary/dictionary_hash.txt", mode="w", encoding="utf-8_sig") as hash_file:
            hash_file.write(dict_hash)
            hash_value = 0
            print_log_if_dev_mode("Cache dictionary hash.", OrderedDict(Hash=dict_hash))
    if os.path.exists("resource/dictionary/dictionary.bin"):
        if hash_value == dict_hash:
            with open("resource/dictionary/dictionary.bin", mode="rb") as dict_bin_file:
                dictionary = pickle.load(dict_bin_file)
                print_log_if_dev_mode("Read cached dictionary.", OrderedDict(Status="OK"))
        else:
            with open("resource/dictionary/dictionary_hash.txt", mode="w", encoding="utf-8_sig") as hash_file:
                hash_file.write(dict_hash)
            dictionary = core.load_dictionary("resource/dictionary/dictionary.otfd")
            print_log_if_dev_mode("Read and parse dictionary.", OrderedDict(Status="OK"))
            with open("resource/dictionary/dictionary.bin", mode="wb") as dict_bin_file:
                pickle.dump(dictionary, dict_bin_file)
            print_log_if_dev_mode("Update cached dictionary.", OrderedDict(Status="OK"))
    else:
        dictionary = core.load_dictionary("resource/dictionary/dictionary.otfd")
        with open("resource/dictionary/dictionary.bin", mode="wb") as dict_bin_file:
            pickle.dump(dictionary, dict_bin_file)
        print_log_if_dev_mode("Create cache dictionary.", OrderedDict(Status="OK"))
    if os.path.exists("resource/setting/setting.otfd") is False:
        change_theme("theme/auto_theme.css")
        print_log_if_dev_mode("Reset theme setting.", OrderedDict(ResetedTheme="theme/auto_theme.css"))
    core.solve_setting_conflict("resource/setting/default_setting.otfd", "resource/setting/setting.otfd")
    core.solve_setting_conflict("resource/setting/default_flag.otfd", "resource/setting/flag.otfd")
    print_log_if_dev_mode("Solve setting conflict.", OrderedDict(Status="OK"))
    if IS_CUI_MODE:
        print("\nProgram started. Please input query.\n")
        while True:
            print(">>>>>", end="")
            print("\n" + make_response(input())[1] + "\n")
    else:
        eel.init("resource")
        if read_flag("fast_start"):
            eel.start("/html/index.html")
        else:
            eel.start("/html/splash.html")
