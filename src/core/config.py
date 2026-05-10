from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def is_safe_path(p: Any) -> bool:
    """Checks if a path is safe to use (no path traversal or absolute paths)."""
    if not isinstance(p, str) or not p:
        return False
    if '..' in p:
        return False
    if p.startswith('/') or p.startswith('\\'):
        return False
    if len(p) >= 2 and p[1] == ':' and p[0].isalpha():
        return False
    return True


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
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(f"Invalid configuration format in {config_path}. Expected a dictionary.")

        raw_required_files = data.get('required_files') or []
        required_files = [f for f in raw_required_files if is_safe_path(f)]

        raw_chapter_order = data.get('chapter_order') or []
        chapter_order = [f for f in raw_chapter_order if is_safe_path(f)]

        docx_template = data.get('docx_template') or 'template.docx'
        if not is_safe_path(docx_template):
            docx_template = 'template.docx'

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
