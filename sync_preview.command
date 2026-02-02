#!/bin/bash
# sync_preview.command
# 专用于 Wonderland 项目的 H5 预览同步脚本
# 解决路径依赖问题：无论在哪里双击，都能正确定位到 h5_preview 目录运行 npm sync

# 1. 切换到脚本所在目录的根目录
# 假设脚本放在项目根目录
cd "$(dirname "$0")" || exit 1

# 2. 定位到 H5 Preview 目录
PREVIEW_DIR="./04_Delivery/h5_preview"

if [ ! -d "$PREVIEW_DIR" ]; then
    echo "❌ 错误: 找不到 H5 预览目录: $PREVIEW_DIR"
    echo "请确保本脚本位于项目根目录。"
    read -n 1 -s -r -p "按任意键退出..."
    exit 1
fi

echo "📂 进入目录: $PREVIEW_DIR"
cd "$PREVIEW_DIR" || exit 1

# 3. 运行 npm run sync
echo "🔄 开始同步 H5 数据 (npm run sync)..."
npm run sync

if [ $? -eq 0 ]; then
    echo "✅ 同步成功！"
    # 可选：询问是否启动预览
    # echo "是否启动预览服务器? (y/n)"
    # read -r start_now
    # if [[ "$start_now" =~ ^[Yy]$ ]]; then
    #     npm run dev
    # fi
else
    echo "❌ 同步失败，请检查上方错误日志。"
    read -n 1 -s -r -p "按任意键退出..."
    exit 1
fi

# 保持窗口打开 (如果是双击运行)
# read -t 3 -p "3秒后自动关闭..."
