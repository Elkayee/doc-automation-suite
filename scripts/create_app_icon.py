"""Render the app's simple document mark at native Windows icon sizes."""

from pathlib import Path

from PIL import Image, ImageDraw


def main():
    assets = Path(__file__).resolve().parents[1] / 'assets'
    assets.mkdir(exist_ok=True)
    image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 248, 248), radius=48, fill='#172b4d')
    draw.polygon([(65, 43), (153, 43), (194, 84), (194, 214), (65, 214)], fill='white')
    draw.polygon([(153, 43), (153, 84), (194, 84)], fill='#a7c2ff')
    for top, end in [(111, 170), (139, 170), (167, 146)]:
        draw.rounded_rectangle((89, top, end, top + 10), radius=5, fill='#2457d6')
    image.save(assets / 'app.png')
    image.save(assets / 'app.ico', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == '__main__':
    main()
