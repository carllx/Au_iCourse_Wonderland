/**
 * create_template.jsx
 * 
 * Helper script to generate a standard blank session template.
 * Run this ONCE to create the "docs/templates/Blank_48k.sesx" file.
 */

var DOCS_PATH = new File($.fileName).parent.parent.fsName + "/docs/templates";

function main() {
    var folder = new Folder(DOCS_PATH);
    if (!folder.exists) {
        folder.create();
    }

    var templatePath = DOCS_PATH + "/Blank_48k.sesx";
    var templateFile = new File(templatePath);

    if (templateFile.exists) {
        alert("Template already exists at:\n" + templatePath);
        return;
    }

    // Try to create a new session via API (if supported)
    // If not supported, we alert the user to save one manually.
    var session = null;
    try {
        session = app.documents.addMultitrackDocument("Blank_48k");
    } catch (e) {
        alert("Could not auto-create session. Please manually:\n1. File > New > Multitrack Session\n2. Name it 'Blank_48k'\n3. Save to: " + templatePath);
        return;
    }

    if (session) {
        // Save it (if API allows saving)
        // Note: SaveAs via script is also tricky in older APIs
        alert("Session Created!\n\nPlease manually SAVE AS to:\n" + templatePath);
    }
}

main();
