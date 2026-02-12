/**
 * export_tts_docx.js
 * 
 * 功能：将 03_Scripts/tts/*.txt 文件导出为 Word 文档
 * 规则：
 *   - [SLIDE #N: xxx] 标记 → 红色字体
 *   - 朗读内容 → 黑色字体
 * 
 * 用法：
 *   node export_tts_docx.js [文件名|all]
 *   node export_tts_docx.js S02_Phase1_Purify.txt
 *   node export_tts_docx.js all
 */

const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');
const fs = require('fs');
const path = require('path');

// 项目路径配置
const PROJECT_ROOT = path.resolve(__dirname, '../../../../');
const TTS_DIR = path.join(PROJECT_ROOT, '03_Scripts/tts');
const OUTPUT_DIR = path.join(TTS_DIR, 'docx_exports');

// 颜色定义
const COLOR_RED = 'CC0000';    // 标记颜色（红色）
const COLOR_BLACK = '000000';  // 朗读内容（黑色）

/**
 * 解析一行文本，判断是否为 SLIDE 标记
 * @param {string} line 
 * @returns {{ isSlide: boolean, content: string }}
 */
function parseLine(line) {
    const slidePattern = /^\[SLIDE\s*#?\d*:\s*.+\]$/;
    const isSlide = slidePattern.test(line.trim());
    return { isSlide, content: line.trim() };
}

/**
 * 从 txt 文件生成 Word 文档
 * @param {string} txtPath txt 文件路径
 * @param {string} outputPath 输出 docx 路径
 */
async function generateDocx(txtPath, outputPath) {
    const content = fs.readFileSync(txtPath, 'utf-8');
    const lines = content.split('\n');

    const paragraphs = [];
    const baseName = path.basename(txtPath, '.txt');

    // 添加标题
    paragraphs.push(
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [
                new TextRun({
                    text: baseName,
                    bold: true,
                    size: 32,  // 16pt
                    font: 'Microsoft YaHei'
                })
            ],
            spacing: { after: 400 }
        })
    );

    for (const line of lines) {
        if (!line.trim()) {
            // 空行：添加空段落作为分隔
            paragraphs.push(new Paragraph({ spacing: { after: 100 } }));
            continue;
        }

        const { isSlide, content: text } = parseLine(line);

        if (isSlide) {
            // SLIDE 标记：红色、加粗
            paragraphs.push(
                new Paragraph({
                    children: [
                        new TextRun({
                            text: text,
                            color: COLOR_RED,
                            bold: true,
                            size: 24,  // 12pt
                            font: 'Microsoft YaHei'
                        })
                    ],
                    spacing: { before: 300, after: 100 }
                })
            );
        } else {
            // 朗读内容：黑色、常规
            paragraphs.push(
                new Paragraph({
                    children: [
                        new TextRun({
                            text: text,
                            color: COLOR_BLACK,
                            size: 24,  // 12pt
                            font: 'Microsoft YaHei'
                        })
                    ],
                    spacing: { after: 100 }
                })
            );
        }
    }

    const doc = new Document({
        styles: {
            default: {
                document: {
                    run: {
                        font: 'Microsoft YaHei',
                        size: 24  // 12pt
                    }
                }
            }
        },
        sections: [{
            properties: {
                page: {
                    size: {
                        width: 11906,   // A4 宽度 (DXA)
                        height: 16838   // A4 高度 (DXA)
                    },
                    margin: {
                        top: 1440,    // 1 inch
                        right: 1440,
                        bottom: 1440,
                        left: 1440
                    }
                }
            },
            children: paragraphs
        }]
    });

    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputPath, buffer);
    console.log(`✅ 已导出: ${path.basename(outputPath)}`);
}

/**
 * 主函数
 */
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log('用法: node export_tts_docx.js [文件名|all]');
        console.log('示例: node export_tts_docx.js S02_Phase1_Purify.txt');
        console.log('      node export_tts_docx.js all');
        process.exit(1);
    }

    // 确保输出目录存在
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const target = args[0];

    if (target.toLowerCase() === 'all') {
        // 处理所有 txt 文件（排除 _blind.txt 和 Vocabulary_List.md）
        const files = fs.readdirSync(TTS_DIR)
            .filter(f => f.endsWith('.txt') && !f.includes('_blind'));

        for (const file of files) {
            const txtPath = path.join(TTS_DIR, file);
            const outputPath = path.join(OUTPUT_DIR, file.replace('.txt', '.docx'));
            await generateDocx(txtPath, outputPath);
        }
        console.log(`\n📁 所有文件已导出至: ${OUTPUT_DIR}`);
    } else {
        // 处理单个文件
        const txtPath = path.join(TTS_DIR, target);
        if (!fs.existsSync(txtPath)) {
            console.error(`❌ 文件不存在: ${txtPath}`);
            process.exit(1);
        }
        const outputPath = path.join(OUTPUT_DIR, target.replace('.txt', '.docx'));
        await generateDocx(txtPath, outputPath);
    }
}

main().catch(err => {
    console.error('❌ 错误:', err.message);
    process.exit(1);
});
