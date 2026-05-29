import re
import time

def old_method(text):
    return re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)

HTML_BREAK_RE = re.compile(r'<br\s*/?>', flags=re.IGNORECASE)
def new_method(text):
    return HTML_BREAK_RE.sub(' ', text)

text = "Some text with <br> and <br/> and <BR > tags. " * 10000

start = time.time()
old_method(text)
print("old:", time.time() - start)

start = time.time()
new_method(text)
print("new:", time.time() - start)
