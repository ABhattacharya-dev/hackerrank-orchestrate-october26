# Development-overview source and integrity audit

This is a documentation-only audit on `docs/development-overview`, based on the pre-existing research checkout `fcb820ac1d86c839b5185d85c16fadf71275685a`. Protected production remains `7a18c2e966234e1995eecd269e5e18d188437cb8`, tag `submission-v5.1`. Nothing is merged into main.

## Original versus final log

The original fingerprint was recorded before branch changes, logging or editorial file creation. “Timestamped entry” means a heading matching `## [timestamp] title`; generic level-two counts also include headings inside verbatim user prompts and are not conversation-turn counts.

| Measurement | Original | Final |
|---|---:|---:|
| Bytes | 139729 | 152735 |
| Timestamped entry headings | 33 | 35 |
| All Markdown level-two headings | 122 | 134 |

Original full-log SHA-256:

`8b3ed1d4a2bc34364102983d3b04062aef58d8695ec5404c841fb5ea43c86884`

Final full-log SHA-256:

`3343f3cc2a89a5d7e4ac5f43b8d761e0957d929ff4b00a70e9d8a58b4e642f65`

Final log's first 139729 bytes SHA-256:

`8b3ed1d4a2bc34364102983d3b04062aef58d8695ec5404c841fb5ea43c86884`

**Prefix equality: PASS.** Every original byte is identical and in its original position. All33 original timestamped entries and all122 original Markdown headings are preserved, from the initial SESSION START through V6 final guarded results and rejection. No historical prompt, response summary, action, model metadata or timestamp was edited, removed, combined, reordered or backdated. Exactly two authentic timestamped editorial entries were appended: the documentation session start and this user-turn record. New nested prompt headings explain the change in generic heading count.

Original first timestamp/title: `2026-10-24T17:48:20.313590+00:00` — SESSION START.

Original last timestamp/title: `2026-10-25T07:10:44.340402+00:00` — V6 final guarded results and rejection.

Final last timestamp/title: `2026-10-25T08:09:15.778508+00:00` — Editorial development overview and integrity verification.

These are recorded entry timestamps, not recovered execution-start times or original filesystem metadata. The V5 session explicitly reports late persistence; no earlier time is reconstructed.

## Production versus later research history

The production-tag log contains124129 bytes (SHA-256 `64ab43a5f9ca61ce6cfda4d71cba729182cdc99712f2d2cf8ae27b1d9f7eb76b`) and is itself an unchanged prefix of the original editorial input. Its final timestamped entry is Production artifact finalized on main at2026-10-25T05:51:12.237844+00:00. The original editorial input already contained15600 additional bytes of genuine V6 history, including the user prompt and recorded rejection. This supports including V6 as **post-release research**, not implying it occurred before production or modifying the frozen production transcript.

To independently repeat the prefix check from the repository:

```python
import hashlib, subprocess
from pathlib import Path
old = subprocess.check_output(["git", "show", "fcb820a:log.txt"])
now = Path("log.txt").read_bytes()
assert len(old) == 139729
assert now.startswith(old)
assert hashlib.sha256(now[:len(old)]).hexdigest() == "8b3ed1d4a2bc34364102983d3b04062aef58d8695ec5404c841fb5ea43c86884"
```

The full final-log checksum applies to this completed editorial append. A later authorized append may change that full checksum while still preserving the original prefix.

## Content verification

- Overview length:2308 approximate prose/heading words after removing link destinations;12 chronological milestones. Each supplies objective, actual user direction, agent implementation, technical decisions, failures/corrections, measured outcome and source references.
- All four blockquoted excerpts match exact substrings of the original **User Prompt** spans, specifically source entries3,14,24 and31. They were not validated against agent summaries or the newly appended editorial prompt.
- All cited original log line numbers point to timestamped entry headings before the append; all original byte/line positions remain stable. The milestone index supplies complete timestamp/title references for all grouped development entries.
- Git commit references and immutable V3/V4 report paths resolve. Historical exact-row metrics were cross-checked against34465f9,cded062,ee0914f,a0437e3 reports and the recovery comparison. Final results were checked against release_manifest.md at7a18c2e.
- The narrative distinguishes unchanged public/full predictions from improved adversarial intent results, preserves the9→7→1→2→9 regression/recovery, and keeps156 production tests separate from173 V6 research tests.
- The mistaken target-drill description, V5 sample-only regression, V5.1 invalid ambiguous-intent output and virtualenv verification issue, rejected account-only upgrades and unsupported V6 ownership are not concealed.
- No application inference, evaluation, software suite, extraction, source archive or trace archive was run/regenerated for this editorial task. Validation was static source/quotation/link/metric/integrity checking; it is not a newly measured model benchmark.

## Protected-file verification

| Artifact | Unchanged SHA-256 |
|---|---|
| output.csv | `61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891` |
| code.zip | `1681ba4bd15187cc87512c4ba1cb10b03e1ac4fc2229d2632daf7723c63fd312` |

Git comparison confirms all pre-existing code, datasets, dependencies, architecture/progress files, evaluation results, README, official instructions, release manifest and submission artifacts are unchanged from the task's starting checkout. Production Python/dependency files also match7a18c2e directly. Main and its release tag remain at7a18c2e; no existing tag was edited. Changes are limited to the three new transcript Markdown documents and append-only log.txt. No agent-trace.zip was created or original session trace modified.

## Missing metadata and source qualifications

The overview is a retrospective, not an original transcript or structured rollout. Original log entries summarize agent responses/actions, so exact complete responses, individual tool calls, hidden sessions and unrecorded timings cannot be recovered from them. The available records do not establish sub-agent staffing; the user's autonomous delegation to the engineering agent is explicit and is preserved.

Exact engineering-runtime identifiers were unavailable in the original records and remain unavailable here. No model identifier was guessed or inserted into historical entries. Consequently the root exact-model metadata requirement remains incompletely satisfied; this audit does not certify full historical logging-format compliance. The actual local application model and its usage are separately identifiable in source and release reports.

Earlier report headers sometimes retain certification-mode or intermediate results. The source index records how those were qualified, including early undated within-build metrics, corrected restore chronology and the later case_09 source refinement. No canonical inconsistency is treated as proof of a dataset defect. Hosted semantic vision/review experiments were NOT RUN; unavailable sessions are not reconstructed. Trace collection and packaging remain the user's separate task.
