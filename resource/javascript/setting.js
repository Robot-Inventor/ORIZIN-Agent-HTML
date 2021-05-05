load_script("../javascript/component/search_box.js");
load_script("../javascript/component/warning_message.js");

new Konami(function () {
    const body_element = document.body;
    body_element.style.transition = "2s";
    body_element.style.transform = " translateY(150vmax) rotate(45deg)";

    setTimeout(() => {
        body_element.style.transition = "0s";
        body_element.style.transform = "scale(1.2)";
        body_element.style.opacity = "0";
    }, 2000);

    setTimeout(() => {
        body_element.style.transition = "2s";
        body_element.style.transform = "none";
        body_element.style.opacity = "1";
    }, 4000);
});

function save_setting() {
    const setting_value = event.target.tagName == "MWC-SWITCH" ? event.target.checked : event.target.value;
    eel.write_setting(event.target.id, setting_value);
}

async function generate_theme_menu() {
    const theme_dict = await eel.return_theme_dict()();
    const theme_select_element = document.getElementById("theme");
    for (let theme_path in theme_dict) {
        theme_select_element.insertAdjacentHTML("beforeend", `<option value="${theme_path}">${theme_dict[theme_path]}</option>`);
    }
}

generate_theme_menu();

async function set_to_current_setting() {
    document.getElementById("theme").value = await eel.read_setting("theme")();
    document.getElementById("user_name").value = await eel.read_setting("user_name")();
    document.getElementById("news_site_url").value = await eel.read_setting("news_site_url")();
    const search_engine_setting = await eel.read_setting("search_engine")();
    document.querySelector(`mwc-radio[name='search_engine_list'][value='${search_engine_setting}']`).checked = true;
    document.getElementById("python_interpreter").value = await eel.read_setting("python_interpreter")();
    document.getElementById("pitch").value = document.getElementById("pitch_value").innerHTML = await eel.read_setting("pitch")();
    document.getElementById("speed").value = document.getElementById("speed_value").innerHTML = await eel.read_setting("speed")();
    document.getElementById("volume").value = document.getElementById("volume_value").innerHTML = await eel.read_setting("volume")();

    if (await eel.read_setting("bold_text")() == "True") {
        document.getElementById("bold_text").checked = true;
    }
    if (await eel.read_setting("bigger_text")() == "True") {
        document.getElementById("bigger_text").checked = true;
    }
    if (await eel.read_setting("continuous_speech_recognition")() == "True") {
        document.getElementById("continuous_speech_recognition").checked = true;
    }
    if (await eel.read_setting("show_tips")() == "True") {
        document.getElementById("show_tips").checked = true;
    }
    if (await eel.read_flag("add_readable_text_setting")()) {
        document.getElementById("readable_text_setting").style.display = "block";
    }
    if (await eel.read_flag("show_tips_setting")()) {
        document.getElementById("tips_setting").style.display = "block";
    }
}

set_to_current_setting();

async function sound_test() {
    const script = new SpeechSynthesisUtterance("これは、音声のテストです。");
    script.pitch = Number(await eel.read_setting("pitch")());
    script.rate = Number(await eel.read_setting("speed")());
    script.volume = Number(await eel.read_setting("volume")());
    speechSynthesis.speak(script);

    eel.print_log_if_dev_mode("Sound test.", {
        "Pitch": script.pitch, "Speed": script.rate, "Volume": script.volume
    });
}

function save_sound_setting(setting_name) {
    document.getElementById(setting_name + "_value").textContent = document.getElementById(setting_name).value;
    save_setting();
}

function compare_and_return_latest_version_num(version1, version2) {
    if (version1 === version2) {
        return version1;
    } else {
        let v1_array = version1.split(".");
        for (let i = 0; i < v1_array.length; i++) {
            v1_array[i] = parseInt(v1_array[i]);
        }
        let v2_array = version2.split(".");
        for (let i = 0; i < v2_array.length; i++) {
            v2_array[i] = parseInt(v2_array[i]);
        }

        if (v1_array[0] < v2_array[0]) {
            return version2;
        } else if (v1_array[0] > v2_array[0]) {
            return version1;
        } else {
            if (v1_array[1] < v2_array[1]) {
                return version2;
            } else if (v1_array[1] > v2_array[1]) {
                return version1;
            } else {
                if (v1_array[2] < v2_array[2]) {
                    return version2;
                } else {
                    return version1;
                }
            }
        }
    }
}

document.querySelectorAll("mwc-radio[name='search_engine_list']").forEach((element) => {
    element.addEventListener("change", () => {
        setTimeout(() => {
            eel.write_setting("search_engine", document.querySelector("mwc-radio[name='search_engine_list'][checked]").value);
        }, 100);
    });
});

document.getElementById("check_update").addEventListener("click", async function () {
    function sanitize(string) {
        const sanitize_table = {
            "&": '&amp;',
            "'": '&#x27;',
            "`": '&#x60;',
            "\"": '&quot;',
            "<": '&lt;',
            ">": '&gt;',
        };
        Object.keys(sanitize_table).forEach((key) => {
            string.replaceAll(key, sanitize_table[key]);
        });
        return string;
    }

    document.getElementById("update_detail").innerHTML = "アップデートを確認中です...";
    const response = await fetch("../information.json");
    const information_data = await response.json();
    const version_information = information_data.Version;
    const release_data = await eel.get_release(information_data.Channel)();

    const latest_version = compare_and_return_latest_version_num(version_information, release_data[0]);
    const update_detail = document.getElementById("update_detail");
    if (latest_version === version_information) {
        update_detail.innerHTML = "利用可能なアップデートはありません。最新のバージョンを使用中です。";
    } else {
        update_detail.innerHTML = `<h1>${release_data[0]}</h1>${release_data[1]}<br><a href='https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/releases' target='_blank' rel='noreferrer noopener' class='ripple_effect'><mwc-button label="ダウンロード" icon="open_in_new" trailingIcon></mwc-button></a>`;
    }
});

document.getElementById("reset_setting_button").addEventListener("click", () => {
    const dialog = document.getElementById("reset_check_dialog");
    document.getElementById("dialog_content").textContent = "設定をすべてデフォルトに戻します。よろしいですか。";
    dialog.show();
    dialog.addEventListener("closed", () => {
        if (event.detail.action === "yes") {
            eel.reset_setting();
            location.reload();
        }
    });
});

document.getElementById("factory_reset_button").addEventListener("click", () => {
    const dialog = document.getElementById("reset_check_dialog");
    document.getElementById("dialog_content").textContent = "ORIZIN Agent HTMLを初期化します。よろしいですか。";
    dialog.show();
    dialog.addEventListener("closed", () => {
        if (event.detail.action === "yes") {
            eel.factory_reset();
            location.href = "splash.html";
        }
    });
});

window.addEventListener("load", () => {
    const search_box = document.getElementById("search_box");
    search_box.init("div.fill_panel section");
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
