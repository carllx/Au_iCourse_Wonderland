const fs = require('fs');
const path = require('path');
const PptxGenJS = require('pptxgenjs');
const sizeOf = require('image-size');

// Configuration
const CONFIG = {
    theme: {
        bgColor: '000000', // Pure Black
        textColor: 'FFFFFF', // White
        accentColor: '00FFFF', // Cyan
        warningColor: 'FF3333', // Red
        mutedColor: '888888', // Grey
        font: 'Arial' // Fallback font
    },
    layout: {
        width: 10,
        height: 5.625 // 16:9 in inches
    },
    split: {
        textRatio: 0.4,  // 左边文字区域占 40%
        imageRatio: 0.6, // 右边图片区域占 60%
        padding: 0.3     // 内边距 (inches)
    },
    paths: {
        root: path.resolve(__dirname, '../../'),
        database: path.resolve(__dirname, '../../02_Visuals/Slide_Database.md'),
        assets: path.resolve(__dirname, '../../02_Visuals/assets'),
        output: path.resolve(__dirname, '../../04_Delivery/ppt_output')
    }
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.paths.output)) {
    fs.mkdirSync(CONFIG.paths.output, { recursive: true });
}

// --- Parsers ---

function parseDatabase(dbPath) {
    const content = fs.readFileSync(dbPath, 'utf-8');
    const db = {};
    let currentId = null;

    const lines = content.split('\n');
    for (const line of lines) {
        const idMatch = line.match(/^##\s+(S[\w_]+)/);
        if (idMatch) {
            currentId = idMatch[1];
            db[currentId] = { id: currentId };
            continue;
        }

        if (currentId) {
            const fieldMatch = line.match(/^\*\s+\*\*(\w+)\*\*:\s*(.*)/);
            if (fieldMatch) {
                const key = fieldMatch[1];
                let value = fieldMatch[2].trim();

                if (key === 'Type') {
                    const typeMatch = value.match(/\[(.*?)\]/);
                    value = typeMatch ? typeMatch[1] : value;
                }

                if (key === 'Ref') {
                    const refMatch = value.match(/\((.*?)\)/);
                    value = refMatch ? refMatch[1] : value;
                }

                db[currentId][key] = value;
            }
        }
    }
    return db;
}

function parseScript(scriptPath) {
    const content = fs.readFileSync(scriptPath, 'utf-8');
    const slides = [];
    const lines = content.split('\n');
    let currentBlock = [];
    let inBlock = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Detect Blockquote
        if (line.startsWith('>')) {
            inBlock = true;
            currentBlock.push(line);
        } else {
            if (inBlock) {
                processBlock(currentBlock, slides);
                currentBlock = [];
            }
            inBlock = false;
        }
    }
    if (inBlock) processBlock(currentBlock, slides);

    return slides;
}

function processBlock(blockLines, slides) {
    // 1. Check if block contains [SLIDE: ID]
    const blockText = blockLines.join('\n');
    const slideMatch = blockText.match(/\[SLIDE:\s*(S[\w_]+)\]/);

    if (!slideMatch) return;

    const id = slideMatch[1];
    const slideData = { id, source: 'script', List: [] };

    // 2. Extract Data
    for (const line of blockLines) {
        // Remove '>' and leading spaces
        const cleanLine = line.replace(/^>\s*/, '').trim();
        if (!cleanLine) continue; // Skip empty lines

        // Check if line is just the ID ref
        if (cleanLine.includes('[SLIDE:')) {
            // Check if it's in a Key: Value format
            if (cleanLine.match(/^\*\s+\*\*Ref/)) continue;
        }

        // Match Key-Value: * **Key**: Value
        const kvMatch = cleanLine.match(/^\*\s+\*\*(\w+)\*\*:\s*(.*)/);
        if (kvMatch) {
            const key = kvMatch[1];
            const val = kvMatch[2].trim();
            slideData[key] = val;
            continue;
        }

        // Match loose Text keys (e.g. Text: ...)
        const textMatch = cleanLine.match(/^Text:\s*(.*)/);
        if (textMatch) {
            slideData.Text = textMatch[1].trim();
            continue;
        }

        const layoutMatch = cleanLine.match(/^Layout:\s*(.*)/);
        if (layoutMatch) {
            slideData.Layout = layoutMatch[1].trim();
            continue;
        }

        // Capture loose lines as Body Text
        // Heuristic: If it's NOT a key-value pair, NOT the Ref line, and NOT a director cue
        const directorCues = ['[VISUAL]', '[AUDIO]', '[PACING]', '[REF]', '[SCENE]'];
        const isDirectorCue = directorCues.some(cue => cleanLine.startsWith(cue) || cleanLine === cue);

        if (!cleanLine.includes('[SLIDE:') && !cleanLine.startsWith('* **') && !isDirectorCue) {
            slideData.List.push(cleanLine);
        }
    }

    slides.push(slideData);
}

