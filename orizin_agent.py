#!/usr/bin/env python
# -*- coding: utf8 -*-

import eel
import sys
import tkinter as tk
from tkinter import messagebox
import oa_core as core
import random
import subprocess
import webbrowser
import os
import otfdlib
import datetime


@eel.expose
def change_theme(_css_theme_path):
    _css_file_path = "resource/css/layout.css"
    _css_file = open(_css_file_path, mode="r")
    _old_css = _css_file.read()
    _css_file.close()
    if os.path.exists(f"resource/css/{_css_theme_path}") is False:
        _light_theme_file = open("resource/css/theme/light_theme.css", mode="r")
        _light_theme = _light_theme_file.read()
        _light_theme_file.close()
        _new_theme = open(f"resource/css/{_css_theme_path}", mode="w")
        _new_theme.write(_light_theme)
        _new_theme.close()
    _new_css = f'@import url("{_css_theme_path}");{_old_css[_old_css.find(";") + 1:]}'
    _css_file = open(_css_file_path, mode="w")
    _css_file.write(_new_css)
    _css_file.close()
    write_setting("theme", _css_theme_path)
    return


@eel.expose
def write_custom_css_theme(_value):
    if len(_value) == 5:
        _custom_css_data = ":root {\n    --bg: " + _value[0] + ";\n    --card_bg: " + _value[1] + ";\n    --text: " + _value[2] + ";\n    --shadow: " + _value[3] + ";\n    --theme_color: " + _value[4] + ";\n}"
        _f = open("resource/css/theme/custom_theme.css", mode="w")
        _f.write(_custom_css_data)
        _f.close()
        return
    else:
        root = tk.Tk()
        root.withdraw()
        error = messagebox.showerror("ORIZIN Agent　エラー", "カスタムCSSテーマに不正な値を書き込もうとしています。")
        root.destroy()
        return


@eel.expose
def read_setting(_setting_name):
    return core.read_setting("resource/setting/setting.otfd", _setting_name)


@eel.expose
def write_setting(_setting_name, _setting_value):
    return core.write_setting("resource/setting/setting.otfd", _setting_name, _setting_value)


@eel.expose
def read_flag(_flag_name):
    return core.read_flag("resource/setting/flag.otfd", _flag_name)


@eel.expose
def set_flag(_flag_name, _flag_value):
    core.set_flag("resource/setting/flag.otfd", _flag_name, _flag_value)
    return


