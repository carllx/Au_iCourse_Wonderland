"""Unit tests for Power directory setup utilities."""

import pytest
from pathlib import Path
import tempfile
import shutil

from migration_scripts.core.power_setup import PowerSetup
from migration_scripts.core.file_ops import FileOperations


class TestPowerSetup:
    """Test suite for PowerSetup class."""
    
    def test_create_powers_base_directory(self):
        """Test creating the base .kiro/powers/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            powers_dir = PowerSetup.create_powers_base_directory(base_path)
            
            assert powers_dir.exists()
            assert powers_dir.is_dir()
            assert powers_dir == base_path / ".kiro" / "powers"
    
    def test_create_powers_base_directory_idempotent(self):
        """Test that creating base directory multiple times is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Create once
            powers_dir1 = PowerSetup.create_powers_base_directory(base_path)
            
            # Create again
            powers_dir2 = PowerSetup.create_powers_base_directory(base_path)
            
            assert powers_dir1 == powers_dir2
            assert powers_dir1.exists()
    
    def test_create_power_directory_basic(self):
        """Test creating a basic Power directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            result = PowerSetup.create_power_directory("lab-factory", base_path)
            
            assert 'power_dir' in result
            assert result['power_dir'].exists()
            assert result['power_dir'].is_dir()
            assert result['power_dir'].name == "lab-factory-power"
    
    def test_create_power_directory_with_steering(self):
        """Test creating a Power directory with steering subdirectory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            result = PowerSetup.create_power_directory(
                "lab-factory",
                base_path,
                create_steering=True
            )
            
            assert 'power_dir' in result
            assert 'steering_dir' in result
            assert result['power_dir'].exists()
            assert result['steering_dir'].exists()
            assert result['steering_dir'].is_dir()
            assert result['steering_dir'].name == "steering"
            assert result['steering_dir'].parent == result['power_dir']
    
    def test_create_power_directory_without_steering(self):
        """Test creating a Power directory without steering subdirectory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            result = PowerSetup.create_power_directory(
                "validation-suite",
                base_path,
                create_steering=False
            )
            
            assert 'power_dir' in result
            assert 'steering_dir' not in result
            assert result['power_dir'].exists()
            
            # Verify steering directory was not created
            steering_dir = result['power_dir'] / "steering"
            assert not steering_dir.exists()
    
    def test_create_power_directory_with_underscore_name(self):
        """Test creating a Power directory with underscore in skill name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            result = PowerSetup.create_power_directory("transcript_compiler", base_path)
            
            assert result['power_dir'].exists()
            assert result['power_dir'].name == "transcript-compiler-power"
    
    def test_create_all_power_directories(self):
        """Test creating all three Power directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            results = PowerSetup.create_all_power_directories(base_path)
            
            # Check that all three skills are in results
            assert 'lab-factory' in results
            assert 'validation-suite' in results
            assert 'transcript_compiler' in results
            
            # Check lab-factory has steering directory
            assert 'power_dir' in results['lab-factory']
            assert 'steering_dir' in results['lab-factory']
            assert results['lab-factory']['power_dir'].exists()
            assert results['lab-factory']['steering_dir'].exists()
            
            # Check validation-suite does not have steering directory
            assert 'power_dir' in results['validation-suite']
            assert 'steering_dir' not in results['validation-suite']
            assert results['validation-suite']['power_dir'].exists()
            
            # Check transcript_compiler does not have steering directory
            assert 'power_dir' in results['transcript_compiler']
            assert 'steering_dir' not in results['transcript_compiler']
            assert results['transcript_compiler']['power_dir'].exists()
    
    def test_create_all_power_directories_correct_names(self):
        """Test that all Power directories have correct kebab-case names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            results = PowerSetup.create_all_power_directories(base_path)
            
            # Verify directory names
            assert results['lab-factory']['power_dir'].name == "lab-factory-power"
            assert results['validation-suite']['power_dir'].name == "validation-suite-power"
            assert results['transcript_compiler']['power_dir'].name == "transcript-compiler-power"
    
    def test_verify_power_structure_all_valid(self):
        """Test verifying a complete Power structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Create all directories
            PowerSetup.create_all_power_directories(base_path)
            
            # Verify structure
            verification = PowerSetup.verify_power_structure(base_path)
            
            assert verification['lab-factory'] is True
            assert verification['validation-suite'] is True
            assert verification['transcript_compiler'] is True
    
    def test_verify_power_structure_missing_directory(self):
        """Test verifying when a Power directory is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Create only some directories
            PowerSetup.create_power_directory("lab-factory", base_path, create_steering=True)
            PowerSetup.create_power_directory("validation-suite", base_path)
            # Don't create transcript_compiler
            
            # Verify structure
            verification = PowerSetup.verify_power_structure(base_path)
            
            assert verification['lab-factory'] is True
            assert verification['validation-suite'] is True
            assert verification['transcript_compiler'] is False
    
    def test_verify_power_structure_missing_steering(self):
        """Test verifying when steering directory is missing for lab-factory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Create lab-factory without steering directory
            PowerSetup.create_power_directory("lab-factory", base_path, create_steering=False)
            
            # Verify structure
            verification = PowerSetup.verify_power_structure(base_path)
            
            # Should fail because lab-factory requires steering directory
            assert verification['lab-factory'] is False
    
    def test_verify_power_structure_no_directories(self):
        """Test verifying when no directories exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Don't create any directories
            verification = PowerSetup.verify_power_structure(base_path)
            
            assert verification['lab-factory'] is False
            assert verification['validation-suite'] is False
            assert verification['transcript_compiler'] is False
    
    def test_get_power_directory_path(self):
        """Test getting the path to a Power directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            path = PowerSetup.get_power_directory_path("lab-factory", base_path)
            
            expected = base_path / ".kiro" / "powers" / "lab-factory-power"
            assert path == expected
    
    def test_get_power_directory_path_with_underscore(self):
        """Test getting path for skill name with underscore."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            path = PowerSetup.get_power_directory_path("transcript_compiler", base_path)
            
            expected = base_path / ".kiro" / "powers" / "transcript-compiler-power"
            assert path == expected
    
    def test_skills_constant_has_correct_structure(self):
        """Test that SKILLS constant has the expected structure."""
        skills = PowerSetup.SKILLS
        
        assert len(skills) == 3
        
        # Check each skill has required fields
        for skill in skills:
            assert 'name' in skill
            assert 'display_name' in skill
            assert 'has_steering' in skill
            assert isinstance(skill['name'], str)
            assert isinstance(skill['display_name'], str)
            assert isinstance(skill['has_steering'], bool)
    
    def test_skills_constant_has_correct_skills(self):
        """Test that SKILLS constant contains the three expected skills."""
        skill_names = [skill['name'] for skill in PowerSetup.SKILLS]
        
        assert 'lab-factory' in skill_names
        assert 'validation-suite' in skill_names
        assert 'transcript_compiler' in skill_names
    
    def test_skills_constant_steering_flags(self):
        """Test that steering flags are set correctly."""
        skills_dict = {skill['name']: skill for skill in PowerSetup.SKILLS}
        
        # Only lab-factory should have steering
        assert skills_dict['lab-factory']['has_steering'] is True
        assert skills_dict['validation-suite']['has_steering'] is False
        assert skills_dict['transcript_compiler']['has_steering'] is False


