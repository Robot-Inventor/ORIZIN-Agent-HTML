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
    const fetch_response = await fetch("../information.txt");
    const information_content = await fetch_response.text();

    document.getElementById("information_area").innerHTML = information_content.replace(/\n/g, "<br>");

    const version_information = information_content.match(/Version:.*/)[0].replace("Version:", "");
    const release_data = version_information.indexOf("dev") === -1 ? await eel.get_release("stable")() : await eel.get_release("develop")();
    const latest_version = compare_and_return_latest_version_num(version_information, release_data[0]);

    document.getElementById("update_status").innerHTML = version_information === latest_version ? "<i class='material_icon'>check_circle_outline</i>最新版をご利用中です。" : `<a href="https://github.com/Robot-Inventor/ORIZIN-Agent-HTML/releases/tag/${latest_version}" target="_blank" rel="noopener noreferrer">${latest_version}</a>にアップデート可能です。`
}

load_information();
