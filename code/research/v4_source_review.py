"""Research-only two-tier source validation. No automatic vision admission.

Tier B independently reads a structured original record. A proposed relationship
never confirms itself. Images/PDFs remain proposals without an independent scoped
region verifier; page-wide co-occurrence is explicitly unsupported.
"""
import json,re
from pathlib import Path
from ghostgraph.contract import timestamp
from ghostgraph.evidence import identities,DEFAULTS,prefix,Observation,EvidenceStore
OWNER_FIELDS=('user_id','subject_reference','customer_reference','subject_ref','subject_selector','email','owner_email','requester_email')

def pointer(document,path):
    if path=='':return document
    if not path.startswith('/'):raise ValueError('JSON pointer required')
    value=document
    for part in path[1:].split('/'):
        key=part.replace('~1','/').replace('~0','~')
        if isinstance(value,list) and not re.fullmatch(r'0|[1-9][0-9]*',key):raise ValueError('noncanonical array locator')
        value=value[int(key)] if isinstance(value,list) else value[key]
    return value

def validate_source(proposal,store,identity,request):
    required={'subject','system_id','resource_id','evidence_id','locator'}
    if not isinstance(proposal,dict) or set(proposal)!=required or not all(isinstance(v,str) for v in proposal.values()):return None,'invalid schema'
    cutoff=timestamp(request['audit_at']);tokens,uid,note=identity.resolve(request['email'],cutoff)
    if uid is None or (note and 'multiple' in note):return None,'ambiguous request identity'
    if proposal['subject'] not in tokens:return None,'subject is not a grounded request alias'
    key=proposal['system_id'],proposal['resource_id']
    for obs in store.by_resource.get(key,[]):
        if obs.evidence_id==proposal['evidence_id'] and obs.locator in {proposal['locator'],proposal['locator'].lstrip('/')} and max(obs.available,obs.observed)<=cutoff and proposal['subject'] in obs.subject_tokens:
            return obs,'TIER_A existing eligible scoped observation'
    meta=next((m for m in store.manifest if m['file_id']==proposal['evidence_id']),None)
    if meta is None:return None,'invented evidence'
    available=timestamp(meta['captured_at'])
    if available>cutoff:return None,'future capture'
    path=(store.dataset/meta['file_path']).resolve()
    if not path.is_relative_to(store.dataset/'evidence'):return None,'path scope'
    if path.suffix!='.json':return None,'diagnostic proposal only: no independent original-region verifier'
    try:
        document=json.loads(path.read_text());record=pointer(document,proposal['locator'])
    except (OSError,ValueError,TypeError,KeyError,IndexError):return None,'invalid original locator'
    if not isinstance(record,dict) or record.get('resource_id')!=key[1]:return None,'resource not in exact scoped record'
    if any(isinstance(v,list) and any(isinstance(r,dict) and 'resource_id' in r for r in v) for v in record.values()):return None,'multiple resource records within proposed scope'
    owners={k:record[k] for k in OWNER_FIELDS if k in record}
    if isinstance(record.get('profile'),dict):owners.update({k:record['profile'][k] for k in OWNER_FIELDS if k in record['profile']})
    source_tokens=identities(owners)
    if proposal['subject'] not in source_tokens:return None,'no explicit subject/authoritative ownership field in scoped record'
    stable={t for t in source_tokens if t.startswith('user_')}
    if stable and stable!={uid}:return None,'conflicting stable ownership'
    for token in source_tokens:
        if '@' in token:
            _,owner,issue=identity.resolve(token,cutoff)
            if (owner and owner!=uid) or (issue and 'multiple' in issue):return None,'foreign or reassigned alias'
    system,category=DEFAULTS.get(prefix(key[1]),(None,None))
    inherited_time=document.get('captured_at') or document.get('exported_at') or meta['captured_at']
    explicit_system=record.get('system')
    systems={explicit_system} if explicit_system else set()
    parts=proposal['locator'].split('/')[1:]
    ancestor=document
    for position,part in enumerate(parts[:-1]):
        key_part=part.replace('~1','/').replace('~0','~')
        ancestor=ancestor[int(key_part)] if isinstance(ancestor,list) else ancestor[key_part]
        if isinstance(ancestor,dict):
            inherited_time=ancestor.get('captured_at') or inherited_time
            if ancestor.get('data_store'):systems.add(ancestor['data_store'])
            explicit_system=explicit_system or ancestor.get('data_store')
        if position==1 and parts[0]=='service_exports':
            systems.add(key_part);explicit_system=explicit_system or key_part
    if len(systems)>1:return None,'conflicting original system scopes'
    system=explicit_system or system
    if system!=key[0]:return None,'unverified source system'
    try:observed=timestamp(record.get('observed_at') or record.get('recorded_at') or inherited_time)
    except (ValueError,TypeError):return None,'invalid original observation timestamp'
    if observed>cutoff:return None,'future observation'
    fields=dict(record);fields.pop('_covers_all_copies',None)
    if 'reported_result' in fields or fields.get('result') in {'SUCCESS','PARTIAL','FAILED','COMPLETE'}:return None,'operation claim is not a state observation'
    category=fields.get('record_type') or category
    if prefix(key[1])=='account' and fields.get('account_status')=='DELETED':category='ACCOUNT_TOMBSTONE'
    state=EvidenceStore.infer_state(fields,category)
    if 'status_code' in fields:state={404:'ABSENT',200:'PRESENT'}.get(fields['status_code'])
    if state is None:return None,'unsupported source state'
    fields['source_validation']={'tier':'B','locator':proposal['locator'],'rationale':'resource and authoritative subject field in exact original JSON record; eligible timestamps and identity conflict checks'}
    return Observation(meta['file_id'],meta['file_path'],proposal['locator'],available,observed,system,key[1],category,state,source_tokens,fields),'TIER_B independently read original record'
