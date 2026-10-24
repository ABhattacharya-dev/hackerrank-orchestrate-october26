"""Official output vocabulary, deterministic serialization, and strict validation."""

import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path

GROUPS = {
    "FINDING": [("REPORT_REMAINING_RECORD", "PRESENT"), ("REPORT_EXPOSED_PII", "PRESENT"),
                ("REPORT_ACTIVE_DATA_FLOW", "ACTIVE"), ("REPORT_RESTORE_RISK", "ACTIVE")],
    "REMEDIATION": [("DISABLE_DATA_FLOW", "DISABLED"), ("BLOCK_RESTORE", "BLOCKED"),
                    ("DELETE_RECORD", "ABSENT"), ("REDACT_RECORD", "REDACTED"),
                    ("ANONYMIZE_RECORD", "ANONYMIZED")],
    "VERIFICATION": [("VERIFY_RECORD_ABSENT", "ABSENT"), ("VERIFY_RECORD_PRESENT", "PRESENT"),
                     ("VERIFY_RECORD_REDACTED", "REDACTED"), ("VERIFY_RECORD_ANONYMIZED", "ANONYMIZED"),
                     ("VERIFY_DATA_FLOW_DISABLED", "DISABLED"), ("VERIFY_RESTORE_BLOCKED", "BLOCKED")],
}
OPERATIONS = {op: (phase, state, pi, oi) for pi, (phase, pairs) in enumerate(GROUPS.items())
              for oi, (op, state) in enumerate(pairs)}
FIELDS = ["case_id", "deletion_status", "steps_json"]
STEP_FIELDS = {"step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"}


