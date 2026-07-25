import json

with open('main.ipynb', 'r', encoding='utf-8') as f:
    d = json.load(f)

src = d['cells'][0]['source']

# Replace the first line 'import nbimporter' with importnb logic
if src[0].startswith('import nbimporter'):
    src[0] = 'import importnb\n'
    src.insert(1, 'with importnb.Notebook():\n')
    
    last_import_idx = 1
    for i in range(2, len(src)):
        if src[i].startswith('from ') or src[i].startswith('import '):
            if 'os' in src[i] or 'glob' in src[i]:
                # Don't indent standard imports if we don't want to, but it's fine.
                pass
            src[i] = '    ' + src[i]
            last_import_idx = i
            
    # Add a newline after the block if needed
    src.insert(last_import_idx + 1, '\n')

with open('main.ipynb', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=1)
print("Updated main.ipynb successfully.")
