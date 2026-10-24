"""Bitemporal, scope-preserving reconstruction with explicit uncertainty.

Parser quality and availability recency never override contradictory direct facts.
Claim events cannot establish resulting state. Absence is scoped, not universal.
"""
from collections import defaultdict
from dataclasses import dataclass, field

POSITIVE={'PRESENT','IDENTIFIABLE','ACTIVE'}

@dataclass
class TemporalResult:
    state: str
    witness: object = None
    scopes: list = field(default_factory=list)
    issues: list = field(default_factory=list)

    def explain(self):
        return dict(state=self.state,scopes=self.scopes,issues=self.issues)


def scope_key(obs):
    if obs.scope != 'logical':return obs.scope
    return 'logical:'+obs.fields.get('_source_origin','unspecified')


def _reconstruct(observations,cutoff):
    eligible=[o for o in observations if o.kind=='observation' and max(o.available,o.observed)<=cutoff]
    if not eligible:return TemporalResult('UNKNOWN',issues=[{'code':'NO_ELIGIBLE_STATE_OBSERVATION'}])
    groups=defaultdict(list)
    for obs in eligible:groups[scope_key(obs)].append(obs)
    states=[];witnesses=[];issues=[]
    for scope,items in sorted(groups.items()):
        newest=max(o.observed for o in items)
        peers=[o for o in items if o.observed==newest]
        values={o.state for o in peers}
        refs=[dict(evidence_id=o.evidence_id,source=o.source,locator=o.locator,observed=o.observed,available=o.available,state=o.state)
              for o in sorted(peers,key=lambda o:(o.evidence_id,o.source,o.locator,o.state))]
        state=next(iter(values)) if len(values)==1 else 'CONFLICT'
        states.append(dict(scope=scope,state=state,observed=newest,evidence=refs))
        if state=='CONFLICT':
            issues.append(dict(code='CONFLICT',scope=scope))
        elif state=='UNKNOWN':
            issues.append(dict(code='UNSUPPORTED_SCOPED_STATE',scope=scope))
        else:
            witnesses.append(min(peers,key=lambda o:(o.evidence_id,o.source,o.locator)))
    # A proven positive copy survives absence or uncertainty in other scopes.
    logical=[s for s in states if s['scope'].startswith('logical:')]
    if len({s['state'] for s in logical})>1:
        # Collector origins are not proof of distinct physical replicas. A newer
        # export from a different collector cannot silently erase an older
        # observation, nor prove the older copy still exists at another store.
        issues.append({'code':'SCOPE_ALIGNMENT_UNKNOWN'})
        explicit_positive=[o for o in witnesses if not scope_key(o).startswith('logical:') and o.state in POSITIVE]
        if not explicit_positive:
            return TemporalResult('UNKNOWN',None,states,issues)
    positives=[o for o in witnesses if o.state in POSITIVE]
    if positives:
        witness=max(positives,key=lambda o:(o.observed,o.evidence_id,o.locator))
        return TemporalResult(witness.state,witness,states,issues)
    if issues:
        return TemporalResult('CONFLICT' if any(i['code']=='CONFLICT' for i in issues) else 'UNKNOWN',None,states,issues)
    values={o.state for o in witnesses}
    if len(values)>1:
        # Different required treatments/state vocabularies are not interchangeable.
        return TemporalResult('UNKNOWN',None,states,[{'code':'INCOMPARABLE_SCOPE_STATES'}])
    witness=max(witnesses,key=lambda o:(o.observed,o.evidence_id,o.locator))
    if witness.state=='ABSENT' and not any(o.fields.get('_covers_all_copies') is True for o in witnesses):
        # Preserve a valid scoped absence witness for explanations/candidate checks,
        # but do not certify universal absence from one lookup or incomplete coverage.
        return TemporalResult('UNKNOWN',witness,states,[{'code':'COPY_COVERAGE_UNPROVEN'}])
    return TemporalResult(witness.state,witness,states,issues)


MUTATIONS={'DELETE_RECORD','REDACT_RECORD','ANONYMIZE_RECORD','RESTORE_BACKUP',
           'SYNC_RECORD','UPDATE_RECORD','INDEX_RECORD','CREATE_EXPORT','REFRESH_CACHE',
           'DISABLE_DATA_FLOW','BLOCK_RESTORE'}


def reconstruct(observations,cutoff,claims=()):
    result=_reconstruct(observations,cutoff)
    if not result.scopes:return result
    from .contract import timestamp
    keys={o.key for o in observations}
    for claim in claims:
        if claim.get('event_type') not in MUTATIONS:continue
        if not any(resource==claim.get('resource_id') for system,resource in keys):continue
        try: when=timestamp(claim.get('event_time'))
        except (ValueError,TypeError):
            result.issues.append({'code':'MUTATION_CLAIM_TIME_UNKNOWN','activity_id':claim.get('activity_id')})
            result.state,result.witness='UNKNOWN',None
            continue
        if when<=cutoff and any(when>s['observed'] for s in result.scopes):
            result.issues.append({'code':'UNVERIFIED_MUTATION_AFTER_OBSERVATION',
                                 'activity_id':claim.get('activity_id'),'event_time':when})
            result.state,result.witness='UNKNOWN',None
    return result
