from pathlib import Path
from collections import Counter
import json
root=Path(__file__).resolve().parent.parent
r=json.loads((root/'学习记录/学习记录.json').read_text(encoding='utf-8-sig'))
resume=r['resumeState'];day=resume['asOf'];d=r['dailyStudyProgress'][day]
assert d['pendingQuestion']['id']==resume['questionId']
counts=Counter(s['lesson'] for s in r['sessions'] if s['date']==day)
out={'asOf':day,'authoritativeRecord':'学习记录/学习记录.json','resume':resume,
     'today':{'records':d['answeredQuestions'],'byLesson':dict(counts),'reportedMinutes':d.get('actualMinutes'),'timeReport':d.get('timeReport'),'remainingBudget':d.get('remainingPlannedMinutes')},
     'preparedEntry':r.get('preparedLessons',{}).get('entryRelativePath'),
     'activeModule':{k:r['lessonProgress'].get(resume['lesson'],{}).get(k) for k in ['status','mastered','covered','pending']},
     'rules':['一题一答，按备课顺序推进','先讲完整小节，减少简单重复题','原答及时保存；小节或3—5题后同步核验','只按需读相关旧错，不加载全部历史原答']}
print(json.dumps(out,ensure_ascii=False,indent=2))
