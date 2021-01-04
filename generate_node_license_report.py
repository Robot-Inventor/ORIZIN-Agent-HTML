import glob
import json
import os
import re


LICENSE_ALLOW_LIST = ["MIT", "ISC", "BSD-3-Clause", "0BSD",
                      "Apache-2.0", "(MIT OR Apache-2.0)", "BSD-2-Clause"]


def generate():
    package_dictionary = {}
    for package_json_path in glob.glob("node_modules/**/package.json", recursive=True):
        with open(package_json_path, encoding="utf-8_sig") as f:
            package_data = json.load(f)

        if "name" in package_data:
            package_name = package_data["name"]
        else:
            continue

        package_directory = os.path.dirname(package_json_path) + "/"
        package_license_type = None
        if "license" in package_data:
            package_license_type = package_data["license"]
        elif "licenses" in package_data:
            package_license_type = package_data["licenses"][0]["type"]
        if package_license_type and package_license_type not in LICENSE_ALLOW_LIST:
            raise Exception(
                f"{package_directory} の {package_name} のpackage.jsonでプロジェクトで許可されていないライセンスが検出されました。")

        if "version" in package_data:
            package_version = "v" + package_data["version"]
        else:
            package_version = ""

        license_file_name = "LICENSE" if os.path.exists(
            package_directory + "LICENSE") else "LICENSE.txt" if os.path.exists(package_directory + "LICENSE.txt") else None
        if license_file_name:
            with open(package_directory + license_file_name, encoding="utf-8_sig") as f:
                package_license = f.read()
            package_dictionary[package_name] = package_license
        elif package_license_type:
            if package_license_type == "MIT":
                package_license = """Copyright <YEAR> <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
            elif package_license_type == "ISC":
                package_license = """Copyright <YEAR> <OWNER>

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE."""
            elif package_license_type == "BSD-2-Clause":
                package_license = """Copyright <YEAR> <COPYRIGHT HOLDER>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
            else:
                package_license = package_license_type
                raise ValueError(
                    f"{package_directory} のパッケージ {package_name} でライセンスファイルが見つからず、package.jsonでプログラムに登録されていないライセンスタイプが検出されました。\n検出されたライセンスタイプ：{package_license_type}")

        else:
            continue

        package_repository_link_button = ""
        if "repository" in package_data:
            package_repository_url = re.sub(
                "^git\+", "", package_data["repository"]["url"])
            package_repository_url = re.sub(
                r"git://github\.com/(.*?)\.git", r"https://github.com/\1", package_repository_url)
            package_repository_link_button = f'<a href="{package_repository_url}" target="_blank" rel="noopener noreferrer" class="ripple_effect button shadow">リポジトリーを開く<i class="material_icon">open_in_new</i></a>'

        package_dictionary[package_name] = f"""<details>
                        <summary class="ripple_effect">{package_name} {package_version}</summary>
                        <pre>
{package_license}
                        </pre>
                        {package_repository_link_button}
                    </details>"""

    license_html = "\n".join([package_dictionary[key]
                              for key in sorted(package_dictionary.keys())])

    return license_html


if __name__ == "__main__":
    print(generate())
