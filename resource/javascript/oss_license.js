async function insert_license() {
    document.getElementById("license_section").insertAdjacentHTML("beforeend", await eel.generate_node_license_report()());
}

insert_license();
