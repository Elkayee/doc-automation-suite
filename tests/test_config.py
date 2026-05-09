
import yaml

from src.core.config import TemplateConfig


def test_is_safe_path():
    assert TemplateConfig.is_safe_path("template.docx") is True
    assert TemplateConfig.is_safe_path("sub/folder/file.md") is True
    assert TemplateConfig.is_safe_path("file_with_spaces.txt") is True

    assert TemplateConfig.is_safe_path("../secret.txt") is False
    assert TemplateConfig.is_safe_path("sub/../../secret.txt") is False
    assert TemplateConfig.is_safe_path("/etc/passwd") is False
    assert TemplateConfig.is_safe_path("\\Windows\\System32") is False
    assert TemplateConfig.is_safe_path("C:\\secret.txt") is False
    assert TemplateConfig.is_safe_path("") is False
    assert TemplateConfig.is_safe_path(None) is False
    assert TemplateConfig.is_safe_path(123) is False


def test_load_sanitizes_paths(tmp_path):
    config_file = tmp_path / "config.yaml"
    data = {
        "name": "Test",
        "docx_template": "../malicious.docx",
        "required_files": ["safe.md", "/etc/passwd", "dir/safe2.md"],
        "chapter_order": ["safe.md", "C:\\Windows", "../out.md"],
    }
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    config = TemplateConfig.load(config_file)
    assert config.docx_template == "template.docx"
    assert config.required_files == ["safe.md", "dir/safe2.md"]
    assert config.chapter_order == ["safe.md"]


def test_load_handles_nulls(tmp_path):
    config_file = tmp_path / "config.yaml"
    data = {
        "name": None,
        "description": None,
        "type": None,
        "docx_template": None,
        "required_files": None,
        "settings": None,
        "chapter_order": None,
    }
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    config = TemplateConfig.load(config_file)
    assert config.name == "Unknown Template"
    assert config.description == ""
    assert config.type == "report"
    assert config.docx_template == "template.docx"
    assert config.required_files == []
    assert config.settings == {}
    assert config.chapter_order == []
