"""Build the editable DOCX style templates; never touches user workspaces."""

import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.config import TemplateConfig
from src.core.docx_helpers import DocxHelpers
from src.core.report_fields import configure_styles


def main():
    templates = Path(__file__).resolve().parents[1] / 'templates'
    for name in ['tieu_luan_nd30', 'bao_cao_bai_tap_lon', 'bao_cao_cong_so', 'bien_ban']:
        project = templates / name
        config = TemplateConfig.load(project / 'config.yaml')
        document = Document()
        configure_styles(document, config)
        DocxHelpers.apply_page_settings(document, DocxHelpers.get_page_settings(config))
        document.save(project / config.docx_template)
        print(name)


if __name__ == '__main__':
    main()
