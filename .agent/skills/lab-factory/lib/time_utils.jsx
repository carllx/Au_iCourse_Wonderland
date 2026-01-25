// scripts/time_utils.jsx
// Description: 时间单位转换工具，解决 Python 层（秒）与 JSX 层（采样点）的认知不一致问题。
// Usage: #include "time_utils.jsx" 或复制函数到目标脚本

/**
 * TimeUtils - 时间单位转换工具集
 * 
 * 核心问题：
 * - Python/SRT 层使用秒 (Seconds)
 * - Audition JSX 层使用采样点 (Samples)
 * - 直接传递数值会导致 sampleRate 倍的偏差！
 */
var TimeUtils = (function () {

    /**
     * 秒 → 采样点
     * @param {number} seconds - 时间（秒）
     * @param {number} sampleRate - 采样率（如 48000）
     * @returns {number} 采样点数（四舍五入到整数）
     */
    function secondsToSamples(seconds, sampleRate) {
        if (typeof seconds !== "number" || typeof sampleRate !== "number") {
            $.writeln("[TimeUtils ERROR] secondsToSamples: 参数必须是数字");
            return 0;
        }
        if (sampleRate <= 0) {
            $.writeln("[TimeUtils ERROR] secondsToSamples: 采样率必须大于 0");
            return 0;
        }
        return Math.round(seconds * sampleRate);
    }

    /**
     * 采样点 → 秒
     * @param {number} samples - 采样点数
     * @param {number} sampleRate - 采样率（如 48000）
     * @returns {number} 时间（秒）
     */
    function samplesToSeconds(samples, sampleRate) {
        if (typeof samples !== "number" || typeof sampleRate !== "number") {
            $.writeln("[TimeUtils ERROR] samplesToSeconds: 参数必须是数字");
            return 0;
        }
        if (sampleRate <= 0) {
            $.writeln("[TimeUtils ERROR] samplesToSeconds: 采样率必须大于 0");
            return 0;
        }
        return samples / sampleRate;
    }

    /**
     * 时间码字符串 → 采样点
     * @param {string} timecode - 格式: "HH:MM:SS.mmm" 或 "MM:SS.mmm"
     * @param {number} sampleRate - 采样率
     * @returns {number} 采样点数
     */
    function timecodeToSamples(timecode, sampleRate) {
        var seconds = timecodeToSeconds(timecode);
        return secondsToSamples(seconds, sampleRate);
    }

    /**
     * 时间码字符串 → 秒
     * @param {string} timecode - 格式: "HH:MM:SS.mmm" 或 "MM:SS.mmm"
     * @returns {number} 时间（秒）
     */
    function timecodeToSeconds(timecode) {
        if (typeof timecode !== "string") {
            $.writeln("[TimeUtils ERROR] timecodeToSeconds: 参数必须是字符串");
            return 0;
        }

        var parts = timecode.split(":");
        var seconds = 0;

        if (parts.length === 3) {
            // HH:MM:SS.mmm
            seconds = parseFloat(parts[0]) * 3600 + parseFloat(parts[1]) * 60 + parseFloat(parts[2]);
        } else if (parts.length === 2) {
            // MM:SS.mmm
            seconds = parseFloat(parts[0]) * 60 + parseFloat(parts[1]);
        } else {
            // 可能只是秒数
            seconds = parseFloat(timecode);
        }

        if (isNaN(seconds)) {
            $.writeln("[TimeUtils ERROR] timecodeToSeconds: 无法解析时间码 '" + timecode + "'");
            return 0;
        }

        return seconds;
    }

    /**
     * 获取当前文档的采样率（安全封装）
     * @returns {number} 采样率，失败返回 0
     */
    function getDocumentSampleRate() {
        if (!app.activeDocument) {
            $.writeln("[TimeUtils ERROR] getDocumentSampleRate: 无活动文档");
            return 0;
        }
        return app.activeDocument.sampleRate || 0;
    }

    // 公开 API
    return {
        secondsToSamples: secondsToSamples,
        samplesToSeconds: samplesToSeconds,
        timecodeToSamples: timecodeToSamples,
        timecodeToSeconds: timecodeToSeconds,
        getDocumentSampleRate: getDocumentSampleRate
    };
})();

// 使用示例 (取消注释以测试)
// $.writeln("5 秒 = " + TimeUtils.secondsToSamples(5, 48000) + " 采样点 @48kHz");
// $.writeln("240000 采样点 = " + TimeUtils.samplesToSeconds(240000, 48000) + " 秒 @48kHz");
// $.writeln("'00:01:30.500' = " + TimeUtils.timecodeToSeconds("00:01:30.500") + " 秒");
