new Ripple(".ripple_effect");

function compare_and_return_latest_version_num(version1, version2) {
    if (version1 === version2) {
        return version1;
    } else {
        let v1_array = version1.split(".");
        for (let i = 0; i < v1_array.length; i++) {
            v1_array[i] = parseInt(v1_array[i]);
        }
        let v2_array = version2.split(".");
        for (let i = 0; i < v2_array.length; i++) {
            v2_array[i] = parseInt(v2_array[i]);
        }

        if (v1_array[0] < v2_array[0]) {
            return version2;
        } else if (v1_array[0] > v2_array[0]) {
            return version1;
        } else {
            if (v1_array[1] < v2_array[1]) {
                return version2;
            } else if (v1_array[1] > v2_array[1]) {
                return version1;
            } else {
                if (v1_array[2] < v2_array[2]) {
                    return version2;
                } else {
                    return version1;
                }
            }
        }
    }
}

async function load_information() {
    function sanitize(string) {
        const sanitize_table = {
            "&": '&amp;',
            "'": '&#x27;',
            "`": '&#x60;',
            "\"": '&quot;',
            "<": '&lt;',
            ">": '&gt;',
        };
        Object.keys(sanitize_table).forEach((key) => {
            string.replaceAll(key, sanitize_table[key]);
        });
        return string;
    }

    const information_content = await load_json("../information.json");

    const information_area = document.getElementById("information_area");
    information_area.textContent = "";
    Object.keys(information_content).forEach((key) => {
        information_area.insertAdjacentHTML("beforeend", `${key}: ${information_content[key]}<br>`);
    });

    const version_information = sanitize(information_content.Version);
    const release_data = await eel.get_release(information_content.Channel)();
    const latest_version = compare_and_return_latest_version_num(version_information, release_data[0]);

    const update_status = document.getElementById("update_status");
    if (latest_version === version_information) {
        update_status.innerHTML = "<mwc-icon>check_circle_outline</mwc-icon>最新版をご利用中です。";
    } else {
        update_status.innerHTML = `<a href="https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/releases/tag/${latest_version}" target="_blank" rel="noopener noreferrer">${latest_version}</a>にアップデート可能です。`;
    }
}

load_information();
