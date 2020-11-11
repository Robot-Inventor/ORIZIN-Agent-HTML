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

async function load_header() {
    const response = await fetch("basic.html");
    const data = await response.text();
    document.querySelector("header").innerHTML = data;
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
}

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

$(function() {
    load_header();
    eel.print_log_if_dev_mode("Page header loaded.", {"Status": "OK"});
    readable_text_setting();
    feed_buck_setting();
    eel.print_log_if_dev_mode("Page rendered.", {"File": location.pathname});
});

const TRANSITION_TIME = 300;

function open_menu() {
    document.getElementById("menu_open_button").style.transform = "rotate(180deg)";
    setTimeout(() => {
        $("#side_menu_bar_overlay").fadeIn(TRANSITION_TIME);
        document.getElementById("side_menu_bar").style.transform = "none";
    }, 50);
    setTimeout(() => {
        document.getElementById("menu_close_button").style.transform = "rotate(180deg)";
    }, 100);
}

function close_menu() {
    document.getElementById("menu_close_button").style.transform = "rotate(0deg)";
    setTimeout(() => {
        $("#side_menu_bar_overlay").fadeOut(TRANSITION_TIME);
        document.getElementById("side_menu_bar").style.transform = "translate(-100%)";
    }, 50);
    setTimeout(() => {
        document.getElementById("menu_open_button").style.transform = "rotate(0deg)";
    }, 100);
}

async function move_page(place) {
    close_menu();
    setTimeout(() => {
        location.href = place;
    }, TRANSITION_TIME);
}

async function feed_buck_setting() {
    if(await eel.read_flag("show_feedback_button")()) {
        document.getElementById("feedback_button").style.display = "block";
    }
}
