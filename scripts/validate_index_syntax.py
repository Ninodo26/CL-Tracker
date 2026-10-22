import os
import re
import subprocess
import sys

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Extract JavaScript inside <script> tags (except template tag)
script_blocks = re.findall(r'<script(?![^>]*type=["\']text/template["\'])[^>]*>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(script_blocks)} script blocks.")

for i, block in enumerate(script_blocks):
    filename = f"scripts/temp_test_block_{i}.js"
    with open(filename, "w", encoding="utf-8") as tf:
        tf.write(block)
    
    # Run node --check
    res = subprocess.run(["node", "--check", filename], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR in script block {i}:")
        print(res.stderr)
        sys.exit(1)
    else:
        print(f"Script block {i}: SYNTAX OK!")
    
    try:
        os.remove(filename)
    except:
        pass

print("ALL SCRIPT BLOCKS PASSED SYNTAX CHECK!")
