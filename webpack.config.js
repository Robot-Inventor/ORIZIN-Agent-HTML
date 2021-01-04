const path = require("path");

module.exports = {
    mode: "production",
    entry: "./resource/javascript/import.js",
    output: {
        filename: "bundle.js",
        path: path.join(__dirname, "resource/javascript")
    },
    optimization: {
        minimize: false
    }
};
