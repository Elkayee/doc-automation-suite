import re
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImportedImageAsset:
    absolute_path: Path
    relative_path: str
    alt_text: str


class ProjectImageAssetService:
    IMAGE_DIR = Path('assets') / 'images'

    @staticmethod
    def image_dir(project_path: Path) -> Path:
        return Path(project_path) / ProjectImageAssetService.IMAGE_DIR

    @staticmethod
    def default_alt_text(source_path: Path) -> str:
        words = re.sub(r'[_\-]+', ' ', source_path.stem).strip()
        return words or 'Image'

    @classmethod
    def list_images(cls, project_path: Path) -> list[ImportedImageAsset]:
        target_dir = cls.image_dir(project_path)
        if not target_dir.exists():
            return []

        assets = []
        for path in sorted(target_dir.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}:
                continue
            assets.append(
                ImportedImageAsset(
                    absolute_path=path,
                    relative_path=path.relative_to(project_path).as_posix(),
                    alt_text=cls.default_alt_text(path),
                )
            )
        return assets

    @staticmethod
    def _unique_target_path(target_dir: Path, filename: str) -> Path:
        candidate = target_dir / filename
        if not candidate.exists():
            return candidate

        stem = candidate.stem
        suffix = candidate.suffix
        index = 2
        while True:
            numbered = target_dir / f'{stem}-{index}{suffix}'
            if not numbered.exists():
                return numbered
            index += 1

    @classmethod
    def import_image(cls, project_path: Path, source_path: Path) -> ImportedImageAsset:
        target_dir = cls.image_dir(project_path)
        target_dir.mkdir(parents=True, exist_ok=True)

        source = Path(source_path)
        target = cls._unique_target_path(target_dir, source.name)
        shutil.copy2(source, target)
        return ImportedImageAsset(
            absolute_path=target,
            relative_path=target.relative_to(project_path).as_posix(),
            alt_text=cls.default_alt_text(source),
        )
