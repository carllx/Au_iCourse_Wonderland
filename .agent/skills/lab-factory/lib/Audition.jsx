/**
 * Audition.jsx
 * 
 * THE AUDITION AUTOMATION TOOLKIT
 * "Atomic Capabilities for the Industrial Machine"
 * 
 * Description:
 * A stateless, modular library for automating Adobe Audition.
 * De-couples low-level API mechanics from high-level scenario logic.
 * 
 * Usage:
 * #include "Audition.jsx"
 * Audition.IO.importFile("/path/to/file.wav");
 * Audition.Track.getOrCreate(session, 0, "MyTrack");
 */

var Audition = (function () {

    // -------------------------------------------------------------
    // MODULE: IO (Input/Output & robustImport)
    // -------------------------------------------------------------
    var IO = (function () {

        function findOpenDocument(pathObj) {
            if (!app.documents) return null;
            var path = pathObj.fsName;
            var name = pathObj.displayName;

            for (var i = 0; i < app.documents.length; i++) {
                var d = app.documents[i];
                // Strict check: if looking for WAV/Audio, ignore Multitrack documents
                if (pathObj.name.match(/\.(wav|mp3|aif)$/i)) {
                    try { if (d.reflect.name == "MultitrackDocument") continue; } catch (e) { }
                }

                if (d.path === path || d.displayName === name) return d;
                try { if (d.fullName === path) return d; } catch (e) { }
                try { if (d.reflect.name == "MultitrackDocument" && d.path == path) return d; } catch (e) { }
            }
            return null;
        }

        /**
         * Robustly imports a file into Audition.
         * Handles .sesx (Sessions), .wav (Audio), and applies the "Nuclear Fix"
         * (OS-level execution) if standard APIs fail.
         */
        function importFile(pathString) {
            var fileObj = new File(pathString);
            if (!fileObj.exists) {
                return null;
            }
            var doc = findOpenDocument(fileObj);
            if (doc) return doc;


            // Strategy 1: Project Import (Best for Audio Assets, keeps UI clean)
            if (!pathString.match(/\.sesx$/i)) {
                try {
                    if (app.project && app.project.importFiles) {
                        if (app.project.importFiles([fileObj.fsName])) {
                            doc = findOpenDocument(fileObj);
                            if (doc) return doc;
                            if (app.activeDocument) return app.activeDocument;
                        }
                    }
                } catch (e) { }
            }

            // Strategy 2: openDocument (Standard API)
            try {
                doc = app.openDocument(fileObj.fsName);
                if (doc) return doc;
            } catch (e) { }

            // Strategy 3: openDocument Fallback (Standard)
            try {
                // Legacy method (fails in 2024)
                // doc = app.openDocument(fileObj); 
            } catch (e) { }

            // Strategy 3.1: Strict Parameter Open (Audition 2024 Fix)
            // The "Illegal Parameter" error occurs because 2024 demands a specific object, not a string.
            try {
                if (typeof DocumentOpenParameter !== "undefined") {
                    var params = new DocumentOpenParameter();
                    params.path = fileObj.fsName;
                    doc = app.openDocument(params);
                    if (doc) return doc;
                }
            } catch (e) { }

            // Strategy 4: The Nuclear Option (OS Execute + Wait Loop)
            // Solves "Illegal Parameter" errors in Audition 2024 for SESSIONS only.
            // WARNING: Do NOT run this on WAVs, or it will open Apple Music!
            try {
                if (fileObj.name.match(/\.sesx$/i)) {
                    var executed = fileObj.execute();
                    if (executed) {
                        for (var w = 0; w < 20; w++) {
                            $.sleep(200);
                            doc = findOpenDocument(fileObj);
                            if (doc) return doc;
                        }
                        if (app.activeDocument) return app.activeDocument;
                    }
                }
            } catch (e) { }

            // Failed
            return null;
        }

        return {
            importFile: importFile
        };
    })();

    // -------------------------------------------------------------
    // MODULE: Session (Multitrack Management)
    // -------------------------------------------------------------
    var Session = (function () {

        function getActiveMultitrack() {
            if (!app.documents) return null;
            for (var i = 0; i < app.documents.length; i++) {
                var d = app.documents[i];
                try {
                    if (d.reflect.name === "MultitrackDocument" || typeof d.audioTracks !== "undefined") {
                        return d;
                    }
                } catch (e) { }
            }
            return null;
        }

        function openTemplate(templatePath) {
            return IO.importFile(templatePath);
        }

        return {
            findFirst: getActiveMultitrack,
            openTemplate: openTemplate
        };
    })();

    // -------------------------------------------------------------
    // MODULE: Track (Track Manipulation)
    // -------------------------------------------------------------
    var Track = (function () {

        function getOrCreate(sessionDoc, index) {
            if (!sessionDoc) return null;
            if (index < sessionDoc.audioTracks.length) {
                return sessionDoc.audioTracks[index];
            } else {
                // Fix: add() takes no args or a specific Object type, not a string name.
                // In Audition 2024, this might still fail. safe-fail path:
                try {
                    return sessionDoc.audioTracks.add();
                } catch (e) {
                    return null; // Graceful degradation
                }
            }
        }

        function setName(track, name) {
            if (track) track.name = name;
        }

        function setControls(track, mute, solo, rec) {
            if (!track) return;
            if (typeof mute === 'boolean') track.mute = mute;
            if (typeof solo === 'boolean') track.solo = solo;
            // rec support varies by API version, safe to omit if not strictly needed or wrap in try
        }

        return {
            getOrCreate: getOrCreate,
            setName: setName,
            setControls: setControls
        };
    })();

    // -------------------------------------------------------------
    // MODULE: Clip (Time & Placement)
    // -------------------------------------------------------------
    var Clip = (function () {

        function addToTrack(track, audioDoc, startTime) {
            if (!track || !audioDoc) return null;
            var time = (typeof startTime === 'number') ? startTime : 0;

            try {
                return track.audioClips.add(audioDoc, time);
            } catch (e) {
                return null;
            }
        }

        function setColor(clip, colorObj) {
            if (clip && colorObj) {
                try { clip.color = colorObj; } catch (e) { }
            }
        }

        return {
            addToTrack: addToTrack,
            setColor: setColor
        };
    })();

    // -------------------------------------------------------------
    // MODULE: Markers
    // -------------------------------------------------------------
    var Markers = (function () {
        function addCycle(sessionDoc, name, start, duration) {
            if (!sessionDoc || !sessionDoc.markers) return;
            try {
                var m = sessionDoc.markers.add(start, duration);
                m.name = name;
                m.type = MarkerType.CYCLE;
                return m;
            } catch (e) { return null; }
        }

        return {
            addCycle: addCycle
        };
    })();

    // -------------------------------------------------------------
    // MODULE: Log (Silent Output)
    // -------------------------------------------------------------
    var Log = (function () {
        var SENTINEL_PATH = "/Users/yamlam/Downloads/class_audition_ext/logs/sentinel_simple.txt";

        function sentinel(objOrMsg) {
            try {
                var f = new File(SENTINEL_PATH);
                f.open("w");
                var content = (typeof objOrMsg === 'object') ? JSON.stringify(objOrMsg) : objOrMsg;
                f.writeln(content);
                f.close();
            } catch (e) {
                // Silently fail or try alert if absolutely necessary? 
                // For silent mode, we suppress.
            }
        }
        return { sentinel: sentinel };
    })();

    // -------------------------------------------------------------
    // MODULE: State (Inspection & Cleanup)
    // -------------------------------------------------------------
    var State = (function () {

        /**
         * Returns list of all open documents with metadata.
         * Safe against 'undefined' paths.
         */
        function getOpenDocuments() {
            var results = [];
            if (!app.documents) return results;

            for (var i = 0; i < app.documents.length; i++) {
                var d = app.documents[i];
                var docInfo = {
                    ref: d,
                    name: "Unknown",
                    path: null,
                    type: "Unknown"
                };

                try { docInfo.name = d.displayName; } catch (e) { }
                try { docInfo.path = d.fullName; } catch (e) { }
                try { docInfo.type = d.reflect.name; } catch (e) { }

                results.push(docInfo);
            }
            return results;
        }

        /**
         * Force closes all documents.
         * @param {boolean} force - If true, discards changes (close(0)).
         */
        function closeAll(force) {
            var maxRetries = 3;
            var saveMode = force ? 0 : 2; // 0=NoSave, 2=Prompt(if supported) or Save? verify API. usually 0 is safe-no-save.

            for (var r = 0; r < maxRetries; r++) {
                var docs = app.documents;
                if (!docs || docs.length === 0) break;

                // Reverse iteration
                for (var i = docs.length - 1; i >= 0; i--) {
                    var d = docs[i];
                    try {
                        // Strategy A: Standard close
                        if (d.close) {
                            d.close(saveMode);
                        }
                        // Strategy B: CloseDocument (legacy/alt)
                        else if (d.closeDocument) {
                            d.closeDocument(saveMode);
                        }
                        // Strategy C: Active Document Switch (Stubborn files)
                        else {
                            app.activeDocument = d;
                            if (app.activeDocument.close) app.activeDocument.close(saveMode);
                        }
                    } catch (e) {
                        // Fallback catch
                    }
                }
                $.sleep(200);
            }
        }

        return {
            getOpenDocuments: getOpenDocuments,
            closeAll: closeAll
        };
    })();

    // -------------------------------------------------------------
    // PUBLIC API
    // -------------------------------------------------------------
    return {
        IO: IO,
        Session: Session,
        Track: Track,
        Clip: Clip,
        Markers: Markers,
        State: State,
        Log: Log
    };

})();
