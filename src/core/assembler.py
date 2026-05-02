import os
from pathlib import Path
from typing import Tuple, List

class DocumentAssembler:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        
    def get_config(self):
        from src.core.config import TemplateConfig
        config_path = self.workspace_dir / 'config.yaml'
        if config_path.exists():
            return TemplateConfig.load(config_path)
        return None
        
    def assemble_markdown(self) -> Tuple[str, List[str]]:
        """Reads required files from workspace/chapters and joins them."""
        config = self.get_config()
        if not config:
            raise FileNotFoundError("Workspace is missing config.yaml")
            
        chapters_dir = self.workspace_dir / 'chapters'
        if not chapters_dir.exists():
            raise FileNotFoundError(f"Chapters directory missing in {self.workspace_dir}")
            
        parts = []
        processed_files = []
        
        for filename in config.required_files:
            file_path = chapters_dir / filename
            if file_path.exists():
                with open(file_path, encoding='utf-8') as f:
                    parts.append(f.read().strip())
                processed_files.append(str(file_path))
            else:
                print(f"  [WARN] Missing required file: {filename}")
                
        final_md = '\n\n'.join(parts)
        return final_md, processed_files
        
    def save_assembled(self, output_path: Path) -> Tuple[str, List[str]]:
        final_md, processed_files = self.assemble_markdown()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_md)
        return final_md, processed_files
