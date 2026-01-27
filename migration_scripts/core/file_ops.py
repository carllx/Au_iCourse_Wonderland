"""File system operations for migration."""

from pathlib import Path
from typing import List, Optional
import hashlib


class FileOperations:
    """Handles file system operations for the migration process."""
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            path: Path to the directory
            
        Raises:
            OSError: If directory creation fails
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Failed to create directory {path}: {e}")
    
    @staticmethod
    def read_file(path: Path) -> str:
        """
        Read content from a file.
        
        Args:
            path: Path to the file
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            return path.read_text(encoding='utf-8')
        except IOError as e:
            raise IOError(f"Failed to read file {path}: {e}")
    
    @staticmethod
    def write_file(path: Path, content: str) -> None:
        """
        Write content to a file.
        
        Args:
            path: Path to the file
            content: Content to write
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Ensure parent directory exists
            FileOperations.ensure_directory(path.parent)
            path.write_text(content, encoding='utf-8')
        except IOError as e:
            raise IOError(f"Failed to write file {path}: {e}")
    
    @staticmethod
    def file_exists(path: Path) -> bool:
        """
        Check if a file exists.
        
        Args:
            path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return path.exists() and path.is_file()
    
    @staticmethod
    def directory_exists(path: Path) -> bool:
        """
        Check if a directory exists.
        
        Args:
            path: Path to check
            
        Returns:
            True if directory exists, False otherwise
        """
        return path.exists() and path.is_dir()
    
    @staticmethod
    def get_file_size(path: Path) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: Path to the file
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.stat().st_size
    
    @staticmethod
    def list_files(directory: Path, pattern: str = "*") -> List[Path]:
        """
        List files in a directory matching a pattern.
        
        Args:
            directory: Directory to search
            pattern: Glob pattern (default: "*")
            
        Returns:
            List of matching file paths
        """
        if not directory.exists():
            return []
        return [f for f in directory.glob(pattern) if f.is_file()]
    
    @staticmethod
    def list_files_recursive(directory: Path, pattern: str = "*") -> List[Path]:
        """
        Recursively list files in a directory matching a pattern.
        
        Args:
            directory: Directory to search
            pattern: Glob pattern (default: "*")
            
        Returns:
            List of matching file paths
        """
        if not directory.exists():
            return []
        return [f for f in directory.rglob(pattern) if f.is_file()]
    
    @staticmethod
    def compute_directory_hash(directory: Path) -> str:
        """
        Compute a hash of all files in a directory (for verification).
        
        Args:
            directory: Directory to hash
            
        Returns:
            SHA256 hash of directory contents
        """
        if not directory.exists():
            return ""
        
        hasher = hashlib.sha256()
        
        # Get all files sorted by path for consistent hashing
        files = sorted(FileOperations.list_files_recursive(directory))
        
        for file_path in files:
            # Hash the relative path
            rel_path = file_path.relative_to(directory)
            hasher.update(str(rel_path).encode('utf-8'))
            
            # Hash the file content
            try:
                content = file_path.read_bytes()
                hasher.update(content)
            except IOError:
                # Skip files that can't be read
                continue
        
        return hasher.hexdigest()
