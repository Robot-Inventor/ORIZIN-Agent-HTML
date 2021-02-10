async function readable_text_setting() {
    const use_bold_text = await eel.read_setting("bold_text")();
    if (use_bold_text === "True") {
        document.body.style.fontWeight = "bold";
    }
    const use_bigger_text = await eel.read_setting("bigger_text")();
    if (use_bigger_text === "True") {
        document.body.style.fontSize = "1.1em";
    }
}

// eslint-disable-next-line no-unused-vars
async function load_file(file_path, target_element) {
    const fetch_response = await fetch(file_path);
    const response_content = await fetch_response.text();
    const target_type = Object.prototype.toString.call(target_element);
    switch (target_type) {
        case "[object HTMLPreElement]":
            target_element.innerHTML = response_content;
            break;
        case "[object String]":
            document.querySelector(target_element).innerHTML = response_content;
            break;
    }
}

async function feed_buck_setting() {
    if(await eel.read_flag("show_feedback_button")()) {
        document.getElementById("feedback_button").style.display = "block";
    }
}

// eslint-disable-next-line no-unused-vars
function open_menu() {
    document.getElementById("menu_open_button").classList.add("open");
    setTimeout(() => {
        document.getElementById("side_menu_bar_overlay").classList.add("visible");
        document.getElementById("side_menu_bar").classList.add("open");
    }, 50);
    setTimeout(() => {
        document.getElementById("menu_close_button").classList.add("open");
    }, 100);
}

function close_menu() {
    document.getElementById("menu_close_button").classList.remove("open");
    setTimeout(() => {
        document.getElementById("side_menu_bar_overlay").classList.remove("visible");
        document.getElementById("side_menu_bar").classList.remove("open");
    }, 50);
    setTimeout(() => {
        document.getElementById("menu_open_button").classList.remove("open");
    }, 100);
}

// eslint-disable-next-line no-unused-vars
async function move_page(place) {
    close_menu();
    setTimeout(() => {
        location.href = place;
    }, 300);
}


document.querySelector("header").innerHTML = `
<div id="top_app_bar">
    <span class="ripple_effect"><img src="../image/menu_icon.svg" id="menu_open_button" onclick="open_menu()" title="メニューを開く"></span><span class="ripple_effect"><a href="index.html" title="ホーム画面へ戻る" id="app_name">ORIZIN Agent HTML</a></span>
</div>
<div id="side_menu_bar_overlay" onclick="close_menu()"></div>
<div id="side_menu_bar">
    <button id="menu_close_button" class="ripple_effect" onclick="close_menu()" title="メニューを閉じる"><i class="material_icon">arrow_forward</i></button>
    <div class="ripple_effect" onclick="move_page('index.html')" title="ホーム画面に戻る">
        <i class="material_icon">home</i>ホーム
    </div>
    <hr>
    <div class="ripple_effect" onclick="move_page('setting.html')" title="様々な設定をする">
        <i class="material_icon">settings</i>設定
    </div>
    <hr>
    <div class="ripple_effect" onclick="move_page('oss_license.html')" title="使用しているOSSの名称とライセンスの一覧を見る">
        <i class="material_icon">assignment</i>オープンソースソフトウェアライセンス
    </div>
    <hr>
    <div class="ripple_effect" onclick="move_page('privacy_policy.html')" title="ユーザーの情報の扱い方について見る">
        <i class="material_icon">privacy_tip</i>プライバシーポリシー
    </div>
    <hr>
    <div class="ripple_effect" onclick="move_page('feedback.html')" id="feedback_button" title="フィードバックを送信する">
        <i class="material_icon">feedback</i>フィードバック
    </div>
    <hr>
    <div class="ripple_effect" onclick="move_page('about_oa.html')" title="バージョンやソフトウェアの概要を見る">
        <i class="material_icon">info</i>ORIZIN Agentについて
    </div>
    <hr>
    <a href="https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/wiki" target="_blank" rel="noreferrer noopener">
        <div title="使い方が書かれているサイトを開く" class="ripple_effect">
            <i class="material_icon">help</i>ヘルプ＆Wiki(GitHub)<i class="material_icon">open_in_new</i>
        </div>
    </a>
    <hr>
    <div id="copyright_in_menu">
        Copyright &copy; 2019 - 2021 Robot-Inventor
    </div>
</div>
<style>
    #feedback_button {
        display: none;
    }
</style>
`;

new Ripple(".ripple_effect", {
    debug: false,
    on: "mousedown",
    opacity: 0.4,
    color: "auto",
    multi: false,
    duration: 0.7,
    rate: function(pxPerSecond) {
        return pxPerSecond;
    },
    easing: "linear"
});

