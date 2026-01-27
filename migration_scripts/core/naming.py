"""Naming conversion utilities for migration."""

import re


class NamingConverter:
    """Handles naming conversions for Power directories."""
    
    @staticmethod
    def to_kebab_case(name: str) -> str:
        """
        Convert a skill name to kebab-case format.
        
        Handles:
        - Uppercase letters (converts to lowercase)
        - Spaces (converts to hyphens)
        - Underscores (converts to hyphens)
        - Multiple consecutive special characters (collapses to single hyphen)
        - Leading/trailing special characters (removes them)
        
        Args:
            name: Original skill name (e.g., "Lab Factory", "validation_suite", "TranscriptCompiler")
            
        Returns:
            kebab-case formatted name (e.g., "lab-factory", "validation-suite", "transcript-compiler")
            
        Examples:
            >>> NamingConverter.to_kebab_case("Lab Factory")
            'lab-factory'
            >>> NamingConverter.to_kebab_case("validation_suite")
            'validation-suite'
            >>> NamingConverter.to_kebab_case("TranscriptCompiler")
            'transcript-compiler'
            >>> NamingConverter.to_kebab_case("My__Skill  Name")
            'my-skill-name'
        """
        if not name:
            return ""
        
        # Step 1: Insert hyphens before uppercase letters that follow lowercase letters or digits
        # This handles camelCase and PascalCase (e.g., "TranscriptCompiler" -> "Transcript-Compiler")
        # Also handles cases like "Lab2Factory" -> "Lab2-Factory"
        result = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
        
        # Step 2: Convert to lowercase
        result = result.lower()
        
        # Step 3: Replace spaces and underscores with hyphens
        result = re.sub(r'[\s_]+', '-', result)
        
        # Step 4: Replace any other non-alphanumeric characters (except hyphens) with hyphens
        result = re.sub(r'[^a-z0-9-]+', '-', result)
        
        # Step 5: Collapse multiple consecutive hyphens into a single hyphen
        result = re.sub(r'-+', '-', result)
        
        # Step 6: Remove leading and trailing hyphens
        result = result.strip('-')
        
        return result
    
    @staticmethod
    def skill_to_power_directory(skill_name: str) -> str:
        """
        Convert a skill name to a Power directory name.
        
        Adds the "-power" suffix to the kebab-case skill name.
        
        Args:
            skill_name: Original skill name
            
        Returns:
            Power directory name (e.g., "lab-factory-power")
            
        Examples:
            >>> NamingConverter.skill_to_power_directory("Lab Factory")
            'lab-factory-power'
            >>> NamingConverter.skill_to_power_directory("validation_suite")
            'validation-suite-power'
        """
        kebab_name = NamingConverter.to_kebab_case(skill_name)
        if not kebab_name:
            return "power"
        return f"{kebab_name}-power"
