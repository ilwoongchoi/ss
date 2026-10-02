with open('_slot_clean.txt','r',encoding='utf-8-sig',errors='replace') as f:
    content = f.read()
content = content.replace('\ufeff','').replace('\x00','')
with open('_slot_final.md','w',encoding='utf-8') as f:
    f.write(content)
print(f'Done, {len(content)} chars')
