import re
from enum import Enum, auto
from typing import List, Optional, Dict, Any

class BlockType(Enum):
    SLIDE = auto()
    AUDIO = auto()
    VISUAL = auto()
    PACING = auto()
    METADATA = auto() # Headers, comments, etc.

class ScriptBlock:
    def __init__(self, block_type: BlockType, content: str, line_no: int, slide_id: Optional[str] = None):
        self.block_type = block_type
        self.content = content
        self.line_no = line_no
        self.slide_id = slide_id # Associated Slide ID (if applicable/known at parse time)

    def __repr__(self):
        return f"<{self.block_type.name} Line:{self.line_no} Content:'{self.content[:20]}...'>"

class WonderlandScriptParser:
    """
    Standard parser for Wonderland Scripts (.md).
    Unifies the interpretation of "Narrative" vs "Metadata" vs "Visuals".
    """

    # Class A Tags: Narrative Anchors (Must be spoken)
    CLASS_A_TAGS = [
        "STORY TIME", "PHILOSOPHY", "CULTURAL REF", "TEACHING MOMENT"
    ]
    
    # Class B Tags: Technical Bridges (Often spoken or context setting)
    # Depending on strictness, these might be optionally spoken, but usually for Audio purposes they are content.
    CLASS_B_TAGS = [
        "TECH NOTE", "DID YOU KNOW", "WARNING"
    ]

    def __init__(self):
        self.slide_pattern = re.compile(r"(?:\[SLIDE:\s*|\(PPT:\s*)(S\d+[a-z]?_\w+)(?:\]|\))")
        self.audio_tag_pattern = re.compile(r"\*\*\[AUDIO\]\*\*")
        # Metadata pattern: Comments, headers, horizontal rules
        self.meta_pattern = re.compile(r"^\s*\(|^\s*#|^\s*---|^\s*$")
        
        # Semantic Tag Pattern
        # Matches: > [TEACHING MOMENT: Title] Content
        self.semantic_start_pattern = re.compile(
            r"^\s*>\s*\[(" + "|".join(self.CLASS_A_TAGS + self.CLASS_B_TAGS) + r")(?:[^\]]*)\]:?\s*(.*)", 
            re.IGNORECASE
        )

    def parse(self, lines: List[str]) -> List[ScriptBlock]:
        blocks: List[ScriptBlock] = []
        
        pending_slide = None
        last_slide_id = None
        
        in_semantic_block = False
        in_visual_block = False
        in_pacing_block = False # Not strictly used for state machine if visual block covers it, but good for type differentiation

        for i, line in enumerate(lines):
            line_num = i + 1
            original_line = line
            clean_line = re.sub(r"\*\*|__", "", line).strip()
            
            # --- 1. Slide Detection ---
            slide_match = self.slide_pattern.search(line)
            if slide_match:
                slide_id = slide_match.group(1)
                pending_slide = slide_id
                last_slide_id = slide_id
                
                # Slide marker resets block states
                in_semantic_block = False 
                in_visual_block = False
                
                blocks.append(ScriptBlock(BlockType.SLIDE, slide_id, line_num, slide_id))
                continue

            # --- 2. Semantic Block State Machine (Class A/B) ---
            # Check for start of Semantic Block
            semantic_match = self.semantic_start_pattern.match(line)
            if semantic_match:
                in_semantic_block = True
                content = semantic_match.group(2).strip()
                # Clean content
                content = re.sub(r"\*\*|__", "", content)
                
                if content:
                    blocks.append(ScriptBlock(BlockType.AUDIO, content, line_num, pending_slide or last_slide_id))
                    if pending_slide: pending_slide = None
                continue
            
            # Check if continuing Semantic Block
            if in_semantic_block:
                if line.strip().startswith(">"):
                    # Still in blockquote
                    content = re.sub(r"^\s*>\s*", "", clean_line)
                    content = re.sub(r"[\*\_]", "", content).strip()
                    content = re.sub(r"\([^\)]+\)", "", content).strip() # Remove parens inside block
                    
                    if content:
                        blocks.append(ScriptBlock(BlockType.AUDIO, content, line_num, pending_slide or last_slide_id))
                        if pending_slide: pending_slide = None
                    continue
                else:
                    # Semantic block ended
                    in_semantic_block = False
                    # Fallthrough to normal processing for this line?? 
                    # If this line broke the block, it might be a normal text line or metadata.
                    # Let's proceed to process it as a new line.

            # --- 3. Standard Block Processing ---
            
            # Check for Visual/Pacing
            # Standard Visual Block: > [VISUAL] ...
            # Standard Pacing Block: > [PACING] ...
            # Or just > [ACT: ...
            if line.strip().startswith(">"):
                # If we are here, it's NOT a semantic block (caught above or state false)
                # It's likely Visual or Metadata
                block_type = BlockType.VISUAL
                if "[PACING]" in line or "[WAIT]" in line:
                    block_type = BlockType.PACING
                
                # Extract content just in case consumer wants it
                content = re.sub(r"^\s*>\s*", "", clean_line)
                blocks.append(ScriptBlock(block_type, content, line_num, pending_slide or last_slide_id))
                continue

            # --- 4. Audio / Narration Processing ---
            
            # Skip Audio Header Tag
            if self.audio_tag_pattern.search(line):
                continue
            
            # Metadata Filters
            # Remove numbered list markers for cleaning checking
            check_line = re.sub(r"^\d+\.\s*", "", clean_line)
            
            # Skip Directed Metadata (Role:, Context:, etc.)
            if re.match(r"^(Technique|Step|Note|Scene|Action|Context|Role|Tone):", check_line, re.IGNORECASE):
                blocks.append(ScriptBlock(BlockType.METADATA, clean_line, line_num))
                continue
            
            # Skip typical metadata lines
            if self.meta_pattern.match(clean_line):
                blocks.append(ScriptBlock(BlockType.METADATA, clean_line, line_num))
                continue

            # Skip Stage Directions in parens: (Laughs)
            if re.match(r'^[\(\（].*?[\)\）]$', clean_line):
                blocks.append(ScriptBlock(BlockType.METADATA, clean_line, line_num))
                continue

            # If we survived all filters, it's Audio!
            clean_content = re.sub(r"\([^\)]+\)", "", clean_line).strip() # Remove inline stage directions
            clean_content = re.sub(r"[:：]$", "", clean_content).strip() # Remove trailing colons
            
            if clean_content:
                blocks.append(ScriptBlock(BlockType.AUDIO, clean_content, line_num, pending_slide or last_slide_id))
                if pending_slide: pending_slide = None

        return blocks
