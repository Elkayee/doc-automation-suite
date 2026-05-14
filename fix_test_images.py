import sys
from pathlib import Path

# Create a 1x1 minimal valid PNG dummy file
DUMMY_PNG_CONTENT = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

test_extracted_path = Path('test_extracted.png')
if not test_extracted_path.exists():
    with open(test_extracted_path, 'wb') as f:
        f.write(DUMMY_PNG_CONTENT)
    print(f"Created {test_extracted_path}")
