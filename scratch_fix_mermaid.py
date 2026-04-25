import re

def fix(filepath):
    txt = open(filepath, encoding='utf-8').read()
    # Remove quotes inside | |
    txt = re.sub(r'-->\|"([^"]+)"\|', r'-->|\1|', txt)
    open(filepath, 'w', encoding='utf-8').write(txt)

fix(r'chapters\Ch05_CHƯƠNG_3_NGHIÊN_CỨU_CHUYÊN_SÂU_—_UC06_.md')
fix('fix_ascii.py')
