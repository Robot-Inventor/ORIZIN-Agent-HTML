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

function toggle_switch_component() {
    toggle_element_num = 0;
    document.querySelectorAll("input[type=checkbox].toggle").forEach(function(toggle_element) {
        toggle_id = toggle_element.getAttribute("id");
        if (!toggle_id) {
            toggle_element.setAttribute("id", "toggle_element_" + toggle_element_num);
            toggle_id = "toggle_element_" + toggle_element_num;
            toggle_element_num += 1;
        }
        toggle_element.insertAdjacentHTML("afterend", "<label for='" + toggle_id + "' class='ripple_effect'></label>");
    });
}

function underline_textbox_cmponent() {
    input_element_num = 0;
    document.querySelectorAll("input[type=text].underline_textbox").forEach(function(input_element) {
        input_group_id = "input_group_" + input_element_num;
        input_element.insertAdjacentHTML("afterend", "<div class='text_input_group' id='" + input_group_id + "'><div class='text_underline'></div></div>");
        text_input_group = document.querySelector("div.text_input_group#" + input_group_id);
        text_input_group.insertBefore(input_element, document.querySelector("div.text_input_group#" + input_group_id + " div.text_underline"));
        input_element_num += 1;
    });
}

$(function() {
    $("header").load("basic.html");
    eel.print_log_if_dev_mode("Page header loaded.", {"Status": "OK"});
    $.ripple(".ripple_effect", {
        debug: false,
        on: 'mousedown',
        opacity: 0.4,
        color: "auto",
        multi: false,
        duration: 0.7,
        rate: function(pxPerSecond) {
            return pxPerSecond;
        },
        easing: 'linear'
    });
    readable_text_setting();
    toggle_switch_component();
    underline_textbox_cmponent();
    eel.print_log_if_dev_mode("Page rendered.", {"File": location.pathname});
});
