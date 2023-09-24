const fs = require('fs')
const {JSDOM, ResourceLoader} = require("jsdom");

let userAgent = process.argv[3]

const {window} = new JSDOM(``, {
    url: process.argv[2],
    referrer: process.argv[2],
    contentType: "text/html",
    runScripts: "outside-only",
    includeNodeLocations: false,
    pretendToBeVisual: true,
    resources: new ResourceLoader({userAgent})
});

window.eval(fs.readFileSync(__dirname + "/hsw.js", "utf-8"))

window.run(process.argv[4]).then(function (result) {
    console.log(result)
})