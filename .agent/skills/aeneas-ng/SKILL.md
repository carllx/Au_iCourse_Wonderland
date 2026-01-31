---
name: Aeneas NG Integration
description: 专用于 Wonderland 项目的精细化语音对齐工具封装。基于 aeneas-ng-api 实现。
---

# Aeneas NG Integration Skill

## 简介
这是 [Aeneas NG API](https://github.com/carllx/aeneas-ng-api) 的本地集成封装。
用于将 `.txt` 逐字稿与 `.aac/.mp3` 音频文件进行强制对齐，生成无漂移的精确 `.srt` 时间戳。

## 使用前提
- 必须安装 `aeneas-ng-api` (通常位于 `~/Downloads/aeneas-ng-api`)
- 必须使用 `mybase` Python 环境 (`/opt/anaconda3/envs/mybase/bin/python`)
- 必须修正 `aeneas-ng-api` 中的相对引用问题

## 功能
- **Align**: 逐字稿 + 音频 -> SRT
- **Transcribe**: 音频 -> SRT (无稿)

## 常用命令
### 对齐单个文件
```bash
python .agent/skills/aeneas-ng/scripts/align.py \
    --audio "03_Scripts/tts/S02.aac" \
    --text "03_Scripts/tts/S02.txt" \
    --output "03_Scripts/tts/S02.srt"
```

### 批量对齐
```bash
python .agent/skills/aeneas-ng/scripts/batch_align.py \
    --dir "03_Scripts/tts"
```

## 文件结构
- `scripts/align.py`: 核心包装脚本，动态加载外部 api
