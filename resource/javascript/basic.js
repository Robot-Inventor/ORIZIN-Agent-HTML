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
    if (await eel.read_flag("show_feedback_button")()) {
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

// eslint-disable-next-line no-unused-vars
function load_script(url) {
    const script_element = document.createElement("script");
    script_element.setAttribute("src", url);
    document.body.appendChild(script_element);
}


document.querySelector("header").innerHTML = `
<div id="top_app_bar">
    <mwc-icon-button icon="menu" onclick="open_menu()" id="menu_open_button"></mwc-icon-button><span class="ripple_effect"><a href="index.html" title="ホーム画面へ戻る" id="app_name">ORIZIN Agent HTML</a></span>
</div>
<div id="side_menu_bar_overlay" onclick="close_menu()"></div>
<div id="side_menu_bar">
    <mwc-icon-button id="menu_close_button" onclick="close_menu()" icon="arrow_forward"></mwc-icon-button>
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
    rate: function (pxPerSecond) {
        return pxPerSecond;
    },
    easing: "linear"
});

window.addEventListener("load", () => {
    readable_text_setting();
    feed_buck_setting();
    eel.print_log_if_dev_mode("Page rendered.", { "File": location.pathname });

    Mousetrap.prototype.stopCallback = function (e, element, combo) {
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

class Scrollbar {
    attach({
        selector = "body",
        color = "black",
        width_thin = 4,
        visibility_class = "show_scrollbar"
    } = {}) {
        this.target_selector = selector;
        this.scrollbar_color = color;
        this.scrollbar_visibility_class = visibility_class;
        this.scrollbar_width_thin = width_thin;

        this.hide_scrollbar_timer = setTimeout(() => { });

        const style_element = document.createElement("style");
        style_element.textContent = `
${this.target_selector} {
    overflow: hidden overlay;
}
${this.target_selector}::-webkit-scrollbar {
    display: none;
}

${this.target_selector}.${this.scrollbar_visibility_class}::-webkit-scrollbar {
    display: block;
    width: ${this.scrollbar_width_thin}px;
}

${this.target_selector}.${this.scrollbar_visibility_class}::-webkit-scrollbar-thumb {
    background: ${this.scrollbar_color};
    border-radius: ${this.scrollbar_width_thin}px;
}

${this.target_selector}.${this.scrollbar_visibility_class}::-webkit-scrollbar-corner {
    display: none;
}
        `;
        document.body.insertAdjacentElement("beforeend", style_element);

        document.querySelectorAll(this.target_selector).forEach((element) => {
            element.addEventListener("mouseover", () => {
                element.classList.add(this.scrollbar_visibility_class);
            }, false);

            element.addEventListener("mouseleave", () => {
                element.classList.remove(this.scrollbar_visibility_class);
            }, false);

            element.addEventListener("scroll", () => {
                clearTimeout(this.hide_scrollbar_timer);
                element.classList.add(this.scrollbar_visibility_class);
                this.hide_scrollbar_timer = setTimeout(() => {
                    element.classList.remove(this.scrollbar_visibility_class);
                }, 5000);
            }, false);
        });
    }
}

const scrollbar = new Scrollbar();
scrollbar.attach({ selector: "#side_menu_bar", color: "var(--text)" });
scrollbar.attach({ selector: ".fill_panel", color: "var(--text)" });