class TestPowerSetupIntegration:
    """Integration tests for PowerSetup."""
    
    def test_full_migration_workflow(self):
        """Test the complete workflow of creating all Power directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Step 1: Create all directories
            results = PowerSetup.create_all_power_directories(base_path)
            
            # Step 2: Verify all directories exist
            powers_dir = base_path / ".kiro" / "powers"
            assert powers_dir.exists()
            
            # Step 3: Check each power directory
            lab_factory_dir = powers_dir / "lab-factory-power"
            assert lab_factory_dir.exists()
            assert (lab_factory_dir / "steering").exists()
            
            validation_suite_dir = powers_dir / "validation-suite-power"
            assert validation_suite_dir.exists()
            assert not (validation_suite_dir / "steering").exists()
            
            transcript_compiler_dir = powers_dir / "transcript-compiler-power"
            assert transcript_compiler_dir.exists()
            assert not (transcript_compiler_dir / "steering").exists()
            
            # Step 4: Verify structure
            verification = PowerSetup.verify_power_structure(base_path)
            assert all(verification.values())
    
    def test_idempotent_creation(self):
        """Test that creating directories multiple times is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            
            # Create once
            results1 = PowerSetup.create_all_power_directories(base_path)
            
            # Create again
            results2 = PowerSetup.create_all_power_directories(base_path)
            
            # Both should succeed and point to same directories
            assert results1['lab-factory']['power_dir'] == results2['lab-factory']['power_dir']
            
            # Verify structure is still valid
            verification = PowerSetup.verify_power_structure(base_path)
            assert all(verification.values())
