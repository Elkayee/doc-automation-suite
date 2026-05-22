import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def _check_path_string(val: str) -> None:
    if not isinstance(val, str):
        return
    if os.path.isabs(val) or val.startswith('/') or val.startswith('\\'):
        raise ValueError(f'Absolute paths are not allowed: {val}')
    if len(val) >= 2 and val[1] == ':' and val[0].isalpha():
        raise ValueError(f'Absolute paths are not allowed: {val}')
    parts = val.replace('\\', '/').split('/')
    if '..' in parts:
        raise ValueError(f"Parent directory references ('..') are not allowed: {val}")


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

        for item in data.get('required_files', []):
            _check_path_string(item)
        for item in data.get('chapter_order', []):
            _check_path_string(item)
        if 'docx_template' in data:
            _check_path_string(data['docx_template'])

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
