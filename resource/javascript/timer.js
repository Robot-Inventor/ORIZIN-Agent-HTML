fitty("#time div");

eel.expose(update_time);
eel.expose(play_time_up_sound);
eel.expose(timer_status);
eel.expose(set_time);
eel.expose(reset_status);

let hour = 0;
let minute = 0;
let second = 10;
let is_reseted = false;
let is_stopped = false;
let is_first_start = true;
let is_finished = false;

function update_time(time) {
    document.querySelector("#time div").textContent = time;
    if (time.match("0+:0+:0+")) {
        document.querySelector("#time div").classList.add("blink");
        is_finished = true;
    }
}

function timer_status() {
    if (is_stopped) {
        return "stopped"
    } else {
        return "started"
    }
}

function reset_status() {
    const result = is_reseted;
    is_reseted = false;
    return result
}

function set_time() {
    update_time(hour + ":" + minute + ":" + second);
}

window.addEventListener("load", () => {
    let settings = new Object;
    const pair = location.search.substring(1).split("&");
    for (var i = 0; pair[i]; i++) {
        var kv = pair[i].split("=");
        settings[kv[0]] = kv[1];
    }
    hour = settings.h;
    minute = settings.m;
    second = settings.s;
    if (hour + minute + second != 0) {
        update_time(hour + ":" + minute + ":" + second);
        document.getElementById("time_setting_outer").style.top = "-100vh";
        document.getElementById("hour").value = hour;
        document.getElementById("minute").value = minute;
        document.getElementById("second").value = second;
    }
});

function reset() {
    if (!is_first_start) {
        is_reseted = true;
    }
    if (is_finished) {
        is_reseted = false;
        is_finished = false;
    }
    display_stopped_timer();
    document.querySelector("#time div").classList.remove("blink");
    set_time();
    is_first_start = true;
}

function display_stopped_timer() {
    document.querySelector("#time div").classList.add("blink");
    document.getElementById("start").textContent = "スタート";
    document.getElementById("circle").addEventListener("click", display_started_timer);
    document.getElementById("start").addEventListener("click", display_started_timer);
    document.getElementById("time").addEventListener("click", display_started_timer);
    is_stopped = true;
}

function display_started_timer() {
    document.querySelector("#time div").classList.remove("blink");
    document.getElementById("start").textContent = "ストップ";
    document.getElementById("circle").addEventListener("click", display_stopped_timer);
    document.getElementById("start").addEventListener("click", display_stopped_timer);
    document.getElementById("time").addEventListener("click", display_stopped_timer);
    if (is_first_start) {
        const sound = new Audio("");
        sound.play();
        eel.timer(hour, minute, second);
    }
    is_stopped = false;
    is_first_start = false;
}

function play_time_up_sound() {
    const sound = new Audio("../sound/timer.mp3");
    sound.play();
    sound.addEventListener("ended", function () {
        if (is_stopped === false) {
            sound.currentTime = 0;
            sound.play();
        } else {
            document.querySelector("#time div").classList.remove("blink");
            reset();
        }
    }, false);
}

function submit_time() {
    document.getElementById("time_setting_outer").style.top = "-100vh";
    const hour_setting = document.getElementById("hour").value;
    const minute_setting = document.getElementById("minute").value;
    const second_setting = document.getElementById("second").value;
    update_time(hour_setting + ":" + minute_setting + ":" + second_setting);
    hour = hour_setting;
    minute = minute_setting;
    second = second_setting;
    is_reseted = false;
}
