load_script("../javascript/component/warning_message.js");

function get_radio_value(name) {
    const selected_radio = document.querySelector(`mwc-radio[name="${name}"][checked]`);
    if (selected_radio) {
        return selected_radio.value;
    } else {
        return null;
    }
}

function get_textbox_value(name) {
    const element = document.querySelector(`underlined-textbox[name="${name}"]`);
    if (element.value) {
        return element.value;
    } else {
        return "";
    }
}

function ask_changing_page(event) {
    event.preventDefault();
    event.returnValue = "";
}

function show_error(message_content) {
    const dialog = document.getElementById("error_dialog");
    document.getElementById("dialog_content").innerHTML = message_content;
    dialog.show();

    const error_message = document.getElementById("error_message");
    error_message.textContent = message_content;
    error_message.style.display = "block";
}

async function get_oa_info() {
    const fetch_response = await fetch("../information.txt");
    const information_content = await fetch_response.text();
    return information_content.replaceAll("\r\n", "\n").replaceAll("\r", "\n");
}

async function get_system_info() {
    const system_info = UAParser();
    system_info.python_version = await eel.get_python_version()();
    system_info.python_os = await eel.get_os()();
    system_info.oa_info = await get_oa_info();
    return JSON.stringify(system_info, null, 4);
}

window.addEventListener("beforeunload", ask_changing_page);

const show_system_info_button = document.getElementById("show_system_info");
show_system_info_button.addEventListener("click", async () => {
    document.getElementById("system_info_preview").textContent = await get_system_info();
    show_system_info_button.remove();
});

const submit_button = document.getElementById("submit");
submit_button.addEventListener("click", async () => {
    submit_button.disabled = true;

    const feedback_type_name = "entry.1463225208";
    const feedback_detail_name = "entry.166666813";
    const github_url_name = "entry.99636056";
    const system_info_name = "entry.1783167764";

    const feedback_type_value = get_radio_value(feedback_type_name);
    const feedback_detail_value = get_textbox_value(feedback_detail_name);
    const github_url_value = get_textbox_value(github_url_name);
    const system_info = document.getElementById("send_system_info").checked ? await get_system_info() : "";

    const github_url_regex = /https:\/\/github\.com\/[\w!?/+\-_~;.,*&@#$%()'[\]]+/;

    if (feedback_type_value === null) {
        show_error("フィードバックの種類を選択してください。");
        submit_button.disabled = false;
        return;
    }

    if (feedback_detail_value === "") {
        show_error("テキストボックスに詳細を入力してください。");
        submit_button.disabled = false;
        return;
    }

    if (github_url_value !== "" && !github_url_regex.test(github_url_value)) {
        show_error("GitHubの有効なURLを入力してください。");
        submit_button.disabled = false;
        return;
    }

    const dummy_send_target = document.createElement("iframe");
    dummy_send_target.style.display = "none";
    dummy_send_target.name = "dummy_send_target";
    document.getElementById("feedback").appendChild(dummy_send_target);

    const form_iframe = document.createElement("iframe");
    form_iframe.src = encodeURI(`https://docs.google.com/forms/d/e/1FAIpQLSfxjq1neTulfxxCG1TlGGj_lYn-R1Wo7ciPwPyM3cNwTYuZ7A/formResponse?${feedback_type_name}=${feedback_type_value}&${feedback_detail_name}=${feedback_detail_value}&${github_url_name}=${github_url_value}&${system_info_name}=${system_info}&submit=Submit`);
    form_iframe.style.display = "none";

    form_iframe.addEventListener("load", function () {
        document.getElementById("feedback").remove();
        document.getElementById("instruction_message").remove();
        document.getElementById("words_of_thanks").style.display = "block";

        window.removeEventListener("beforeunload", ask_changing_page, false);
    });
    document.getElementById("feedback").appendChild(form_iframe);
});
