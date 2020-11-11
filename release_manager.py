import urllib.request
import html
import re
import typing


def get_content(string: str, tag_name: str) -> str:
    pattern = re.compile(f"<{tag_name}(| type=\".*?\")>.*?</{tag_name}>", re.MULTILINE | re.DOTALL)
    result = re.search(pattern, string)
    if(result):
        return re.sub(f"(<(|/){tag_name}(| type=\".*?\")>)", "", result.group())
    else:
        return "Not Found"


def get_latest_version(channel: typing.Literal["stable", "develop"]) -> str:
    atom_file = html.unescape(urllib.request.urlopen("https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/tags.atom").read().decode())
    if channel == "stable":
        if(latest_version := re.search("<title>v(\d|\.).*?(?!dev)-\w*?</title>", atom_file)):
            return latest_version.group().replace("<title>", "").replace("</title>", "")
        else:
            raise ValueError("指定されたチャンネルの最新バージョンを取得できませんでした。")
    elif channel == "develop":
        if(latest_version := re.search("<title>v(\d|\.).*?dev-\w*?</title>", atom_file)):
            return latest_version.group().replace("<title>", "").replace("</title>", "")
        else:
            raise ValueError("指定されたチャンネルの最新バージョンを取得できませんでした。")
    else:
        raise ValueError(f"引数として不正なチャンネル「{channel}」が指定されました。「stable」または「develop」を指定してください。")


def get_release(channel: typing.Literal["stable", "develop"], version: str = "") -> str:
    atom_file = html.unescape(urllib.request.urlopen("https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/releases.atom").read().decode("utf-8"))
    pattern = re.compile(f"<title>{version if version else get_latest_version(channel)}</title>.*?</entry>", re.MULTILINE | re.DOTALL)
    if(latest_release := re.search(pattern, atom_file)):
        return get_content(latest_release.group(), "content")
    else:
        raise ValueError("最新のリリースを取得できませんでした。")
