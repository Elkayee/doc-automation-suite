from pathlib import Path
import pytest
from pydantic import ValidationError
from click.testing import CliRunner
from fastapi.testclient import TestClient

from src.core.config import TemplateConfig
from src.cli import cli
from src.api import app


def test_template_config_pydantic_validation():
    # Valid config should succeed
    cfg = TemplateConfig(
        name="Test",
        description="Desc",
        type="report",
        required_files=["chap1.md", "chap2.md"],
        docx_template="template.docx"
    )
    assert cfg.name == "Test"

    # Absolute paths should fail validation
    with pytest.raises(ValidationError):
        TemplateConfig(docx_template=str(Path("/absolute/path/template.docx").absolute()))

    # Directory traversal paths should fail validation
    with pytest.raises(ValidationError):
        TemplateConfig(required_files=["../traversal.md"])


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "compile" in result.output
    assert "list-templates" in result.output
    assert "create" in result.output


def test_api_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Doc Automation Suite API"


def test_api_templates():
    client = TestClient(app)
    response = client.get("/templates")
    assert response.status_code == 200
    assert "templates" in response.json()
