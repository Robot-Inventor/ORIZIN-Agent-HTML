async function load_info() {
    const fetch_data = await fetch("../information.json");
    const response = await fetch_data.json();
    Object.keys(response).forEach((key) => {
        document.getElementById("information").insertAdjacentText("beforeend", `${key}: ${response[key]}\n`);
    });
}

load_info();

document.getElementById("open_splash_screen_button").addEventListener("click", function () {
    const screen_width = screen.availWidth;
    const screen_height = screen.availHeight;
    const window_option = `top=${screen_height / 4}, left=${screen_width / 4}, width=${screen_width / 2}, height=${screen_height / 2}`;
    window.open("information.html", "_blank", window_option);
});

document.getElementById("copy_information_button").addEventListener("click", () => {
    navigator.clipboard.writeText(document.getElementById("information").textContent);
    document.getElementById("copied_message_snackbar").show();
});
