import re, json

with open('prose.txt','r',encoding='utf-8') as f:
    text = f.read()

# Extract numbered node definitions 1-73 from the detailed section
nodes = {}
# pattern: N. name — description...
# We use the first occurrence of each numbered node in the detailed section
for m in re.finditer(r'^(\d{1,2})\.\s+([\w_]+)\s+—', text, re.MULTILINE):
    num, name = int(m.group(1)), m.group(2)
    if num not in nodes:
        nodes[num] = {'name': name, 'source': 'detail'}

# Add nodes from the mapping table 71-84
# The mapping table has rows like | 71 | left_amygdala | ...
table_rows = re.findall(r'\|\s*(\d+)\s*\|\s*([\w_]+)\s*\|', text)
for num, name in table_rows:
    n = int(num)
    if n not in nodes:
        nodes[n] = {'name': name, 'source': 'table'}

print('Total unique numbered nodes:', len(nodes))
for k in sorted(nodes):
    print(k, nodes[k]['name'])
