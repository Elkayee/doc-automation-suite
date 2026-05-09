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

    @staticmethod
    def is_safe_path(path_str: str) -> bool:
        if not path_str or not isinstance(path_str, str):
            return False
        # Block absolute paths
        if path_str.startswith('/') or path_str.startswith('\\') or (len(path_str) > 1 and path_str[1] == ':'):
            return False
        # Block directory traversal
        if '..' in path_str:
            return False
        return True

    @classmethod
    def load(cls, config_path: Path) -> 'TemplateConfig':
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(f"Invalid configuration format in {config_path}. Expected a dictionary.")

        # Sanitize scalar values
        docx_template = data.get('docx_template') or 'template.docx'
        if not cls.is_safe_path(docx_template):
            docx_template = 'template.docx'

        # Sanitize lists
        raw_required_files = data.get('required_files') or []
        required_files = [f for f in raw_required_files if cls.is_safe_path(f)]

        raw_chapter_order = data.get('chapter_order') or []
        chapter_order = [f for f in raw_chapter_order if cls.is_safe_path(f)]

        return cls(
            name=data.get('name') or 'Unknown Template',
            description=data.get('description') or '',
            type=data.get('type') or 'report',
            required_files=required_files,
            docx_template=docx_template,
            settings=data.get('settings') or {},
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
