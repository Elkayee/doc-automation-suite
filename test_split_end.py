text = "a\r\nb\nc\n"

print("old:", text.replace('\r\n', '\n').replace('\r', '\n').split('\n'))

def new_method(text):
    lines = text.splitlines(keepends=False)
    if text.endswith('\n') or text.endswith('\r'):
        lines.append('')
    return lines

print("new:", new_method(text))

print("unicode:", "\x0b\x0c\u2028".splitlines(keepends=False))
