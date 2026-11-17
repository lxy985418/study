from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import json, re

root = Path(__file__).resolve().parent.parent
r = json.loads((root / '学习记录/学习记录.json').read_text(encoding='utf-8-sig'))
sessions = r['sessions']
assert len({s['id'] for s in sessions}) == len(sessions), 'Duplicate session IDs'
derived = [json.loads(line) for line in (root / '学习记录/逐题记录.jsonl').read_text(encoding='utf-8').splitlines() if line]
assert derived == sessions, 'Refresh derived exports after updating the canonical JSON'
pending = [(day, d['pendingQuestion']) for day,d in r['dailyStudyProgress'].items() if d.get('pendingQuestion',{} ) and d['pendingQuestion'].get('status') in ['awaiting_answer','awaiting_remaining_answer']]
if pending:
    day, q = max(pending, key=lambda x:x[0])
    assert r['resumeState']['questionId'] == q['id'], 'Resume state is stale'
    current = (root / '学习记录/当前进度.md').read_text(encoding='utf-8')
    assert q['id'] in current, 'Human current-progress page is stale'
counts = Counter(s['date'] for s in sessions)
for day,d in r['dailyStudyProgress'].items():
    assert d['answeredQuestions'] == counts[day], 'Daily count mismatch: ' + day
bad=[]; checked=0
for p in root.rglob('*.md'):
    if any(part in ['.git','.obsidian','归档历史'] for part in p.relative_to(root).parts): continue
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
        target=unquote(target.strip().strip('<>'))
        if re.match(r'https?://|mailto:',target) or target.startswith('#'):continue
        if re.match(r'file:|[A-Za-z]:[\\/]|/',target):bad.append((str(p),target));continue
        if not (p.parent/target.split('#')[0]).exists():bad.append((str(p),target))
        checked+=1
assert not bad, 'Broken or machine-specific Markdown links: ' + repr(bad)
print(json.dumps({'sessions':len(sessions),'counts':dict(counts),'localLinksChecked':checked,'pendingQuestion':r['resumeState']['questionId']},ensure_ascii=False))