@eel.expose
def make_response(_not_normalized_query):
    _query = core.normalize(_not_normalized_query)
    _url_format_query = _not_normalized_query
    _url_format_query.replace(" ", "+").replace("　", "+")
    if core.judge(_query, ["じゃんけん", "ジャンケン"]):
        hand_shapes = ["グー", "チョキ", "パー"]
        selected_hand_shape = hand_shapes[random.randint(0, 2)]
        return [f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。", f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。"]
    elif core.judge(_query, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen(["python", "resource/python/easter_egg.py"])
        return ["イースターエッグを起動します。", "イースターエッグを起動します。"]
    elif core.judge(_query, ["予定", "よてい", "カレンダ", "かれんだ", "calender", "リマインダ", "リマインド", "りまいんだ", "りまいんど", "remind"]):
        webbrowser.open_new("https://calendar.google.com/")
        return ["Googleカレンダーを開きます", "Googleカレンダーを開きます。"]
    elif core.judge(_query, ["マップ", "まっぷ", "地図", "ちず", "場所", "ばしょ", "どこ", "何処", "行き方", "いきかた", "ゆきかた", "行きかた", "いき方", "ゆき方", "案内", "あんない", "道"]):
        webbrowser.open_new("https://google.com/maps/search/" + _query)
        return [f"Googleマップで「{_query}」を検索します。", f"Googleマップで「{_query}」を検索します。"]
    elif core.judge(_query, ["タイマ", "たいま"]):
        webbrowser.open_new("https://google.com/search?q=timer&hl=en")
        return ["タイマーを表示します。", "タイマーを表示します"]
    elif core.judge(_query, ["ストップウォッチ", "ストップウオッチ", "stopwatch"]):
        webbrowser.open_new("https://google.com/search?q=stopwatch&hl=en")
        return ["ストップウォッチを表示します。", "ストップウォッチを表示します。"]
    elif core.judge(_query, ["計算", "けいさん", "電卓", "でんたく"]):
        webbrowser.open_new("https://google.com/search?q=電卓")
        return ["電卓を開きます。", "電卓を開きます。"]
    elif core.judge(_query, ["何時", "時間", "時刻", "時計", "なんじ", "じかん", "じこく", "とけい", "日付", "ひづけ", "何日", "なんにち", "日にち", "ひにち"]):
        if read_flag("return_time_using_datetime_lib"):
            time = datetime.datetime.now()
            time = time.strftime('%Y年%m月%d日 %H:%M:%S')
            return [f"現在は{time}です。", f"現在は{time}です。"]
        else:
            webbrowser.open_new("https://google.com/search?q=今何時")
            return ["Googleで現在の時刻を検索します。", "Googleで現在の時刻を検索します。"]
    elif core.judge(_query, ["twitter", "ツイッタ", "ついった", "tweet", "ツイート", "ついーと"]):
        webbrowser.open_new("https://twitter.com/")
        return ["Twitterを開きます。", "Twitterを開きます。"]
    elif core.judge(_query, ["コロナ", "ころな", "corona", "covid19", "sarscov2", "感染", "かんせん", "肺炎", "はいえん"]):
        webbrowser.open_new("https://www.cas.go.jp/jp/influenza/novel_coronavirus.html")
        return ["内閣官房の新型コロナウイルスに関するページを表示します。", "内閣官房の新型コロナウイルスに関するページを表示します。"]
    elif core.judge(_query, ["facebook", "フェイスブック", "ふぇいすぶっく", "フェースブック", "ふぇーすぶっく"]):
        webbrowser.open_new("https://www.facebook.com/")
        return ["Facebookを開きます。", "Facebookを開きます。"]
    elif core.judge(_query, ["テレビ", "tv", "てれび", "番組", "ばんぐみ", "tver", "ティーバ", "てぃーば"]):
        webbrowser.open_new("https://tver.jp/")
        return ["TVerを開きます。", "TVerを開きます。"]
    elif core.judge(_query, ["youtube", "ユーチューブ", "ゆーちゅーぶ", "ようつべ", "ヨウツベ", "よーぶべ", "ヨーツベ"]) and core.judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ", "再生", "さいせい", "見せ", "観せ", "みせ", "見たい", "観たい", "みたい"]) and read_flag("search_in_youtube"):
        webbrowser.open_new("https://www.youtube.com/results?search_query={}".format(_url_format_query))
        return [f"YouTubeで「{_not_normalized_query}」を検索します。", f"YouTubeで「{_not_normalized_query}」を検索します。"]
    elif core.judge(_query, ["youtube", "ユーチューブ", "ゆーちゅーぶ", "ようつべ", "ヨウツベ", "よーぶべ", "ヨーツベ"]):
        webbrowser.open_new("https://www.youtube.com/")
        return ["YouTubeを開きます。", "YouTubeを開きます。"]
    elif core.judge(_query, ["instagram", "インスタ", "いんすた"]):
        webbrowser.open_new("https://www.instagram.com/")
        return ["Instagramを開きます。", "Instagramを開きます。"]
    elif core.judge(_query, ["github", "ギットハブ", "ぎっとはぶ"]):
        webbrowser.open_new("https://github.com/")
        return ["GitHubを開きます。", "GitHubを開きます。"]
    elif core.judge(_query, ["地震", "じしん"]):
        webbrowser.open_new("https://www.jma.go.jp/jp/quake/")
        return ["気象庁の地震情報のページを開きます。", "気象庁の地震情報のページを開きます。"]
    elif core.judge(_query, ["トレンド", "とれんど", "trend"]):
        webbrowser.open_new("https://trends.google.com/trends/trendingsearches/daily?geo=JP")
        return ["Googleトレンドを開きます。", "Googleトレンドを開きます。"]
    elif core.judge(_query, ["news", "ニュース", "にゅーす"]):
        webbrowser.open_new(read_setting("news_site_url"))
        return ["ニュースを開きます。", "ニュースを開きます。"]
    elif core.judge(_query, ["翻訳", "ほんやく"]):
        webbrowser.open_new("https://translate.google.co.jp/?hl=ja")
        return ["Google翻訳を開きます。", "Google翻訳を開きます。"]
    elif core.judge(_query, ["メール", "めーる", "mail"]):
        webbrowser.open_new("https://mail.google.com/")
        return ["Gmailを開きます。", "Gmailを開きます。"]
    elif core.judge(_query, ["ラジオ", "らじお", "radio"]):
        webbrowser.open_new("http://radiko.jp/")
        return ["radikoを開きます。", "radikoを開きます。"]
    elif core.judge(_query, ["写真", "しゃしん", "画像", "がぞう", "フォト", "ふぉと", "photo", "ピクチャ", "ぴくちゃ", "picture"]):
        webbrowser.open_new("https://photos.google.com/")
        return ["Googleフォトを開きます。", "Googleフォトを開きます。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "記憶", "きおく", "記録", "きろく"]) and core.judge(_query, ["削除", "さくじょ", "消去", "しょうきょ", "クリア", "clear", "くりあ", "消し", "けし", "忘れ", "わすれ"]):
        if os.path.exists("memo.txt") is False:
            return ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            _f = open("memo.txt", mode="r", newline="")
            _memo = _f.read()
            _f.close()
            if _memo.strip() == "":
                return ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                _f = open("memo.txt", mode="w", newline="")
                _f.write("")
                _f.close()
                return ["覚えているメモをすべて消去しました。", "覚えているメモをすべて消去しました。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "何", "なに", "内容", "ないよう"]) and core.judge(_query, ["覚えている", "おぼえている", "覚えてる", "おぼえてる", "記憶", "きおく", "記録", "きろく", "教え", "おしえ", "読", "よめ", "よん", "よみ"]):
        if os.path.exists("memo.txt") is False:
            return ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            _f = open("memo.txt", mode="r", newline="")
            _memo = _f.read()
            _f.close()
            if _memo.strip() == "":
                return ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                _memo_list = _memo.strip().split("\n")
                _memo_list = [f"{num + 1}つ目は、「{_memo_list[num]}」です。" for num in range(len(_memo_list))]
                _memo_content_to_read = "".join(_memo_list)
                return [f"覚えているメモを読み上げます。{_memo_content_to_read}以上が、覚えているメモです。", f"覚えているメモを読み上げます。{_memo_content_to_read}以上が、覚えているメモです。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "覚えて", "おぼえて", "覚えと", "おぼえと", "記憶", "きおく", "記録", "きろく"]):
        if os.path.exists("memo.txt") is False:
            _f = open("memo.txt", mode="w", newline="")
            _f.close()
        _f = open("memo.txt", mode="a", newline="")
        _f.write(f"{_not_normalized_query}\n")
        _f.close()
        return [f"「{_not_normalized_query}」とメモしました。", f"「{_not_normalized_query}」とメモしました。"]
    elif core.judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ"]):
        webbrowser.open_new(f"https://google.com/search?q={_url_format_query}")
        return [f"Googleで「{_not_normalized_query}」を検索します。", f"Googleで「{_not_normalized_query}」を検索します。"]
    elif core.judge(_query, ["サイコロ", "さいころ", "ダイス", "だいす", "dice"]):
        dice_result = random.randint(1, 6)
        return [f"サイコロを振りますね。{dice_result}が出ました。", f"サイコロを振りますね。{dice_result}が出ました。"]
    elif core.judge(_query, ["コイン", "こいん", "coin"]) and core.judge(_query, ["トス", "とす", "toss", "投げ", "なげ"]):
        coin = ["表", "裏"]
        result = coin[random.randint(0, 1)]
        return [f"コイントスをしますね。{result}が出ました。", f"コイントスをしますね。{result}が出ました。"]
    elif core.judge(_query, ["みくじ", "御籤", "神籤", "ミクジ"]):
        fortune_repertoire = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
        result = fortune_repertoire[random.randint(0, len(fortune_repertoire) - 1)]
        return [f"おみくじをします。ガラガラ...。結果は・・・{result}です。", f"おみくじをします。ガラガラ...。結果は・・・{result}です。"]
    elif core.judge(_query, ["さようなら", "サヨウナラ", "バイバイ", "終了", "しゅうりょう", "シャットダウン", "しゃっとだうん", "shutdown"]) and read_flag("exit_by_voice_command"):
        return ["", "<script>window.close()</script>"]
    else:
        _response = core.respond(dictionary, _query)
        _user_name = read_setting("user_name")
        return [_response[0].format(user_name=_user_name), _response[1].format(user_name=_user_name)]


@eel.expose
def check_update():
    return core.check_update("resource/information.txt",
                             "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/resource/information.txt",
                             "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/update_message.txt")


if __name__ == "__main__":
    try:
        dictionary = core.load_dictionary("resource/dictionary/dictionary.otfd")
    except Exception as error_message:
        root = tk.Tk()
        root.withdraw()
        dictionary_error = messagebox.showerror("ORIZIN Agent　エラー", error_message)
        sys.exit()
    if os.path.exists("resource/setting/setting.otfd") is False:
        change_theme("theme/light_theme.css")
    core.solve_setting_conflict("resource/setting/default_setting.otfd", "resource/setting/setting.otfd")
    core.solve_setting_conflict("resource/setting/default_flag.otfd", "resource/setting/flag.otfd")
    eel.init("resource")
    eel.start("/html/splash.html")
