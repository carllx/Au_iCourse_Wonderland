"""Script scanning and documentation generation utilities."""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re


class ScriptInfo:
    """Information about a discovered script."""
    
    def __init__(
        self,
        name: str,
        path: Path,
        script_type: str,
        skill: str
    ):
        """
        Initialize script information.
        
        Args:
            name: Script filename
            path: Full path to the script
            script_type: Type of script ('python', 'jsx', 'executor')
            skill: Skill name the script belongs to
        """
        self.name = name
        self.path = path
        self.script_type = script_type
        self.skill = skill
        self.purpose: Optional[str] = None
        self.parameters: Dict[str, str] = {}
        self.dependencies: List[str] = []
        self.execution_context: Optional[str] = None
    
    def __repr__(self):
        return f"ScriptInfo(name={self.name}, type={self.script_type}, skill={self.skill})"


class ScriptScanner:
    """Scans directories for scripts and generates documentation."""
    
    # Script file extensions to scan
    SCRIPT_EXTENSIONS = {'.py', '.jsx'}
    
    @staticmethod
    def scan_skill_directory(skill_path: Path) -> List[ScriptInfo]:
        """
        Scan a skill directory for scripts in lib/ and scripts/ subdirectories.
        
        Args:
            skill_path: Path to the skill directory (e.g., .agent/skills/lab-factory)
            
        Returns:
            List of ScriptInfo objects for discovered scripts
        """
        scripts = []
        skill_name = skill_path.name
        
        # Scan lib/ directory
        lib_dir = skill_path / "lib"
        if lib_dir.exists() and lib_dir.is_dir():
            scripts.extend(ScriptScanner._scan_directory(lib_dir, skill_name))
        
        # Scan scripts/ directory
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists() and scripts_dir.is_dir():
            scripts.extend(ScriptScanner._scan_directory(scripts_dir, skill_name))
        
        return scripts
    
    @staticmethod
    def _scan_directory(directory: Path, skill_name: str) -> List[ScriptInfo]:
        """
        Scan a single directory for script files.
        
        Args:
            directory: Directory to scan
            skill_name: Name of the skill
            
        Returns:
            List of ScriptInfo objects
        """
        scripts = []
        
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix in ScriptScanner.SCRIPT_EXTENSIONS:
                script_type = 'python' if file_path.suffix == '.py' else 'jsx'
                script_info = ScriptInfo(
                    name=file_path.name,
                    path=file_path,
                    script_type=script_type,
                    skill=skill_name
                )
                scripts.append(script_info)
        
        return scripts
    
    @staticmethod
    def scan_all_skills(agent_path: Path) -> Dict[str, List[ScriptInfo]]:
        """
        Scan all skill directories for scripts.
        
        Args:
            agent_path: Path to .agent directory
            
        Returns:
            Dictionary mapping skill names to lists of ScriptInfo objects
        """
        skills_dir = agent_path / "skills"
        if not skills_dir.exists():
            return {}
        
        all_scripts = {}
        
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                scripts = ScriptScanner.scan_skill_directory(skill_dir)
                if scripts:
                    all_scripts[skill_dir.name] = scripts
        
        return all_scripts
    
    @staticmethod
    def scan_executors(agent_path: Path) -> List[ScriptInfo]:
        """
        Scan the executors directory for Python scripts.
        
        Args:
            agent_path: Path to .agent directory
            
        Returns:
            List of ScriptInfo objects for executor scripts
        """
        executors_dir = agent_path / "executors"
        if not executors_dir.exists():
            return []
        
        scripts = []
        
        for file_path in executors_dir.iterdir():
            if file_path.is_file() and file_path.suffix == '.py':
                script_info = ScriptInfo(
                    name=file_path.name,
                    path=file_path,
                    script_type='executor',
                    skill='executors'
                )
                scripts.append(script_info)
        
        return scripts
    
    @staticmethod
    def extract_script_metadata(script_info: ScriptInfo) -> ScriptInfo:
        """
        Extract metadata from script file (docstrings, comments, etc.).
        
        Args:
            script_info: ScriptInfo object to enrich with metadata
            
        Returns:
            Updated ScriptInfo object
        """
        if not script_info.path.exists():
            return script_info
        
        try:
            content = script_info.path.read_text(encoding='utf-8')
            
            if script_info.script_type == 'python':
                script_info = ScriptScanner._extract_python_metadata(content, script_info)
            elif script_info.script_type == 'jsx':
                script_info = ScriptScanner._extract_jsx_metadata(content, script_info)
            
        except (IOError, UnicodeDecodeError):
            # If we can't read the file, just return the basic info
            pass
        
        return script_info
    
    @staticmethod
    def _extract_python_metadata(content: str, script_info: ScriptInfo) -> ScriptInfo:
        """
        Extract metadata from Python script.
        
        Args:
            content: Script file content
            script_info: ScriptInfo object to update
            
        Returns:
            Updated ScriptInfo object
        """
        # Extract module docstring (first triple-quoted string)
        docstring_pattern = r'^"""(.*?)"""'
        match = re.search(docstring_pattern, content, re.DOTALL | re.MULTILINE)
        if match:
            docstring = match.group(1).strip()
            # Use first line as purpose
            first_line = docstring.split('\n')[0].strip()
            if first_line:
                script_info.purpose = first_line
        
        # Extract argparse arguments
        arg_pattern = r'parser\.add_argument\([\'"]([^\'\"]+)[\'"].*?help=[\'"]([^\'\"]+)[\'"]'
        for match in re.finditer(arg_pattern, content):
            param_name = match.group(1)
            param_help = match.group(2)
            script_info.parameters[param_name] = param_help
        
        # Extract import statements as dependencies
        import_pattern = r'^(?:from|import)\s+(\w+)'
        imports = set()
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            module = match.group(1)
            # Filter out standard library modules (basic heuristic)
            if module not in {'os', 'sys', 're', 'json', 'pathlib', 'typing', 'argparse'}:
                imports.add(module)
        
        if imports:
            script_info.dependencies = sorted(list(imports))
        
        return script_info
    
    @staticmethod
    def _extract_jsx_metadata(content: str, script_info: ScriptInfo) -> ScriptInfo:
        """
        Extract metadata from JSX/ExtendScript file.
        
        Args:
            content: Script file content
            script_info: ScriptInfo object to update
            
        Returns:
            Updated ScriptInfo object
        """
        # Extract block comments at the start of file
        comment_pattern = r'^/\*\*(.*?)\*/'
        match = re.search(comment_pattern, content, re.DOTALL)
        if match:
            comment = match.group(1).strip()
            # Look for @description or first line
            desc_pattern = r'@description\s+(.+)'
            desc_match = re.search(desc_pattern, comment)
            if desc_match:
                script_info.purpose = desc_match.group(1).strip()
            else:
                # Use first non-empty line
                lines = [line.strip().lstrip('*').strip() for line in comment.split('\n')]
                for line in lines:
                    if line:
                        script_info.purpose = line
                        break
        
        # JSX scripts typically don't have command-line parameters
        # but may have dependencies on other JSX files
        include_pattern = r'#include\s+[\'"]([^\'\"]+)[\'"]'
        includes = []
        for match in re.finditer(include_pattern, content):
            includes.append(match.group(1))
        
        if includes:
            script_info.dependencies = includes
        
        return script_info
    
    @staticmethod
    def generate_usage_example(script_info: ScriptInfo) -> str:
        """
        Generate a command-line usage example for a script.
        
        Args:
            script_info: ScriptInfo object
            
        Returns:
            Command-line usage string
        """
        if script_info.script_type == 'python' or script_info.script_type == 'executor':
            cmd = f"python3 {script_info.path}"
            
            # Add common parameters if they exist
            if script_info.parameters:
                # Add a few example parameters
                param_examples = []
                for param in list(script_info.parameters.keys())[:2]:
                    if param.startswith('--'):
                        param_examples.append(f"{param} <value>")
                
                if param_examples:
                    cmd += " " + " ".join(param_examples)
            
            return cmd
        
        elif script_info.script_type == 'jsx':
            # JSX scripts are typically run through Adobe applications
            # or via command-line tools like osascript (macOS)
            return f"# Run via Adobe Audition or include in manifest\n# Location: {script_info.path}"
        
        return str(script_info.path)
    
    @staticmethod
    def generate_script_documentation(script_info: ScriptInfo) -> str:
        """
        Generate complete documentation for a script using the template.
        
        Args:
            script_info: ScriptInfo object with metadata
            
        Returns:
            Markdown formatted documentation
        """
        from .content_merger import ContentMerger
        
        # Ensure we have at least basic metadata
        if not script_info.purpose:
            script_info.purpose = f"{script_info.script_type.upper()} script"
        
        # Generate usage example
        usage = ScriptScanner.generate_usage_example(script_info)
        
        # Use ContentMerger to create standardized documentation
        return ContentMerger.create_script_documentation(
            script_name=script_info.name,
            purpose=script_info.purpose,
            location=script_info.path,
            usage_example=usage,
            parameters=script_info.parameters if script_info.parameters else None,
            dependencies=script_info.dependencies if script_info.dependencies else None,
            execution_context=script_info.execution_context
        )
    
    @staticmethod
    def generate_all_documentation(
        scripts: List[ScriptInfo],
        extract_metadata: bool = True
    ) -> str:
        """
        Generate documentation for multiple scripts.
        
        Args:
            scripts: List of ScriptInfo objects
            extract_metadata: Whether to extract metadata from script files
            
        Returns:
            Combined markdown documentation for all scripts
        """
        if not scripts:
            return ""
        
        docs = []
        
        for script_info in scripts:
            if extract_metadata:
                script_info = ScriptScanner.extract_script_metadata(script_info)
            
            doc = ScriptScanner.generate_script_documentation(script_info)
            docs.append(doc)
        
        return "\n".join(docs)
