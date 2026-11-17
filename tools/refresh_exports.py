from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
record = json.loads((root / '学习记录/学习记录.json').read_text(encoding='utf-8-sig'))
sessions = record['sessions']
if len({x['id'] for x in sessions}) != len(sessions):
    raise SystemExit('Duplicate question IDs; reconcile before exporting.')
(root / '学习记录/逐题记录.jsonl').write_text(''.join(json.dumps(s, ensure_ascii=False) + '\n' for s in sessions), encoding='utf-8')
for day in sorted({s['date'] for s in sessions}):
    rows = [s for s in sessions if s['date'] == day]
    lines = ['# ' + day + ' 逐题学习记录', '', '按实际作答日期归档，保留完整原答及分项评估。', '', '[当前进度](../当前进度.md)', '']
    for i, s in enumerate(rows, 1):
        lines += ['## 记录 ' + str(i), '', '记录ID：`' + s['id'] + '`。', '']
        if s.get('question'): lines += ['题目：' + str(s['question']), '']
        if 'userAnswer' in s: lines += ['原答：' + str(s['userAnswer']), '']
        if s.get('assessment'): lines += ['评价与订正：' + s['assessment'], '']
        lines += ['<details><summary>完整记录</summary>', '', '```json', json.dumps(s, ensure_ascii=False, indent=2), '```', '', '</details>', '']
    (root / ('学习记录/逐题记录/' + day + '.md')).write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Derived records refreshed. Also update current progress and daily subject summaries before sync.')
