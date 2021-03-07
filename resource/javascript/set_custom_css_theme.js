let css_data = {};

async function check_current_css_theme_information() {
    css_data = await eel.check_current_css_theme_information()();
    const swatches_values = [
        "rgb(244, 67, 54)",
        "rgb(233, 30, 99)",
        "rgb(156, 39, 176)",
        "rgb(103, 58, 183)",
        "rgb(63, 81, 181)",
        "rgb(33, 150, 243)",
        "rgb(3, 169, 244)",
        "rgb(0, 188, 212)",
        "rgb(0, 150, 136)",
        "rgb(76, 175, 80)",
        "rgb(139, 195, 74)",
        "rgb(205, 220, 57)",
        "rgb(255, 235, 59)",
        "rgb(255, 193, 7)"
    ];
    const components_values = {
        preview: true,
        opacity: true,
        hue: true,
        interaction: {
            hex: true,
            rgba: true,
            hsla: true,
            hsva: true,
            cmyk: true,
            input: true,
            clear: true,
            save: true,
            cancel: true
        }
    };
    const i18n_values = {
        "btn:save": "決定",
        "btn:clear": "リセット",
        "btn:cancel": "キャンセル"
    };
    const bg = Pickr.create({
        el: "#bg",
        theme: "classic",
        default: css_data["--bg"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    bg.on("save", (color, instance) => {
        css_data["--bg"] = color.toHEXA().toString();
        bg.hide();
    });

    const card_bg = Pickr.create({
        el: "#card_bg",
        theme: "classic",
        default: css_data["--card_bg"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    card_bg.on("save", (color, instance) => {
        css_data["--card_bg"] = color.toHEXA().toString();
        card_bg.hide();
    });

    const text = Pickr.create({
        el: "#text",
        theme: "classic",
        default: css_data["--text"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    text.on("save", (color, instance) => {
        css_data["--text"] = color.toHEXA().toString();
        text.hide();
    });

    const shadow = Pickr.create({
        el: "#shadow",
        theme: "classic",
        default: css_data["--shadow"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    shadow.on("save", (color, instance) => {
        css_data["--shadow"] = color.toHEXA().toString();
        shadow.hide();
    });

    const theme_color = Pickr.create({
        el: "#theme_color",
        theme: "classic",
        default: css_data["--theme_color"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    theme_color.on("save", (color, instance) => {
        css_data["--theme_color"] = color.toHEXA().toString();
        theme_color.hide();
    });

    const header_background_color = Pickr.create({
        el: "#header_background_color",
        theme: "classic",
        default: css_data["--header_background_color"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    header_background_color.on("save", (color, instance) => {
        css_data["--header_background_color"] = color.toHEXA().toString();
        header_background_color.hide();
    });

    const error_text_color = Pickr.create({
        el: "#error_text_color",
        theme: "classic",
        default: css_data["--error_text_color"],
        swatches: swatches_values,
        components: components_values,
        i18n: i18n_values
    });
    error_text_color.on("save", (color, instance) => {
        css_data["--error_text_color"] = color.toHEXA().toString();
        error_text_color.hide();
    });
}

check_current_css_theme_information();

window.addEventListener("beforeunload", function () {
    eel.write_custom_css_theme(css_data);
    eel.change_theme("theme/user/custom_theme.css");
});
