"""Unit tests for power_metadata module."""

import pytest
import yaml
from migration_scripts.core.power_metadata import (
    LAB_FACTORY_METADATA,
    VALIDATION_SUITE_METADATA,
    TRANSCRIPT_COMPILER_METADATA,
    POWER_METADATA_MAP,
    get_power_metadata,
    get_all_power_names,
    generate_frontmatter_for_power,
    generate_all_frontmatters
)


class TestPowerMetadataConstants:
    """Test the metadata constant definitions."""
    
    def test_lab_factory_metadata_structure(self):
        """Test Lab Factory metadata has all required fields."""
        assert 'name' in LAB_FACTORY_METADATA
        assert 'description' in LAB_FACTORY_METADATA
        assert 'keywords' in LAB_FACTORY_METADATA
        
    def test_lab_factory_metadata_values(self):
        """Test Lab Factory metadata has correct values."""
        assert LAB_FACTORY_METADATA['name'] == 'Lab Factory'
        assert 'Adobe Audition' in LAB_FACTORY_METADATA['description']
        assert 'audition' in LAB_FACTORY_METADATA['keywords']
        assert 'automation' in LAB_FACTORY_METADATA['keywords']
        assert 'jsx' in LAB_FACTORY_METADATA['keywords']
        
    def test_validation_suite_metadata_structure(self):
        """Test Validation Suite metadata has all required fields."""
        assert 'name' in VALIDATION_SUITE_METADATA
        assert 'description' in VALIDATION_SUITE_METADATA
        assert 'keywords' in VALIDATION_SUITE_METADATA
        
    def test_validation_suite_metadata_values(self):
        """Test Validation Suite metadata has correct values."""
        assert VALIDATION_SUITE_METADATA['name'] == 'Validation Suite'
        assert 'validation' in VALIDATION_SUITE_METADATA['keywords']
        assert 'testing' in VALIDATION_SUITE_METADATA['keywords']
        assert 'quality' in VALIDATION_SUITE_METADATA['keywords']
        
    def test_transcript_compiler_metadata_structure(self):
        """Test Transcript Compiler metadata has all required fields."""
        assert 'name' in TRANSCRIPT_COMPILER_METADATA
        assert 'description' in TRANSCRIPT_COMPILER_METADATA
        assert 'keywords' in TRANSCRIPT_COMPILER_METADATA
        
    def test_transcript_compiler_metadata_values(self):
        """Test Transcript Compiler metadata has correct values."""
        assert TRANSCRIPT_COMPILER_METADATA['name'] == 'Transcript Compiler'
        assert 'LinXin' in TRANSCRIPT_COMPILER_METADATA['description']
        assert 'transcript' in TRANSCRIPT_COMPILER_METADATA['keywords']
        assert 'compiler' in TRANSCRIPT_COMPILER_METADATA['keywords']
        assert 'linxin' in TRANSCRIPT_COMPILER_METADATA['keywords']
        
    def test_power_metadata_map_contains_all_powers(self):
        """Test POWER_METADATA_MAP contains all three Powers."""
        assert 'lab-factory-power' in POWER_METADATA_MAP
        assert 'validation-suite-power' in POWER_METADATA_MAP
        assert 'transcript-compiler-power' in POWER_METADATA_MAP
        assert len(POWER_METADATA_MAP) == 3


class TestGetPowerMetadata:
    """Test the get_power_metadata function."""
    
    def test_get_lab_factory_metadata(self):
        """Test retrieving Lab Factory metadata."""
        metadata = get_power_metadata('lab-factory-power')
        assert metadata == LAB_FACTORY_METADATA
        
    def test_get_validation_suite_metadata(self):
        """Test retrieving Validation Suite metadata."""
        metadata = get_power_metadata('validation-suite-power')
        assert metadata == VALIDATION_SUITE_METADATA
        
    def test_get_transcript_compiler_metadata(self):
        """Test retrieving Transcript Compiler metadata."""
        metadata = get_power_metadata('transcript-compiler-power')
        assert metadata == TRANSCRIPT_COMPILER_METADATA
        
    def test_get_unknown_power_raises_error(self):
        """Test that unknown power name raises KeyError."""
        with pytest.raises(KeyError) as exc_info:
            get_power_metadata('unknown-power')
        assert 'unknown-power' in str(exc_info.value)


class TestGetAllPowerNames:
    """Test the get_all_power_names function."""
    
    def test_returns_all_three_powers(self):
        """Test that all three power names are returned."""
        names = get_all_power_names()
        assert len(names) == 3
        assert 'lab-factory-power' in names
        assert 'validation-suite-power' in names
        assert 'transcript-compiler-power' in names


