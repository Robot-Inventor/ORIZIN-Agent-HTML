class ExperimentCard extends HTMLElement {
    constructor() {
        super();

        const shadow = this.attachShadow({ mode: "open" });

        const section = document.createElement("section");

        this.icon_element = document.createElement("mwc-icon");
        this.icon_element.textContent = this.getAttribute("icon");

        const top_outer = document.createElement("div");
        top_outer.setAttribute("id", "top_outer");

        this.experiment_title = document.createElement("span");
        this.experiment_title.textContent = this.getAttribute("experiment-title");

        this.mwc_switch = document.createElement("mwc-switch");
        this.read_flag(this.getAttribute("experiment-name"));
        this.mwc_switch.addEventListener("change", () => {
            eel.set_flag(this.getAttribute("experiment-name"), this.mwc_switch.checked);
        });

        const information = document.createElement("slot");
        information.setAttribute("class", "information");

        const style = document.createElement("style");
        style.textContent = `
section {
    border-bottom: solid 0.05em var(--text);
    padding: 1em;
    padding-left: 0;
    font-weight: bold;
    display: grid;
    grid-template-columns: 2rem;
}

mwc-icon {
    --mdc-icon-size: 1.5rem;
    color: inherit;
    grid-row: 1;
    grid-column: 1;
}

#top_outer {
    grid-row: 1;
    grid-column: 2;
}

mwc-switch {
    margin-left: 1rem;
}

.information {
    font-weight: normal;
    font-size: 0.9em;
    opacity: 0.7;
    color: var(--text);
    display: block;
    grid-row: 2;
    grid-column: 2;
}
        `;

        top_outer.appendChild(this.experiment_title);
        top_outer.appendChild(this.mwc_switch);

        section.appendChild(this.icon_element);
        section.appendChild(top_outer);
        section.appendChild(information);
        shadow.appendChild(section);
        shadow.appendChild(style);
    }

    async read_flag(flag_name) {
        const flag_value = await eel.read_flag(flag_name)();
        this.mwc_switch.checked = flag_value;
    }

    static get observedAttributes() {
        return ["icon", "experiment-title", "experiment-name"];
    }

    attributeChangedCallback(name, old_value, new_value) {
        switch (name) {
            case "icon":
                this.icon_element.textContent = new_value;
                break;

            case "experiment-title":
                this.experiment_title.textContent = new_value;
                break;

            case "experiment-name":
                this.read_flag(this.getAttribute("experiment-name"));
                this.mwc_switch.addEventListener("change", () => {
                    eel.set_flag(this.getAttribute("experiment-name"), this.mwc_switch.checked);
                });
                break;
        }
    }

    get icon() {
        return this.icon_element.textContent;
    }

    set icon(value) {
        this.setAttribute("icon", value);
    }

    get experimentTitle() {
        return this.experiment_title.textContent;
    }

    set experimentTitle(value) {
        this.setAttribute("experiment-title", value);
    }

    get experimentName() {
        return this.getAttribute("experiment-name");
    }

    set experimentName(value) {
        this.setAttribute("experiment-name", value);
    }
}

customElements.define("experiment-card", ExperimentCard);
