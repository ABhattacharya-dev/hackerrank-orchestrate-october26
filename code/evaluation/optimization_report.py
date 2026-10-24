"""Render measured mismatch explanations and AI ablations into submitted Markdown.

Evaluation-only: reference answers never flow to ingestion, inference or planning.
"""
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def load(name):return json.loads((ROOT/'.ghostgraph'/f'{name}.json').read_text())


def explanation(step,diagnostic):
    key=step['system_id'],step['resource_id']
    ledger=next((e for e in diagnostic.get('obligation_ledger',[]) if (e['system'],e['resource'])==key),None)
    if ledger is None:
        return 'No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.'
    issues=ledger.get('issues',[])
    temporal=next((e for e in diagnostic.get('temporal_ledger',[]) if (e['system'],e['resource'])==key),{})
    reasons=[]
    if temporal.get('state') in {'UNKNOWN','CONFLICT'}:reasons.append('Temporal state is '+temporal['state']+'; copy coverage or contradictory observations remain unresolved.')
    if issues:reasons.append('Policy proof gaps: '+', '.join(issues)+'.')
    if ledger.get('applicability')!='SATISFIED':reasons.append('Policy applicability is '+str(ledger.get('applicability'))+'; safe treatment cannot be assumed.')
    if not reasons:reasons.append('Current grounded ledger supports a different or partial plan; review the reference state/citation against scoped evidence and the obligation ledger.')
    return ' '.join(reasons)


