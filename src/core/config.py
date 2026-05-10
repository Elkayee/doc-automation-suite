from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def is_safe_path(path: str) -> bool:
    """Validate path to prevent directory traversal."""
    if not path:
        return False
    # Prevent directory traversal
    if '..' in path:
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

        # Sanitize required_files against path traversal
        raw_required_files = data.get('required_files', [])
        safe_required_files = [p for p in raw_required_files if is_safe_path(str(p))]

        # Sanitize docx_template against path traversal
        raw_docx_template = data.get('docx_template', 'template.docx')
        safe_docx_template = raw_docx_template if is_safe_path(str(raw_docx_template)) else 'template.docx'

        return cls(
            name=data.get('name', 'Unknown Template'),
            description=data.get('description', ''),
            type=data.get('type', 'report'),
            required_files=safe_required_files,
            docx_template=safe_docx_template,
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
