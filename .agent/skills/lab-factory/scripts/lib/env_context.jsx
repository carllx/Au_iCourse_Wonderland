/**
 * EnvContext - 环境上下文解析器
 * 
 * 统一解决多执行模式（VS Code / osascript / MCP）下的路径解析问题。
 * 遵循 ES3 规范。
 * 
 * @usage
 *   #include "lib/env_context.jsx"
 *   var root = EnvContext.getProjectRoot();
 *   var config = EnvContext.loadConfig();
 */

var EnvContext = {

    /**
     * 获取项目根目录
     * 通过当前执行脚本的位置反推（假设脚本在 scripts/lib/ 下）
     * 
     * @returns {string} 项目根目录的绝对路径
     */
    getProjectRoot: function () {
        var current = new File($.fileName).parent;
        // 向上递归寻找包含 .agent 的目录 (锚点探测法)
        // 限制递归深度防止死循环
        var retry = 0;
        while (current !== null && retry < 10) {
            var agentDir = new Folder(current.fsName + "/.agent");
            if (agentDir.exists) {
                return current.fsName;
            }
            current = current.parent;
            retry++;
        }

        // Fallback: 如果找不到 .agent (例如在 .agent 内部深层执行但权限问题看不到?)
        // 尝试基于已知结构的硬编码回退
        // 假设路径为 .agent/skills/lab-factory/scripts/lib/
        $.writeln("[WARN] EnvContext: 锚点探测失败，使用回退策略");
        var f = new File($.fileName);
        return f.parent.parent.parent.parent.parent.fsName;
    },

    /**
     * 获取配置文件路径
     * @returns {string} env.config.json 的绝对路径
     */
    getConfigPath: function () {
        return this.getProjectRoot() + "/env.config.json";
    },

    /**
     * 从配置文件读取项目配置
     * 
     * @returns {Object|null} 配置对象，读取失败返回 null
     */
    loadConfig: function () {
        var configPath = this.getConfigPath();
        var configFile = new File(configPath);

        if (!configFile.exists) {
            $.writeln("[WARN] EnvContext: 配置文件不存在: " + configPath);
            return null;
        }

        try {
            configFile.open("r");
            var content = configFile.read();
            configFile.close();

            // ES3 兼容的 JSON 解析
            var config = eval("(" + content + ")");
            return config;
        } catch (e) {
            $.writeln("[ERROR] EnvContext: 配置文件解析失败: " + e.message);
            return null;
        }
    },

    /**
     * 读取外部数据文件（用于 MCP/Python 层传递数据）
     * 
     * @param {string} relativePath - 相对于项目根目录的路径
     * @returns {Object|null} 解析后的 JSON 对象
     */
    loadExternalData: function (relativePath) {
        var fullPath = this.getProjectRoot() + "/" + relativePath;
        var dataFile = new File(fullPath);

        if (!dataFile.exists) {
            $.writeln("[WARN] EnvContext: 外部数据文件不存在: " + fullPath);
            return null;
        }

        try {
            dataFile.open("r");
            var content = dataFile.read();
            dataFile.close();

            var data = eval("(" + content + ")");
            return data;
        } catch (e) {
            $.writeln("[ERROR] EnvContext: 外部数据解析失败: " + e.message);
            return null;
        }
    },

    /**
     * 获取当前执行模式
     * 
     * @returns {string} "vscode" | "osascript" | "mcp" | "unknown"
     */
    getExecutionMode: function () {
        var config = this.loadConfig();

        if (config && config.execution_mode && config.execution_mode !== "auto") {
            return config.execution_mode;
        }

        // 自动检测模式
        // VS Code 调试时通常有 BridgeTalk 消息特征
        // osascript 调用时无法获取特定环境变量
        // 这里提供基础检测，可根据实际情况扩展

        if (typeof BridgeTalk !== "undefined" && BridgeTalk.appName) {
            return "vscode";  // 可能是 VS Code 通过 BridgeTalk 调用
        }

        return "unknown";
    },

    /**
     * 打印环境诊断信息
     */
    printDiagnostics: function () {
        $.writeln("=== EnvContext 诊断信息 ===");
        $.writeln("项目根目录: " + this.getProjectRoot());
        $.writeln("配置文件路径: " + this.getConfigPath());
        $.writeln("执行模式: " + this.getExecutionMode());

        var config = this.loadConfig();
        if (config) {
            $.writeln("配置内容: " + config.toSource());
        } else {
            $.writeln("配置内容: [未加载]");
        }
        $.writeln("===========================");
    }
};
