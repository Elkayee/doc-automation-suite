import re
import time

def old_method(text):
    text = re.sub(r'([,;:])\s*\.(?=(?:\s|$|[*_`)\]}>"\']))', '.', text)
    text = re.sub(r'\s+([.,;:!?)])', r'\1', text)
    text = re.sub(r'([([{])\s+', r'\1', text)
    text = re.sub(r'\s+([)\]}])', r'\1', text)
    text = re.sub(r'([.,;:!?])([^\s\d.,;:!?)\]}\'"\\`*_])', r'\1 \2', text)
    return text

R1 = re.compile(r'([,;:])\s*\.(?=(?:\s|$|[*_`)\]}>"\']))')
R2 = re.compile(r'\s+([.,;:!?)])')
R3 = re.compile(r'([([{])\s+')
R4 = re.compile(r'\s+([)\]}])')
R5 = re.compile(r'([.,;:!?])([^\s\d.,;:!?)\]}\'"\\`*_])')

def new_method(text):
    text = R1.sub('.', text)
    text = R2.sub(r'\1', text)
    text = R3.sub(r'\1', text)
    text = R4.sub(r'\1', text)
    text = R5.sub(r'\1 \2', text)
    return text

text = "This is a test , . with ( spaces ) and ! punctuation." * 1000

start = time.time()
old_method(text)
print("old:", time.time() - start)

start = time.time()
new_method(text)
print("new:", time.time() - start)
