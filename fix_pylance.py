import json

with open('main.ipynb', 'r', encoding='utf-8') as f:
    d = json.load(f)

source = d['cells'][0]['source']

for i in range(len(source)):
    if source[i].strip().startswith('from ') and 'import' in source[i]:
        # Avoid adding multiple type ignores if we run it again
        if '# type: ignore' not in source[i]:
            source[i] = source[i].rstrip('\n') + '  # type: ignore\n'

with open('main.ipynb', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=1)
