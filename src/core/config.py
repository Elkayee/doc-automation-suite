from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

from src.core.file_io import atomic_write


class TemplateConfig(BaseModel):
    name: str = "Unknown Template"
    description: str = ""
    type: str = "report"
    required_files: list[str] = Field(default_factory=list)
    docx_template: str = "template.docx"
    settings: dict[str, Any] = Field(default_factory=dict)
    chapter_order: list[str] = Field(default_factory=list)
    metadata: dict[str, str | None] = Field(default_factory=dict)
    metadata_fields: dict[str, str] = Field(default_factory=dict)
    required_metadata: list[str] = Field(default_factory=list)
    chapter_outline: list[str] = Field(default_factory=list)
    bibliography: str | None = None
    csl: str | None = None

    @model_validator(mode='before')
    @classmethod
    def normalize_legacy_settings(cls, data):
        if isinstance(data, dict):
            data = dict(data)
            settings = dict(data.get('settings') or {})
            for old, new in [('line_spacing', 'line_spacing_value'), ('first_line_indent', 'special_indent_by_cm')]:
                if old in settings:
                    settings.setdefault(new, settings.pop(old))
            data['settings'] = settings
        return data

    @field_validator('required_files', 'chapter_order')
    @classmethod
    def validate_required_files(cls, files: list[str]) -> list[str]:
        for f in files:
            p = PurePosixPath(f.replace('\\', '/'))
            if not f.strip() or p.is_absolute() or PureWindowsPath(f).drive or '..' in p.parts:
                raise ValueError(f"Invalid path in required_files: {f}")
        return files

    @field_validator('docx_template', 'bibliography', 'csl')
    @classmethod
    def validate_docx_template(cls, docx_template: str | None) -> str | None:
        if docx_template is None:
            return None
        p = PurePosixPath(docx_template.replace('\\', '/'))
        if not docx_template.strip() or p.is_absolute() or PureWindowsPath(docx_template).drive or '..' in p.parts:
            raise ValueError(f"Invalid path in docx_template: {docx_template}")
        return docx_template

    @classmethod
    def load(cls, config_path: Path) -> 'TemplateConfig':
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        if not isinstance(data, dict):
            raise ValueError(f"Invalid configuration format in {config_path}. Expected a dictionary.")

        return cls.model_validate(data)

    def save(self, config_path: Path) -> None:
        data = self.model_dump(exclude_none=True)
        # Filter empty fields to keep yaml output clean
        if 'chapter_order' in data and not data['chapter_order']:
            data.pop('chapter_order')

        atomic_write(config_path, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

