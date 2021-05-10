class WarningMessage extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({ mode: "open" });

        this.slot_element = document.createElement("slot");

        const icon_element = document.createElement("i");
        icon_element.setAttribute("class", "material_icon");
        icon_element.textContent = "warning";

        const style_element = document.createElement("style");
        style_element.textContent = `
:host {
    display: block;
}

* {
    color: var(--error_text_color);
    font-weight: bold;
}

i.material_icon {
    font-family: "Material Icons";
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    transform: translateY(0.15em);
    margin: 0 0.4em 0 0;
}
        `;

        shadow.appendChild(icon_element);
        shadow.appendChild(this.slot_element);
        shadow.appendChild(style_element);
    }
}

customElements.define("warning-message", WarningMessage);
