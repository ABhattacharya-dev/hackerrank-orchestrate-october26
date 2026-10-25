"""Independent fixed intent probes and an available local alternative.

Training remains the frozen authored corpus. Probes are never fit examples; no
hyperparameter or scope-guard changes are selected from their failures.
"""
import json,time
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.intent import IntentClassifier,explicit_scope,is_ambiguous,normalize,POSITIVE,NEGATIVE
from sklearn.svm import LinearSVC
from sklearn.base import clone
from sklearn.pipeline import make_pipeline
PROBES=[
 ('explicit','Please permanently erase the registration and its saved personal records.',True),
 ('implicit','I am exercising the right to be forgotten for this membership.',True),
 ('fr_delete','Merci de procéder à la suppression définitive de mon profil client.',True),
 ('es_delete','Solicito que borren permanentemente la información de mi perfil.',True),
 ('de_delete','Bitte entfernen Sie mein Kundenprofil und sämtliche persönlichen Angaben endgültig.',True),
 ('pt_delete','Quero que apaguem de vez o perfil e as informações pessoais associadas.',True),
 ('ja_delete','登録済みのプロフィールと関連する個人情報を完全に消去してください。',True),
 ('ko_delete','가입된 계정과 연결된 개인정보를 영구적으로 지워 주십시오.',True),
 ('negation','Do not erase the profile; I am requesting a password recovery message.',False),
 ('fr_negation','Je souhaite uniquement consulter mes informations, pas supprimer mon profil.',False),
 ('es_negation','No quiero borrar mis datos; necesito una copia para revisarlos.',False),
 ('ja_negation','プロフィールを削除しないでください。データの写しだけを希望します。',False),
 ('ko_negation','계정을 삭제하지 마십시오. 개인정보 사본만 받고 싶습니다.',False),
 ('hypothetical','What would happen if I chose to close my customer profile later?',False),
 ('hypothetical_two','If I someday opt to erase the account, what records would remain?',False),
 ('deactivation','Temporarily deactivate the account for my holiday, preserving all saved information.',False),
 ('deactivation_two','Suspend sign-in for a month and retain the profile for my return.',False),
 ('marketing','Remove this address only from promotional campaigns; retain the account.',False),
 ('export','Provide a portable download of my records so I can move them to another provider.',False),
 ('correction','Correct the house number on the customer profile; keep all transaction records.',False),
 ('quoted','Translate this sentence into French: "Please delete my account and data."',False),
 ('forwarded','Forwarded customer quote: "Erase my personal information." I only need a translation.',False),
 ('conditional','If the missing refund arrives, then erase the account; until then take no deletion action.',None),
 ('conditional_two','Delete my account only after I separately confirm the closure; I have not confirmed yet.',None),
 ('third_party','I am asking you to erase my neighbor\'s profile without their consent.',False),
 ('third_party_two','As an observer, I think another customer should delete their account; this is not my request.',False),
 ('duplicate','Please complete the permanent erasure I already requested for this profile.',True),
 ('duplicate_two','This repeats my earlier instruction to remove my account and its personal data.',True),
 ('question','Can you explain the consequences of account erasure before I decide?',False),
 ('uncertain','I am undecided whether to erase the profile and want advice first.',None),
 ('cancel','Withdraw my previous deletion instruction and keep the registration.',False),
 ('positive_export','Send a final export, then permanently erase my membership and identifying information.',True),
]

def score(rows,key):
    return dict(total=len(rows),correct=sum(r[key]==r['expected'] for r in rows),
        false_authorization=sum(r[key] is True and r['expected'] is not True for r in rows),
        missed_deletion=sum(r[key] is not True and r['expected'] is True for r in rows),
        abstentions=sum(r[key] is None for r in rows),failures=[r['id'] for r in rows if r[key]!=r['expected']])

def main():
    root=Path(__file__).resolve().parents[2];cache=root/'.ghostgraph/v4';cache.mkdir(exist_ok=True)
    training={normalize(t).casefold() for t in POSITIVE+NEGATIVE}
    assert not any(normalize(t).casefold() in training for _,t,_ in PROBES)
    started=time.perf_counter();baseline=IntentClassifier()
    alternative=make_pipeline(clone(baseline.model.steps[0][1]),LinearSVC(C=1.0,class_weight='balanced',random_state=0))
    alternative.fit([normalize(t) for t in POSITIVE+NEGATIVE],[True]*len(POSITIVE)+[False]*len(NEGATIVE))
    rows=[]
    for name,text,expected in PROBES:
        guard,_=explicit_scope(text);ambiguous=is_ambiguous(text)
        result=baseline.classify(text)
        predicted=None if result['low_confidence'] else result['authorized']
        alt=bool(alternative.predict([normalize(text)])[0])
        rows.append(dict(id=name,text=text,expected=expected,guards=None if ambiguous else guard,
            baseline=predicted,guarded_svc=None if ambiguous else guard if guard is not None else alt))
    result=dict(rows=rows,metrics={arm:score(rows,arm) for arm in ['guards','baseline','guarded_svc']},runtime_seconds=time.perf_counter()-started,
        provider='local sklearn',baseline_model='frozen word/char TF-IDF logistic regression with scope guards',alternative_model='same authored training and TF-IDF features, LinearSVC C=1 with same scope guards',
        baseline_learned_calls=baseline.calls,baseline_cache_hits=baseline.cache_hits,alternative_learned_calls=len(rows),fits=2,api_input_tokens=0,api_output_tokens=0,api_cost_usd=0,
        note='Fixed authored probes are a small independent diagnostic, not a generalization guarantee. Conditional consent expects deferral. No model was tuned on these failures. No replacement adopted.')
    (cache/'intent_comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
