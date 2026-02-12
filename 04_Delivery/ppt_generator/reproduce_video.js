const PptxGenJS = require("pptxgenjs");
const path = require("path");

async function testVideo() {
    const pres = new PptxGenJS();
    const slide = pres.addSlide();

    // Use absolute path to ensure correctness
    const videoPath = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/assets/S02_Phase1_Purify/S02_Preview_NoiseOnly_rec.mp4";
    console.log("Testing video path:", videoPath);

    // Add video media
    slide.addMedia({
        type: "video",
        path: videoPath,
        x: 1, y: 1, w: 8, h: 4.5
    });

    try {
        await pres.writeFile({ fileName: "test_video.pptx" });
        console.log("Video PPT generated successfully.");
    } catch (err) {
        console.error("Error generating video PPT:", err);
    }
}

testVideo();
