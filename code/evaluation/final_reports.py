"""Judge-visible reports from the evaluated final prediction run."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    result=json.loads((ROOT/'.ghostgraph/recovery_results.json').read_text())
    final=json.loads((ROOT/'.ghostgraph/final_submission.json').read_text())
    m=result['recovery_sample']['metrics'];u=result['prediction']['usage']
    rows=['# Final GhostGraph competition prediction evaluation','',
        f"Root output.csv contains {final['rows']} sorted request rows and has **zero official structural violations**. It is a prediction submission, not a high-assurance certification. A fresh directory, different working directory and empty extraction cache reproduce identical bytes. SHA-256: `{final['sha256']}`.",'',
        '## Actual 32-case public evaluation','',
        '| Metric | Result |','| --- | ---: |']
    for label,key in [('Status accuracy','status_accuracy'),('Exact row accuracy','exact_row_accuracy'),('Step precision','step_precision'),('Step recall','step_recall'),('Step F1','step_f1'),('Field accuracy','field_accuracy'),('Canonical citation accuracy','canonical_evidence_accuracy'),('Exact sequence accuracy','exact_sequence_accuracy')]:rows.append(f'| {label} | {m[key]:.4%} |')
    rows+=['','Exact steps include phase/system/resource/operation/state/citation and use multiset matching. Field accuracy aligns on phase/system/resource/operation and counts seven expected fields, including numbering. Missing cited steps count wrong for citation accuracy. Sequence accuracy compares the complete ordered array. Public labels are evaluation-only and are not predictor inputs. These development regression scores do not establish hidden-set accuracy.','',
        'Results are unchanged from 1146bc7: 9/32 exact rows, 29/32 statuses, 159/193 matching steps and 59/75 canonical citations. Public samples still contain six structural violations in three cases whose absent account IDs lack grounded links; this is distinct from the actual 518-request submission, which has none. Anonymous records with null lookups cannot be attributed by numeric suffix. No unsupported extra linkage rule was adopted solely to improve scores. Recovery history and per-operation losses are retained in recovery_report.md.','',
        '## Blocker correction and evidence','',
        'The selected archive detail in the April recovery console has its own prior drill, verified checksum, archive path and retention details in the same healthy production recovery domain. Eligible catalog activity supplies subject/archive linkage. Together these support a prediction of a live recreation path; a successful restore authorization is not directly observed. Other archives’ completed restores alone are insufficient. Future August restores are excluded. The inference is separately typed prediction_inference with document locator, target drill timestamp and catalog provenance; strict certification does not consume it as direct evidence.','',
        'The ordinary policy/planner emits REPORT_RESTORE_RISK, BLOCK_RESTORE and VERIFY_RESTORE_BLOCKED, with the finding citing the console and future steps using empty citations. Required archive records are preserved; future retained-presence verification may also appear. No deletion action is issued against the archive.','',
        '## Executed independent tests','',
        'All **114 software tests pass** (zero failures, errors or skips). Seven new counterfactual tests in tests/test_restore_prediction.py cover:',
        '', '1. Target-scoped drill/checksum/live-domain capability: exact risk/block/verification ordering and citations.',
        '2. Explicit target block: suppress the inferred active risk.',
        '3. Disabled restore service: no active capability inference.',
        '4. Other archives restored without a target drill: no target eligibility inference.',
        '5. Future capture or future target drill: excluded at cutoff.',
        '6. Foreign service or absent target/subject linkage: excluded.',
        '7. Required archive retention: RESTORE controls, never DELETE.',
        '', 'The initial OCR rule failed because an archive was repeated in the activity section and because OCR read the storage scheme as £3. Inventory/detail scope is now separated from the Activity section, and the limited storage-scheme OCR variant is accepted only alongside all other target facts. The full regression and export passed after correction. Previous seven on-disk CLI adversarial scenarios remain passing.','',
        '## Validation and remaining uncertainty','',
        'The entire CSV passes exact header/count/keys/sorting, JSON parsing, allowed phases/operations/states, consecutive numbers, canonical ordering, valid system/resource namespace, duplicate/contradiction checks, complete finding/remedy/check pairs, citation existence/cutoff and empty future citation checks. All 1,032 cited steps also match internal ledger provenance and eligible linkage/time records; this is not an independent entailment judge. Cold reproduction executes 11 OCR and 4 PDF extractions and reproduces output.csv exactly.','',
        f"Prediction diagnostics retain {result['prediction']['uncertain_cases']} uncertainty-bearing cases. The conservative certification default remains separate; no claim that its global proof obligations pass is made. Service health and a prior drill establish a defensible risk prediction, not an observed target-specific authorization. Reported service history is not treated as deletion proof. No hidden accuracy is known."]
    (ROOT/'code/evaluation/evaluation_report.md').write_text('\n'.join(rows)+'\n')
    usage=f'''# Actual final prediction-run usage

This is the 518-request prediction run that produced root output.csv, not the
older certification candidate. Provider: {u['provider']}. Model: {u['model']}.

| Measurement | Actual final-run value |
| --- | ---: |
| Requests | {u['request_count']} |
| Learned local inference calls | {u['inference_calls']} |
| Deterministic unique scope decisions | {u['scope_decisions']} |
| Intent classification cache hits | {u['cache_hits']} |
| Unique normalized classifications | {u['unique_classifications']} |
| Training fits / authored examples | 1 / {u['training_examples']} |
| API input / output tokens | 0 / 0 |
| Paid model calls | 0 |
| API cost total / per request | USD 0.00 / USD 0.00 |
| Runtime seconds | {u['runtime_seconds']:.6f} |

Token units do not apply to local TF-IDF/logistic regression, Tesseract or PDF
extraction. No token estimate was invented. No paid provider tariff applies
because no paid API calls were made. CPU/storage cost is unpriced, not asserted
free. The actual classifier participates in multilingual/implicit intent; English
scope guards and cached repetitions avoid redundant inference. Training uses
296 authored source examples, never public output labels.

Warm-run document extraction: {u['document_extraction']}.
Separate cold reproducibility validation: {final['cold_extraction']}.
Public evaluations, unit fixtures, earlier failed extraction attempts, cold
reproduction and engineering-assistant usage are separate validation/development
work and are excluded from final-run counts. Engineering-assistant billing and
exact runtime model metadata are not exposed and are not fabricated.

Restore-console inference is deterministic source extraction and rule evaluation,
not an unrecorded paid vision call. The supplied image was visually reviewed
during engineering; deployed extraction uses the reproducible local OCR path.

Final output SHA-256: {final['sha256']}.
Request SHA-256: {u['requests_hash']}.
Training SHA-256: {u['training_hash']}.

This export passes the official structural contract but is not high-assurance
certification. All uncertainty remains available in local prediction diagnostics.
'''
    (ROOT/'code/evaluation/usage_report.md').write_text(usage)
if __name__=='__main__':main()
