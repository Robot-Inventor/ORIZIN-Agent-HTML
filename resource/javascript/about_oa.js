async function load_info() {
    const information = await load_json("../information.json");
    Object.keys(information).forEach((key) => {
        document.getElementById("information").insertAdjacentText("beforeend", `${key}: ${information[key]}\n`);
    });
}

load_info();

document.getElementById("open_splash_screen_button").addEventListener("click", function () {
    const screen_width = screen.availWidth;
    const screen_height = screen.availHeight;
    const window_option = `top=${screen_height / 4}, left=${screen_width / 4}, width=${screen_width / 2}, height=${screen_height / 2}`;
    window.open("information.html", "_blank", window_option);
});

const copy_button = document.getElementById("copy_information_button");
let change_copy_button_timer;
copy_button.addEventListener("click", () => {
    clearTimeout(change_copy_button_timer);
    navigator.clipboard.writeText(document.getElementById("information").textContent);
    document.getElementById("copied_message_snackbar").show();
    copy_button.icon = "checked";
    change_copy_button_timer = setTimeout(() => {
        copy_button.icon = "content_copy";
    }, 5000);
});
