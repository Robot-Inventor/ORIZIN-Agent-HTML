load_script("../javascript/component/experiment_card.js");
load_script("../javascript/component/search_box.js");
load_script("../javascript/component/warning_message.js");

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

window.addEventListener("load", () => {
    const search_box = document.getElementById("search_box");
    search_box.init("experiment-card");
});

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
