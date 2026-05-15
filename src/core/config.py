from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TemplateConfig:
    name: str
    description: str
    type: str  # e.g., "report", "exam"
    required_files: list[str]
    docx_template: str
    settings: dict[str, Any] = field(default_factory=dict)
    chapter_order: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, config_path: Path) -> 'TemplateConfig':
        if not config_path.exists():
            raise FileNotFoundError(f'Config file not found: {config_path}')

        with open(config_path, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(f'Invalid configuration format in {config_path}. Expected a dictionary.')

        def _check_path_traversal(val: Any) -> None:
            if isinstance(val, str) and '..' in val.replace('\\', '/').split('/'):
                raise ValueError(f'Path traversal detected in configuration: {val}')
            elif isinstance(val, list):
                for item in val:
                    _check_path_traversal(item)
            elif isinstance(val, dict):
                for v in val.values():
                    _check_path_traversal(v)

        _check_path_traversal(data.get('docx_template'))
        _check_path_traversal(data.get('required_files', []))
        _check_path_traversal(data.get('chapter_order', []))
        _check_path_traversal(data.get('settings', {}))

        return cls(
            name=data.get('name', 'Unknown Template'),
            description=data.get('description', ''),
            type=data.get('type', 'report'),
            required_files=data.get('required_files', []),
            docx_template=data.get('docx_template', 'template.docx'),
            settings=data.get('settings', {}),
            chapter_order=data.get('chapter_order', []) or [],
        )

    def save(self, config_path: Path) -> None:
        data = {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'docx_template': self.docx_template,
            'required_files': self.required_files,
            'settings': self.settings,
        }
        if self.chapter_order:
            data['chapter_order'] = self.chapter_order

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
