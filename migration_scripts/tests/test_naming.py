"""Unit tests for naming conversion utilities."""

import pytest
from migration_scripts.core.naming import NamingConverter


class TestNamingConverter:
    """Test suite for NamingConverter class."""
    
    def test_to_kebab_case_with_spaces(self):
        """Test conversion of names with spaces."""
        assert NamingConverter.to_kebab_case("Lab Factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("My Skill Name") == "my-skill-name"
        assert NamingConverter.to_kebab_case("Single") == "single"
    
    def test_to_kebab_case_with_underscores(self):
        """Test conversion of names with underscores."""
        assert NamingConverter.to_kebab_case("validation_suite") == "validation-suite"
        assert NamingConverter.to_kebab_case("transcript_compiler") == "transcript-compiler"
        assert NamingConverter.to_kebab_case("my_skill_name") == "my-skill-name"
    
    def test_to_kebab_case_with_camel_case(self):
        """Test conversion of camelCase names."""
        assert NamingConverter.to_kebab_case("labFactory") == "lab-factory"
        assert NamingConverter.to_kebab_case("validationSuite") == "validation-suite"
        assert NamingConverter.to_kebab_case("transcriptCompiler") == "transcript-compiler"
    
    def test_to_kebab_case_with_pascal_case(self):
        """Test conversion of PascalCase names."""
        assert NamingConverter.to_kebab_case("LabFactory") == "lab-factory"
        assert NamingConverter.to_kebab_case("ValidationSuite") == "validation-suite"
        assert NamingConverter.to_kebab_case("TranscriptCompiler") == "transcript-compiler"
    
    def test_to_kebab_case_with_mixed_formats(self):
        """Test conversion of names with mixed formatting."""
        assert NamingConverter.to_kebab_case("Lab_Factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("validation Suite") == "validation-suite"
        assert NamingConverter.to_kebab_case("Transcript_Compiler") == "transcript-compiler"
    
    def test_to_kebab_case_with_multiple_consecutive_separators(self):
        """Test handling of multiple consecutive spaces/underscores."""
        assert NamingConverter.to_kebab_case("My__Skill  Name") == "my-skill-name"
        assert NamingConverter.to_kebab_case("Lab___Factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("Test    Skill") == "test-skill"
    
    def test_to_kebab_case_with_leading_trailing_separators(self):
        """Test removal of leading/trailing separators."""
        assert NamingConverter.to_kebab_case("_Lab Factory_") == "lab-factory"
        assert NamingConverter.to_kebab_case(" Validation Suite ") == "validation-suite"
        assert NamingConverter.to_kebab_case("__Transcript__") == "transcript"
    
    def test_to_kebab_case_with_special_characters(self):
        """Test handling of special characters."""
        assert NamingConverter.to_kebab_case("Lab@Factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("Validation#Suite") == "validation-suite"
        assert NamingConverter.to_kebab_case("Test!Skill$Name") == "test-skill-name"
    
    def test_to_kebab_case_with_numbers(self):
        """Test handling of numbers in names."""
        assert NamingConverter.to_kebab_case("Lab Factory 2") == "lab-factory-2"
        assert NamingConverter.to_kebab_case("Validation3Suite") == "validation3-suite"
        assert NamingConverter.to_kebab_case("Test123") == "test123"
    
    def test_to_kebab_case_already_kebab_case(self):
        """Test that already kebab-case names remain unchanged."""
        assert NamingConverter.to_kebab_case("lab-factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("validation-suite") == "validation-suite"
        assert NamingConverter.to_kebab_case("transcript-compiler") == "transcript-compiler"
    
    def test_to_kebab_case_empty_string(self):
        """Test handling of empty string."""
        assert NamingConverter.to_kebab_case("") == ""
    
    def test_to_kebab_case_only_special_characters(self):
        """Test handling of strings with only special characters."""
        assert NamingConverter.to_kebab_case("___") == ""
        assert NamingConverter.to_kebab_case("   ") == ""
        assert NamingConverter.to_kebab_case("@#$") == ""
    
    def test_skill_to_power_directory_basic(self):
        """Test conversion of skill names to power directory names."""
        assert NamingConverter.skill_to_power_directory("Lab Factory") == "lab-factory-power"
        assert NamingConverter.skill_to_power_directory("validation_suite") == "validation-suite-power"
        assert NamingConverter.skill_to_power_directory("TranscriptCompiler") == "transcript-compiler-power"
    
    def test_skill_to_power_directory_with_complex_names(self):
        """Test power directory naming with complex skill names."""
        assert NamingConverter.skill_to_power_directory("My Complex Skill") == "my-complex-skill-power"
        assert NamingConverter.skill_to_power_directory("Test_Skill_123") == "test-skill-123-power"
    
    def test_skill_to_power_directory_empty_string(self):
        """Test power directory naming with empty string."""
        assert NamingConverter.skill_to_power_directory("") == "power"
    
    def test_actual_skill_names(self):
        """Test with the actual skill names from the project."""
        # These are the three skills mentioned in the requirements
        assert NamingConverter.to_kebab_case("lab-factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("validation-suite") == "validation-suite"
        assert NamingConverter.to_kebab_case("transcript_compiler") == "transcript-compiler"
        
        # Test the power directory names
        assert NamingConverter.skill_to_power_directory("lab-factory") == "lab-factory-power"
        assert NamingConverter.skill_to_power_directory("validation-suite") == "validation-suite-power"
        assert NamingConverter.skill_to_power_directory("transcript_compiler") == "transcript-compiler-power"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_unicode_characters(self):
        """Test handling of unicode characters."""
        # Unicode characters should be replaced with hyphens
        assert NamingConverter.to_kebab_case("Lab™Factory") == "lab-factory"
        assert NamingConverter.to_kebab_case("Café Skill") == "caf-skill"
    
    def test_very_long_names(self):
        """Test handling of very long names."""
        long_name = "This Is A Very Long Skill Name With Many Words"
        result = NamingConverter.to_kebab_case(long_name)
        assert result == "this-is-a-very-long-skill-name-with-many-words"
        assert "-" in result
        assert result.islower() or not result.isalpha()  # All letters should be lowercase
    
    def test_consecutive_uppercase_letters(self):
        """Test handling of consecutive uppercase letters (acronyms)."""
        assert NamingConverter.to_kebab_case("HTTPServer") == "httpserver"
        assert NamingConverter.to_kebab_case("XMLParser") == "xmlparser"
        # Note: This is expected behavior - acronyms are kept together
    
    def test_mixed_case_with_numbers(self):
        """Test mixed case with numbers."""
        assert NamingConverter.to_kebab_case("Lab2Factory") == "lab2-factory"
        assert NamingConverter.to_kebab_case("Test123Skill456") == "test123-skill456"
