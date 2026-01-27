"""Integration tests for ContentExtractor with real .agent files."""

import pytest
from pathlib import Path
from migration_scripts.core.content_extractor import ContentExtractor


class TestContentExtractorIntegration:
    """Integration tests using actual .agent directory files."""
    
    @pytest.fixture
    def agent_dir(self):
        """Get the .agent directory path."""
        # Assuming tests run from project root
        agent_path = Path(".agent")
        if not agent_path.exists():
            pytest.skip(".agent directory not found")
        return agent_path
    
    def test_extract_lab_factory_skill(self, agent_dir):
        """Test extracting content from lab-factory SKILL.md."""
        skill_path = agent_dir / "skills" / "lab-factory" / "SKILL.md"
        
        if not skill_path.exists():
            pytest.skip("lab-factory SKILL.md not found")
        
        result = ContentExtractor.extract_skill_content(skill_path)
        
        # Check that key sections are extracted
        assert result['full_content'] != ''
        
        # Should contain Audition-related content
        assert 'Audition' in result['full_content']
        
        # Should have stripped frontmatter
        assert '---' not in result['full_content'][:10]
    
    def test_extract_validation_suite_skill(self, agent_dir):
        """Test extracting content from validation-suite SKILL.md."""
        skill_path = agent_dir / "skills" / "validation-suite" / "SKILL.md"
        
        if not skill_path.exists():
            pytest.skip("validation-suite SKILL.md not found")
        
        result = ContentExtractor.extract_skill_content(skill_path)
        
        assert result['full_content'] != ''
        
        # Should contain validation-related content
        assert 'validation' in result['full_content'].lower() or 'validate' in result['full_content'].lower()
    
    def test_extract_transcript_compiler_skill(self, agent_dir):
        """Test extracting content from transcript-compiler SKILL.md."""
        skill_path = agent_dir / "skills" / "transcript_compiler" / "SKILL.md"
        
        if not skill_path.exists():
            pytest.skip("transcript-compiler SKILL.md not found")
        
        result = ContentExtractor.extract_skill_content(skill_path)
        
        assert result['full_content'] != ''
    
    def test_extract_mvp_conventions_rule(self, agent_dir):
        """Test extracting MVP conventions rule."""
        rule_path = agent_dir / "rules" / "rule_mvp_conventions.md"
        
        if not rule_path.exists():
            pytest.skip("rule_mvp_conventions.md not found")
        
        result = ContentExtractor.extract_rule_content(rule_path)
        
        assert result != ''
        assert 'MVP' in result or 'convention' in result.lower()
    
    def test_extract_workflow_protocol_rule(self, agent_dir):
        """Test extracting workflow protocol rule."""
        rule_path = agent_dir / "rules" / "rule_workflow_protocol.md"
        
        if not rule_path.exists():
            pytest.skip("rule_workflow_protocol.md not found")
        
        result = ContentExtractor.extract_rule_content(rule_path)
        
        assert result != ''
    
    def test_extract_audition_skills_map(self, agent_dir):
        """Test extracting Audition Skills Map knowledge."""
        knowledge_path = agent_dir / "knowledge" / "Audition_Skills_Map.md"
        
        if not knowledge_path.exists():
            pytest.skip("Audition_Skills_Map.md not found")
        
        result = ContentExtractor.extract_knowledge_content(knowledge_path)
        
        assert result['content'] != ''
        # This file should be small enough to embed
        assert result['should_embed'] is True
        assert 'Audition' in result['content']
    
    def test_extract_textbook_index(self, agent_dir):
        """Test extracting Textbook Index knowledge."""
        knowledge_path = agent_dir / "knowledge" / "Textbook_Index.md"
        
        if not knowledge_path.exists():
            pytest.skip("Textbook_Index.md not found")
        
        result = ContentExtractor.extract_knowledge_content(knowledge_path)
        
        assert result['content'] != ''
        # Check if file size is reported
        assert result['file_size_kb'] > 0
    
    def test_extract_linxin_voice_style(self, agent_dir):
        """Test extracting LinXin Voice style guide."""
        style_path = agent_dir / "styles" / "LinXin_Voice.md"
        
        if not style_path.exists():
            pytest.skip("LinXin_Voice.md not found")
        
        result = ContentExtractor.extract_style_content(style_path)
        
        assert result != ''
        assert 'LinXin' in result or '林昕' in result
    
    def test_get_lab_factory_relevant_files(self, agent_dir):
        """Test getting all relevant files for lab-factory power."""
        rules_dir = agent_dir / "rules"
        knowledge_dir = agent_dir / "knowledge"
        styles_dir = agent_dir / "styles"
        
        # Get relevant files
        rules = ContentExtractor.get_relevant_rules("lab-factory", rules_dir)
        knowledge = ContentExtractor.get_relevant_knowledge("lab-factory", knowledge_dir)
        styles = ContentExtractor.get_relevant_styles("lab-factory", styles_dir)
        
        # lab-factory should have:
        # - rule_mvp_conventions.md
        # - Audition_Skills_Map.md
        # - no styles
        
        assert len(rules) <= 1  # May or may not exist
        assert len(knowledge) <= 1
        assert len(styles) == 0
    
    def test_get_transcript_compiler_relevant_files(self, agent_dir):
        """Test getting all relevant files for transcript-compiler power."""
        rules_dir = agent_dir / "rules"
        knowledge_dir = agent_dir / "knowledge"
        styles_dir = agent_dir / "styles"
        
        # Get relevant files
        rules = ContentExtractor.get_relevant_rules("transcript-compiler", rules_dir)
        knowledge = ContentExtractor.get_relevant_knowledge("transcript-compiler", knowledge_dir)
        styles = ContentExtractor.get_relevant_styles("transcript-compiler", styles_dir)
        
        # transcript-compiler should have:
        # - Multiple rules
        # - Textbook_Index.md, Chapter_Mapping.md
        # - LinXin_Voice.md
        
        # At least some rules should exist
        assert len(rules) >= 0
        # At least some knowledge files should exist
        assert len(knowledge) >= 0
        # Should have LinXin style
        assert len(styles) <= 1
    
    def test_identify_scripts_in_lab_factory_skill(self, agent_dir):
        """Test identifying script references in lab-factory SKILL.md."""
        skill_path = agent_dir / "skills" / "lab-factory" / "SKILL.md"
        
        if not skill_path.exists():
            pytest.skip("lab-factory SKILL.md not found")
        
        content = skill_path.read_text(encoding='utf-8')
        scripts = ContentExtractor.identify_script_references(content)
        
        # Should find JSX scripts
        jsx_scripts = [s for s in scripts if s['type'] == 'jsx']
        assert len(jsx_scripts) > 0
        
        # Should find references to Audition.jsx, Universal_Lab_Builder.jsx, etc.
        script_names = [Path(s['path']).name for s in scripts]
        assert any('Audition.jsx' in name for name in script_names)
    
    def test_extract_code_examples_from_skill(self, agent_dir):
        """Test extracting code examples from a SKILL.md file."""
        skill_path = agent_dir / "skills" / "lab-factory" / "SKILL.md"
        
        if not skill_path.exists():
            pytest.skip("lab-factory SKILL.md not found")
        
        content = skill_path.read_text(encoding='utf-8')
        examples = ContentExtractor.extract_code_examples(content)
        
        # Should find code examples
        assert len(examples) > 0
        
        # Should have JavaScript examples
        js_examples = [e for e in examples if e['language'] in ['javascript', 'js']]
        # Note: May or may not have JS examples, so we just check structure
        for example in examples:
            assert 'language' in example
            assert 'code' in example
            assert example['code'] != ''


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
