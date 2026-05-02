import os
from pathlib import Path
from docx import Document

class DocxBuilder:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.config = self._get_config()
        self.doc = self._init_document()

    def _get_config(self):
        from src.core.config import TemplateConfig
        config_path = self.workspace_dir / 'config.yaml'
        if config_path.exists():
            return TemplateConfig.load(config_path)
        return None

    def _init_document(self):
        """Loads template.docx if it exists, otherwise creates a blank Document."""
        if self.config and self.config.docx_template:
            template_path = self.workspace_dir / self.config.docx_template
            if template_path.exists():
                return Document(str(template_path))
        return Document()

    def build_from_markdown(self, md_content: str, img_cache_dir: Path):
        """
        Applies markdown parsing and writes to self.doc.
        (This will integrate the parse_and_write logic from make.py)
        """
        # For now, we stub this out to be integrated in the next pass.
        # It should read md_content line by line and add to self.doc
        p = self.doc.add_paragraph("DOCX generation triggered. (Parser logic will be migrated here)")

    def save(self, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.doc.save(str(output_path))
        except PermissionError as exc:
            raise RuntimeError(
                f"Khong the ghi file {output_path.name}. Hay dong file Word cu truoc khi build lai."
            ) from exc
