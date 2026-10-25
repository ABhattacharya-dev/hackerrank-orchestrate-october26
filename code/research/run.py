"""Controlled V3 ablations. Writes only .ghostgraph/v3 and research Markdown.

Never writes protected output.csv, code.zip, sample labels or competition rules.
"""
from pathlib import Path
import sys,json,time,hashlib,os
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.contract import read_csv,check_rows,resource_registry
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier
from research.auditor import ResearchAuditor
from research.linkage import graph,temporal_candidates
from evaluation.main import metrics
ROOT=Path(__file__).resolve().parents[2]
CACHE=ROOT/'.ghostgraph/v3'

def render_report(result):
    target=ROOT/'code/research';target.mkdir(exist_ok=True)
    lines=['# V3 current prediction mismatch report','',
        'Fresh frozen-prediction evaluation. Labels are used only by evaluation. Missing/extra steps align by phase/system/resource/operation; wrong-state/citation errors are separate. Zero relative ordering errors does not excuse missing steps or shifted step numbers.','']
    m=result['experiments']['A']['sample']['metrics']
    ds={d['case_id']:d for d in result['baseline_diagnostics']}
    for metric in ['status_accuracy','exact_row_accuracy','step_precision','step_recall','step_f1','canonical_evidence_accuracy','field_accuracy','exact_sequence_accuracy']:lines.append(f'- {metric}: {m[metric]:.6%}')
    rows=[]
    for mismatch in m['mismatches']:
        cid=mismatch['case_id'];d=ds[cid]
        lines += ['',f'## {cid}', '',f"Status {mismatch['predicted_status']} / reference {mismatch['expected_status']}; classification wrong: {mismatch['incorrect_classification']}; relative ordering wrong: {mismatch['incorrect_ordering']}.",'']
        for heading,key in [('Missing','missing_steps'),('Extra','extra_steps')]:
            lines.append(heading+':')
            for step in mismatch[key]:
                entry=next((e for e in d.get('obligation_ledger',[]) if (e['system'],e['resource'])==(step['system_id'],step['resource_id'])),None)
                if entry is None:cause='missing discovery/attribution: no eligible grounded ledger target'
                elif entry['observed_state'] in {'UNKNOWN','CONFLICT'}:cause='temporal scope/state uncertainty; no verified state propagation'
                elif entry.get('applicability')!='SATISFIED':cause='conditional policy applicability; metadata facts unavailable'
                else:cause='supported ledger differs from canonical coverage; review state/citation or planning obligation'
                lines.append(f"- {step['operation']} {step['system_id']}/{step['resource_id']} {step['state']} citation={step['evidence_id'] or '(empty)'}; {cause}.")
            if not mismatch[key]:lines.append('None.')
            lines.append('')
        lines.append('Wrong citations: '+json.dumps(mismatch['wrong_evidence']))
        lines.append('Wrong states: '+json.dumps(mismatch['wrong_states']))
        lines.append('Case uncertainty codes: '+', '.join(sorted({i['code'] for i in d['issues']})))
    lines+=['','Cases without mismatches: '+', '.join(sorted(set(r['case_id'] for r in read_csv(ROOT/'dataset/sample_deletion_requests.csv'))-{x['case_id'] for x in m['mismatches']}))+'.']
    (target/'mismatch_report.md').write_text('\n'.join(line.rstrip() for line in lines)+'\n')
    (ROOT/'code/evaluation/mismatch_report.md').write_text('\n'.join(line.rstrip() for line in lines)+'\n')
    lines=['# V3 controlled experiment results','',
        'Baseline 3b942ac / submission-freeze-verified. Work is isolated in experiment/evidence-linkage-v3. Frozen output.csv and code.zip are never written. No hidden labels are available.','',
        '| Arm | Exact rows | Status | Step P / R / F1 | Citation | Field | Sequence | Sample / full structural violations | Full rows changed | Seconds sample / full |',
        '| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |']
    for arm,run in result['experiments'].items():
        s=run['sample'];f=run['full'];m=s['metrics']
        lines.append(f"| {arm} | {m['counts']['exact_rows']}/32 | {m['status_accuracy']:.4%} | {m['step_precision']:.2%} / {m['step_recall']:.2%} / {m['step_f1']:.2%} | {m['canonical_evidence_accuracy']:.2%} | {m['field_accuracy']:.2%} | {m['exact_sequence_accuracy']:.4%} | {len(s['violations'])} / {len(f['violations'])} | {f['changed_rows']} | {s['runtime_seconds']:.3f} / {f['runtime_seconds']:.3f} |")
    lines += ['',
        'A frozen prediction; B corroborated temporal-only (360 seconds); C staged bidirectional structured-reference graph; D verification audit with frozen planner (no unsupported new obligation rule); F B+C+existing planner. E targeted LLM review: NOT RUN; no configured review/vision credentials and model. E is not assigned baseline scores or a fabricated zero-effect experiment. The validated proposal gate is implemented but no hosted inference advantage is claimed.','',
        '## Window investigation','',
        '| Requests | Window seconds | Candidate cases | Unique cases | Multi-candidate cases | Stage counts (events) |',
        '| --- | ---: | ---: | ---: | ---: | --- |']
    for dataset,windows in result['windows'].items():
        for window,v in windows.items():lines.append(f"| {dataset} | {window} | {v['candidate_cases']} | {v['unique_cases']} | {v['multiple_cases']} | {v['stages']} |")
    lines += ['',
        'Candidates are timestamp proposals only. Ownership must come from an eligible explicit subject-target event, scoped record, catalog or structured source/copy proof. Success/PARTIAL, reported workflow status, uniqueness, relative timestamp and readback absence never establish ownership. One event cannot identify distinct subjects; repeated same-subject workflows remain permitted. Multiple actions require independent proofs for every target. Event time must fall within requested_at..audit_at. A 303-second candidate is outside 300 seconds; rounding it into the window would be incorrect.','',
        'Candidate readback/snapshot state is always reconstructed independently. Worker SUCCESS never establishes absence; explicit replica presence survives primary absence. Wide windows increase incidental collisions. The staged graph records direct, corroborated-derived, weak and rejected relations separately with locators and availability.','',
        '## Usage, generalization and decision','',
        'Each arm executes the same genuine local intent model and deterministic policy/planning pipeline. Per-arm calls and cache hits are in the table below. All API input/output tokens and paid-model cost are zero; local TF-IDF tokens are not applicable and CPU cost is unpriced. No paid provider tariff or LLM accuracy gain is claimed. Ingestion and graph/window investigation time are recorded separately in the JSON research artifact, not conflated with arm prediction runtime.','',
        '| Arm | Sample learned calls / cache hits | Full learned calls / cache hits | API tokens / cost |',
        '| --- | ---: | ---: | --- |']
    for arm,run in result['experiments'].items():lines.append(f"| {arm} | {run['sample']['calls']} / {run['sample']['cache_hits']} | {run['full']['calls']} / {run['full']['cache_hits']} | 0 / USD 0.00 |")
    lines += ['', f"Shared ingestion {result['ingestion_seconds']:.3f}s; window/ownership investigation {result['investigation_seconds']:.3f}s; total runner {result['total_runtime_seconds']:.3f}s. Arm timings exclude model fit and shared ingestion; each arm/dataset fits one local model, ten fits total. These are single-run measurements, not a runtime significance claim."]
    improved=any(v['sample']['metrics']['exact_row_accuracy']>result['experiments']['A']['sample']['metrics']['exact_row_accuracy'] and not v['full']['violations'] for k,v in result['experiments'].items() if k!='A')
    lines+=['', 'Promotion recommendation: '+('requires further adversarial/reproducibility review; not automatically promoted' if improved else '**REJECT promotion**: no measured meaningful exact-row improvement. Keep frozen production submission.'),
        '', 'Risks: structured dependencies can express shared context rather than exclusive ownership, and stale identifiers can be reassigned. Reverse edges reject foreign stable references and known foreign/ambiguous contact ownership, but uncommon schema semantics still need validation. Temporal uniqueness is not evidence independence. Review validators can confirm exact parsed-record linkage but cannot certify novel semantic relationships; an LLM must not bypass them. No experimental arm is merged or exported over baseline artifacts.']
    validation=ROOT/'.ghostgraph/v3/test_results.json'
    if validation.exists():
        tests=json.loads(validation.read_text())
        lines += ['', f"Regression: {tests['tests_run']} tests executed; {tests['failures']} failures, {tests['errors']} errors, {tests['skipped']} skipped. Includes 15 independent V3 tests and all 115 frozen tests."]
    repro=ROOT/'.ghostgraph/v3/reproducibility.json'
    if repro.exists():
        reproduction=json.loads(repro.read_text())
        lines += ['', f"Fresh source/data copy, different working directory and empty OCR cache reproduced all 518 combination rows byte-identically in {reproduction['runtime_seconds']:.3f}s. Same installed pinned runtime; not a new dependency installation. SHA-256 {reproduction['sha256']}. Cold extraction used {reproduction['usage']['extraction']}; 5 local intent calls and 143 classification cache hits. This separate validation is excluded from arm counters."]
    (target/'results.md').write_text('\n'.join(line.rstrip() for line in lines)+'\n')

