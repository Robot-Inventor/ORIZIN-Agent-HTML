const search_box = document.getElementById("search_box");

async function read_flag(flag_name) {
    const flag_value = await eel.read_flag(flag_name)();
    document.getElementById(flag_name).checked = flag_value;
}

document.querySelectorAll("div.fill_panel section mwc-switch").forEach((element) => {
    read_flag(element.id);

    element.addEventListener("change", function () {
        eel.set_flag(event.target.id, event.target.checked);
    });
});

document.getElementById("continue_button").addEventListener("click", function () {
    document.getElementById("section_outer").style.display = "block";
    document.getElementById("continue_check_menu").style.display = "none";
    document.getElementById("continue_check_message").textContent = "ここにある機能は全て試験機能であり、実装が不十分な可能性があります。有効にするとデータが破損したり、動作が不安定になったり、その他の問題が生じたりする場合があります。";
});

document.getElementById("back_button").addEventListener("click", function () {
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

search_box.init("div.fill_panel section");
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
