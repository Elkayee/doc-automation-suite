import os
import struct
import time
from pathlib import Path
from urllib.parse import quote

import requests

from src.core.logger import logger


class MediaDownloader:
    @staticmethod
    def get_png_dimensions(path):
        with open(path, 'rb') as handle:
            handle.read(16)
            width = struct.unpack('>I', handle.read(4))[0]
            height = struct.unpack('>I', handle.read(4))[0]
        return width, height

    @staticmethod
    def get_jpeg_dimensions(path):
        with open(path, 'rb') as handle:
            if handle.read(2) != b'\xff\xd8':
                raise ValueError('Not a JPEG file')

            while True:
                marker_prefix = handle.read(1)
                if not marker_prefix:
                    break
                if marker_prefix != b'\xff':
                    continue

                marker = handle.read(1)
                while marker == b'\xff':
                    marker = handle.read(1)

                if not marker or marker in {
                    b'\xd8', b'\xd9', b'\x01',
                    b'\xd0', b'\xd1', b'\xd2', b'\xd3',
                    b'\xd4', b'\xd5', b'\xd6', b'\xd7',
                }:
                    continue

                segment_length = struct.unpack('>H', handle.read(2))[0]
                if marker in {
                    b'\xc0', b'\xc1', b'\xc2', b'\xc3',
                    b'\xc5', b'\xc6', b'\xc7',
                    b'\xc9', b'\xca', b'\xcb',
                    b'\xcd', b'\xce', b'\xcf',
                }:
                    handle.read(1)
                    height = struct.unpack('>H', handle.read(2))[0]
                    width = struct.unpack('>H', handle.read(2))[0]
                    return width, height

                handle.seek(segment_length - 2, os.SEEK_CUR)

        raise ValueError('Could not determine JPEG dimensions')

    @classmethod
    def get_image_dimensions(cls, path):
        suffix = Path(path).suffix.lower()
        if suffix == '.png':
            return cls.get_png_dimensions(path)
        if suffix in {'.jpg', '.jpeg'}:
            return cls.get_jpeg_dimensions(path)
        return None, None

    @staticmethod
    def plantuml_hex_encode(text):
        return '~h' + text.encode('utf-8').hex()

    @classmethod
    def plantuml_png_url(cls, code):
        normalized = code.strip()
        if '@startuml' not in normalized:
            normalized = f'@startuml\n{normalized}\n@enduml'
        return f'https://www.plantuml.com/plantuml/png/{cls.plantuml_hex_encode(normalized)}'

    @classmethod
    def render_plantuml(cls, code, idx, img_cache):
        cache_dir = Path(img_cache)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f'diagram_{idx:03d}.png'
        if cache_file.exists():
            logger.info(f'Using cached PlantUML diagram_{idx:03d}.png')
            return str(cache_file)
        try:
            logger.info(f'Rendering PlantUML diagram {idx}...')
            url = cls.plantuml_png_url(code)
            response = requests.get(url, timeout=30)
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                cache_file.write_bytes(response.content)
                logger.info(f'Successfully rendered and saved diagram {idx} to {cache_file}')
                time.sleep(0.5)
                return str(cache_file)
            logger.warning(f'PlantUML API returned status {response.status_code} for diagram {idx}')
            return None
        except Exception as exc:
            logger.error(f'Error rendering PlantUML diagram {idx}: {exc}')
            return None

    @staticmethod
    def render_latex(latex_code, idx, img_cache):
        cache_dir = Path(img_cache)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f'math_{idx:03d}.png'
        if cache_file.exists():
            logger.info(f'Using cached LaTeX formula math_{idx:03d}.png')
            return str(cache_file)
        try:
            logger.info(f'Rendering LaTeX math formula {idx}...')
            encoded = quote(latex_code, safe='')
            url = f'https://latex.codecogs.com/png.image?\\dpi{{150}}{encoded}'
            response = requests.get(url, timeout=15)
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                cache_file.write_bytes(response.content)
                logger.info(f'Successfully rendered and saved LaTeX formula math_{idx:03d}.png')
                return str(cache_file)
            logger.warning(f'Codecogs LaTeX API returned status {response.status_code} for formula {idx}')
            return None
        except Exception as exc:
            logger.error(f'Error rendering LaTeX formula {idx}: {exc}')
            return None
