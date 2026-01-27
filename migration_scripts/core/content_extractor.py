"""Content extraction and filtering utilities for migration."""

from pathlib import Path
from typing import List, Dict, Optional, Set
import re


class ContentExtractor:
    """Handles intelligent extraction and filtering of content from source files."""
    
    # Mapping of skills to their relevant rules
    SKILL_RULES_MAP = {
        "lab-factory": ["rule_mvp_conventions.md"],
        "validation-suite": [],
        "transcript-compiler": [
            "rule_workflow_protocol.md",
            "rule_pedagogy_scaffolding.md",
            "rule_script_standards.md",
            "rule_narrative_consistency.md"
        ]
    }
    
    # Mapping of skills to their relevant knowledge files
    SKILL_KNOWLEDGE_MAP = {
        "lab-factory": ["Audition_Skills_Map.md"],
        "validation-suite": [],
        "transcript-compiler": ["Textbook_Index.md", "Chapter_Mapping.md"]
    }
    
    # Mapping of skills to their relevant style guides
    SKILL_STYLES_MAP = {
        "lab-factory": [],
        "validation-suite": [],
        "transcript-compiler": ["LinXin_Voice.md"]
    }
    
    @staticmethod
    def extract_skill_content(skill_md_path: Path) -> Dict[str, str]:
        """
        Extract core content from a SKILL.md file.
        
        Args:
            skill_md_path: Path to the SKILL.md file
            
        Returns:
            Dictionary with extracted sections:
            - 'overview': Overview/description section
            - 'capabilities': Core capabilities/features
            - 'usage': Usage instructions
            - 'dependencies': Dependencies and file references
            - 'limitations': Known limitations
            - 'protocols': Robustness protocols or best practices
            - 'full_content': Complete content without frontmatter
        """
        if not skill_md_path.exists():
            return {
                'overview': '',
                'capabilities': '',
                'usage': '',
                'dependencies': '',
                'limitations': '',
                'protocols': '',
                'full_content': ''
            }
        
        try:
            content = skill_md_path.read_text(encoding='utf-8')
            
            # Strip frontmatter
            clean_content = ContentExtractor._strip_frontmatter(content)
            
            # Extract sections
            sections = ContentExtractor._extract_sections(clean_content)
            
            return {
                'overview': ContentExtractor._find_section(sections, ['概述', 'Overview', '核心架构']),
                'capabilities': ContentExtractor._find_section(sections, ['核心架构', 'Core', '能力', 'Capabilities', 'Features']),
                'usage': ContentExtractor._find_section(sections, ['使用', 'Usage', '策略', 'Strategy', '开发流程']),
                'dependencies': ContentExtractor._find_section(sections, ['依赖', 'Dependencies', '📌 依赖文件']),
                'limitations': ContentExtractor._find_section(sections, ['局限', 'Limitations', '⚠️ 已知局限']),
                'protocols': ContentExtractor._find_section(sections, ['协议', 'Protocol', '鲁棒性', 'Robustness', '🛡️']),
                'full_content': clean_content
            }
            
        except IOError:
            return {
                'overview': '',
                'capabilities': '',
                'usage': '',
                'dependencies': '',
                'limitations': '',
                'protocols': '',
                'full_content': ''
            }
    
    @staticmethod
    def extract_rule_content(rule_path: Path, skill_context: str = "") -> str:
        """
        Extract relevant content from a rule file.
        
        Args:
            rule_path: Path to the rule file
            skill_context: Optional skill context for filtering
            
        Returns:
            Extracted rule content without frontmatter
        """
        if not rule_path.exists():
            return ""
        
        try:
            content = rule_path.read_text(encoding='utf-8')
            clean_content = ContentExtractor._strip_frontmatter(content)
            
            # For rules, we typically want the full content
            # as they are usually concise and fully relevant
            return clean_content.strip()
            
        except IOError:
            return ""
    
    @staticmethod
    def extract_knowledge_content(
        knowledge_path: Path,
        skill_context: str = "",
        max_size_kb: int = 50
    ) -> Dict[str, str]:
        """
        Extract relevant content from a knowledge file.
        
        For large files (>max_size_kb), returns a summary and reference.
        For small files, returns the full content.
        
        Args:
            knowledge_path: Path to the knowledge file
            skill_context: Optional skill context for filtering
            max_size_kb: Maximum size in KB for embedding (default: 50)
            
        Returns:
            Dictionary with:
            - 'content': Full content or summary
            - 'should_embed': Boolean indicating if content should be embedded
            - 'file_size_kb': File size in KB
        """
        if not knowledge_path.exists():
            return {
                'content': '',
                'should_embed': False,
                'file_size_kb': 0
            }
        
        try:
            # Check file size
            size_bytes = knowledge_path.stat().st_size
            size_kb = size_bytes / 1024
            
            content = knowledge_path.read_text(encoding='utf-8')
            clean_content = ContentExtractor._strip_frontmatter(content)
            
            # Decide whether to embed or reference
            should_embed = size_kb < max_size_kb
            
            if should_embed:
                return {
                    'content': clean_content.strip(),
                    'should_embed': True,
                    'file_size_kb': size_kb
                }
            else:
                # For large files, extract a summary
                summary = ContentExtractor._extract_summary(clean_content)
                return {
                    'content': summary,
                    'should_embed': False,
                    'file_size_kb': size_kb
                }
                
        except IOError:
            return {
                'content': '',
                'should_embed': False,
                'file_size_kb': 0
            }
    
    @staticmethod
    def extract_style_content(style_path: Path) -> str:
        """
        Extract content from a style guide file.
        
        Args:
            style_path: Path to the style guide file
            
        Returns:
            Extracted style guide content without frontmatter
        """
        if not style_path.exists():
            return ""
        
        try:
            content = style_path.read_text(encoding='utf-8')
            clean_content = ContentExtractor._strip_frontmatter(content)
            return clean_content.strip()
            
        except IOError:
            return ""
    
    @staticmethod
    def get_relevant_rules(skill_id: str, rules_dir: Path) -> List[Path]:
        """
        Get list of relevant rule files for a skill.
        
        Args:
            skill_id: Skill identifier (e.g., "lab-factory")
            rules_dir: Path to the rules directory
            
        Returns:
            List of paths to relevant rule files
        """
        rule_names = ContentExtractor.SKILL_RULES_MAP.get(skill_id, [])
        return [rules_dir / name for name in rule_names if (rules_dir / name).exists()]
    
    @staticmethod
    def get_relevant_knowledge(skill_id: str, knowledge_dir: Path) -> List[Path]:
        """
        Get list of relevant knowledge files for a skill.
        
        Args:
            skill_id: Skill identifier (e.g., "lab-factory")
            knowledge_dir: Path to the knowledge directory
            
        Returns:
            List of paths to relevant knowledge files
        """
        knowledge_names = ContentExtractor.SKILL_KNOWLEDGE_MAP.get(skill_id, [])
        return [knowledge_dir / name for name in knowledge_names if (knowledge_dir / name).exists()]
    
    @staticmethod
    def get_relevant_styles(skill_id: str, styles_dir: Path) -> List[Path]:
        """
        Get list of relevant style guide files for a skill.
        
        Args:
            skill_id: Skill identifier (e.g., "lab-factory")
            styles_dir: Path to the styles directory
            
        Returns:
            List of paths to relevant style guide files
        """
        style_names = ContentExtractor.SKILL_STYLES_MAP.get(skill_id, [])
        return [styles_dir / name for name in style_names if (styles_dir / name).exists()]
    
    @staticmethod
    def _strip_frontmatter(content: str) -> str:
        """
        Remove YAML frontmatter from markdown content.
        
        Args:
            content: Markdown content that may contain frontmatter
            
        Returns:
            Content without frontmatter
        """
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content.strip()
    
    @staticmethod
    def _extract_sections(content: str) -> Dict[str, str]:
        """
        Extract sections from markdown content based on headers.
        
        Args:
            content: Markdown content
            
        Returns:
            Dictionary mapping section titles to their content
        """
        sections = {}
        
        # Split by headers (## or #)
        # Pattern matches: ## Title or # Title
        header_pattern = r'^(#{1,6})\s+(.+?)$'
        
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = match.group(2).strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    @staticmethod
    def _find_section(sections: Dict[str, str], keywords: List[str]) -> str:
        """
        Find a section by matching keywords in section titles.
        
        Args:
            sections: Dictionary of section titles to content
            keywords: List of keywords to search for
            
        Returns:
            Content of the first matching section, or empty string
        """
        for title, content in sections.items():
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    return content
        return ""
    
    @staticmethod
    def _extract_summary(content: str, max_lines: int = 20) -> str:
        """
        Extract a summary from content (first N lines or first section).
        
        Args:
            content: Full content
            max_lines: Maximum number of lines to include
            
        Returns:
            Summary text
        """
        lines = content.split('\n')
        
        # Try to get the first section (up to the second header)
        summary_lines = []
        header_count = 0
        
        for line in lines:
            if re.match(r'^#{1,6}\s+', line):
                header_count += 1
                if header_count > 2:  # Stop after second header
                    break
            summary_lines.append(line)
            
            if len(summary_lines) >= max_lines:
                break
        
        summary = '\n'.join(summary_lines).strip()
        
        if len(lines) > len(summary_lines):
            summary += "\n\n*[Content truncated - see full file for details]*"
        
        return summary
    
    @staticmethod
    def extract_code_examples(content: str) -> List[Dict[str, str]]:
        """
        Extract code examples from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            List of dictionaries with 'language' and 'code' keys
        """
        examples = []
        
        # Pattern matches: ```language\ncode\n```
        pattern = r'```(\w*)\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for language, code in matches:
            examples.append({
                'language': language or 'text',
                'code': code.strip()
            })
        
        return examples
    
    @staticmethod
    def filter_relevant_content(
        content: str,
        keywords: List[str],
        context_lines: int = 3
    ) -> str:
        """
        Filter content to only include sections relevant to given keywords.
        
        Args:
            content: Full content
            keywords: List of keywords to search for
            context_lines: Number of context lines to include around matches
            
        Returns:
            Filtered content containing only relevant sections
        """
        if not keywords:
            return content
        
        lines = content.split('\n')
        relevant_line_indices = set()
        
        # Find lines containing keywords
        for i, line in enumerate(lines):
            for keyword in keywords:
                if keyword.lower() in line.lower():
                    # Add this line and context
                    for j in range(max(0, i - context_lines), 
                                 min(len(lines), i + context_lines + 1)):
                        relevant_line_indices.add(j)
        
        if not relevant_line_indices:
            return content  # No matches, return full content
        
        # Extract relevant lines
        sorted_indices = sorted(relevant_line_indices)
        filtered_lines = []
        
        for i in sorted_indices:
            filtered_lines.append(lines[i])
        
        return '\n'.join(filtered_lines)
    
    @staticmethod
    def identify_script_references(content: str) -> List[Dict[str, str]]:
        """
        Identify script references in content (paths to .py, .jsx files).
        
        Args:
            content: Content to search
            
        Returns:
            List of dictionaries with script information
        """
        scripts = []
        
        # Pattern for file paths ending in .py or .jsx
        # Matches: path/to/script.py or path/to/script.jsx
        pattern = r'([^\s]+\.(?:py|jsx))'
        
        matches = re.findall(pattern, content)
        
        for match in matches:
            # Clean up the path (remove markdown formatting)
            clean_path = match.strip('`*[]()').strip()
            
            # Determine script type
            script_type = 'python' if clean_path.endswith('.py') else 'jsx'
            
            scripts.append({
                'path': clean_path,
                'type': script_type
            })
        
        # Remove duplicates
        seen = set()
        unique_scripts = []
        for script in scripts:
            key = (script['path'], script['type'])
            if key not in seen:
                seen.add(key)
                unique_scripts.append(script)
        
        return unique_scripts
