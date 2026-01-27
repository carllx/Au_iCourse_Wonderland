/**
 * Setup_Panning_Lab.jsx
 * 
 * MANIFEST for Lesson 04: Stereo Panning (Visceral Panning)
 * Uses Universal_Lab_Builder to generate the session.
 */

#include "../../../../../.agent/skills/lab-factory/lib/Universal_Lab_Builder.jsx"

    (function () {
        var manifest = {
            sessionName: "Panning_Lab_Session",
            templatePath: "../../../templates/Blank_48k.sesx",
            assets: [
                {
                    name: "Reference Mix (Muted)",
                    path: "/docs/course_materials/04_stereo_panning/assets/visceral_mix_reference.wav",
                    trackIndex: 0,
                    mute: true,
                    color: { r: 100, g: 100, b: 100 } // Gray
                },
                {
                    name: "Opponent (Center)",
                    path: "/docs/course_materials/04_stereo_panning/assets/opponent_voice.wav",
                    trackIndex: 1,
                    color: { r: 0, g: 255, b: 0 } // Green
                },
                {
                    name: "Internal Heartbeat",
                    path: "/docs/course_materials/04_stereo_panning/assets/internal_heartbeat_visceral.wav",
                    trackIndex: 2,
                    color: { r: 255, g: 0, b: 0 } // Red
                },
                {
                    name: "The Wall (Low Threat)",
                    path: "/docs/course_materials/04_stereo_panning/assets/external_threat_low_L.wav",
                    trackIndex: 3,
                    color: { r: 100, g: 0, b: 200 } // Purple
                },
                {
                    name: "The Needle (High Threat)",
                    path: "/docs/course_materials/04_stereo_panning/assets/external_threat_high_R.wav",
                    trackIndex: 4,
                    color: { r: 255, g: 255, b: 0 } // Yellow
                }
            ]
        };

        UniversalLabBuilder.build(manifest);
    })();
