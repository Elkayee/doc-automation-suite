import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def validate_no_path_traversal(value, field_name=''):
    if isinstance(value, str):
        is_abs = (
            os.path.isabs(value)
            or value.startswith('/')
            or value.startswith('\\')
            or (len(value) >= 2 and value[1] == ':' and value[0].isalpha())
        )
        has_dotdot = '..' in value.replace('\\', '/').split('/')
        if is_abs or has_dotdot:
            raise ValueError(f"Path traversal detected in field '{field_name}': {value}")
    elif isinstance(value, dict):
        for k, v in value.items():
            validate_no_path_traversal(v, f'{field_name}.{k}' if field_name else str(k))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            validate_no_path_traversal(item, f'{field_name}[{i}]')


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

        validate_no_path_traversal(data)

        if not isinstance(data, dict):
            raise ValueError(f'Invalid configuration format in {config_path}. Expected a dictionary.')

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