def timestamp(value):
    """Reject missing or timezone-naive times instead of guessing availability."""
    if not value:
        raise ValueError("missing timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.timestamp()


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def step(operation, system, resource, evidence=""):
    phase, state, _, _ = OPERATIONS[operation]
    return dict(step_no=0, phase=phase, system_id=system, resource_id=resource,
                operation=operation, state=state, evidence_id=evidence)


def order_key(item):
    _, _, pi, oi = OPERATIONS[item["operation"]]
    return pi, oi, item["system_id"], item["resource_id"]


def ordered(steps):
    result = sorted(steps, key=order_key)
    for i, item in enumerate(result, 1):
        item["step_no"] = i
    return result


class ContractViolation(AssertionError):
    def __init__(self,violations):
        self.violations=violations
        super().__init__('; '.join(f"{v['case_id']}: {v['code']}" for v in violations))


def parse_steps(text):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('duplicate JSON key')
            result[key]=value
        return result
    def finite(value):raise ValueError('non-finite JSON number')
    return json.loads(text,object_pairs_hook=unique,parse_constant=finite)


def plan_violations(status,steps,require_complete=True):
    errors=[]
    by_resource={}
    for item in steps:
        key=item['system_id'],item['resource_id']
        by_resource.setdefault(key,set()).add(item['operation'])
    for key,ops in sorted(by_resource.items()):
        def fail(code):errors.append(dict(code=code,system=key[0],resource=key[1]))
        treatments=ops & {'DELETE_RECORD','REDACT_RECORD','ANONYMIZE_RECORD'}
        if len(treatments)>1:fail('CONTRADICTORY_REMEDIATION')
        end_absent=bool(ops & {'DELETE_RECORD','VERIFY_RECORD_ABSENT'})
        end_present=bool(ops & {'REDACT_RECORD','ANONYMIZE_RECORD','VERIFY_RECORD_PRESENT','VERIFY_RECORD_REDACTED','VERIFY_RECORD_ANONYMIZED'})
        if end_absent and end_present:fail('CONTRADICTORY_FINAL_RECORD_STATE')
        if {'VERIFY_RECORD_REDACTED','VERIFY_RECORD_ANONYMIZED'}<=ops:fail('CONTRADICTORY_RECORD_TREATMENT')
        if not require_complete or status!='INCOMPLETE':continue
        requirements={
            'REPORT_REMAINING_RECORD':[('DELETE_RECORD','VERIFY_RECORD_ABSENT')],
            'REPORT_EXPOSED_PII':[('REDACT_RECORD','VERIFY_RECORD_REDACTED'),('ANONYMIZE_RECORD','VERIFY_RECORD_ANONYMIZED')],
            'REPORT_ACTIVE_DATA_FLOW':[('DISABLE_DATA_FLOW','VERIFY_DATA_FLOW_DISABLED')],
            'REPORT_RESTORE_RISK':[('BLOCK_RESTORE','VERIFY_RESTORE_BLOCKED')],
        }
        for finding,alternatives in requirements.items():
            if finding in ops and not any(set(pair)<=ops for pair in alternatives):fail('FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION')
        reverse={remedy:(finding,verify) for finding,pairs in requirements.items() for remedy,verify in pairs}
        for remedy,(finding,verify) in reverse.items():
            if remedy in ops and not {finding,verify}<=ops:fail('ORPHAN_REMEDIATION')
    return errors


def check_rows(rows,requests,citation_times,*,require_proofs=True,known_resource_pairs=None):
    errors=[]
    def error(cid,code,**fields):errors.append(dict(case_id=cid,code=code,**fields))
    expected={r['case_id']:r for r in requests}
    if len(expected)!=len(requests):error('*','DUPLICATE_REQUEST_IDS')
    if [r.get('case_id') for r in rows]!=sorted(expected):error('*','OUTPUT_IDS_COUNT_OR_ORDER')
    for row in rows:
        cid=row.get('case_id','?')
        if set(row)!=set(FIELDS):error(cid,'CSV_COLUMNS')
        status=row.get('deletion_status')
        if status not in {'COMPLETE','INCOMPLETE','NOT_APPLICABLE'}:error(cid,'STATUS')
        try:steps=parse_steps(row.get('steps_json'))
        except (ValueError,TypeError):error(cid,'INVALID_JSON');continue
        if not isinstance(steps,list):error(cid,'STEPS_NOT_ARRAY');continue
        if status=='NOT_APPLICABLE' and steps:error(cid,'NON_DELETION_HAS_STEPS')
        if require_proofs and status!='NOT_APPLICABLE' and not steps:error(cid,'NO_SUPPORTED_STEPS')
        valid=[];semantic=set()
        for i,item in enumerate(steps,1):
            if not isinstance(item,dict) or set(item)!=STEP_FIELDS:error(cid,'STEP_FIELDS',step=i);continue
            if type(item['step_no']) is not int or item['step_no']!=i:error(cid,'STEP_NUMBER',step=i)
            if not all(isinstance(item[k],str) for k in STEP_FIELDS-{'step_no'}):error(cid,'STEP_TYPES',step=i);continue
            if item['operation'] not in OPERATIONS:error(cid,'OPERATION',step=i);continue
            valid.append(item)
            if (item['phase'],item['state'])!=OPERATIONS[item['operation']][:2]:error(cid,'PHASE_STATE',step=i)
            for field in ['system_id','resource_id']:
                if not re.fullmatch(r'[a-z][a-z0-9_]*',item[field]):error(cid,'INVALID_IDENTIFIER',step=i,field=field)
            pair=item['system_id'],item['resource_id']
            if known_resource_pairs is not None and pair not in known_resource_pairs:error(cid,'UNKNOWN_RESOURCE_SYSTEM_PAIR',step=i)
            key=(item['phase'],item['operation'],*pair)
            if key in semantic:error(cid,'DUPLICATE_STEP',step=i)
            semantic.add(key)
            cited=status=='COMPLETE' or item['phase']=='FINDING'
            if status=='COMPLETE' and item['phase']!='VERIFICATION':error(cid,'COMPLETE_NOT_VERIFICATION_ONLY',step=i)
            if cited:
                if item['evidence_id'] not in citation_times:error(cid,'UNKNOWN_OR_MISSING_CITATION',step=i)
                elif cid in expected and citation_times[item['evidence_id']]>timestamp(expected[cid]['audit_at']):error(cid,'FUTURE_CITATION',step=i)
            elif item['evidence_id']!='':error(cid,'PROPOSED_STEP_HAS_CITATION',step=i)
        if len(valid)==len(steps) and valid!=sorted(valid,key=order_key):error(cid,'STEP_ORDER')
        if require_proofs and status=='INCOMPLETE' and not any(s['phase']=='FINDING' for s in valid):error(cid,'INCOMPLETE_WITHOUT_FINDING')
        for item in plan_violations(status,valid,require_proofs):
            error(cid,item.pop('code'),**item)
    return errors


def validate_rows(rows,requests,citation_times,*,require_proofs=True,known_resource_pairs=None):
    errors=check_rows(rows,requests,citation_times,require_proofs=require_proofs,known_resource_pairs=known_resource_pairs)
    if errors:raise ContractViolation(errors)


def canonical_json(steps):
    # Stable object keys, compact UTF-8 JSON, no NaN or duplicate keys.
    fields=['step_no','phase','system_id','resource_id','operation','state','evidence_id']
    return json.dumps([{key:s[key] for key in fields} for s in steps],ensure_ascii=False,separators=(',',':'),allow_nan=False)


def resource_registry(store):
    from .evidence import DEFAULTS,prefix
    pairs=set(store.by_resource)
    for when,system,resource,tokens,eid in store.links:pairs.add((system,resource))
    for row in store.claims:
        if row.get('target_system') and row.get('resource_id'):pairs.add((row['target_system'],row['resource_id']))
    for obs in store.observations:
        for key in ['source_resource_id','upstream_resource_id','replica_of']:
            value=obs.fields.get(key)
            if isinstance(value,str) and prefix(value) in DEFAULTS:pairs.add((DEFAULTS[prefix(value)][0],value))
    return pairs


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, path)
