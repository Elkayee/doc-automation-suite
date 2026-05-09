import shutil
import unittest
from pathlib import Path

from src.core.image_assets import ProjectImageAssetService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ImageAssetServiceTests(unittest.TestCase):
    def test_import_image_copies_into_project_assets_directory(self):
        workspace = PROJECT_ROOT / 'tests' / '_tmp_image_asset_import'
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
        workspace.mkdir(parents=True, exist_ok=True)
        try:
            imported = ProjectImageAssetService.import_image(workspace, PROJECT_ROOT / 'test_extracted.png')

            self.assertTrue(imported.absolute_path.exists())
            self.assertEqual(imported.relative_path, 'assets/images/test_extracted.png')
            self.assertEqual(imported.alt_text, 'test extracted')
        finally:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)

    def test_list_images_returns_only_supported_image_assets(self):
        workspace = PROJECT_ROOT / 'tests' / '_tmp_image_asset_list'
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
        image_dir = workspace / 'assets' / 'images'
        image_dir.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(PROJECT_ROOT / 'test_extracted.png', image_dir / 'a.png')
            (image_dir / 'notes.txt').write_text('ignore me', encoding='utf-8')

            assets = ProjectImageAssetService.list_images(workspace)

            self.assertEqual(len(assets), 1)
            self.assertEqual(assets[0].relative_path, 'assets/images/a.png')
        finally:
            if workspace.exists():
                shutil.rmtree(workspace, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
