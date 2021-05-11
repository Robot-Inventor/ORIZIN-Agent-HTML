class WarningMessage extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({ mode: "open" });

        this.slot_element = document.createElement("slot");

        const icon_element = document.createElement("mwc-icon");
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

mwc-icon {
    --mdc-icon-size: 1em;
    transform: translateY(10%);
    margin-right: 0.5em;
    color: var(--error_text_color);
}
        `;

        shadow.appendChild(icon_element);
        shadow.appendChild(this.slot_element);
        shadow.appendChild(style_element);
    }
}

customElements.define("warning-message", WarningMessage);
