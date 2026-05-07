from src.core.config import TemplateConfig
from pathlib import Path
import yaml
import tempfile

def test_path_traversal_sanitization():
    with tempfile.TemporaryDirectory() as d:
        config_path = Path(d) / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump({
                "name": "Test",
                "required_files": ["good.md", "../evil.md", "bad/file.md", "worse\\file.md"],
                "chapter_order": ["../../etc/passwd", "normal.md"]
            }, f)

        config = TemplateConfig.load(config_path)
        assert "good.md" in config.required_files
        assert "../evil.md" not in config.required_files
        assert "bad/file.md" not in config.required_files
        assert "worse\\file.md" not in config.required_files
        assert "normal.md" in config.chapter_order
        assert "../../etc/passwd" not in config.chapter_order

if __name__ == "__main__":
    test_path_traversal_sanitization()
