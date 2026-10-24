"""Frozen independently authored intent probes; never used to train the model.

Rules-only abstains when no explicit scope is available. Scores distinguish this
from a negative decision; eager/selective guarded arms use identical semantics.
"""
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.intent import IntentClassifier,explicit_scope,is_ambiguous,POSITIVE,NEGATIVE,normalize
from ghostgraph.contract import read_csv

# Frozen before the first experiment; failures are reported, not tuned away.
PROBES=[
 ('en_implicit', 'I invoke the right to be forgotten for this membership.', True),
 ('en_access', 'Please furnish a portable archive; I will remain a subscriber.', False),
 ('en_delete', 'Erase all personal records held under this membership now.', True),
 ('en_negation', 'Do not erase the profile; I need a login recovery link.', False),
 ('en_uncertain', 'I am not sure whether to delete the profile yet.', None),
 ('en_hypothetical', 'What would happen if I decided to erase my profile next month?', False),
 ('fr_delete', 'Merci de supprimer définitivement mon profil et mes coordonnées.', True),
 ('fr_access', 'Je veux seulement consulter une copie de mes informations, pas les supprimer.', False),
 ('fr_correct', 'Corrigez mon numéro de téléphone et gardez mon compte ouvert.', False),
 ('es_delete', 'Quiero eliminar permanentemente mi perfil y la información asociada.', True),
 ('es_access', 'Solo necesito descargar una copia de mis datos; no borren mi perfil.', False),
 ('es_correct', 'Deseo corregir mi teléfono y mantener mi cuenta.', False),
 ('pt_delete', 'Por favor apaguem definitivamente o meu perfil e as informações pessoais.', True),
 ('pt_access', 'Preciso apenas de uma cópia dos meus dados, sem excluir a conta.', False),
 ('pt_correct', 'Corrijam o meu endereço de contato e mantenham a conta ativa.', False),
 ('de_delete', 'Ich bitte um endgültige Löschung meines Profils und aller persönlichen Angaben.', True),
 ('de_access', 'Ich möchte nur eine Kopie meiner Daten; bitte das Konto nicht löschen.', False),
 ('ja_delete', '登録したプロフィールと個人情報を完全に削除するようお願いします。', True),
 ('ja_access', '個人データのコピーを送ってください。アカウントは削除しないでください。', False),
 ('ko_delete', '등록된 프로필과 모든 개인정보를 영구적으로 삭제해 주시기 바랍니다.', True),
 ('ko_access', '개인 데이터 사본을 받고 싶습니다. 계정은 삭제하지 마세요.', False),
 ('en_cancel', 'Cancel the request to erase this profile; keep it available.', False),
 ('en_optout', 'Only remove this address from marketing lists; keep the account active.', False),
 ('en_complete', 'Investigate my previous erasure and finish removing its leftover identifiers.', True),
]


def decision(result):
    return None if result['low_confidence'] or result['ambiguous'] else result['authorized']


def experiment(items):
    eager=IntentClassifier(selective=False);selective=IntentClassifier()
    rows=[];start=time.perf_counter()
    for name,text,expected in items:
        rule,_=explicit_scope(text)
        if is_ambiguous(text):rule=None
        e=eager.classify(text);s=selective.classify(text)
        rows.append(dict(id=name,expected=expected,rules_only=rule,
            ml_only=e['probability']>=.5,guarded_eager=decision(e),guarded_selective=decision(s),
            selective_source=s['decision_source'],probability=s['probability']))
    elapsed=time.perf_counter()-start
    # Replays must use cached results without executing additional inference.
    first_calls=selective.calls
    for _,text,_ in items:selective.classify(text)
    if selective.calls!=first_calls:raise AssertionError('cache replay executed inference')
    arms={}
    for arm in ['rules_only','ml_only','guarded_eager','guarded_selective']:
        correct=sum(r[arm]==r['expected'] for r in rows)
        arms[arm]=dict(correct=correct,total=len(rows),accuracy=correct/len(rows),
            abstentions=sum(r[arm] is None for r in rows),
            false_authorizations=sum(r[arm] is True and r['expected'] is not True for r in rows),
            false_rejections=sum(r[arm] is False and r['expected'] is True for r in rows),
            failures=[r['id'] for r in rows if r[arm]!=r['expected']])
    assert all(r['guarded_eager']==r['guarded_selective'] for r in rows)
    return dict(arms=arms,rows=rows,eager_calls=eager.calls,selective_calls=first_calls,
                replay_cache_hits=selective.cache_hits,runtime_seconds=elapsed)


def main():
    root=Path(__file__).resolve().parents[2];cache=root/'.ghostgraph';cache.mkdir(exist_ok=True)
    training={normalize(t).casefold() for t in POSITIVE+NEGATIVE}
    assert not any(normalize(t).casefold() in training for _,t,_ in PROBES),'probe leaked into training'
    labels={r['case_id']:r['deletion_status']!='NOT_APPLICABLE' for r in read_csv(root/'dataset/sample_output.csv')}
    public=[(r['case_id'],r['request_text'],labels[r['case_id']]) for r in read_csv(root/'dataset/sample_deletion_requests.csv')]
    result=dict(public=experiment(public),independent=experiment(PROBES),
        interpretation='Public samples have no negative intents. Authored probes are a small development diagnostic, not a representative multilingual benchmark. Ambiguity requires abstention. No model/training changes were selected from probe failures.')
    (cache/'ai_ablation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({key:{k:v for k,v in value.items() if k!='rows'} for key,value in result.items() if isinstance(value,dict)},indent=2))

if __name__=='__main__':main()