def render():
    m=load('sample_metrics');p=load('planning_acceptance');a=load('ai_ablation')
    ds={d['case_id']:d for d in load('sample_diagnostics')}
    lines=['# Public-sample mismatch report','',
        'Generated from the actual full 32-case public evaluation. Reference answers are read only by evaluation. Reasons below describe present implementation gaps, not proof of dataset defects. Alternative valid citations still count wrong against exact public reference IDs.','',
        '| Metric | Result |','| --- | ---: |']
    for label,key in [('Case status accuracy','status_accuracy'),('Step precision','step_precision'),('Step recall','step_recall'),('Step F1','step_f1'),('Field accuracy','field_accuracy'),('Canonical evidence citation accuracy','canonical_evidence_accuracy'),('Exact sequence accuracy','exact_sequence_accuracy'),('Exact row accuracy','exact_row_accuracy')]:
        value=m[key];lines.append(f'| {label} | {value:.4%} |')
    c=m['counts'];missing=Counter(s['operation'] for d in m['mismatches'] for s in d['missing_steps'])
    lines+=['','## Error impact and priorities','',
        f"Status errors: {c['cases']-c['status_correct']}; missing operations: {c['missing_steps']}; extra operations: {c['extra_steps']}; wrong states on aligned operations: {c['wrong_states']}; wrong citations on aligned operations: {c['wrong_evidence']}; relative ordering errors among shared steps: {c['ordering_errors']}.",'',
        'State/citation mismatches align on phase, system, resource and operation. Missing operations remain missing rather than being relabeled as wrong fields. Relative-order checks exclude omissions; omitted preceding steps can still change absolute step numbers and field/sequence scores. Exact step metrics use multiset matching including citations. Field accuracy counts all seven expected fields, including step_no, and treats missing steps as seven wrong fields. Evidence accuracy includes omitted expected cited steps as wrong; aligned-citation error counts alone are not a recall measure.','',
        '| Missing operation | Count |','| --- | ---: |']
    lines += [f'| {op} | {n} |' for op,n in missing.most_common()]
    lines += ['',
        '1. Recover missing grounded identity/resource links and eligible primary/copy proofs before optimizing formatting or intent. Verification omissions dominate measured loss. Never infer absent account IDs from case/user suffixes.',
        '2. Extract explicit retention, shared-context and restore capability facts where supplied. Unknown conditions remain blockers; adding blanket category assumptions would weaken policy correctness.',
        '3. Review extra resources against their catalog and direct observations. Do not suppress supported findings solely because the public reference omits them.',
        '4. Preserve deterministic output and consent guards. Selective inference saves model work; public audit-status scores do not justify replacing evidence reasoning with an LLM.',
        '', '## Every remaining mismatched case','']
    for mismatch in m['mismatches']:
        cid=mismatch['case_id'];diag=ds[cid]
        lines += [f'### {cid}','',f"Classification: predicted `{mismatch['predicted_status']}`, reference `{mismatch['expected_status']}`. Incorrect: `{mismatch['incorrect_classification']}`. Relative ordering incorrect: `{mismatch['incorrect_ordering']}`.",'']
        for heading,key in [('Missing steps','missing_steps'),('Extra steps','extra_steps')]:
            lines.append(heading+':')
            lines.append('')
            if not mismatch[key]:lines+=['None.',''];continue
            for s in mismatch[key]:
                lines.append(f"- `{s['phase']} {s['operation']} {s['system_id']}/{s['resource_id']} {s['state']}`; citation `{s['evidence_id'] or '(empty)'}`. {explanation(s,diag)}")
            lines.append('')
        for heading,key in [('Wrong states','wrong_states'),('Wrong evidence','wrong_evidence')]:
            lines.append(f"{heading}: "+(json.dumps(mismatch[key]) if mismatch[key] else 'None on aligned operations.')+'\n')
        codes=sorted({i['code'] for i in diag['issues']})
        lines += ['Diagnosed case gaps: '+(', '.join(f'`{x}`' for x in codes) or 'none')+'.','']
    lines+=['## Structural acceptance','',
        f"Generated sample rows passing: {p['valid_subset_rows']}/32. Violations: {len(p['generated_structural_violations'])} across {len(p['blocked_cases'])} cases: {', '.join(p['blocked_cases'])}. All reference rows pass. This milestone's all-structural-checks exit condition is **not met**; the valid subset is diagnostic only.",
        '', '## Selective AI experiment','',
        'Ablation uses the same fixed training corpus and English scope/ambiguity guards. Rules-only abstains on unhandled language. ML-only uses the learned probability at 0.5 without guards. Guarded eager and guarded selective share decisions; selective skips inference when scope guards decide. Expected ambiguity is abstention, and unhandled definite intents count incorrect in the all-item accuracy. Calls exclude fitting and include real predict_proba execution; no API tokens apply.','',
        '| Dataset / arm | Correct | Abstentions | False authorizations |','| --- | ---: | ---: | ---: |']
    for dataset in ['public','independent']:
        for arm,v in a[dataset]['arms'].items():lines.append(f"| {dataset} / {arm} | {v['correct']}/{v['total']} | {v['abstentions']} | {v['false_authorizations']} |")
    lines+=['']
    for dataset in ['public','independent']:
        v=a[dataset];lines.append(f"- {dataset}: eager {v['eager_calls']} model calls, selective {v['selective_calls']}; replay {v['replay_cache_hits']} cache hits and no additional inference calls.")
    lines+=['',
        'Public samples contain only deletion intents; this measures intent coverage, not the full audit verdict. The 24 independently authored probes were frozen before their first run and checked for exact training-text overlap. They include multilingual deletion/access/correction, implicit consent, cancellation, opt-out and uncertainty. Their small development-only design cannot establish multilingual generalization. Probe failures were not used to change model training. Actual probe texts, expected decisions and arm predictions are reproducible in `evaluation/ai_ablation.py`.','',
        'The optional vision extractor was not evaluated against a hosted model: both GHOSTGRAPH_VISION_API_KEY and GHOSTGRAPH_VISION_MODEL were absent. Five artifacts remain queued for semantic review. No vision calls, token costs or image-accuracy gains are claimed. Local discriminative inference remains a genuine participating AI component.','',
        '## Experiments and limitations','',
        'The M5 baseline at commit f54c83e scored 28/32 status, 2/32 exact sequences, 111/115 exact step precision and 111/193 recall. A proposed document reclassification replaced attachment treatment with shared-context redaction when a document mentioned an order reference. It added three extra steps with no recovered reference steps (111/118 precision, unchanged recall), and did not establish a stronger document-role proof, so it was reverted. The initial new document fixtures also exposed missing synthetic-manifest setup; those experimental fixtures were discarded with the rejected parser change. No passing test claim includes those failed runs.','',
        'The adopted change only gates inference and normalizes deduplication keys; the training examples, policy and temporal rules are unchanged. Full regression tests run after evaluator, rejected parser and selective-inference changes. Caching uses model/training hash plus canonical text and returns copies so callers cannot corrupt cached decisions. Deterministic scope outputs have probability null, not a fabricated ML confidence.','',
        'All errors above have a reproducible diagnosis, but many require better evidence extraction or authoritative linkage rather than output padding. Structural acceptance and final export remain blocked. No hidden-set accuracy is known.']
    (ROOT/'code/evaluation/mismatch_report.md').write_text('\n'.join(lines)+'\n')
    print('Rendered mismatch_report.md from actual evaluation, structural checks and AI ablation')

if __name__=='__main__':render()
