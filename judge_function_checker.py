import re
import glob
from oa_core import normalize


if __name__ == "__main__":
    result = []
    for file in glob.glob("**/*.py", recursive=True):
        if file == "oa_core.py":
            continue
        print(f"{file} を検証中...", end="")
        with open(file, mode="r", encoding="utf-8_sig") as f:
            content = re.sub(" *", "", f.read().replace("\n", "").replace(' "', '"').replace(" [", "["))
        pattern = re.compile(r"judge\(.*?\)", re.MULTILINE | re.DOTALL)
        functions = re.findall(pattern, content)
        for target in functions:
            if target.replace("judge(_query,", "") != normalize(target.replace("judge(_query,", "")):
                result.append(f'\033[31m{file}　内の{target}に正規化によって無効になる文字が含まれています。\033[0m')
        print("完了")
    print("すべてのファイルの検証が完了しました。")
    if result:
        print(f"\033[31mエラーが{len(result)}個見つかりました。\033[0m")
        print("\n".join(result))
    else:
        print("エラーは見つかりませんでした。")