class TestGenerateFrontmatterForPower:
    """Test the generate_frontmatter_for_power function."""
    
    def test_generates_valid_yaml_for_lab_factory(self):
        """Test generating frontmatter for Lab Factory produces valid YAML."""
        frontmatter = generate_frontmatter_for_power('lab-factory-power')
        
        # Should start and end with ---
        assert frontmatter.startswith('---\n')
        assert frontmatter.endswith('---\n')
        
        # Extract YAML content
        yaml_content = frontmatter.split('---')[1].strip()
        parsed = yaml.safe_load(yaml_content)
        
        # Verify structure
        assert parsed['name'] == 'Lab Factory'
        assert 'Adobe Audition' in parsed['description']
        assert isinstance(parsed['keywords'], list)
        assert 'audition' in parsed['keywords']
        
    def test_generates_valid_yaml_for_validation_suite(self):
        """Test generating frontmatter for Validation Suite produces valid YAML."""
        frontmatter = generate_frontmatter_for_power('validation-suite-power')
        
        # Extract and parse YAML
        yaml_content = frontmatter.split('---')[1].strip()
        parsed = yaml.safe_load(yaml_content)
        
        # Verify structure
        assert parsed['name'] == 'Validation Suite'
        assert isinstance(parsed['keywords'], list)
        assert 'validation' in parsed['keywords']
        
    def test_generates_valid_yaml_for_transcript_compiler(self):
        """Test generating frontmatter for Transcript Compiler produces valid YAML."""
        frontmatter = generate_frontmatter_for_power('transcript-compiler-power')
        
        # Extract and parse YAML
        yaml_content = frontmatter.split('---')[1].strip()
        parsed = yaml.safe_load(yaml_content)
        
        # Verify structure
        assert parsed['name'] == 'Transcript Compiler'
        assert 'LinXin' in parsed['description']
        assert isinstance(parsed['keywords'], list)
        assert 'transcript' in parsed['keywords']
        
    def test_unknown_power_raises_error(self):
        """Test that unknown power name raises KeyError."""
        with pytest.raises(KeyError):
            generate_frontmatter_for_power('unknown-power')


class TestGenerateAllFrontmatters:
    """Test the generate_all_frontmatters function."""
    
    def test_generates_frontmatters_for_all_powers(self):
        """Test that frontmatters are generated for all three Powers."""
        all_frontmatters = generate_all_frontmatters()
        
        assert len(all_frontmatters) == 3
        assert 'lab-factory-power' in all_frontmatters
        assert 'validation-suite-power' in all_frontmatters
        assert 'transcript-compiler-power' in all_frontmatters
        
    def test_all_generated_frontmatters_are_valid_yaml(self):
        """Test that all generated frontmatters contain valid YAML."""
        all_frontmatters = generate_all_frontmatters()
        
        for power_name, frontmatter in all_frontmatters.items():
            # Should have YAML delimiters
            assert frontmatter.startswith('---\n')
            assert frontmatter.endswith('---\n')
            
            # Should be parseable
            yaml_content = frontmatter.split('---')[1].strip()
            parsed = yaml.safe_load(yaml_content)
            
            # Should have required fields
            assert 'name' in parsed
            assert 'description' in parsed
            assert 'keywords' in parsed
            assert isinstance(parsed['keywords'], list)
            assert len(parsed['keywords']) > 0


class TestMetadataRequirements:
    """Test that metadata meets requirements from design document."""
    
    def test_lab_factory_has_required_keywords(self):
        """Test Lab Factory has keywords specified in design doc."""
        keywords = LAB_FACTORY_METADATA['keywords']
        # From design doc: audition, automation, audio, jsx, extendscript
        assert 'audition' in keywords
        assert 'automation' in keywords
        assert 'audio' in keywords
        assert 'jsx' in keywords
        assert 'extendscript' in keywords
        
    def test_validation_suite_has_required_keywords(self):
        """Test Validation Suite has keywords specified in design doc."""
        keywords = VALIDATION_SUITE_METADATA['keywords']
        # From design doc: validation, testing, quality, links, consistency
        assert 'validation' in keywords
        assert 'testing' in keywords
        assert 'quality' in keywords
        assert 'links' in keywords
        assert 'consistency' in keywords
        
    def test_transcript_compiler_has_required_keywords(self):
        """Test Transcript Compiler has keywords specified in design doc."""
        keywords = TRANSCRIPT_COMPILER_METADATA['keywords']
        # From design doc: transcript, compiler, course, content, pedagogy, linxin
        assert 'transcript' in keywords
        assert 'compiler' in keywords
        assert 'course' in keywords
        assert 'content' in keywords
        assert 'pedagogy' in keywords
        assert 'linxin' in keywords
        
    def test_all_metadata_has_at_least_three_keywords(self):
        """Test that all Powers have at least 3 keywords (design recommendation)."""
        for power_name, metadata in POWER_METADATA_MAP.items():
            assert len(metadata['keywords']) >= 3, \
                f"{power_name} should have at least 3 keywords"