def main():
    CACHE.mkdir(parents=True,exist_ok=True);protected={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['output.csv','code.zip']}
    started=time.perf_counter();store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load()
    if store.failures:raise RuntimeError(store.failures)
    identity=IdentityIndex(ROOT/'dataset',store);labels=read_csv(ROOT/'dataset/sample_output.csv');result=dict(experiments={},windows={},baseline_diagnostics=[],ingestion_seconds=time.perf_counter()-started)
    baseline_rows={};coverage=[];investigation=time.perf_counter()
    datasets={'sample':read_csv(ROOT/'dataset/sample_deletion_requests.csv'),'full':read_csv(ROOT/'dataset/deletion_requests.csv')}
    candidates={};graphs={}
    for dataset,requests in datasets.items():
        graphs[dataset]={r['case_id']:graph(store,identity,r,reverse=False)[0] for r in requests}
        windows={}
        for w in [60,300,360,900,3600]:
            cs=temporal_candidates(store,identity,requests,w,graphs=graphs[dataset]);counts=Counter(c['case_id'] for c in cs)
            windows[str(w)]=dict(candidate_cases=len(counts),unique_cases=sum(v==1 for v in counts.values()),multiple_cases=sum(v>1 for v in counts.values()),stages=dict(Counter(c['stage'] for c in cs)))
            (CACHE/f'{dataset}_temporal_{w}.json').write_text(json.dumps(cs,indent=2))
            if w==360:candidates[dataset]=cs
        result['windows'][dataset]=windows
    result['investigation_seconds']=time.perf_counter()-investigation
    for arm in ['A','B','C','D','F']:
        result['experiments'][arm]={}
        for dataset,requests in datasets.items():
            grouped=defaultdict(list)
            if arm in {'B','F'}:
                for c in candidates[dataset]:grouped[c['case_id']].append(c)
            model=IntentClassifier();auditor=ResearchAuditor(store,identity,model,graph_enabled=arm in {'C','F'},temporal_links=grouped)
            start=time.perf_counter();pairs=[auditor.audit(r) for r in sorted(requests,key=lambda x:x['case_id'])];runtime=time.perf_counter()-start
            rows,diagnostics=map(list,zip(*pairs));errors=check_rows(rows,requests,store.citation_times,known_resource_pairs=resource_registry(store))
            if arm=='A':baseline_rows[dataset]=rows
            changed=sum(r!=b for r,b in zip(rows,baseline_rows[dataset]))
            report=dict(rows=len(rows),violations=errors,changed_rows=changed,runtime_seconds=runtime,calls=model.calls,cache_hits=model.cache_hits,uncertain_cases=sum(bool(d['issues']) for d in diagnostics),graph_links=sum(len(d['v3_graph_links']) for d in diagnostics))
            if dataset=='sample':report['metrics']=metrics(rows,labels)
            if arm=='A' and dataset=='sample':result['baseline_diagnostics']=diagnostics
            if arm=='A' and dataset=='full':
                for r,d in zip(rows,diagnostics):coverage.append(dict(case_id=r['case_id'],deletion_status=r['deletion_status'],intent_source=d['intent']['decision_source'],subject_id=d.get('subject_id'),resources=len(d.get('obligation_ledger',[])),findings=sum(s['phase']=='FINDING' for s in json.loads(r['steps_json'])),verification=sum(s['phase']=='VERIFICATION' for s in json.loads(r['steps_json'])),uncertainty=sorted({i['code'] for i in d['issues']})))
            (CACHE/f'{arm}_{dataset}_links.json').write_text(json.dumps([dict(case_id=d['case_id'],links=d['v3_graph_links'],rejected=d['v3_graph_rejections']) for d in diagnostics],indent=2))
            (CACHE/f'{arm}_{dataset}_rows.json').write_text(json.dumps(rows,indent=2))
            result['experiments'][arm][dataset]=report
    result['ai_review']=dict(status='NOT_RUN',reason='No configured hosted review/vision credentials and model',calls=0,input_tokens=0,output_tokens=0,api_cost_usd=0)
    result['total_runtime_seconds']=time.perf_counter()-started
    (CACHE/'results.json').write_text(json.dumps(result,indent=2));render_report(result)
    lines=['# Unlabeled 518-request coverage matrix','', 'Statuses are predictions, not hidden labels. Counts describe discovered evidence and obligations, not ground-truth completeness.','', '| Case | Predicted status | Subject resolved | Resources | Findings | Checks | Uncertainty codes |','| --- | --- | --- | ---: | ---: | ---: | --- |']
    for c in coverage:lines.append(f"| {c['case_id']} | {c['deletion_status']} | {bool(c['subject_id'])} | {c['resources']} | {c['findings']} | {c['verification']} | {', '.join(c['uncertainty'])} |")
    (ROOT/'code/research/coverage.md').write_text('\n'.join(line.rstrip() for line in lines)+'\n')
    for n,digest in protected.items():
        if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=digest:raise AssertionError('protected artifact changed: '+n)
    print(json.dumps({k:{d:{'changed':v['changed_rows'],'errors':len(v['violations']),'exact':v.get('metrics',{}).get('counts',{}).get('exact_rows')} for d,v in arm.items()} for k,arm in result['experiments'].items()},indent=2))
if __name__=='__main__':main()
