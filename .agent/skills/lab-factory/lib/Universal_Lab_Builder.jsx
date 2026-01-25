/**
 * Universal_Lab_Builder.jsx
 * 
 * CORE ENGINE for Antigravity Lab Factory.
 * CONSUMER of Audition Automation Toolkit.
 * 
 * Function:
 * Interprets a "Manifest" object and creates a session using the 
 * atomic capabilities of the Audition.jsx library.
 */

#include "env_context.jsx"
#include "Audition.jsx"

var UniversalLabBuilder = (function () {

    var PROJECT_ROOT = EnvContext.getProjectRoot();
    var LOG_FILE_PATH = PROJECT_ROOT + "/logs/execution_errors.log";

    // ---------------------------------------------------------
    // Private: Logging
    // ---------------------------------------------------------
    function log(type, msg) {
        var logFile = new File(LOG_FILE_PATH);
        logFile.encoding = "UTF-8";
        logFile.open("a");
        logFile.writeln(new Date().toString() + " [" + type + "]: " + msg);
        logFile.close();
    }

    function logError(msg) { log("ERROR", msg); }
    function logInfo(msg) { log("INFO", msg); }

    // ---------------------------------------------------------
    // Public: Build Function
    // ---------------------------------------------------------
    function build(manifest) {
        logInfo("Starting build for manifest: " + manifest.sessionName);

        try {
            // 1. Session Setup
            var session = Audition.Session.findFirst();
            if (!session) {
                var templatePath = PROJECT_ROOT + "/docs/templates/Blank_48k.sesx";
                if (new File(manifest.templatePath).exists) templatePath = manifest.templatePath;

                if (!new File(templatePath).exists) {
                    var err = "Template missing: " + templatePath;
                    logError(err);
                    alert(err);
                    return;
                }

                // Strategy: Copy-on-Write (Prevent Template Pollution)
                var sessionsDir = new Folder(PROJECT_ROOT + "/docs/sessions");
                if (!sessionsDir.exists) sessionsDir.create();

                // Use manifest name or timestamp for unique session file
                var timestamp = new Date().getTime();
                var safeSessionName = (manifest.sessionName || "Lab_Session") + "_" + timestamp;
                var targetSessionPath = sessionsDir.fsName + "/" + safeSessionName + ".sesx";

                var templateFile = new File(templatePath);
                if (templateFile.copy(targetSessionPath)) {
                    logInfo("Template copied to: " + targetSessionPath);
                    Audition.IO.importFile(targetSessionPath);
                } else {
                    logError("Failed to copy template to: " + targetSessionPath);
                    // Fallback (Risky but necessary if copy fails)
                    Audition.IO.importFile(templatePath);
                }

                // Re-check
                session = Audition.Session.findFirst();
                if (!session) {
                    // One small wait for slow machines
                    $.sleep(1000);
                    session = Audition.Session.findFirst();
                }

                if (!session) {
                    var err = "Failed to open Multitrack Session Template.";
                    logError(err);
                    alert(err);
                    return;
                }
                logInfo("Session opened: " + session.name);
            }

            // 2. Asset Population
            var failures = [];

            for (var i = 0; i < manifest.assets.length; i++) {
                var item = manifest.assets[i];
                var fullPath = PROJECT_ROOT + item.path;

                // A. Validate File
                if (!new File(fullPath).exists) {
                    failures.push(item.name + " (File not found)");
                    continue;
                }

                // B. Import via Toolkit
                var waveDoc = Audition.IO.importFile(fullPath);
                if (!waveDoc) {
                    failures.push(item.name + " (Import failed)");
                    continue;
                }

                // C. Get/Create Track via Toolkit
                var track = null;
                try {
                    var tIdx = (item.trackIndex !== undefined) ? item.trackIndex : i;
                    track = Audition.Track.getOrCreate(session, tIdx);
                } catch (e) {
                    failures.push(item.name + " (Track Access Error)");
                    continue;
                }

                if (!track) {
                    failures.push(item.name + " (Manual Import Required: Track creation limit)");
                    continue;
                }

                // D. Configure Track & Clip via Toolkit
                try {
                    Audition.Track.setName(track, item.trackName || item.name);
                    Audition.Track.setControls(track, !!item.mute, !!item.solo);

                    if (track.audioClips) {
                        var startTime = (item.startTime !== undefined) ? item.startTime : 0;
                        var clip = Audition.Clip.addToTrack(track, waveDoc, startTime);

                        if (clip && item.color) {
                            Audition.Clip.setColor(clip, item.color);
                        }
                    }
                } catch (e) {
                    failures.push(item.name + " (Clip Placement Error: " + e.message + ")");
                }

                // E. Optional Markers via Toolkit
                if (item.markers) {
                    for (var m = 0; m < item.markers.length; m++) {
                        var mk = item.markers[m];
                        Audition.Markers.addCycle(session, mk.name, mk.start, mk.duration);
                    }
                }
            }

            // 3. Final Report
            if (failures.length > 0) {
                var msg = "Lab Setup Complete with Issues:\n" + failures.join("\n");
                logError(msg);
                alert(msg);
            } else {
                logInfo("Lab Setup Success: " + manifest.sessionName);
                alert("Lab Setup Complete: " + manifest.sessionName);
            }

        } catch (e) {
            logError("CRITICAL BUILDER ERROR: " + e.toString());
            alert("Builder Error: " + e.toString());
        }
    }

    return { build: build };
})();
