import yaml

from src.core.config import TemplateConfig, is_safe_path


def test_is_safe_path():
    assert is_safe_path('valid.md') is True
    assert is_safe_path('sub/valid.md') is True

    assert is_safe_path('../../etc/passwd') is False
    assert is_safe_path('/etc/passwd') is False
    assert is_safe_path('\\Windows\\System32') is False
    assert is_safe_path('C:\\Windows') is False
    assert is_safe_path('d:/secret') is False
    assert is_safe_path('') is False
    assert is_safe_path(None) is False
    assert is_safe_path(123) is False


def test_template_config_load_sanitizes_paths(tmp_path):
    config_path = tmp_path / 'config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(
            {
                'name': 'Test Template',
                'required_files': ['safe1.md', '../unsafe.md', '/absolute.md'],
                'chapter_order': ['C:\\win.md', 'safe2.md', '../../etc/shadow'],
                'docx_template': '../../malicious.docx',
            },
            f,
        )

    config = TemplateConfig.load(config_path)

    assert config.required_files == ['safe1.md']
    assert config.chapter_order == ['safe2.md']
    assert config.docx_template == 'template.docx'


def test_template_config_load_handles_nulls(tmp_path):
    config_path = tmp_path / 'config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(
            {
                'name': None,
                'description': None,
                'type': None,
                'required_files': None,
                'chapter_order': None,
                'docx_template': None,
            },
            f,
        )

    config = TemplateConfig.load(config_path)

    assert config.name == 'Unknown Template'
    assert config.description == ''
    assert config.type == 'report'
    assert config.required_files == []
    assert config.chapter_order == []
    assert config.docx_template == 'template.docx'
