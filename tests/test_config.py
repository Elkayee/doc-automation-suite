import pytest
from pathlib import Path
from src.core.config import TemplateConfig
import tempfile
import yaml

def test_template_config_valid_paths():
    config = TemplateConfig(
        name="Test",
        description="A test",
        type="report",
        required_files=["valid.md", "folder/other.md"],
        docx_template="template.docx",
        chapter_order=["valid.md"]
    )
    assert config.name == "Test"

def test_template_config_path_traversal_docx_template():
    with pytest.raises(ValueError, match="Path traversal detected in path"):
        TemplateConfig(
            name="Test",
            description="A test",
            type="report",
            required_files=[],
            docx_template="../template.docx"
        )

def test_template_config_path_traversal_required_files():
    with pytest.raises(ValueError, match="Path traversal detected in path"):
        TemplateConfig(
            name="Test",
            description="A test",
            type="report",
            required_files=["valid.md", "../../secret.md"],
            docx_template="template.docx"
        )

def test_template_config_path_traversal_chapter_order():
    with pytest.raises(ValueError, match="Path traversal detected in path"):
        TemplateConfig(
            name="Test",
            description="A test",
            type="report",
            required_files=["valid.md"],
            docx_template="template.docx",
            chapter_order=["valid.md", "../other.md"]
        )

def test_template_config_load_with_traversal():
    with tempfile.TemporaryDirectory() as tempdir:
        config_path = Path(tempdir) / 'config.yaml'
        with open(config_path, 'w') as f:
            yaml.safe_dump({
                'name': 'Test',
                'required_files': ['valid.md', '../secret.md'],
                'docx_template': 'template.docx'
            }, f)

        with pytest.raises(ValueError, match="Path traversal detected in path"):
            TemplateConfig.load(config_path)

def test_template_config_load_valid():
    with tempfile.TemporaryDirectory() as tempdir:
        config_path = Path(tempdir) / 'config.yaml'
        with open(config_path, 'w') as f:
            yaml.safe_dump({
                'name': 'Test',
                'required_files': ['valid.md'],
                'docx_template': 'template.docx'
            }, f)

        config = TemplateConfig.load(config_path)
        assert config.name == "Test"
        assert config.required_files == ["valid.md"]


def test_template_config_absolute_path_docx_template():
    with pytest.raises(ValueError, match="Absolute paths are not allowed"):
        TemplateConfig(
            name="Test",
            description="A test",
            type="report",
            required_files=[],
            docx_template="/etc/passwd"
        )
