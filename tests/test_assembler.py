import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import yaml

from src.core.assembler import DocumentAssembler

class DocumentAssemblerTests(unittest.TestCase):
    def test_prevents_path_traversal_in_config(self):
        with TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            chapters = workspace / 'chapters'
            chapters.mkdir()

            # Create a secret file outside chapters
            secret_file = workspace / 'secret.txt'
            secret_file.write_text("SUPER SECRET")

            # Create malicious config
            config_data = {
                'name': 'Malicious',
                'description': 'Test',
                'type': 'report',
                'chapter_order': ['../../secret.txt'],
                'required_files': ['../secret.txt']
            }
            with open(workspace / 'config.yaml', 'w') as f:
                yaml.dump(config_data, f)

            assembler = DocumentAssembler(workspace)
            filenames = assembler.get_chapter_filenames()

            # The malicious paths should be skipped
            self.assertNotIn('../../secret.txt', filenames)
            self.assertNotIn('../secret.txt', filenames)

if __name__ == '__main__':
    unittest.main()
