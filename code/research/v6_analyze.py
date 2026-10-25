"""Evaluator/report builder, separate from request/activity inference."""
import json,hashlib,statistics
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from ghostgraph.contract import read_csv,timestamp
from evaluation.main import step_key
ROOT=Path(__file__).resolve().parents[2];CACHE=ROOT/'.ghostgraph/v6'
def iso(x):return datetime.fromtimestamp(x,timezone.utc).isoformat().replace('+00:00','Z')
def main():
 r=json.loads((CACHE/'results.json').read_text());rev=json.loads((CACHE/'review_reproduction.json').read_text());placebo=json.loads((CACHE/'placebos.json').read_text())
 requests={name:{q['case_id']:q for q in read_csv(ROOT/'dataset'/file)} for name,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]}
 temporal=[];complete=[];incomplete=[];newedges={};changed_ids={}
 for dataset,variants in r.items():
  base={x['case_id']:x for x in read_csv(CACHE/(dataset+'_A.csv'))}
  for arm,x in variants.items():
   newedges[(dataset,arm)]=[e for e in x['selected_edges'] if not e.get('already_grounded')]
   changed_ids[(dataset,arm)]=[c['case_id'] for c in x['changes']]
   ds={d['case_id']:d for d in json.loads((CACHE/(dataset+'_'+arm+'_diagnostics.json')).read_text())}
   for edge in x['selected_edges']:
    q=requests[dataset][edge['case_id']];cut=timestamp(q['audit_at'])
    if not timestamp(q['requested_at'])<=timestamp(edge['event_time'])<=cut:temporal.append([dataset,arm,edge['case_id'],'event'])
    if timestamp(q['reported_at'])>cut:temporal.append([dataset,arm,edge['case_id'],'report'])
    for ref in edge['own']:
     if max(ref['available'],ref.get('observed',ref['available']))>cut:temporal.append([dataset,arm,edge['case_id'],'owner source'])
   for d in ds.values():
    cut=timestamp(requests[dataset][d['case_id']]['audit_at'])
    for proof in d.get('proofs',[]):
     if max(proof['available'],proof['observed'])>cut:temporal.append([dataset,arm,d['case_id'],'state source'])
   for change in x['changes']:
    q=requests[dataset][change['case_id']];d=ds[q['case_id']];edge=d.get('v6_assignment')
    if dataset!='full':continue
    for step in change['added']:
     proof=next((p for p in d.get('proofs',[]) if p['system']==step['system_id'] and p['resource']==step['resource_id']),None)
     entry=dict(variant=arm,case_id=q['case_id'],resource=step['resource_id'],operation=step['operation'],evidence_id=step['evidence_id'],
          audit_at=q['audit_at'],proof=proof,assignment=edge)
     if change['before_status']=='COMPLETE':
      assert step['operation']=='VERIFY_RECORD_ABSENT' and proof and proof['state']=='ABSENT' and step['evidence_id']==proof['evidence_id']
      complete.append(entry)
     else:
      assert step['evidence_id']=='';incomplete.append(entry)
   # Existing account relationships never disappear, even on collision rejection.
   from research.v6_assignment import account_ids
   for row in read_csv(CACHE/(dataset+'_'+arm+'.csv')):assert account_ids(base[row['case_id']])<=account_ids(row)
 assert not temporal,temporal
 (CACHE/'temporal_and_changes.json').write_text(json.dumps(dict(temporal_violations=temporal,complete_changes=complete,incomplete_changes=incomplete,new_edges={f'{d}_{v}':e for (d,v),e in newedges.items()}),indent=2))
 audit='''# V6 candidate audit

Protected production:7a18c2e, submission-v5.1. Research branch:experiment/activity-assignment-v6. Production inference modules, output.csv and code.zip are unchanged. No canonical labels are read by v6_assignment.py; labels enter only reproduction/evaluation/report tooling.

## Independent source reproduction

All reviewer counts reproduce exactly:508 authorized full requests,342 without account_service steps;108 unique compatible candidates in the fixed [-120,+30] minute window, split73 INCOMPLETE/35 COMPLETE. Public13 unique candidates agree with all13 canonical IDs (evaluation only);57 unique candidates in the166 already-grounded full requests agree with all57 current account sets. All539 qualifying account DELETE_RECORD events have source deletion_worker, with270 SUCCESS,158 PARTIAL and111 FAILED results.

Mapping COMPLETE→SUCCESS, PARTIALLY_COMPLETE→PARTIAL, NOT_STARTED→FAILED is a lexical workflow-compatibility hypothesis, not an official causal mapping or a deletion-state fact. FAILED is compatible with an unsuccessful start attempt but does not prove a worker belongs to the request. Mapping was fixed from the review/source vocabularies, not optimized using canonical labels. Workflow claims and operation outcomes do not determine actual record state.

The supplied asymmetric window has no independent preregistration/provenance available in the repository. Whether the external reviewer tuned it against known public cases cannot be established. It is a development hypothesis, not held-out validation. V6 froze the supplied window and a five-window comparison grid before scoring, and did not search for an optimal public score.

## Window sensitivity

Unique means exactly one eligible event, not nearest event, one resource per subject, or a forced global one-to-one matching. Bounds require event≥requested_at, event≤audit_at and workflow report≤audit_at. Enforcing the first two bounds changes none of the reviewer counts in this dataset, but they remain required safeguards. Wider windows are less likely to appear unique, and can expose a false narrow singleton.

| Window | Status filter | Missing-account unique | Existing-account unique / agree | Public unique / agree |
|---|---|---:|---:|---:|
'''
 for name in ['five_minutes','half_hour','wide_review','two_hours','one_day']:
  for status in [False,True]:
   x=rev['windows'][f'{name}:status={status}:bounds=True'];audit+=f"| {name} | {status} | {x['missing_full']['unique']} | {x['grounded_full']['unique']} / {x['grounded_full']['matches']} | {x['sample']['unique']} / {x['sample']['matches']} |\n"
 audit+='\n## Eight conflicting five-minute singletons\n\nAll eight status-compatible narrow-window singleton candidates disagree with the existing resource set. A disagreement is not itself proof that a customer cannot have multiple accounts, but it invalidates using narrow uniqueness as ownership proof. Existing edges are never removed.\n\n| Case | Worker | Candidate | Grounded resource | Delta seconds |\n|---|---|---|---|---:|\n'
 for c in rev['windows']['five_minutes:status=True:bounds=True']['grounded_full']['conflicts']:
  audit+=f"| {c['case_id']} | {c['activity_id']} | {c['candidate']} | {','.join(c['known'])} | {c['delta_seconds']:.0f} |\n"
 audit+='''
## Provenance classes and candidate graph

The graph records directly evidenced existing relationships (`already_grounded` with separate source proofs), independently corroborated candidate relationships (`own` positive eligible references), weak time/status-only candidates, and rejected/conflicting candidates with explicit reasons. New weak relationships are never relabeled as direct evidence. The ordinary ledger's temporary discovery seed is replaced in diagnostics by an explicitly labeled research hypothesis; existing grounded resources delegate to the baseline ledger without replacement. No strict-certification code is changed or invoked with candidate edges.

B uses a unique status-compatible event plus bounds/foreign-owner/history/existing-assignment consistency checks. Absence of a contradiction is not positive ownership proof. C adds conservative bipartite collision rejection across contemporaneously eligible requests from different independently resolved subjects. It does not maximize a one-to-one assignment: such exclusivity is not established. Repeated same-subject requests can share an event; multiple events/resources remain unresolved rather than forced. Future peer requests/statuses and future identity snapshots cannot affect earlier collision checks. D additionally requires positive ownership corroboration before ordinary source-grounded state/policy planning. All108 new singleton candidates lack that corroboration;57 have corroboration only because they are already grounded controls. Eight of those controls are collision-rejected as event associations, while their actual existing resource edges remain in output.

Per-window candidate records, source event locators/times, eligibility, ownership proofs and B/C/D rejection reasons are enumerated in v6_edge_provenance.md and reproducibly generated .ghostgraph/v6/*_edges.json. No inference uses numeric suffixes, nearest-ID conventions, canonical resource labels or worker SUCCESS as a resulting-state observation.

## case_09: eligible state is not eligible ownership

Request cutoff:2026-09-16T09:00:00Z. The eligible activity_3703 (system_activity.csv row3704) identifies account_3960 as a worker target at2026-09-07T07:55:18Z,3882 seconds before reported_at. It contains no subject identifier. A full account snapshot really is eligible: evidence_93, evidence/databases/customer_data_inventory_20260916.sql, snapshot_scope row for account_service (line12) and table customer_profiles, captured2026-09-16T08:37:39Z. Its exhaustive lookup supports absence of that specified resource conditional on identifying the target; it does not supply the missing subject/account relationship. B/C use the worker correlation assumption to propose a future empty-citation account verification. D rejects the unsupported ownership inference.

The actual profile readback in evidence_06 line86 observes account_3960 absent at2026-09-16T08:57:34Z, but the file was captured2026-09-18T11:55:24Z: it is ineligible. The retained audit_record_4902 and its subject trace exist only in the same late file (readback line28, observed2026-09-16T08:52:59Z). Original-source identifier search finds no eligible record/catalog/worker reference identifying or proving presence of that audit resource. Its verification cannot be recovered without late-source use or inventing an ID. No late trace is used to tie the worker target to user_61. Citation clamping would not fix that ownership leak; it is not performed.

No supplied external prototype or provenance proving an untuned window is present. The reviewer counts are verified; the stronger ownership/generalization interpretation is not established.
'''
 (ROOT/'code/research/v6_candidate_audit.md').write_text(audit)
 # One record per request/activity pair, with all variant decisions side by side.
 edge_md='''# V6 per-candidate source provenance

Only events inside the fixed time window are candidates. All rejected in-window events are retained. Status mismatches, ambiguity, collisions, identity/ownership checks and missing corroboration are explicit. IDs here are participant source keys, not ownership inferred from suffixes. Raw JSON with full timestamps/locators is regenerated by v6_run.py under ignored .ghostgraph/v6. Ownership references are evaluated only for otherwise unique eligible candidates; rejecting a nonunique set does not assert ownership of any member.

| Dataset | Case | Source activity (CSV keyed locator) | Resource | Event time | Delta sec | B | C | D | Eligible ownership evidence |
|---|---|---|---|---|---:|---|---|---|---|
'''
 for dataset in ['sample','full']:
  arms={v:{(e['case_id'],e['activity_id']):e for e in json.loads((CACHE/(dataset+'_'+v+'_edges.json')).read_text())} for v in ['B','C','D']}
  for key,e in arms['B'].items():
   values=[]
   for arm in ['B','C','D']:
    d=arms[arm][key];values.append('selected '+('grounded' if d.get('already_grounded') else 'candidate') if d['selected'] else ','.join(d['rejections']) or 'not selected')
   refs=';'.join(sorted({x['evidence_id']+':'+x['locator'] for x in e.get('own',[])})) or 'none / not established'
   edge_md+=f"| {dataset} | {e['case_id']} | {e['activity_id']} | {e['resource_id']} | {e['event_time']} | {e['delta_seconds']:.0f} | {' | '.join(values)} | {refs} |\n"
 (ROOT/'code/research/v6_edge_provenance.md').write_text(edge_md)
 results='''# V6 activity assignment experiment results

## Decision: reject promotion; retain V5.1

The constrained weak-correlation B ablation improves public scores but does not establish ownership of their new targets. Synthetic unrelated-singleton controls produce false assignments even after collision rejection. Requiring independent ownership corroboration removes every new link and produces no accuracy improvement. Thus B/C fail the evidence/generalization promotion criteria; D is defensible but offers no gain. No main merge, production ZIP replacement, analytics attribution, temporal relaxation or hidden-accuracy claim is made.

## Controlled strategies

A is the frozen V5.1 predictor. B is unique wide-window/status matching with independent negative consistency checks and the unchanged planner. C adds conservative cross-subject collision rejection. D is C plus positive eligible ownership corroboration. An explicit whole-case guard preserves the baseline when an account-only addition would upgrade INCOMPLETE to COMPLETE; no invented finding or empty-citation COMPLETE is created. Every variant uses eligible independent observations/exhaustive snapshots for current state, never reported SUCCESS. Existing policy, state engine, order and serializer are untouched. Future empty-citation checks for INCOMPLETE rows are generated by the ordinary policy planner, not simulated remediation. B/C results are explicitly conditional hypotheses, not defensible ownership conclusions merely because CSV structure passes.

## Public32 metrics (known development examples)

| Variant | Exact rows | Statuses | Matching steps | Precision | Recall | F1 | Citation accuracy | Field accuracy | Sequence | Sample structural errors | Full structural errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''
 for arm,x in r['sample'].items():
  m=x['metrics'];c=m['counts'];results+=f"| {arm} | {c['exact_rows']}/32 | {c['status_correct']}/32 | {c['exact_step_matches']}/193 | {m['step_precision']:.2%} | {m['step_recall']:.2%} | {m['step_f1']:.2%} | {m['canonical_evidence_accuracy']:.2%} | {m['field_accuracy']:.2%} | {m['exact_sequence_accuracy']:.2%} | {len(x['violations'])} | {len(r['full'][arm]['violations'])} |\n"
 results+='\nAll variants retain the six pre-existing sample-only structural errors after the account-only status guard. Full518 has zero in every variant. These sample errors are not disguised as submission compliance. B adds6 exact-correct public steps and0 additional incorrect operations; C adds5 correct and0 additional incorrect. Existing4 extra public steps remain. No new public account ID is incorrect, but there are no labels for full-set ownership accuracy. Public successes are not independent proof.\n\n'
 results+='## Rejected exploratory account-only upgrades\n\nBefore applying the explicit whole-case guard, the ordinary prediction planner would have upgraded two unsupported empty public rows to COMPLETE after an inferred account-absence lookup. That exploratory B run showed12/32 exact,31/32 statuses and167/193 steps; C showed11/32,31/32 and166/193. Those numbers violate the requested restriction on account-only completion and are NOT the final candidate results. The guard was added from the task constraint, with an independently fictional regression test; final metrics above preserve the original case status. No unsupported finding was invented to preserve the apparent gains. The earlier observations and correction are disclosed, not hidden.\n\n## Graph additions versus output changes\n\n| Variant | Full selected edges | New hypothetical edges | Existing selected controls | Full row changes | COMPLETE changes | INCOMPLETE changes | Renumbered common steps |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
 for arm,x in r['full'].items():
  results+=f"| {arm} | {len(x['selected_edges'])} | {len(newedges[('full',arm)])} | {sum(bool(e.get('already_grounded')) for e in x['selected_edges'])} | {len(x['changes'])} | {sum(c['before_status']=='COMPLETE' for c in x['changes'])} | {sum(c['before_status']=='INCOMPLETE' for c in x['changes'])} | {sum(c['renumbered'] for c in x['changes'])} |\n"
 results+='\nOf the108 initial unique missing-account candidates: B accepts108 conditional edges but changes107 rows (34/35 COMPLETE and73/73 INCOMPLETE); one COMPLETE target lacks eligible state proof and gets no invented step. C retains94 of108 and changes93 (28 COMPLETE/65 INCOMPLETE);14 collide with another subject request. D accepts0 new relationships. New edges are distinct from new serialized rows. Every old account resource set is preserved; adding sorted account verifications shifts step numbers but never reorders common semantic steps (zero public ordering errors). Exact-row improvement is measured with actual arrays, not inferred from recall.\n\n'
 # 108-row source/state audit, with a separate COMPLETE state-proof obligation.
 results+='## All108 unlabeled candidates and source-grounded planning audit\n\nEach event proposes a target only; none of these108 has an independent eligible owner link. An ABSENT observation is conditional state evidence for that target, not evidence it belongs to the requester. D rejects every row for missing ownership. INCOMPLETE future checks have empty citation IDs and use rule_01 USER_PROFILE/Always/DELETE, conditional on the weak assignment; they do not claim remediation happened.\n\n| Case | Account | Worker | Delta min | Baseline | B change | C change | Independent state witness / locator | Available UTC | Audit cutoff |\n|---|---|---|---:|---|---|---|---|---|---|\n'
 ds={d['case_id']:d for d in json.loads((CACHE/'full_B_diagnostics.json').read_text())};base={x['case_id']:x for x in read_csv(CACHE/'full_A.csv')}
 for e in sorted(newedges[('full','B')],key=lambda e:e['case_id']):
  cid=e['case_id'];proof=next((p for p in ds[cid].get('proofs',[]) if p['resource']==e['resource_id'] and p['system']=='account_service'),None)
  ref=(proof['state']+' '+proof['evidence_id']+':'+proof['locator']) if proof else 'NONE; no actual-state claim'
  available=iso(proof['available']) if proof else 'none'
  results+=f"| {cid} | {e['resource_id']} | {e['activity_id']} | {e['delta_seconds']/60:.2f} | {base[cid]['deletion_status']} | {cid in changed_ids[('full','B')]} | {cid in changed_ids[('full','C')]} | {ref} | {available} | {e['audit_at']} |\n"
 results+='\nFor each changed COMPLETE row above, the cited eligible snapshot/readback witness supports the added VERIFY_RECORD_ABSENT; all34 B /28 C witness/state/citation/cutoff combinations were checked programmatically. No row changes an existing full-set status or drops a resource. For each changed INCOMPLETE row, the target comes from the exact eligible worker ID and the policy obligation is future verification only; lack of actual ownership makes that obligation unsuitable for promotion despite structural validity. Full details, including supporting source path/availability, are reproducibly generated in temporal_and_changes.json.\n\n'
 results+='## Exact changed full-row IDs\n\n'
 for arm in ['A','B','C','D']:results+='**'+arm+' ('+str(len(changed_ids[('full',arm)]))+'):** '+(', '.join(changed_ids[('full',arm)]) or 'none')+'\n\n'
 results+='## Negative controls and accidental matches\n\nSeventeen independently authored mutation/control tests accompany the156 existing tests (173 passing software tests). Passing tests means the stated behavior/failures were verified, not that weak B/C passed assignment-safety controls.\n\n| Scenario | B | C | D |\n|---|---|---|---|\n| Unrelated unique compatible anonymous worker | False assignment admitted | False assignment admitted | Rejected: no ownership corroboration |\n| One event, two contemporaneous different subjects | Collision not rejected | Rejects ambiguous assignments | Rejects |\n| Repeated same subject requests | No forced exclusivity | Sharing allowed | Still requires positive owner proof |\n| Explicit foreign owner / reused shared email | Rejects | Rejects | Rejects |\n| Multiple valid events/resources / unrelated batch | No arbitrary singleton | No forced maximum matching | Preserves uncertainty |\n| Wrong result / missing event / outside window | Rejects | Rejects | Rejects |\n| After-cutoff event or capture | Rejects / cannot corroborate | Same | Same |\n| Future foreign source or peer request | Cannot influence earlier inference | Same | Same |\n| Old deleted plus current present account | Never forces one per person | Same | Preserves independent owner proofs |\n| Primary absent, replica present | Temporal engine returns PRESENT | Same | Same |\n\n'
 results+='Placebo schedule shifts move requested_at, reported_at and audit_at together, retaining their durations; the event stream is unchanged. Disagreement is measured against the original166 grounded resource sets, not invented hidden labels or proof that a customer can have only one account.\n\n| Shift days | Unique compatible events | Grounded unique | Agree with original IDs | Disagree |\n|---:|---:|---:|---:|---:|\n'
 for days,x in placebo['schedule_shifts'].items():results+=f"| {days} | {x['unique_count']} | {x['grounded_unique']} | {x['grounded_agreements']} | {len(x['grounded_disagreements'])} |\n"
 pp=placebo['status_permutations'];total=sum(x['grounded_unique'] for x in pp);wrong=sum(len(x['grounded_disagreements']) for x in pp);unique=[x['unique_count'] for x in pp]
 results+=f"\nThirty fixed-seed611 status permutations preserve marginal status counts. Unique-event counts range{min(unique)}–{max(unique)} (mean{statistics.mean(unique):.2f}), versus165 unmutated. They produce{wrong}/{total} grounded-resource disagreements. These are stress/disagreement rates, not estimated hidden-set accuracy. ±30-day shifts yield117/148 unique matches with34/40 grounded disagreements; timing clusters can manufacture uniqueness. Original57/57 agreement is meaningful positive-control correlation but is selected from the already-grounded subset, not exchangeable guaranteed truth for anonymous accounts. Even under an unproven independent/exchangeable-binomial assumption,0 errors in57 would only bound the one-sided95% error rate below{1-.05**(1/57):.2%}; it cannot certify the108 new edges.\n\n"
 results+='## Temporal compliance, reproducibility and usage\n\nEvery selected worker event and workflow report is eligible by the case cutoff; requested_at lower bounds are enforced. Every admitted owner reference and actual state witness has max(available,observed)≤audit_at. An audit across all variant diagnostics reports0 violations. No capture time is clamped/backdated; no future record is used to infer an ID or reject an earlier owner. case_09 late traces are excluded despite earlier embedded event times; its eligible SQL state does not supply ownership or the retained-audit identity. Worker SUCCESS/FAILED remains only a correlation feature, never a state witness. Strict certification modules are unchanged.\n\nAll eight final sample/full variant CSVs reproduced byte for byte on a repeat run; baseline A and safe D full output reproduce protected CSV exactly. Reproduction uses the same pinned environment and cached source extraction; a new clean-host or cold-OCR run was not needed for this rejected research variant and is not claimed. Input artifacts/tag/main are verified unchanged. All candidates/predictions go under ignored .ghostgraph/v6; production output.csv/code.zip are never written.\n\n| Dataset/arm | Audit/assignment runtime sec | Local learned calls after baseline | Classification cache hits |\n|---|---:|---:|---:|\n'
 for dataset,variants in r.items():
  for arm,x in variants.items():results+=f"| {dataset}/{arm} | {x['runtime_seconds']:.3f} | {x['calls']} | {x['cache_hits']} |\n"
 results+='\nA counts its full baseline inference; B/C/D timings and calls are incremental on A, excluding shared ingestion and model fitting. A complete measured four-arm runner uses6 learned calls for samples and20 for full518 (26 total), including duplicate inference across isolated arms. The assignment algorithm itself is deterministic and introduces no learned model. Provider/model: local scikit-learn, unchanged ghostgraph-intent-hybrid-word-char-logreg-v5-selective and V5.1 authorization gates. No hosted AI calls; API tokens and paid API cost0. Local token units are inapplicable and CPU cost is unpriced. Whole-session/test inference totals were not globally instrumented and are not fabricated.\n\n'
 results+='''## Promotion criteria verdict

B improves exact public rows and F1 while C improves F1 without exact-row gain; both pass full518 structural checks and introduce0 wrong public account IDs, but fail independent false-attribution controls and per-row source-grounded ownership. D respects those safeguards and temporal rules but has no exact-row/F1 improvement. No arm meets every promotion criterion. Reject V6 promotion; keep production submission-v5.1 at7a18c2e. There is no analytics experiment or production repack. All full-set new assignment correctness remains UNKNOWN without labels/corroboration, not falsely reported as0 errors.

Reproduce from the experimental branch:

```bash
PYTHONPATH=code python3 -m research.v6_reproduce
PYTHONPATH=code python3 -m research.v6_controls
PYTHONPATH=code python3 -m research.v6_run
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
PYTHONPATH=code python3 -m research.v6_analyze
```

No canonical output labels are read by the candidate/assignment algorithm. Raw outputs and full provenance are generated only in ignored .ghostgraph/v6; the Markdown reports preserve the useful results for source review. No missing structured session trace or exact engineering-model metadata is manufactured.
'''
 (ROOT/'code/research/v6_assignment_results.md').write_text(results)
 print('Reports written; temporal violations:',len(temporal),'promotion: REJECT')
if __name__=='__main__':main()
