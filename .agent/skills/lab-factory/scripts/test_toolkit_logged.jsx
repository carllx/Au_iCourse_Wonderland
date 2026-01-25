/**
 * test_toolkit_logged.jsx
 * 
 * Verifies Audition.jsx and logs results to Desktop.
 */

#include "../lib/env_context.jsx"
#include "../lib/Audition.jsx"

    (function () {
        var logFile = new File(Folder.desktop + "/toolkit_test_results.log");
        logFile.open("w");
        function log(msg) { logFile.writeln(msg); }

        try {
            var root = EnvContext.getProjectRoot();
            log("Root: " + root);

            // 1. Test IO
            var testAssetPath = root + "/docs/course_materials/01_noise_reduction/assets/noisy_voice.wav";
            log("Test 1: Importing " + testAssetPath);

            var doc = Audition.IO.importFile(testAssetPath);
            if (!doc) {
                log("FAIL: Import returned null");
            } else {
                log("PASS: Import success (" + doc.displayName + ")");
            }

            // 2. Test Session
            log("Test 2: finding session");
            var session = Audition.Session.findFirst();
            if (!session) {
                log("FAIL: No Session found");
                // Create one?
            } else {
                log("PASS: Found Session (" + session.name + ")");
            }

            if (session) {
                // 3. Test Track
                log("Test 3: Creating Track");
                var track = Audition.Track.getOrCreate(session, 99); // Force new
                if (!track) {
                    log("FAIL: No track created");
                } else {
                    log("PASS: Track created");
                    Audition.Track.setName(track, "Logged Test Track");
                }

                // 4. Test Clip
                if (track && doc) {
                    log("Test 4: Adding Clip");
                    var clip = Audition.Clip.addToTrack(track, doc, 2.0);
                    if (!clip) {
                        log("FAIL: Clip add failed");
                    } else {
                        log("PASS: Clip added");
                    }
                }
            }

        } catch (e) {
            log("CRITICAL EXCEPTION: " + e.toString());
        } finally {
            logFile.close();
            alert("Logged Test Complete. Check Desktop/toolkit_test_results.log");
        }

    })();