// --- Asset Resolution ---

function findAssetPath(slideRef, slideId) {
    if (slideRef) {
        const relPath = slideRef.replace(/^\.\//, '');
        const absPath = path.resolve(CONFIG.paths.root, '02_Visuals', relPath);
        if (fs.existsSync(absPath)) return absPath;
    }

    const modulePrefix = slideId.split('_')[0];
    try {
        const assetsRoot = CONFIG.paths.assets;
        if (fs.existsSync(assetsRoot)) {
            const dirs = fs.readdirSync(assetsRoot);
            const moduleDirName = dirs.find(d => d.startsWith(modulePrefix));

            if (moduleDirName) {
                const moduleDir = path.join(assetsRoot, moduleDirName);
                const files = fs.readdirSync(moduleDir);
                const file = files.find(f => f.startsWith(slideId));
                if (file) return path.join(moduleDir, file);
            }
        }
    } catch (e) {
        console.error("Path resolution error:", e);
    }

    return null;
}

// --- Image Utilities ---

/**
 * 获取图片尺寸
 */
function getImageDimensions(imagePath) {
    // Skip dimensions check for videos
    if (imagePath.toLowerCase().endsWith('.mp4')) {
        return null;
    }

    try {
        const dimensions = sizeOf(imagePath);
        return { width: dimensions.width, height: dimensions.height };
    } catch (e) {
        console.error(`Failed to get image dimensions: ${imagePath}`, e);
        return null;
    }
}

/**
 * 计算图片在指定区域内的最佳尺寸 (contain 模式)
 * @param {number} imgWidth - 图片原始宽度
 * @param {number} imgHeight - 图片原始高度
 * @param {number} areaWidth - 目标区域宽度
 * @param {number} areaHeight - 目标区域高度
 * @returns {{w: number, h: number, x: number, y: number}} 居中后的尺寸和位置偏移
 */
function calculateContainFit(imgWidth, imgHeight, areaWidth, areaHeight) {
    const imgRatio = imgWidth / imgHeight;
    const areaRatio = areaWidth / areaHeight;

    let w, h;
    if (imgRatio > areaRatio) {
        // 图片更宽，以宽度为基准
        w = areaWidth;
        h = areaWidth / imgRatio;
    } else {
        // 图片更高，以高度为基准
        h = areaHeight;
        w = areaHeight * imgRatio;
    }

    // 居中偏移
    const offsetX = (areaWidth - w) / 2;
    const offsetY = (areaHeight - h) / 2;

    return { w, h, offsetX, offsetY };
}

// --- Layouts ---

/**
 * 默认布局：左文右图 (4:6)
 * 图片根据原始比例自适应放置
 */
function createSplitLayout(pres, slideData, assetPath) {
    const slide = pres.addSlide();
    slide.background = { color: CONFIG.theme.bgColor };

    const { width, height } = CONFIG.layout;
    const { textRatio, imageRatio, padding } = CONFIG.split;

    const textAreaWidth = width * textRatio;
    const imageAreaWidth = width * imageRatio;
    const imageAreaHeight = height;

    // --- LEFT: Text Area ---
    const titleText = slideData.Title || slideData.Text || slideData.dbTitle || slideData.dbConcept || "UNTITLED";

    slide.addText(titleText, {
        x: padding,
        y: padding,
        w: textAreaWidth - padding * 2,
        h: 1.2,
        fontSize: 32,
        fontFace: CONFIG.theme.font,
        color: CONFIG.theme.accentColor,
        bold: true,
        valign: 'top'
    });

    // Body Text (multi-line plain text, NOT bullet list)
    if (slideData.List && slideData.List.length > 0) {
        slide.addText(slideData.List.join('\n'), {
            x: padding,
            y: 1.8,
            w: textAreaWidth - padding * 2,
            h: height - 2.2,
            fontSize: 18,
            fontFace: CONFIG.theme.font,
            color: CONFIG.theme.textColor,
            valign: 'top',
            lineSpacing: 28
        });
    } else {
        const bodyText = slideData.Subtitle || slideData.dbCaption || slideData.dbText || '';
        if (bodyText) {
            slide.addText(bodyText, {
                x: padding,
                y: 1.8,
                w: textAreaWidth - padding * 2,
                h: height - 2.2,
                fontSize: 18,
                fontFace: CONFIG.theme.font,
                color: CONFIG.theme.textColor,
                valign: 'top'
            });
        }
    }

    // --- RIGHT: Visual Area (Image or Video) ---
    if (assetPath) {
        const isVideo = assetPath.toLowerCase().endsWith('.mp4');
        const dimensions = getImageDimensions(assetPath);

        // 视觉区域参数 (右侧 60%，带内边距)
        const imgAreaX = textAreaWidth;
        const imgAreaY = padding;
        const imgAreaW = imageAreaWidth - padding;
        const imgAreaH = imageAreaHeight - padding * 2;

        if (isVideo) {
            // 视频处理: 默认 16:9 比例进行 contain 计算
            // 假设视频是 standard HD (1920x1080)
            const vidW = 16;
            const vidH = 9;
            const fit = calculateContainFit(vidW, vidH, imgAreaW, imgAreaH);

            slide.addMedia({
                type: "video",
                path: assetPath,
                x: imgAreaX + fit.offsetX,
                y: imgAreaY + fit.offsetY,
                w: fit.w,
                h: fit.h
            });
            console.log(`  🎥 Video Added: ${slideData.id}`);

        } else if (dimensions) {
            // 图片处理 (已知尺寸)
            // 计算 contain 模式下的实际尺寸
            const fit = calculateContainFit(
                dimensions.width, dimensions.height,
                imgAreaW, imgAreaH
            );

            slide.addImage({
                path: assetPath,
                x: imgAreaX + fit.offsetX,
                y: imgAreaY + fit.offsetY,
                w: fit.w,
                h: fit.h
            });

            console.log(`  📐 Image ${slideData.id}: ${dimensions.width}x${dimensions.height} → ${fit.w.toFixed(2)}x${fit.h.toFixed(2)} inches`);
        } else {
            // 无法读取尺寸，使用 cover 模式 fallback
            slide.addImage({
                path: assetPath,
                x: imgAreaX,
                y: imgAreaY,
                sizing: {
                    type: 'contain',
                    w: imgAreaW,
                    h: imgAreaH
                }
            });
        }
    } else {
        // 缺失图片提示
        slide.addText("MISSING ASSET: " + slideData.id, {
            x: textAreaWidth + padding,
            y: height / 2 - 0.5,
            w: imageAreaWidth - padding * 2,
            h: 1,
            fontSize: 16,
            color: CONFIG.theme.warningColor,
            align: 'center'
        });
    }
}

/**
 * 标题卡布局 (全屏背景 + 居中文字)
 */
function createTitleCard(pres, slideData, assetPath) {
    const slide = pres.addSlide();
    slide.background = { color: CONFIG.theme.bgColor };

    // Background Image or Video with cover
    if (assetPath) {
        const isVideo = assetPath.toLowerCase().endsWith('.mp4');
        if (isVideo) {
            slide.addMedia({
                type: "video",
                path: assetPath,
                x: 0,
                y: 0,
                w: CONFIG.layout.width,
                h: CONFIG.layout.height
            });
        } else {
            slide.addImage({
                path: assetPath,
                x: 0,
                y: 0,
                sizing: {
                    type: 'cover',
                    w: CONFIG.layout.width,
                    h: CONFIG.layout.height
                }
            });
        }
    }

    // Overlay
    slide.addShape(pres.ShapeType.rect, {
        x: 0, y: 0,
        w: CONFIG.layout.width,
        h: CONFIG.layout.height,
        fill: { color: CONFIG.theme.bgColor, transparency: 30 }
    });

    // Title
    const titleText = slideData.Title || slideData.Text || slideData.dbTitle || slideData.dbConcept || "UNTITLED";

    slide.addText(titleText, {
        x: 0.5, y: 2.0, w: 9, h: 2,
        fontSize: 54,
        fontFace: CONFIG.theme.font,
        color: CONFIG.theme.accentColor,
        bold: true,
        align: 'center',
        valign: 'middle'
    });

    // Subtitle / List
    if (slideData.List && slideData.List.length > 0) {
        slide.addText(slideData.List.join('\n'), {
            x: 1.5, y: 4.0, w: 7, h: 2.5,
            fontSize: 24,
            fontFace: CONFIG.theme.font,
            color: CONFIG.theme.textColor,
            align: 'center',
            bullet: false,
            lineSpacing: 35
        });
    } else {
        const subtitleText = slideData.Subtitle || slideData.Concept;
        if (subtitleText) {
            slide.addText(subtitleText.toUpperCase(), {
                x: 0.5, y: 4.5, w: 9, h: 1,
                fontSize: 24,
                fontFace: CONFIG.theme.font,
                color: CONFIG.theme.textColor,
                align: 'center',
                letterSpacing: 3
            });
        }
    }
}

/**
 * 电影字幕布局 (图片 + 底部字幕条)
 */
function createCinematicCaption(pres, slideData, assetPath) {
    const slide = pres.addSlide();
    slide.background = { color: CONFIG.theme.bgColor };

    if (assetPath) {
        const isVideo = assetPath.toLowerCase().endsWith('.mp4');
        if (isVideo) {
            slide.addMedia({
                type: "video",
                path: assetPath,
                x: 0,
                y: 0,
                w: CONFIG.layout.width,
                h: CONFIG.layout.height * 0.85
            });
        } else {
            slide.addImage({
                path: assetPath,
                x: 0,
                y: 0,
                sizing: {
                    type: 'cover',
                    w: CONFIG.layout.width,
                    h: CONFIG.layout.height * 0.85
                }
            });
        }
    } else {
        slide.addText("MISSING ASSET: " + slideData.id, { x: 1, y: 1, color: CONFIG.theme.warningColor });
    }

    // Caption Bar
    slide.addShape(pres.ShapeType.rect, {
        x: 0, y: CONFIG.layout.height * 0.82,
        w: CONFIG.layout.width,
        h: CONFIG.layout.height * 0.18,
        fill: { color: CONFIG.theme.bgColor, transparency: 10 }
    });

    // Text Logic: Title/Text/List priority
    let textChunk = "";
    if (slideData.List && slideData.List.length > 0) {
        textChunk = slideData.List.join('\n');
    } else {
        textChunk = slideData.Text || slideData.Caption || slideData.dbCaption || slideData.dbText || slideData.dbConcept;
    }

    if (textChunk) {
        slide.addText(textChunk, {
            x: 0.5, y: CONFIG.layout.height * 0.84, w: 9, h: 1,
            fontSize: 20,
            fontFace: "Georgia",
            italic: true,
            color: CONFIG.theme.textColor,
            align: 'center',
            valign: 'top'
        });
    }
}

// --- Main ---

async function main() {
    const scriptName = process.argv[2] || 'S01_Intro.md';
    const scriptPath = path.resolve(CONFIG.paths.root, '03_Scripts', scriptName);

    console.log(`🎬 Generating PPT for ${scriptName} (V4: Split Layout + Aspect Ratio)...`);

    const db = parseDatabase(CONFIG.paths.database);
    const slides = parseScript(scriptPath);

    const pres = new PptxGenJS();
    pres.layout = 'LAYOUT_16x9';

    for (const slideItem of slides) {
        const slideId = slideItem.id;
        const dbData = db[slideId] || {};

        const mergedData = {
            id: slideId,
            ...slideItem,
            dbTitle: dbData.Title,
            dbConcept: dbData.Concept,
            dbCaption: dbData.Caption,
            dbText: dbData.Text,
            Ref: dbData.Ref,
            Type: dbData.Type
        };

        if (!dbData.id) console.warn(`⚠️  DB Entry Missing: ${slideId}`);

        const assetPath = findAssetPath(mergedData.Ref, slideId);

        // 布局选择逻辑
        let layoutType = (mergedData.Layout || mergedData.Type || '').toLowerCase();

        if (layoutType.includes('title')) {
            createTitleCard(pres, mergedData, assetPath);
        } else if (layoutType.includes('cinematic') || layoutType.includes('caption')) {
            createCinematicCaption(pres, mergedData, assetPath);
        } else {
            // 默认使用左右分布布局
            createSplitLayout(pres, mergedData, assetPath);
        }
    }

    const outFilename = scriptName.replace('.md', '_Presentation.pptx');
    const outPath = path.join(CONFIG.paths.output, outFilename);

    await pres.writeFile({ fileName: outPath });
    console.log(`✅ PPT Generated: ${outPath}`);
}

main().catch(err => console.error(err));
