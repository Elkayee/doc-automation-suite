
import pytest
import yaml

from src.core.config import TemplateConfig


def test_config_path_traversal_blocked(tmp_path):
    config_data = {
        'name': 'Test Config',
        'description': 'A malicious config',
        'docx_template': '../../secret.docx',
        'required_files': ['normal.md'],
    }

    config_file = tmp_path / 'malicious.yaml'
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config_data, f)

    with pytest.raises(ValueError, match='Path traversal detected'):
        TemplateConfig.load(config_file)


def test_config_path_traversal_nested_blocked(tmp_path):
    config_data = {
        'name': 'Test Config',
        'description': 'A malicious config',
        'docx_template': 'normal.docx',
        'required_files': ['normal.md'],
        'settings': {'output_dir': 'nested/../../etc/passwd'},
    }

    config_file = tmp_path / 'malicious_nested.yaml'
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config_data, f)

    with pytest.raises(ValueError, match='Path traversal detected'):
        TemplateConfig.load(config_file)


def test_config_path_traversal_list_blocked(tmp_path):
    config_data = {
        'name': 'Test Config',
        'description': 'A malicious config',
        'docx_template': 'normal.docx',
        'required_files': ['normal.md', '../sensitive.md'],
        'settings': {},
    }

    config_file = tmp_path / 'malicious_list.yaml'
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config_data, f)

    with pytest.raises(ValueError, match='Path traversal detected'):
        TemplateConfig.load(config_file)


def test_config_path_traversal_safe(tmp_path):
    config_data = {
        'name': 'Test Config',
        'description': 'A safe config',
        'docx_template': 'normal.docx',
        'required_files': ['normal.md', 'nested/file.md'],
        'settings': {'output_dir': 'output'},
    }

    config_file = tmp_path / 'safe.yaml'
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config_data, f)

    config = TemplateConfig.load(config_file)
    assert config.name == 'Test Config'
    assert config.docx_template == 'normal.docx'
