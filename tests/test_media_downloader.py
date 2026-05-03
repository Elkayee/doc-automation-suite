import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.media_downloader import MediaDownloader


class MediaDownloaderTests(unittest.TestCase):
    @patch('src.core.media_downloader.requests.get')
    def test_render_plantuml_creates_cache_directory_before_write(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/png'}
        mock_response.content = b'png-bytes'
        mock_get.return_value = mock_response

        cache_dir = Path('workspaces') / 'test_media_cache'
        output = MediaDownloader.render_plantuml('@startuml\nAlice -> Bob\n@enduml', 1, str(cache_dir))

        self.assertTrue(cache_dir.exists())
        self.assertTrue(Path(output).exists())


if __name__ == '__main__':
    unittest.main()