window.addEventListener("load", () => {
    readable_text_setting();
    feed_buck_setting();
    eel.print_log_if_dev_mode("Page rendered.", {"File": location.pathname});

    Mousetrap.prototype.stopCallback = function(e, element, combo) {
        var self = this;
        if ((' ' + element.className + ' ').indexOf(' mousetrap ') > -1) {
            return false;
        }
        if (element.tagName === "SEARCH-BOX" || element.tagName === "UNDERLINED-TEXTBOX") {
            if (combo === "esc" || combo === "enter" || combo === "up" || combo === "down") {
                return false;
            } else {
                return true;
            }
        }

        return element.tagName == 'INPUT' || element.tagName == 'SELECT' || element.tagName == 'TEXTAREA' || element.isContentEditable;
    };

    Mousetrap.bind({
        "mod+,": () => {
            location.href = "setting.html";
        },
        "t": () => {
            location.href = "index.html";
        },
        "h": () => {
            location.href = "index.html";
        },
        "home": () => {
            location.href = "index.html";
        },
        "m": () => {
            if (document.getElementById("menu_open_button").classList.contains("open")) {
                document.getElementById("menu_close_button").click();
            } else {
                document.getElementById("menu_open_button").click();
            }
        }
    });
});

class WarningMessage extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({mode: "open"});

        this.slot_element = document.createElement("slot");

        const icon_element = document.createElement("i");
        icon_element.setAttribute("class", "material_icon");
        icon_element.textContent = "warning";

        const style_element = document.createElement("style");
        style_element.textContent = `
:host {
    display: block;
}

* {
    color: var(--error_text_color);
    font-weight: bold;
}

i.material_icon {
    font-family: "Material Icons";
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    transform: translateY(0.15em);
    margin: 0 0.4em 0 0;
}
        `;

        shadow.appendChild(icon_element);
        shadow.appendChild(this.slot_element);
        shadow.appendChild(style_element);
    }
}

customElements.define("warning-message", WarningMessage);

class SearchBox extends HTMLElement {
    constructor() {
        super();

        const input_event = new Event("input");

        const shadow = this.attachShadow({mode: "open"});

        const outer_element = document.createElement("div");
        outer_element.setAttribute("id", "outer");

        const search_icon_element = document.createElement("i");
        search_icon_element.textContent = "search";
        search_icon_element.setAttribute("id", "search_icon");
        search_icon_element.setAttribute("class", "material_icon");

        this.text_box = document.createElement("input");
        this.text_box.setAttribute("id", "search_box");
        this.text_box.setAttribute("placeholder", "設定項目を検索");
        this.text_box.addEventListener("input", () => {
            const value = this.text_box.value;
            this.setAttribute("value", value);
            this.dispatchEvent(input_event);
            clear_icon_element.style.display = value ? "inline-block" : "none";
        });
        this.text_box.addEventListener("focusin", () => {
            outer_element.classList.add("focused");
        });
        this.text_box.addEventListener("focusout", () => {
            outer_element.classList.remove("focused");
        });

        const clear_icon_element = document.createElement("i");
        clear_icon_element.textContent = "clear";
        clear_icon_element.setAttribute("id", "clear_icon");
        clear_icon_element.setAttribute("class", "material_icon ripple_effect");
        clear_icon_element.addEventListener("click", () => {
            this.setAttribute("value", "");
            this.dispatchEvent(input_event);
            clear_icon_element.style.display = "none";
        });

        const style_element = document.createElement("style");
        style_element.textContent = `
#outer {
    background: var(--card_bg);
    width: 50%;
    padding: 0.25rem 0.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    position: relative;
    top: 0;
    left: 0;
    overflow: visible;
}

#outer::before {
    content: "";
    display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    border-radius: 0.25rem;
    border: solid 1px var(--text);
    opacity: 0.2;
    pointer-events: none;
    transition: 0.3s;
}

#outer.focused::before {
    border: solid 1px var(--theme_color);
    opacity: 0.75;
}

.material_icon {
    font-family: "Material Icons";
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    transform: translateY(0.15em);
    color: var(--text);
}

#search_icon {
    margin: 0 0.4em;
    margin-right: 0.5rem;
    cursor: default;
    transition: 0.3s;
}

#outer.focused #search_icon {
    color: var(--theme_color);
}

#search_box {
    width: calc(100% - 4rem);
    height: 100%;
    background: transparent;
    outline: none;
    border: none;
    color: var(--text);
}

#search_box:placeholder {
    color: var(--text);
    opacity: 0.5;
}

#clear_icon {
    cursor: pointer;
    display: none;
    margin-left: 0.5rem;
}
        `;

        outer_element.appendChild(search_icon_element);
        outer_element.appendChild(this.text_box);
        outer_element.appendChild(clear_icon_element);
        shadow.appendChild(outer_element);
        shadow.appendChild(style_element);
    }

    static get observedAttributes() {
        return ["value"];
    }

    attributeChangedCallback(name, old_value, new_value) {
        switch(name) {
            case "value":
                this.text_box.value = new_value;
                break;
        }
    }

    get value() {
        return this.text_box.value;
    }

    set value(value) {
        this.text_box.setAttribute("value", value);
    }
}

customElements.define("search-box", SearchBox);
