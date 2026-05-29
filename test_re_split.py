import re
import time

def old_method(text):
    return text.replace('\r\n', '\n').replace('\r', '\n').split('\n')

def re_method(text):
    return re.split(r'\r\n|\r|\n', text)

text = "line1\r\nline2\rline3\nline4" * 100000

start = time.time()
old_method(text)
print("old:", time.time() - start)

start = time.time()
re_method(text)
print("re:", time.time() - start)
