# ライブラリーの依存関係リスト

各ライブラリーは，ネストされたライブラリーに依存している。また，ライブラリー名の右にはライセンスが書かれている。以下は，依存関係を表しているため重複して書かれているライブラリーがある。

Eel: MIT
- bottle: MIT
- whichcraft: BSD
- bottle-websocket: MIT
    - bottle: MIT
    - gevent-websocket: Apache 2.0
        - gevent: MIT
            - zope.event: ZPL 2.1
                - setuptools: MIT
            - cffi: MIT
                - pycparser: BSD
            - setuptools: MIT
            - greenlet: MIT
            - zope.interface: ZPL 2.1
                - setuptools: MIT
- future: MIT

Python: PSF
- 標準ライブラリー: PSF
- 一部の標準ライブラリー: 要確認

<style>
    ul {
        border-left: solid 0.1rem;
    }
</style>
