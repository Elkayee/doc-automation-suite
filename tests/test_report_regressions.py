from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.core.assembler import DocumentAssembler
from src.core.config import TemplateConfig
from src.core.docx_helpers import DocxHelpers
from src.core.media_downloader import MediaDownloader
from src.core.template_manager import TemplateManager


def test_missing_required_chapter_cannot_be_silently_omitted(tmp_path):
    (tmp_path / 'chapters').mkdir()
    TemplateConfig(required_files=['Ch01.md', 'Ch02.md']).save(tmp_path / 'config.yaml')
    (tmp_path / 'chapters' / 'Ch01.md').write_text('# Present\n', encoding='utf-8')
    with pytest.raises(FileNotFoundError, match='Ch02.md'):
        DocumentAssembler(tmp_path).assemble_markdown()


@pytest.mark.parametrize('kind', ['plantuml', 'latex'])
def test_cache_changes_with_content_and_reuses_identical_content(tmp_path, kind):
    render = MediaDownloader.render_plantuml if kind == 'plantuml' else MediaDownloader.render_latex
    first = Mock(status_code=200, headers={'content-type': 'image/png'}, content=b'first')
    second = Mock(status_code=200, headers={'content-type': 'image/png'}, content=b'second')
    with patch('src.core.media_downloader.requests.get', side_effect=[first, second]) as fetch, patch(
        'src.core.media_downloader.time.sleep'
    ):
        first_path = render('source one', 1, tmp_path)
        second_path = render('source two', 1, tmp_path)
        cached_path = render('source two', 99, tmp_path)
    assert fetch.call_count == 2
    assert Path(first_path).read_bytes() == b'first'
    assert Path(second_path).read_bytes() == b'second'
    assert cached_path == second_path


def test_legacy_paragraph_settings_are_effective_and_new_keys_take_precedence():
    cfg = TemplateConfig(settings={'line_spacing': 2.0, 'first_line_indent': 2.5})
    effective = DocxHelpers.get_paragraph_settings(cfg)
    assert effective['line_spacing_value'] == 2.0
    assert effective['special_indent_by_cm'] == 2.5
    cfg = TemplateConfig(settings={'line_spacing': 2.0, 'line_spacing_value': 1.2})
    assert DocxHelpers.get_paragraph_settings(cfg)['line_spacing_value'] == 1.2


def test_default_report_has_real_toc_scaffold_and_docx_template(tmp_path):
    templates = Path(__file__).resolve().parents[1] / 'templates'
    TemplateManager(templates).create_project('tieu_luan_nd30', tmp_path)
    assert (tmp_path / 'template.docx').is_file()
    assert '[[TOC]]' in (tmp_path / 'chapters' / 'F01_toc.md').read_text(encoding='utf-8')
