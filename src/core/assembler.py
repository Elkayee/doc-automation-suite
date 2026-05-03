from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class ChapterAssemblyEntry:
    filename: str
    path: Path
    content: str
    start_line: int
    end_line: int


class DocumentAssembler:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = Path(workspace_dir)
        self.config_path = self.workspace_dir / 'config.yaml'
        self.chapters_dir = self.workspace_dir / 'chapters'

    def get_config(self):
        from src.core.config import TemplateConfig

        if self.config_path.exists():
            return TemplateConfig.load(self.config_path)
        return None

    def _ensure_workspace(self):
        config = self.get_config()
        if not config:
            raise FileNotFoundError('Workspace is missing config.yaml')
        if not self.chapters_dir.exists():
            raise FileNotFoundError(f'Chapters directory missing in {self.workspace_dir}')
        return config

    def get_chapter_filenames(self) -> List[str]:
        config = self._ensure_workspace()
        ordered = []
        seen = set()

        for filename in config.chapter_order or []:
            if filename in seen:
                continue
            if (self.chapters_dir / filename).exists():
                ordered.append(filename)
                seen.add(filename)

        for filename in config.required_files:
            if filename in seen:
                continue
            if (self.chapters_dir / filename).exists():
                ordered.append(filename)
                seen.add(filename)

        extras = sorted(
            path.name
            for path in self.chapters_dir.glob('*.md')
            if path.name not in seen
        )
        ordered.extend(extras)
        return ordered

    def get_chapter_paths(self) -> List[Path]:
        return [self.chapters_dir / filename for filename in self.get_chapter_filenames()]

    def save_chapter_order(self, chapter_filenames: List[str]) -> None:
        config = self._ensure_workspace()
        config.chapter_order = chapter_filenames
        config.save(self.config_path)

    def assemble_with_metadata(self) -> Tuple[str, List[ChapterAssemblyEntry]]:
        self._ensure_workspace()

        parts: List[str] = []
        entries: List[ChapterAssemblyEntry] = []
        current_line = 1

        for filename in self.get_chapter_filenames():
            file_path = self.chapters_dir / filename
            content = file_path.read_text(encoding='utf-8').strip()
            if not content:
                continue

            line_count = len(content.splitlines())
            start_line = current_line
            end_line = start_line + line_count - 1
            entries.append(
                ChapterAssemblyEntry(
                    filename=filename,
                    path=file_path,
                    content=content,
                    start_line=start_line,
                    end_line=end_line,
                )
            )
            parts.append(content)
            current_line = end_line + 3

        final_md = '\n\n'.join(parts)
        return final_md, entries

    def assemble_markdown(self) -> Tuple[str, List[str]]:
        final_md, entries = self.assemble_with_metadata()
        return final_md, [str(entry.path) for entry in entries]

    def assemble_markdown_for_export(self) -> Tuple[str, List[str]]:
        _final_md, entries = self.assemble_with_metadata()
        parts: List[str] = []
        for entry in entries:
            parts.append(f'<!-- FILE: {entry.filename} -->')
            parts.append(entry.content)
        final_md = '\n\n'.join(parts)
        return final_md, [str(entry.path) for entry in entries]

    def save_assembled(self, output_path: Path) -> Tuple[str, List[str]]:
        final_md, processed_files = self.assemble_markdown()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_md)
        return final_md, processed_files

    def save_assembled_for_export(self, output_path: Path) -> Tuple[str, List[str]]:
        final_md, processed_files = self.assemble_markdown_for_export()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_md)
        return final_md, processed_files
