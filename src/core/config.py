from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, Field, field_validator


class TemplateConfig(BaseModel):
    name: str = "Unknown Template"
    description: str = ""
    type: str = "report"
    required_files: list[str] = Field(default_factory=list)
    docx_template: str = "template.docx"
    settings: dict[str, Any] = Field(default_factory=dict)
    chapter_order: list[str] = Field(default_factory=list)

    @field_validator('required_files')
    @classmethod
    def validate_required_files(cls, files: list[str]) -> list[str]:
        for f in files:
            p = Path(f)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError(f"Invalid path in required_files: {f}")
        return files

    @field_validator('docx_template')
    @classmethod
    def validate_docx_template(cls, docx_template: str) -> str:
        p = Path(docx_template)
        if p.is_absolute() or '..' in p.parts:
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
            
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

