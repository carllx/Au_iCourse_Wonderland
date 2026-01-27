"""Content merging and integration utilities."""

from pathlib import Path
from typing import List, Dict, Optional
import re


class ContentMerger:
    """Handles merging and integration of markdown content."""
    
    # File size threshold for embedding vs referencing (50KB)
    SIZE_THRESHOLD = 50 * 1024
    
    @staticmethod
    def merge_markdown_files(files: List[tuple[Path, str]]) -> str:
        """
        Merge multiple markdown files into a single document.
        
        Args:
            files: List of tuples (file_path, section_title)
                   Each file will be added under the given section title
            
        Returns:
            Merged markdown content
        """
        merged_content = []
        
        for file_path, section_title in files:
            if not file_path.exists():
                merged_content.append(f"\n## {section_title}\n\n")
                merged_content.append(f"*Note: Source file not found: {file_path}*\n\n")
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Add section header
                merged_content.append(f"\n## {section_title}\n\n")
                
                # Add content (strip any existing frontmatter)
                clean_content = ContentMerger._strip_frontmatter(content)
                merged_content.append(clean_content)
                merged_content.append("\n")
                
            except IOError as e:
                merged_content.append(f"\n## {section_title}\n\n")
                merged_content.append(f"*Note: Failed to read file {file_path}: {e}*\n\n")
        
        return "".join(merged_content)
    
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
    def should_embed_file(file_path: Path) -> bool:
        """
        Determine if a file should be embedded or referenced based on size.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file should be embedded, False if it should be referenced
        """
        if not file_path.exists():
            return False
        
        try:
            size = file_path.stat().st_size
            return size < ContentMerger.SIZE_THRESHOLD
        except OSError:
            return False
    
    @staticmethod
    def create_file_reference(file_path: Path, description: str = "") -> str:
        """
        Create a markdown reference to an external file.
        
        Args:
            file_path: Path to the file
            description: Optional description of the file
            
        Returns:
            Markdown formatted file reference
        """
        ref = f"**Location**: `{file_path}`\n\n"
        
        if description:
            ref = f"{description}\n\n{ref}"
        
        # Try to get file size for context
        if file_path.exists():
            try:
                size = file_path.stat().st_size
                size_kb = size / 1024
                ref += f"*File size: {size_kb:.1f} KB*\n\n"
            except OSError:
                pass
        
        return ref
    
    @staticmethod
    def create_script_documentation(
        script_name: str,
        purpose: str,
        location: Path,
        usage_example: str,
        parameters: Optional[Dict[str, str]] = None,
        dependencies: Optional[List[str]] = None,
        execution_context: Optional[str] = None
    ) -> str:
        """
        Create standardized documentation for a script.
        
        Args:
            script_name: Name of the script
            purpose: Brief description of what the script does
            location: Path to the script
            usage_example: Command-line usage example
            parameters: Optional dict of parameter names to descriptions
            dependencies: Optional list of dependencies
            execution_context: Optional execution context requirements
            
        Returns:
            Markdown formatted script documentation
        """
        doc = [f"### {script_name}\n\n"]
        doc.append(f"**Purpose**: {purpose}\n\n")
        doc.append(f"**Location**: `{location}`\n\n")
        doc.append(f"**Usage**:\n```bash\n{usage_example}\n```\n\n")
        
        if parameters:
            doc.append("**Parameters**:\n")
            for param, desc in parameters.items():
                doc.append(f"- `{param}`: {desc}\n")
            doc.append("\n")
        
        if dependencies:
            doc.append("**Dependencies**:\n")
            for dep in dependencies:
                doc.append(f"- {dep}\n")
            doc.append("\n")
        
        if execution_context:
            doc.append(f"**Execution Context**: {execution_context}\n\n")
        
        return "".join(doc)
    
    @staticmethod
    def extract_code_blocks(content: str) -> List[str]:
        """
        Extract all code blocks from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            List of code block contents
        """
        # Match code blocks with triple backticks
        pattern = r'```[\w]*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches
    
    @staticmethod
    def preserve_formatting(content: str) -> str:
        """
        Ensure markdown formatting is preserved during merging.
        
        Args:
            content: Markdown content
            
        Returns:
            Content with preserved formatting
        """
        # Ensure proper spacing around headers
        content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', content)
        
        # Ensure proper spacing around code blocks
        content = re.sub(r'\n(```)', r'\n\n\1', content)
        
        # Remove excessive blank lines (more than 2)
        content = re.sub(r'\n{3,}', r'\n\n', content)
        
        return content.strip()
    
    @staticmethod
    def add_section_prefix(content: str, prefix: str) -> str:
        """
        Add a prefix to all section headers in content.
        
        Args:
            content: Markdown content
            prefix: Prefix to add (e.g., "Rules: ")
            
        Returns:
            Content with prefixed headers
        """
        # Match headers (# Header)
        def replace_header(match):
            hashes = match.group(1)
            title = match.group(2)
            return f"{hashes} {prefix}{title}"
        
        pattern = r'^(#{1,6})\s+(.+)$'
        return re.sub(pattern, replace_header, content, flags=re.MULTILINE)

    @staticmethod
    def add_section_suffix(content: str, suffix: str) -> str:
        """
        Add a suffix to all section headers in content.
        
        Args:
            content: Markdown content
            suffix: Suffix to add (e.g., " (from Rules)")
            
        Returns:
            Content with suffixed headers
        """
        # Match headers (# Header)
        def replace_header(match):
            hashes = match.group(1)
            title = match.group(2)
            return f"{hashes} {title}{suffix}"
        
        pattern = r'^(#{1,6})\s+(.+)$'
        return re.sub(pattern, replace_header, content, flags=re.MULTILINE)
    
    @staticmethod
    def detect_heading_conflicts(contents: List[tuple[str, str]]) -> Dict[str, List[str]]:
        """
        Detect conflicting headings across multiple content pieces.
        
        Args:
            contents: List of tuples (content, source_name)
            
        Returns:
            Dictionary mapping heading text to list of sources where it appears
        """
        heading_pattern = r'^#{1,6}\s+(.+)$'
        heading_sources = {}
        
        for content, source in contents:
            headings = re.findall(heading_pattern, content, re.MULTILINE)
            for heading in headings:
                heading_clean = heading.strip()
                if heading_clean not in heading_sources:
                    heading_sources[heading_clean] = []
                if source not in heading_sources[heading_clean]:
                    heading_sources[heading_clean].append(source)
        
        # Return only conflicts (headings that appear in multiple sources)
        conflicts = {h: sources for h, sources in heading_sources.items() if len(sources) > 1}
        return conflicts
    
    @staticmethod
    def resolve_heading_conflicts(
        files: List[tuple[Path, str, Optional[str]]],
        strategy: str = "prefix"
    ) -> List[tuple[str, str]]:
        """
        Merge files while resolving heading conflicts.
        
        Args:
            files: List of tuples (file_path, section_title, prefix_or_suffix)
                   The third element is optional and used for conflict resolution
            strategy: "prefix" or "suffix" - how to resolve conflicts
            
        Returns:
            List of tuples (merged_content, section_title) ready for final merge
        """
        results = []
        
        for file_info in files:
            file_path = file_info[0]
            section_title = file_info[1]
            modifier = file_info[2] if len(file_info) > 2 else None
            
            if not file_path.exists():
                results.append((
                    f"*Note: Source file not found: {file_path}*\n\n",
                    section_title
                ))
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                clean_content = ContentMerger._strip_frontmatter(content)
                
                # Apply conflict resolution if modifier provided
                if modifier:
                    if strategy == "prefix":
                        clean_content = ContentMerger.add_section_prefix(clean_content, modifier)
                    elif strategy == "suffix":
                        clean_content = ContentMerger.add_section_suffix(clean_content, modifier)
                
                results.append((clean_content, section_title))
                
            except IOError as e:
                results.append((
                    f"*Note: Failed to read file {file_path}: {e}*\n\n",
                    section_title
                ))
        
        return results
