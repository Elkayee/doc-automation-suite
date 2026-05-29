import re
import time

def old_method(text):
    return re.sub(r'\s+', ' ', text).strip()

R = re.compile(r'\s+')
def new_method(text):
    return R.sub(' ', text).strip()

text = "This   is    some \n  text \t  with   spaces." * 1000

start = time.time()
for _ in range(100):
    old_method(text)
print("old:", time.time() - start)

start = time.time()
for _ in range(100):
    new_method(text)
print("new:", time.time() - start)
