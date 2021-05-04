async function insert_license() {
    const fetch_response = await fetch("../json/oss_license.json");
    const response_content = await fetch_response.json();

    Object.keys(response_content).forEach((oss_name) => {
        document.getElementById("license_section").insertAdjacentHTML("beforeend", `
<details>
    <summary class="ripple_effect">${oss_name} ${response_content[oss_name].version}</summary>
    <pre>${response_content[oss_name].license}</pre>
    <a href="${response_content[oss_name].repository}" target="_blank" rel="noopener noreferrer"><mwc-button label="リポジトリーを開く" icon="open_in_new" trailingIcon></mwc-button></a>
</details>
        `);
    });

    document.getElementById("license_section").insertAdjacentHTML("beforeend", await eel.generate_node_license_report()());
}

insert_license();
