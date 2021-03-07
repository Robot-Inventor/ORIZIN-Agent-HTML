eel.expose(start_speak);
eel.expose(add_chat);

new Konami(function () {
    const body_element = document.body;
    body_element.style.transition = "7.5s";
    body_element.style.transform = "rotate(3600deg) scale(0.01)";
    body_element.style.opacity = "0";

    setTimeout(() => {
        body_element.style.transition = "0s";
        body_element.style.transform = "translateY(-100%)";
    }, 7500);

    setTimeout(() => {
        body_element.style.transition = "2s";
        body_element.style.transform = "none";
        body_element.style.opacity = "1";
    }, 9000);
});

function start_speak(content, will_keep_speaking_after_this_function = false, allow_continuous_speech_recognition = true) {
    is_doing_speech_synthesis = true;
    disable_recognition_button();

    const script = new SpeechSynthesisUtterance(content);
    script.pitch = pitch;
    script.rate = speed;
    script.volume = volume;
    speechSynthesis.speak(script);

    script.onend = () => {
        if (!will_keep_speaking_after_this_function) {
            is_doing_speech_synthesis = false;
        }
        change_send_button_status();
        if (!will_keep_speaking_after_this_function || allow_continuous_speech_recognition) {
            enable_recognition_button();
        }
        if (continuous_speech_recognition_user_setting && !will_keep_speaking_after_this_function && allow_continuous_speech_recognition && !is_requested_by_text && !recognition_error_happened) {
            click_recognition_button();
        }
    };
}

