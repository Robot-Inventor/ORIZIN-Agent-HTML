async function move_to_top_page() {
    const is_finished_setup = await eel.read_setting("setup_finished")();
    const place = is_finished_setup == "False" ? "setup.html" : "index.html";
    eel.print_log_if_dev_mode("Move to next page.", { "IsFinishedSetup": is_finished_setup, "Page": place });
    location.replace(place);
}

if (!("speechSynthesis" in window)) {
    alert("ご利用のブラウザは音声合成(TTS / Text To Speech)に対応していません。Web Speech APIに対応した最新のブラウザをお使いください。")
}

if (!("webkitSpeechRecognition" in window)) {
    alert("ご利用のブラウザは音声認識(Speech To Text / STT / Speech Recognition)に対応していません。Web Speech APIに対応した最新のブラウザをお使いください。")
}

setTimeout(() => {
    move_to_top_page();
}, 2000);
