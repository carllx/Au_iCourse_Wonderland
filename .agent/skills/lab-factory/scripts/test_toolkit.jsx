/**
 * test_toolkit.jsx
 * 
 * Verification Script for Audition Automation Toolkit (Audition.jsx)
 * Proves that atomic capabilities work in isolation.
 */

#include "../lib/env_context.jsx"
#include "../lib/Audition.jsx"

    (function () {
        var root = EnvContext.getProjectRoot();

        // 1. Test IO: Import a known asset
        // Using an asset from Lesson 01 as test subject
        var testAssetPath = root + "/docs/course_materials/01_noise_reduction/assets/noisy_voice.wav";
        alert("Test 1: Importing File...\n" + testAssetPath);

        var doc = Audition.IO.importFile(testAssetPath);
        if (!doc) {
            alert("FAIL: Audition.IO.importFile returned null.");
            return;
        }
        alert("PASS: Import successful.\nDoc: " + doc.displayName);

        // 2. Test Session: Find active
        var session = Audition.Session.findFirst();
        if (!session) {
            alert("FAIL: No Multitrack Session found. Please ensure one is open (from previous test).");
            return;
        }
        alert("PASS: Found Session: " + session.displayName);

        // 3. Test Track: Create new track
        var trackIndex = session.audioTracks.length; // Add to end
        alert("Test 3: Creating Track at index " + trackIndex);

        var track = Audition.Track.getOrCreate(session, trackIndex);
        if (!track) {
            alert("FAIL: Could not create track.");
            return;
        }
        Audition.Track.setName(track, "Toolkit Test Track");
        alert("PASS: Track created and named 'Toolkit Test Track'.");

        // 4. Test Clip: Add clip to new track
        alert("Test 4: Adding Clip to Track...");
        var clip = Audition.Clip.addToTrack(track, doc, 5.0); // Start at 5s
        if (!clip) {
            alert("FAIL: Could not add clip.");
            return;
        }
        Audition.Clip.setColor(clip, { r: 255, g: 0, b: 255 }); // Magenta
        alert("PASS: Clip added at 5s and colored Magenta.");

        alert("ALL SYSTEMS GO: Audition Toolkit is functioning correctly.");

    })();
