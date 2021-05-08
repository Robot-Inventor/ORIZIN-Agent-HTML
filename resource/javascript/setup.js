const ALL_CARDS = document.querySelectorAll("div.overlay_inner").length;
let setup_status = 1;

const progress = document.querySelector("progress");
progress.value = setup_status / ALL_CARDS;

const card_array = document.querySelectorAll("div.overlay_inner");
let current_card_index = 0;

function forward_card() {
    card_array[current_card_index].style.marginLeft = "-100vw";
    current_card_index++;
    card_array[current_card_index].style.marginLeft = "0";
    setup_status += 1;
    progress.value = setup_status / ALL_CARDS;
}

function back_card() {
    card_array[current_card_index].style.marginLeft = "100vw";
    current_card_index--;
    card_array[current_card_index].style.marginLeft = "0";
    setup_status -= 1;
    progress.value = setup_status / ALL_CARDS;
}

async function generate_theme_menu() {
    const theme_dict = await eel.return_theme_dict()();
    const theme_select_element = document.getElementById("theme");
    for (let theme_path in theme_dict) {
        const option_element = `<option value="${theme_path}">${theme_dict[theme_path]}</option>`;
        theme_select_element.insertAdjacentHTML("beforeend", option_element);
    }
}

async function set_to_current_setting() {
    const setting_name_list = ["theme", "user_name", "news_site_url", "search_engine", "python_interpreter"];
    for (let i = 0; i < setting_name_list.length; i++) {
        const setting_name = setting_name_list[i];
        document.getElementById(setting_name).value = await eel.read_setting(setting_name)();
    }
}

function save_setting() {
    eel.write_setting("setup_finished", true);

    eel.change_theme(document.getElementById("theme").value);
    eel.write_setting("user_name", document.getElementById("user_name").value);
    eel.write_setting("news_site_url", document.getElementById("news_site_url").value);
    eel.write_setting("search_engine", document.getElementById("search_engine").value);
    eel.write_setting("python_interpreter", document.getElementById("python_interpreter").value);

    location.href = "index.html";
}

generate_theme_menu();

set_to_current_setting();
