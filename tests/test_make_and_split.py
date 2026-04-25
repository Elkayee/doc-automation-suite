import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import make


class MakeAndSplitTests(unittest.TestCase):
    def test_step_assemble_merges_chapters_and_skips_ch08_ch09(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chapters_dir = root / "chapters"
            output_path = root / "report.md"
            chapters_dir.mkdir()

            (chapters_dir / "Ch00_Header.md").write_text("Header", encoding="utf-8")
            (chapters_dir / "Ch01_Intro.md").write_text("Intro", encoding="utf-8")
            (chapters_dir / "Ch08_Ignore.md").write_text("Ignore 8", encoding="utf-8")
            (chapters_dir / "Ch09_Ignore.md").write_text("Ignore 9", encoding="utf-8")

            with mock.patch.object(make, "CH_DIR", str(chapters_dir)), mock.patch.object(
                make, "MD_OUT", str(output_path)
            ):
                make.step_assemble()

            content = output_path.read_text(encoding="utf-8")
            self.assertEqual(content, "Header\n\nIntro")
            self.assertNotIn("Ignore 8", content)
            self.assertNotIn("Ignore 9", content)

    def test_split_script_creates_numbered_chapter_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_path = root / "Bao_Cao_Tieu_Luan_NMCNPM.md"
            source_path.write_text(
                "# Report\n\nIntro block\n\n## Chapter One\nA\n\n## Chapter: Two\nB\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                ["python", str(Path.cwd() / "split_chapters.py")],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            chapter_files = sorted((root / "chapters").glob("*.md"))
            self.assertEqual(
                [path.name for path in chapter_files],
                ["Ch00_header.md", "Ch01_Chapter_One.md", "Ch02_Chapter_Two.md"],
            )
            self.assertIn("Da tao 3 file chapter", completed.stdout)


if __name__ == "__main__":
    unittest.main()
