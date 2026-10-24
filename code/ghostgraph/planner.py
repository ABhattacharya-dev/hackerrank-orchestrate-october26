"""Deterministic status/step assembly; partial plans are never certified final."""
from copy import deepcopy
import re
from .contract import ordered,canonical_json,plan_violations,STEP_FIELDS,OPERATIONS,step

class PlanningBlocked(ValueError):pass


def build_decision(case_id,authorized,findings=(),remediation=(),verification=(),*,issues=(),obligations=(),allow_partial=False):
    groups=[deepcopy(list(group)) for group in (findings,remediation,verification)]
    if not authorized:
        if any(groups):raise PlanningBlocked('non-deletion request cannot have deletion steps')
        return dict(case_id=case_id,deletion_status='NOT_APPLICABLE',steps_json='[]'),[]
    for phase,group in zip(['FINDING','REMEDIATION','VERIFICATION'],groups):
        if any(not isinstance(item,dict) or item.get('phase')!=phase for item in group):
            raise PlanningBlocked('step placed in incorrect planner phase')
    has_actions=bool(groups[0] or groups[1])
    status='INCOMPLETE' if has_actions or not groups[2] else 'COMPLETE'
    required_checks=set()
    required_remedies=set()
    remedy_for={'DELETE':'DELETE_RECORD','REDACT':'REDACT_RECORD','ANONYMIZE':'ANONYMIZE_RECORD',
                'FLOW':'DISABLE_DATA_FLOW','RESTORE':'BLOCK_RESTORE'}
    for obligation in obligations:
        if obligation.get('applicability')!='SATISFIED':continue
        system,resource=obligation['system'],obligation['resource']
        for operation in obligation.get('verification_obligations',[]):
            if operation not in OPERATIONS or OPERATIONS[operation][0]!='VERIFICATION':raise PlanningBlocked('invalid verification obligation')
            required_checks.add((operation,system,resource))
        if obligation.get('remediation_required') is True:
            operation=remedy_for.get(obligation.get('treatment'))
            if operation:required_remedies.add((operation,system,resource))
    if status=='INCOMPLETE':
        for item in groups[2]:item['evidence_id']=''
        # These are future tests of required goal states, not claims that an
        # unsupported current observation or a proposed mutation has succeeded.
        if groups[0]:
            groups[2].extend(step(operation,system,resource) for operation,system,resource in sorted(required_checks))
    steps=[];dedup={}
    for group in groups:
        for item in group:
            if set(item)!=STEP_FIELDS or item['operation'] not in OPERATIONS:raise PlanningBlocked('malformed planner step')
            if (item['phase'],item['state'])!=OPERATIONS[item['operation']][:2]:raise PlanningBlocked('operation phase/state mismatch')
            if not all(isinstance(item[k],str) for k in STEP_FIELDS-{'step_no'}):raise PlanningBlocked('step fields must be strings')
            if not all(re.fullmatch(r'[a-z][a-z0-9_]*',item[k]) for k in ['system_id','resource_id']):raise PlanningBlocked('invalid identifier syntax')
            if item['phase']=='FINDING' and not item['evidence_id']:raise PlanningBlocked('finding requires evidence')
            if item['phase']=='REMEDIATION' and item['evidence_id']:raise PlanningBlocked('proposed remediation cannot claim execution evidence')
            if status=='COMPLETE' and not item['evidence_id']:raise PlanningBlocked('complete verification requires observed evidence')
            key=item['phase'],item['operation'],item['system_id'],item['resource_id']
            previous=dedup.get(key)
            if previous is None or item['evidence_id']<previous['evidence_id']:dedup[key]=item
    steps=ordered(list(dedup.values()))
    violations=plan_violations(status,steps)
    actual={(s['operation'],s['system_id'],s['resource_id']) for s in steps}
    for operation,system,resource in sorted(required_checks-actual):
        violations.append(dict(code='MISSING_REQUIRED_VERIFICATION',operation=operation,system=system,resource=resource))
    for operation,system,resource in sorted(required_remedies-actual):
        violations.append(dict(code='MISSING_REQUIRED_REMEDIATION',operation=operation,system=system,resource=resource))
    if any(v['code'].startswith('CONTRADICTORY_') for v in violations):raise PlanningBlocked('contradictory final resource states')
    if not steps:violations.append(dict(code='NO_SUPPORTED_STEPS'))
    if status=='INCOMPLETE' and not groups[0]:violations.append(dict(code='INCOMPLETE_WITHOUT_FINDING'))
    if status=='COMPLETE' and any(s['phase']!='VERIFICATION' for s in steps):violations.append(dict(code='COMPLETE_NOT_VERIFICATION_ONLY'))
    if (issues or violations) and not allow_partial:raise PlanningBlocked('unresolved evidence or incomplete/contradictory plan')
    row=dict(case_id=case_id,deletion_status=status,steps_json=canonical_json(steps))
    return row,violations