function add_chat(content, is_user = false, is_youtube = false) {
    let class_names = [];
    if (is_user) {
        class_names.push("user");
    }
    if (is_youtube) {
        class_names.push("video");
        content = `<iframe src="https://www.youtube.com/embed/${content}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
    }

    document.getElementById("chat_area").insertAdjacentHTML("beforeend", `<div class="chat_outer ${class_names.join(" ")}"><div class="chat">${content}</div></div>`);
    const chat_area_element = document.getElementById("chat_area");
    chat_area_element.scrollTop = chat_area_element.scrollHeight;
}

function chat_and_speak(chat_content, speak_content = "") {
    if (speak_content === undefined) {
        speak_content = chat_content;
    }
    add_chat(chat_content);
    start_speak(speak_content);
}

function recognition_error(error_str) {
    recognition_error_happened = true;
    const recognition_error_table = {
        "aborted": "音声認識を終了しました。",
        "no-speech": "認識可能な音声を検出できませんでした。",
        "network": "音声認識を使用するにはネット接続が必要です。",
        "audio-capture": "オーディオキャプチャーに失敗しました。",
        "not-allowed": "音声入力が許可されていません。設定を確認して下さい。",
        "service-not-allowed": "必要な音声サービスが許可されていませんでした。",
        "language-not-supported": "サポートされていない言語です。",
        "bad-grammar": "内部処理の文法にエラーがありました。"
    };

    if (error_str === "aborted") {
        if (auto_recognition_abort) {
            auto_recognition_abort = false;
            enable_recognition_button();
        } else {
            chat_and_speak(recognition_error_table[error_str]);
        }
    } else if (recognition_error_table[error_str]) {
        chat_and_speak(recognition_error_table[error_str]);
    } else {
        const error_message = "音声認識の際に不明なエラーが発生しました。";
        chat_and_speak(error_message + "<br><br>エラーメッセージ:<br>" + error_str, error_message)
    }
}

function click_recognition_button() {
    document.getElementById("start_recognition").click();
}

function enable_recognition_button() {
    document.getElementById("start_recognition").disabled = false;
}

function disable_recognition_button() {
    document.getElementById("start_recognition").disabled = true;
}

async function response(content) {
    document.body.style.cursor = "progress";

    query_history.unshift(content);
    add_chat(content, true);

    const script = await eel.make_response(content)();
    if (script.length === 3) {
        start_speak(script[0], false, script[2]);
    } else {
        start_speak(script[0]);
    }
    add_chat(script[1], false);

    document.body.style.cursor = "default";
}

async function read_setting() {
    continuous_speech_recognition_user_setting = (await eel.read_setting("continuous_speech_recognition")() == "True");

    pitch = Number(await eel.read_setting("pitch")());
    speed = Number(await eel.read_setting("speed")());
    volume = Number(await eel.read_setting("volume")());
}

function listening_status(status = false) {
    if (status !== undefined) {
        if (status) {
            document.getElementById("listening_message").style.opacity = 1;
            document.getElementById("start_recognition").classList.add("listening");
            is_listening = true;
        } else {
            document.getElementById("listening_message").style.opacity = 0;
            document.getElementById("start_recognition").classList.remove("listening");
            is_listening = false;
        }
        return is_listening;
    } else {
        return is_listening;
    }
}

function start_recognition() {
    recognition_error_happened = false;
    if (!is_doing_speech_synthesis) {
        is_requested_by_text = false;
        if (listening_status()) {
            recognition.abort();
            listening_status(false);
        } else if (request_form != document.activeElement) {
            recognition.start();
            listening_status(true);
        }
    }
}

function change_send_button_status() {
    const send_button = start_button;

    send_button.disabled = !(request_form.value && !is_doing_speech_synthesis);
    if (listening_status()) {
        auto_recognition_abort = true;
        click_recognition_button();
    }
}

let pitch = 1;
let speed = 1;
let volume = 1;
let continuous_speech_recognition_user_setting = false;
read_setting();

let is_requested_by_text = false;
let is_doing_speech_synthesis = false;
let is_listening = false;
let recognition_error_happened = false;
let auto_recognition_abort = false;
let query_history = [];
let query_history_index = 0;

const request_form = document.getElementById("requestForm");
const start_button = document.getElementById("startButton");

start_button.addEventListener("click", function () {
    if (!is_doing_speech_synthesis) {
        response(request_form.value);
        request_form.value = "";
        is_requested_by_text = true;
        change_send_button_status();
    }
});

SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
const recognition = new SpeechRecognition();
recognition.onresult = () => {
    response(event.results[0][0].transcript);
    listening_status(false);
};

recognition.onaudioend = () => {
    if (!is_doing_speech_synthesis) {
        disable_recognition_button();
        listening_status(false);
    }
};

recognition.onnomatch = () => {
    chat_and_speak("音声を正しく認識できませんでした。もう一度試してみて下さい。");
};

recognition.onerror = (event) => {
    recognition_error(event.error);
};

recognition.onspeechstart = () => {
    document.getElementById("user_speaking_status").style.opacity = "1";
};

recognition.onspeechend = () => {
    document.getElementById("user_speaking_status").style.opacity = "0";
};

Mousetrap.bind({
    "space": () => {
        if (request_form != document.activeElement) {
            click_recognition_button();
        }
    },
    "enter": () => {
        start_button.click();
    },
    "up": () => {
        if (request_form === document.activeElement) {
            if (query_history.length != false) {
                if (query_history_index < query_history.length) {
                    query_history_index += 1;
                }
                request_form.value = query_history[query_history_index - 1];
            }
            change_send_button_status();
        }
    },
    "down": () => {
        if (request_form === document.activeElement) {
            if (query_history_index > 0) {
                query_history_index -= 1;
            }
            request_form.value = query_history[query_history_index - 1];
            if (query_history_index === 0) {
                request_form.value = "";
            }
            change_send_button_status();
        }
    },
    "/": () => {
        event.preventDefault();
        request_form.shadowRoot.querySelector("input").focus();
    },
    "s": () => {
        event.preventDefault();
        request_form.shadowRoot.querySelector("input").focus();
    },
    "esc": () => {
        if (document.activeElement === request_form) {
            request_form.shadowRoot.querySelector("input").blur();
        }
    }
});
