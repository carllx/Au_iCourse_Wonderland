"""Power metadata definitions for the three Powers being migrated."""

from typing import Dict, List, TypedDict
from .yaml_handler import YAMLHandler


class PowerMetadata(TypedDict):
    """Type definition for Power metadata."""
    name: str
    description: str
    keywords: List[str]


# Lab Factory Power metadata
LAB_FACTORY_METADATA: PowerMetadata = {
    'name': 'Lab Factory',
    'description': 'Adobe Audition automation toolkit for audio asset generation and lab setup',
    'keywords': ['audition', 'automation', 'audio', 'jsx', 'extendscript', 'asset-generation']
}

# Validation Suite Power metadata
VALIDATION_SUITE_METADATA: PowerMetadata = {
    'name': 'Validation Suite',
    'description': 'Project health checks, link validation, and pedagogy auditing tools',
    'keywords': ['validation', 'testing', 'quality', 'links', 'consistency', 'pedagogy']
}

# Transcript Compiler Power metadata
TRANSCRIPT_COMPILER_METADATA: PowerMetadata = {
    'name': 'Transcript Compiler',
    'description': 'Compile course transcripts from structured outlines using LinXin pedagogical style',
    'keywords': ['transcript', 'compiler', 'course', 'content', 'pedagogy', 'linxin', 'courseware']
}

# Mapping from power directory names to metadata
POWER_METADATA_MAP: Dict[str, PowerMetadata] = {
    'lab-factory-power': LAB_FACTORY_METADATA,
    'validation-suite-power': VALIDATION_SUITE_METADATA,
    'transcript-compiler-power': TRANSCRIPT_COMPILER_METADATA
}


def get_power_metadata(power_dir_name: str) -> PowerMetadata:
    """
    Get metadata for a specific Power by its directory name.
    
    Args:
        power_dir_name: The kebab-case directory name of the Power
        
    Returns:
        PowerMetadata dictionary
        
    Raises:
        KeyError: If power_dir_name is not recognized
    """
    if power_dir_name not in POWER_METADATA_MAP:
        raise KeyError(f"Unknown power directory name: {power_dir_name}")
    
    return POWER_METADATA_MAP[power_dir_name]


def get_all_power_names() -> List[str]:
    """
    Get a list of all Power directory names.
    
    Returns:
        List of kebab-case Power directory names
    """
    return list(POWER_METADATA_MAP.keys())


def generate_frontmatter_for_power(power_dir_name: str) -> str:
    """
    Generate YAML frontmatter for a specific Power.
    
    Args:
        power_dir_name: The kebab-case directory name of the Power
        
    Returns:
        YAML frontmatter string with delimiters
        
    Raises:
        KeyError: If power_dir_name is not recognized
        ValueError: If metadata is invalid
    """
    metadata = get_power_metadata(power_dir_name)
    return YAMLHandler.create_frontmatter(
        name=metadata['name'],
        description=metadata['description'],
        keywords=metadata['keywords']
    )


def generate_all_frontmatters() -> Dict[str, str]:
    """
    Generate YAML frontmatter for all Powers.
    
    Returns:
        Dictionary mapping power directory names to their frontmatter strings
    """
    return {
        power_name: generate_frontmatter_for_power(power_name)
        for power_name in get_all_power_names()
    }
