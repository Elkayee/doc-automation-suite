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

        docx_template = data.get('docx_template', 'template.docx')
        if '..' in Path(docx_template).parts:
            raise ValueError('Path traversal detected in docx_template.')

        required_files = data.get('required_files', [])
        for req_file in required_files:
            if '..' in Path(req_file).parts:
                raise ValueError(f'Path traversal detected in required_files: {req_file}')

        chapter_order = data.get('chapter_order', []) or []
        for chapter in chapter_order:
            if '..' in Path(chapter).parts:
                raise ValueError(f'Path traversal detected in chapter_order: {chapter}')

        return cls(
            name=data.get('name', 'Unknown Template'),
            description=data.get('description', ''),
            type=data.get('type', 'report'),
            required_files=required_files,
            docx_template=docx_template,
            settings=data.get('settings', {}),
            chapter_order=chapter_order,
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
