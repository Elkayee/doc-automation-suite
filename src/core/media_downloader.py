import os
import struct
from pathlib import Path
import time
from urllib.parse import quote
import requests

class MediaDownloader:
    @staticmethod
    def get_png_dimensions(path):
        with open(path, 'rb') as f:
            f.read(16)
            w = struct.unpack('>I', f.read(4))[0]
            h = struct.unpack('>I', f.read(4))[0]
        return w, h

    @staticmethod
    def get_jpeg_dimensions(path):
        with open(path, 'rb') as f:
            if f.read(2) != b'\xff\xd8':
                raise ValueError('Not a JPEG file')

            while True:
                marker_prefix = f.read(1)
                if not marker_prefix:
                    break
                if marker_prefix != b'\xff':
                    continue

                marker = f.read(1)
                while marker == b'\xff':
                    marker = f.read(1)

                if not marker or marker in {
                    b'\xd8',
                    b'\xd9',
                    b'\x01',
                    b'\xd0',
                    b'\xd1',
                    b'\xd2',
                    b'\xd3',
                    b'\xd4',
                    b'\xd5',
                    b'\xd6',
                    b'\xd7',
                }:
                    continue

                segment_length = struct.unpack('>H', f.read(2))[0]
                if marker in {
                    b'\xc0',
                    b'\xc1',
                    b'\xc2',
                    b'\xc3',
                    b'\xc5',
                    b'\xc6',
                    b'\xc7',
                    b'\xc9',
                    b'\xca',
                    b'\xcb',
                    b'\xcd',
                    b'\xce',
                    b'\xcf',
                }:
                    f.read(1)  # precision
                    height = struct.unpack('>H', f.read(2))[0]
                    width = struct.unpack('>H', f.read(2))[0]
                    return width, height

                f.seek(segment_length - 2, os.SEEK_CUR)

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
        cache_file = os.path.join(img_cache, f'diagram_{idx:03d}.png')
        if os.path.exists(cache_file):
            print(f'  [cache] diagram_{idx:03d}.png')
            return cache_file
        try:
            print(f'  [render] Dang render diagram {idx}...')
            url = cls.plantuml_png_url(code)
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image'):
                with open(cache_file, 'wb') as f:
                    f.write(resp.content)
                print(f'  [OK] Luu vao {cache_file}')
                time.sleep(0.5)
                return cache_file
            print(f'  [WARN] API tra ve {resp.status_code}')
            return None
        except Exception as e:
            print(f'  [ERROR] {e}')
            return None

    @staticmethod
    def render_latex(latex_code, idx, img_cache):
        """Render công thức LaTeX → PNG qua CodeCogs API, cache lại kết quả."""
        cache_file = os.path.join(img_cache, f'math_{idx:03d}.png')
        if os.path.exists(cache_file):
            print(f'  [cache] math_{idx:03d}.png')
            return cache_file
        try:
            print(f'  [render] Dang render công thức toán {idx}...')
            encoded = quote(latex_code, safe='')
            url = f'https://latex.codecogs.com/png.image?\\dpi{{150}}{encoded}'
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image'):
                with open(cache_file, 'wb') as f:
                    f.write(resp.content)
                print(f'  [OK] math_{idx:03d}.png')
                return cache_file
            print(f'  [WARN] CodeCogs trả về {resp.status_code}')
            return None
        except Exception as e:
            print(f'  [ERROR] Render LaTeX: {e}')
            return None
