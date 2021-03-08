class ExperimentCard extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({ mode: "open" });

        const section = document.createElement("section");

        this.icon_element = document.createElement("i");
        this.icon_element.setAttribute("class", "material_icon");
        this.icon_element.textContent = this.getAttribute("icon");

        this.experiment_title = document.createElement("span");
        this.experiment_title.textContent = this.getAttribute("experiment-title");

        this.mwc_switch = document.createElement("mwc-switch");
        this.read_flag(this.getAttribute("experiment-name"));
        this.mwc_switch.addEventListener("change", () => {
            eel.set_flag(this.getAttribute("experiment-name"), this.mwc_switch.checked);
        });

        const information = document.createElement("slot");
        information.setAttribute("class", "information");

        const style = document.createElement("style");
        style.textContent = `
section {
    border-bottom: solid 0.05em var(--text);
    padding: 1em;
    padding-left: 0;
    font-weight: bold;
    display: block;
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
    margin: 0 0.4em;
}

mwc-switch {
    margin-left: 1rem;
}

.information {
    padding-left: 1.5rem;
    font-weight: normal;
    font-size: 0.9em;
    opacity: 0.7;
    color: var(--text);
    display: block;
}
        `;

        section.appendChild(this.icon_element);
        section.appendChild(this.experiment_title);
        section.appendChild(this.mwc_switch);
        section.appendChild(information);
        shadow.appendChild(section);
        shadow.appendChild(style);
    }

    async read_flag(flag_name) {
        const flag_value = await eel.read_flag(flag_name)();
        this.mwc_switch.checked = flag_value;
    }

    static get observedAttributes() {
        return ["icon", "experiment-title", "experiment-name"];
    }

    attributeChangedCallback(name, old_value, new_value) {
        switch (name) {
            case "icon":
                this.icon_element.textContent = new_value;
                break;

            case "experiment-title":
                this.experiment_title.textContent = new_value;
                break;

            case "experiment-name":
                this.read_flag(this.getAttribute("experiment-name"));
                this.mwc_switch.addEventListener("change", () => {
                    eel.set_flag(this.getAttribute("experiment-name"), this.mwc_switch.checked);
                });
                break;
        }
    }

    get icon() {
        return this.icon_element.textContent;
    }

    set icon(value) {
        this.setAttribute("icon", value);
    }

    get experimentTitle() {
        return this.experiment_title.textContent;
    }

    set experimentTitle(value) {
        this.setAttribute("experiment-title", value);
    }

    get experimentName() {
        return this.getAttribute("experiment-name");
    }

    set experimentName(value) {
        this.setAttribute("experiment-name", value);
    }
}

customElements.define("experiment-card", ExperimentCard);

const experiment_list = {
    add_readable_text_setting: {
        icon: "text_format",
        title: "可読性を上げる設定を追加する",
        information: "設定ページにテキストを読みやすくするための項目を追加します。"
    },
    fast_start: {
        icon: "power_settings_new",
        title: "高速起動を有効にする",
        information: "スプラッシュスクリーンをスキップし、高速起動します。"
    },
    get_news_from_google_news: {
        icon: "rss_feed",
        title: "Google News RSSを使用する",
        information: "ユーザーがニュースを要求した際、GoogleニュースのWebページを開くのではなくGoogle News RSSを使用してインターネットからニュースを自動で取得します。"
    },
    use_fast_response_mode: {
        icon: "two_wheeler",
        title: "高速モードを有効にする",
        information: "高速かつ低負荷で応答を返すようにします。Intelligent Match機構は無効になり、適切な応答が見つからなかったことを示す「そうですか」という応答を返す頻度が高くなります。"
    },
    show_feedback_button: {
        icon: "feedback",
        title: "フィードバックボタンを表示する",
        information: "メニュー内にフィードバックボタンを表示し、必要に応じてフィードバックを送信できるようになります。"
    },
    enable_improved_custom_theme_editor: {
        icon: "edit",
        title: "改善されたカスタムテーマの編集ページを使用する",
        information: "設定ページのテーマセクションで [カスタムテーマの編集] を押した際に改善されたページを表示します。"
    }
};

Object.keys(experiment_list).forEach((experiment_name) => {
    const experiment = experiment_list[experiment_name];
    const card = document.createElement("experiment-card");

    card.setAttribute("icon", experiment.icon);
    card.setAttribute("experiment-title", experiment.title);
    card.setAttribute("experiment-name", experiment_name);
    card.textContent = experiment.information;

    document.getElementById("section_outer").appendChild(card);
});

document.getElementById("continue_button").addEventListener("click", () => {
    document.getElementById("section_outer").style.display = "block";
    document.getElementById("continue_check_menu").style.display = "none";
    document.getElementById("continue_check_message").textContent = "ここにある機能は全て試験機能であり、実装が不十分な可能性があります。有効にするとデータが破損したり、動作が不安定になったり、その他の問題が生じたりする場合があります。";
});

document.getElementById("back_button").addEventListener("click", () => {
    window.history.back(-1);
    return false;
});

document.getElementById("refresh_button").addEventListener("click", () => {
    const dialog = document.getElementById("reset_check_dialog");
    dialog.show();
    dialog.addEventListener("closed", () => {
        if (event.detail.action === "yes") {
            eel.reset_flag();
            location.reload();
        }
    });
});

const search_box = document.getElementById("search_box");

search_box.init("experiment-card");

Mousetrap.bind({
    "/": () => {
        search_box.focus();
        event.preventDefault();
    },
    "s": () => {
        search_box.focus();
        event.preventDefault();
    },
    "esc": () => {
        search_box.blur();
    }
});
