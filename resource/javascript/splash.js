async function move_to_top_page() {
    const is_setup_finished = await eel.read_setting("setup_finished")();
    const place = is_setup_finished ? "index.html" : "setup.html";
    eel.print_log_if_dev_mode("Move to next page.", { "IsFinishedSetup": is_setup_finished, "Page": place });
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
