"""Power directory creation and setup utilities."""

from pathlib import Path
from typing import List, Dict
from .file_ops import FileOperations
from .naming import NamingConverter


class PowerSetup:
    """Handles creation of Power directory structures."""
    
    # Define the three skills to migrate
    SKILLS = [
        {
            'name': 'lab-factory',
            'display_name': 'Lab Factory',
            'has_steering': True
        },
        {
            'name': 'validation-suite',
            'display_name': 'Validation Suite',
            'has_steering': False
        },
        {
            'name': 'transcript_compiler',
            'display_name': 'Transcript Compiler',
            'has_steering': False
        }
    ]
    
    @staticmethod
    def create_powers_base_directory(base_path: Path = None) -> Path:
        """
        Create the base .kiro/powers/ directory if it doesn't exist.
        
        Args:
            base_path: Optional base path (defaults to current directory)
            
        Returns:
            Path to the powers directory
            
        Raises:
            OSError: If directory creation fails
        """
        if base_path is None:
            base_path = Path.cwd()
        
        powers_dir = base_path / ".kiro" / "powers"
        FileOperations.ensure_directory(powers_dir)
        
        return powers_dir
    
    @staticmethod
    def create_power_directory(
        skill_name: str,
        base_path: Path = None,
        create_steering: bool = False
    ) -> Dict[str, Path]:
        """
        Create a Power directory structure for a skill.
        
        Args:
            skill_name: Name of the skill (e.g., "lab-factory", "validation_suite")
            base_path: Optional base path (defaults to current directory)
            create_steering: Whether to create a steering subdirectory
            
        Returns:
            Dictionary with paths:
                - 'power_dir': Path to the power directory
                - 'steering_dir': Path to steering directory (if created)
                
        Raises:
            OSError: If directory creation fails
        """
        if base_path is None:
            base_path = Path.cwd()
        
        # Ensure base powers directory exists
        powers_dir = PowerSetup.create_powers_base_directory(base_path)
        
        # Convert skill name to power directory name
        power_dir_name = NamingConverter.skill_to_power_directory(skill_name)
        power_dir = powers_dir / power_dir_name
        
        # Create the power directory
        FileOperations.ensure_directory(power_dir)
        
        result = {'power_dir': power_dir}
        
        # Create steering subdirectory if requested
        if create_steering:
            steering_dir = power_dir / "steering"
            FileOperations.ensure_directory(steering_dir)
            result['steering_dir'] = steering_dir
        
        return result
    
    @staticmethod
    def create_all_power_directories(base_path: Path = None) -> Dict[str, Dict[str, Path]]:
        """
        Create all three Power directories for the migration.
        
        Creates:
        - .kiro/powers/lab-factory-power/ (with steering subdirectory)
        - .kiro/powers/validation-suite-power/
        - .kiro/powers/transcript-compiler-power/
        
        Args:
            base_path: Optional base path (defaults to current directory)
            
        Returns:
            Dictionary mapping skill names to their directory paths
            
        Raises:
            OSError: If directory creation fails
        """
        if base_path is None:
            base_path = Path.cwd()
        
        results = {}
        
        for skill in PowerSetup.SKILLS:
            skill_name = skill['name']
            has_steering = skill['has_steering']
            
            paths = PowerSetup.create_power_directory(
                skill_name=skill_name,
                base_path=base_path,
                create_steering=has_steering
            )
            
            results[skill_name] = paths
        
        return results
    
    @staticmethod
    def verify_power_structure(base_path: Path = None) -> Dict[str, bool]:
        """
        Verify that all Power directories have been created correctly.
        
        Args:
            base_path: Optional base path (defaults to current directory)
            
        Returns:
            Dictionary mapping skill names to verification status (True if valid)
        """
        if base_path is None:
            base_path = Path.cwd()
        
        powers_dir = base_path / ".kiro" / "powers"
        results = {}
        
        for skill in PowerSetup.SKILLS:
            skill_name = skill['name']
            power_dir_name = NamingConverter.skill_to_power_directory(skill_name)
            power_dir = powers_dir / power_dir_name
            
            # Check if power directory exists
            if not FileOperations.directory_exists(power_dir):
                results[skill_name] = False
                continue
            
            # Check if steering directory exists (for lab-factory only)
            if skill['has_steering']:
                steering_dir = power_dir / "steering"
                if not FileOperations.directory_exists(steering_dir):
                    results[skill_name] = False
                    continue
            
            results[skill_name] = True
        
        return results
    
    @staticmethod
    def get_power_directory_path(skill_name: str, base_path: Path = None) -> Path:
        """
        Get the path to a Power directory for a given skill.
        
        Args:
            skill_name: Name of the skill
            base_path: Optional base path (defaults to current directory)
            
        Returns:
            Path to the power directory
        """
        if base_path is None:
            base_path = Path.cwd()
        
        powers_dir = base_path / ".kiro" / "powers"
        power_dir_name = NamingConverter.skill_to_power_directory(skill_name)
        
        return powers_dir / power_dir_name
