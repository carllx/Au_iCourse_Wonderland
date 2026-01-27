"""YAML processing utilities for migration."""

import yaml
from typing import Dict, Any, List
from pathlib import Path


class YAMLHandler:
    """Handles YAML frontmatter generation and validation."""
    
    @staticmethod
    def create_frontmatter(name: str, description: str, keywords: List[str]) -> str:
        """
        Create YAML frontmatter for a power.md file.
        
        Args:
            name: Display name of the Power
            description: Brief description of the Power
            keywords: List of search keywords
            
        Returns:
            YAML frontmatter as string with delimiters
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not name:
            raise ValueError("Power name is required")
        if not description:
            raise ValueError("Power description is required")
        if not keywords or len(keywords) == 0:
            raise ValueError("At least one keyword is required")
        
        frontmatter_data = {
            'name': name,
            'description': description,
            'keywords': keywords
        }
        
        # Generate YAML with proper formatting
        yaml_content = yaml.dump(
            frontmatter_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
        
        # Add YAML delimiters
        return f"---\n{yaml_content}---\n"
    
    @staticmethod
    def parse_frontmatter(content: str) -> Dict[str, Any]:
        """
        Parse YAML frontmatter from a markdown file.
        
        Args:
            content: Full markdown content with frontmatter
            
        Returns:
            Dictionary containing parsed frontmatter
            
        Raises:
            ValueError: If frontmatter is invalid or missing
        """
        if not content.startswith('---'):
            raise ValueError("No YAML frontmatter found")
        
        # Extract frontmatter between --- delimiters
        parts = content.split('---', 2)
        if len(parts) < 3:
            raise ValueError("Invalid YAML frontmatter format")
        
        yaml_content = parts[1].strip()
        
        try:
            frontmatter = yaml.safe_load(yaml_content)
            if not isinstance(frontmatter, dict):
                raise ValueError("Frontmatter must be a dictionary")
            return frontmatter
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML frontmatter: {e}")
    
    @staticmethod
    def validate_frontmatter(frontmatter: Dict[str, Any]) -> bool:
        """
        Validate that frontmatter contains required fields.
        
        Args:
            frontmatter: Parsed frontmatter dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['name', 'description', 'keywords']
        
        for field in required_fields:
            if field not in frontmatter:
                return False
            
            # Check that fields are not empty
            value = frontmatter[field]
            if field == 'keywords':
                if not isinstance(value, list) or len(value) == 0:
                    return False
            else:
                if not value or (isinstance(value, str) and not value.strip()):
                    return False
        
        return True
    
    @staticmethod
    def validate_power_md(file_path: Path) -> tuple[bool, str]:
        """
        Validate a power.md file's YAML frontmatter.
        
        Args:
            file_path: Path to the power.md file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter = YAMLHandler.parse_frontmatter(content)
            
            if not YAMLHandler.validate_frontmatter(frontmatter):
                return False, "Missing required fields (name, description, keywords)"
            
            return True, ""
        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {e}"
