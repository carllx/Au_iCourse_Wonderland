/**
 * probe_api_methods.jsx
 * 
 * Diagnostic script to find correct API syntax for Audition 2024.
 * Logs to Desktop/api_probe.log
 */

function probe() {
    var logFile = new File(Folder.desktop + "/api_probe.log");
    logFile.open("w");
    function log(msg) { logFile.writeln(msg); }

    try {
        log("--- Starting API Probe (Phase 3: System Call) ---");

        // Check system.callSystem
        try {
            if (typeof system !== "undefined" && typeof system.callSystem === "function") {
                log("system.callSystem is available.");
                var ret = system.callSystem("echo 'hello'");
                log("system.callSystem result: " + ret);
            } else {
                log("system.callSystem unavailable.");
            }
        } catch (e) { log("Error checking system.callSystem: " + e.message); }

        // Check app.system (Photoshop style)
        try {
            if (typeof app.system === "function") {
                log("app.system is available.");
                var ret = app.system("echo 'hello'");
                log("app.system result: " + ret);
            } else {
                log("app.system unavailable.");
            }
        } catch (e) { log("Error checking app.system: " + e.message); }


    } catch (e) {
        log("CRITICAL: " + e.toString());
    } finally {
        logFile.close();
        alert("Probe Complete. Check Desktop/api_probe.log");
    }
}

probe();
