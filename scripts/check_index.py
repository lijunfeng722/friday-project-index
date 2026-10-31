#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'repos.json').read_text())['repositories'];ids=[row['id'] for row in rows];assert len(ids)==len(set(ids))
for row in rows:
 assert row['url'].startswith('https://github.com/')
 assert (ROOT/'repos'/f"{row['id']}.md").is_file()
 assert row['url'] in (ROOT/'README.md').read_text()
count=0
for p in ROOT.rglob('*.md'):
 if '.artifacts' in p.parts:continue
 text=p.read_text();assert '/Users/' not in text and 'codex-clipboard-' not in text
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
  if link.startswith(('https://','http://','#')):continue
  assert (p.parent/link.split('#')[0]).is_file(),(p,link)
 assert text.count('```')%2==0
 count+=1
print(json.dumps({'repositories':len(rows),'markdown_files':count,'links':'PASS'},ensure_ascii=False))
