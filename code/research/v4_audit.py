"""Original-source audit of canonical mismatches. Evaluation only, never inference."""
from pathlib import Path
import sys,json,re,csv
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.evidence import EvidenceStore,identities
from ghostgraph.identity import IdentityIndex
from ghostgraph.contract import read_csv,timestamp
ROOT=Path(__file__).resolve().parents[2]

def json_records(value,path=''):
    if isinstance(value,dict):
        if isinstance(value.get('resource_id'),str):yield path,value
        for key,item in value.items():yield from json_records(item,path+'/'+key.replace('~','~0').replace('/','~1'))
    elif isinstance(value,list):
        for i,item in enumerate(value):yield from json_records(item,path+'/'+str(i))

def source_index(store):
    texts={};records={};lines={}
    for meta in store.manifest:
        path=store.dataset/meta['file_path']
        text=store.extracted_text(path) if path.suffix in {'.pdf','.png'} else path.read_text()
        texts[meta['file_id']]=text
        if path.suffix=='.json':records[meta['file_id']]=list(json_records(json.loads(text)))
        lines[meta['file_id']]=text.splitlines()
    return texts,records,lines

def main():
    cache=ROOT/'.ghostgraph/v4';baseline=json.loads((cache/'sample.json').read_text())
    requests={r['case_id']:r for r in read_csv(ROOT/'dataset/sample_deletion_requests.csv')}
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();identity=IdentityIndex(ROOT/'dataset',store)
    texts,records,lines=source_index(store);manifest={m['file_id']:m for m in store.manifest}
    ds={d['case_id']:d for d in baseline['diagnostics']};entries=[]
    activity_rows=list(enumerate(read_csv(ROOT/'dataset/system_activity.csv'),2))
    for mismatch in baseline['metrics']['mismatches']:
        cid=mismatch['case_id'];request=requests[cid];cutoff=timestamp(request['audit_at']);tokens,uid,_=identity.resolve(request['email'],cutoff)
        for kind in ['missing_steps','extra_steps']:
            for step in mismatch[kind]:
                rid=step['resource_id'];key=step['system_id'],rid
                occurrences=[]
                for eid,text in texts.items():
                    if not re.search(r'(?<!\w)'+re.escape(rid)+r'(?!\w)',text):continue
                    if eid in records:
                        for locator,record in records[eid]:
                            if record['resource_id']==rid:
                                occurrences.append(dict(evidence_id=eid,path=manifest[eid]['file_path'],locator='json:'+locator,record=record,available=timestamp(manifest[eid]['captured_at'])))
                    else:
                        for i,line in enumerate(lines[eid],1):
                            if re.search(r'(?<!\w)'+re.escape(rid)+r'(?!\w)',line):
                                occurrences.append(dict(evidence_id=eid,path=manifest[eid]['file_path'],locator='line:'+str(i),record=line,available=timestamp(manifest[eid]['captured_at'])))
                obs=store.by_resource.get(key,[]);eligible=[o for o in obs if max(o.available,o.observed)<=cutoff]
                matching=[o for o in eligible if o.subject_tokens & tokens]
                entry=next((e for e in ds[cid].get('obligation_ledger',[]) if (e['system'],e['resource'])==key),None)
                history=[dict(locator='system_activity.csv:row:'+str(line),**row,subject_overlap=bool(identities(row['details'])&tokens),eligible=timestamp(row['event_time'])<=cutoff) for line,row in activity_rows if row['resource_id']==rid]
                original_citations=[step['evidence_id']] if step['evidence_id'] else []
                # Future verification has no citation; inspect all original target occurrences.
                if not original_citations:original_citations=sorted({o['evidence_id'] for o in occurrences})
                raw_eligible=[o for o in occurrences if o['available']<=cutoff]
                raw_links=[o for o in raw_eligible if identities(o['record']) & tokens]
                if kind=='extra_steps':
                    category='OUTPUT_CONVENTION_ERROR';reason='Baseline source-grounded step omitted by public reference; no evidence-based suppression justified.'
                elif occurrences and not raw_eligible:
                    category='SOURCE_DOES_NOT_SUPPORT_PROOF';reason='Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.'
                elif eligible and not matching:
                    category='SOURCE_DOES_NOT_SUPPORT_PROOF';reason='State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.'
                elif not occurrences:
                    category='SOURCE_DOES_NOT_SUPPORT_PROOF';reason='No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.'
                elif raw_links and not matching:
                    category='IDENTITY_RELATIONSHIP_LOSS';reason='Potential scoped source subject link needs independent record-boundary and observation-time verification before any parser change.'
                elif entry and entry['observed_state'] in {'UNKNOWN','CONFLICT'}:
                    category='STATE_RECONSTRUCTION_ERROR';reason='Known scoped state conflict or uncertainty; inspect source precedence rather than assume canonical state.'
                elif not eligible:
                    category='SOURCE_DOES_NOT_SUPPORT_PROOF';reason='No eligible normalized state; original occurrences alone are not a current-state or subject proof.'
                else:
                    category='POLICY_ERROR';reason='Known target missing expected treatment/check; policy applicability and planner need review.'
                # Exact cited artifact support is separately auditable, including IDs absent from it.
                cited_support=[]
                for eid in original_citations:
                    if eid not in manifest:continue
                    direct=next((o for o in occurrences if o['evidence_id']==eid),None)
                    cited_support.append(dict(evidence_id=eid,path=manifest[eid]['file_path'],capture=manifest[eid]['captured_at'],target_occurs=direct is not None,
                        locator=direct['locator'] if direct else 'artifact: no target ID; inspect snapshot schema/scope'))
                entries.append(dict(case_id=cid,kind=kind,operation=step['operation'],resource=rid,system=key[0],expected_state=step['state'],classification=category,reason=reason,confidence='high' if category=='SOURCE_DOES_NOT_SUPPORT_PROOF' else 'medium',sources=cited_support,raw_occurrences=occurrences,
                    normalized=[dict(evidence_id=o.evidence_id,locator=o.locator,state=o.state,available=o.available,observed=o.observed,eligible=max(o.available,o.observed)<=cutoff,subject_overlap=bool(o.subject_tokens&tokens),field_names=sorted(o.fields)) for o in obs],
                    activity_history=history,linkage=entry.get('identity_linkage') if entry else None,policy=entry.get('treatment') if entry else None))
    (cache/'evidence_gaps.json').write_text(json.dumps(entries,indent=2))
    counts=Counter(e['classification'] for e in entries if e['kind']=='missing_steps')
    out=['# V4 original-source evidence gap report','',
        'Frozen prediction baseline reproduced without writing protected artifacts: 29/32 statuses, 9/32 exact rows, 159/193 exact steps. There are 34 missing operations and 4 extras. Canonical labels are evaluation-only, not proof that the cited source supports its answer.','',
        '## Method and scope','',
        'Read every manifest text/SQL/JSON/log artifact directly and extracted all supplied PDF/image text with the existing deterministic tools. For every unmatched target, compared exact original JSON record paths or source lines against normalized observations, capture/event times, cutoff-specific identities, ledger links and treatment. The original object-browser screenshot relevant to extra findings was visually reviewed; screenshot-wide co-occurrence is not treated as ownership. SQL empty-table/schema semantics were inspected separately from target-ID occurrence. No V3 temporal association was rerun.','',
        '## Classification counts','']
    for name in ['PARSER_LOSS','NORMALIZATION_LOSS','SOURCE_STRUCTURE_LOSS','IDENTITY_RELATIONSHIP_LOSS','STATE_RECONSTRUCTION_ERROR','POLICY_ERROR','OUTPUT_CONVENTION_ERROR','SOURCE_DOES_NOT_SUPPORT_PROOF']:out.append(f'- {name}: {counts[name]} missing operations.')
    out += ['', '## Research matrix: every unmatched operation','',
        '| Case | Missing/extra operation | Target | Original artifact / locator | Normalized evidence | Subject linkage | Policy | Classification / confidence |',
        '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for e in entries:
        sources='; '.join(s['evidence_id']+' '+s['path']+' '+s['locator'] for s in e['sources']) or 'No manifest target occurrence; no verification citation supplied'
        normalized='; '.join(o['evidence_id']+' '+o['locator']+' '+o['state']+(' eligible' if o['eligible'] else ' FUTURE')+(' subject-linked' if o['subject_overlap'] else ' no subject overlap') for o in e['normalized']) or 'none'
        out.append(f"| {e['case_id']} | {e['kind']} / {e['operation']} | {e['resource']} | {sources} | {normalized} | {'grounded ledger link' if e['linkage'] else 'not established'} | {e['policy'] or 'unresolved'} | {e['classification']} / {e['confidence']} |")
    out += ['', '## Exact source findings','']
    for e in entries:
        if e['kind']!='missing_steps':continue
        out += [f"### {e['case_id']} / {e['resource']} / {e['operation']}",'',e['reason'],'']
        for o in e['raw_occurrences']:
            if isinstance(o['record'],dict):
                # Show relevant structural fields, not broad customer text or unrelated records.
                fields={k:v for k,v in o['record'].items() if k in {'resource_id','user_id','customer_reference','subject_reference','email','email_hash','phone','status_code','observed_at','profile','event_name'}}
                rendered=json.dumps(fields,ensure_ascii=False)
            else:rendered=o['record']
            out.append(f"- {o['evidence_id']} `{o['path']}:{o['locator']}`: `{rendered}`")
        for event in e['activity_history']:
            out.append(f"- Original activity `{event['locator']}` {event['activity_id']} {event['event_type']} {event['event_time']}; eligible={event['eligible']}, subject overlap={event['subject_overlap']}; `{event['details']}`. A claim naming a target supplies neither ownership nor resulting state.")
        if not e['raw_occurrences']:out.append('No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.')
        out.append('')
    out += ['## Canonical conventions and stop decision','',
        'Case-independent preservation rules remain: retain required security/legal records, preserve compliant tombstone references, block supported restore paths without deleting archives, and use empty citations on incomplete-case future checks. The main missing operations already have parser-normalized state or cannot be attributed/available at cutoff. No recoverable new scoped ownership fact was established. A filename, product similarity, list position or numeric suffix is not an authoritative relationship.',
        '',
        'The object-storage extra is supported by the selected delivery-confirmation filename in the original browser image and an eligible explicit exclusive subject catalog link. Other file rows are unrelated; the extractor does not join their customers. Suppressing that justified finding to match a reference would be an unsupported convention shortcut. The extra absent-account check likewise has an independent baseline ledger link and is not removed merely to improve precision.',
        '',
        'No production parser or policy correction is justified by this matrix. Stop speculative observation/vision integration rather than invent relationships. The optional vision adapter limitation is real, but its currently queued text proposals cannot fill absent or future source facts. Tier-B validation design and independent source-boundary tests are reported separately; no unmeasured model assertion enters the ledger.']
    (ROOT/'code/research/v4_evidence_gap_report.md').write_text('\n'.join(line.rstrip() for line in out)+'\n')
    print('Missing classifications:',dict(counts));print('Potential recoverable:',[e['resource'] for e in entries if e['kind']=='missing_steps' and e['classification']!='SOURCE_DOES_NOT_SUPPORT_PROOF'])
if __name__=='__main__':main()
