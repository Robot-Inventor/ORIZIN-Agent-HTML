load_script("../javascript/component/experiment_card.js");
load_script("../javascript/component/search_box.js");
load_script("../javascript/component/warning_message.js");

(async () => {
    const experiment_list = await load_json("../json/flag.json");

    Object.keys(experiment_list).forEach((experiment_name) => {
        const experiment = experiment_list[experiment_name];
        const card = document.createElement("experiment-card");

        card.setAttribute("icon", experiment.icon);
        card.setAttribute("experiment-title", experiment.title);
        card.setAttribute("experiment-name", experiment_name);
        card.setAttribute("data-search-tag", experiment.tag.join(", ") + `, ${experiment.title}, ${experiment.icon}`);
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
})();
