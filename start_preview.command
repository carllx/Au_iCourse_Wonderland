#!/bin/bash

# 获取当前脚本所在目录的绝对路径
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到 H5 预览项目目录
cd "$DIR/04_Delivery/h5_preview" || { echo "❌ 错误: 找不到 04_Delivery/h5_preview 目录"; exit 1; }

echo "=================================================="
echo "   H5 Interactive Preview - Auto Launcher"
echo "=================================================="

# 检查是否需要安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 首次运行，正在安装依赖..."
    npm install
fi

# 同步数据
echo "🔄 正在同步课程脚本与素材..."
npm run sync

# 启动服务
echo "🚀 启动预览服务器..."
echo "✅ 请在浏览器中访问显示的 Local URL (通常是 http://localhost:5173)"
echo "--------------------------------------------------"

npm run dev
