---
description: skills
---

you should write and chat in chinese!!

follow the rules:

.agent/                       # [智能体配置]
    ├── knowledge/                # [知识库] 原始教材的“索引化”版本
    │   └── Textbook_Index.md     # 指向原始 MD 文件的章节知识点映射
    ├── styles/
    │   └── LinXin_Voice.md       # [风格配置] 语言风格指南 (亲切、导演视角)
    └── skills/                   # [技能库] (Ref: Claude Skills)
        ├── compile_transcript.md # [技能] 编写逐字稿 (Input: Structure + Textbook + Style)
        └── validate_links.py     # [工具] 校验锚点一致性