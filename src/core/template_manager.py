import os
import shutil
from pathlib import Path
from typing import List, Dict
from src.core.config import TemplateConfig

class TemplateManager:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def list_templates(self) -> Dict[str, TemplateConfig]:
        """Returns a dict mapping template ID (folder name) to its config."""
        templates = {}
        for entry in self.templates_dir.iterdir():
            if entry.is_dir():
                config_path = entry / 'config.yaml'
                if config_path.exists():
                    try:
                        templates[entry.name] = TemplateConfig.load(config_path)
                    except Exception as e:
                        print(f"Error loading template {entry.name}: {e}")
        return templates

    def create_project(self, template_id: str, dest_dir: Path) -> bool:
        """Creates a new project in dest_dir based on the template_id."""
        template_path = self.templates_dir / template_id
        if not template_path.exists() or not (template_path / 'config.yaml').exists():
            raise ValueError(f"Invalid template ID: {template_id}")

        # Create destination directory
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 1. Create config copy
        config = TemplateConfig.load(template_path / 'config.yaml')
        shutil.copy(template_path / 'config.yaml', dest_dir / 'config.yaml')

        # 2. Copy docx template if it exists
        docx_src = template_path / config.docx_template
        if docx_src.exists():
            shutil.copy(docx_src, dest_dir / config.docx_template)

        # 3. Create chapters directory and copy boilerplate
        chapters_dir = dest_dir / 'chapters'
        chapters_dir.mkdir(exist_ok=True)

        boilerplate_dir = template_path / 'boilerplate'

        for filename in config.required_files:
            dest_file = chapters_dir / filename
            src_file = boilerplate_dir / filename if boilerplate_dir.exists() else None

            if src_file and src_file.exists():
                shutil.copy(src_file, dest_file)
            else:
                # Create empty file if no boilerplate exists
                title = filename.replace('.md', '').replace('_', ' ')
                dest_file.write_text(f"# {title}\n\n[Nhập nội dung vào đây]\n", encoding='utf-8')

        return True
