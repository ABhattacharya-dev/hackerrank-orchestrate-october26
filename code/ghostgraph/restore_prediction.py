"""Target-scoped restore capability inference from recovery consoles.

A service's other restores never establish target eligibility. Require a selected
archive's own drill, checksum, path and live domain. This predicts recreation risk,
not successful authorization or completed blocking.
"""
from collections import Counter
from datetime import datetime,timezone
import re
from .contract import timestamp
from .evidence import RESOURCE,Observation


def console_facts(text,meta):
    if meta['origin']!='backup_service':return None
    inventory=re.split(r'\bActivity\b',text,flags=re.I)[0]
    counts=Counter(r for r in RESOURCE.findall(inventory) if r.startswith('backup_'))
    selected=[r for r,n in counts.items() if n>1]
    if len(selected)!=1:return None
    drill=re.search(r'Last\s+d\w*\s+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})',text,re.I)
    if not drill:return None
    try:drilled=datetime.strptime(drill[1],'%d %b %Y').replace(tzinfo=timezone.utc).timestamp()
    except ValueError:return None
    if drilled>timestamp(meta['captured_at']):return None
    # These facts must coexist in the target detail panel and its service page.
    if not all(re.search(p,text,re.I) for p in [r'Vault Recovery Manager',r'Production',r'Healthy',r'Checksum\s+Verified',r'(?:s3|f3|£3)[:/]+',r'Retention end']):return None
    if re.search(r'(?:service\s+disabled|restore\s+(?:blocked|disabled)|access\s+denied)',text,re.I):return None
    return dict(resource=selected[0],target_drill_at=drilled,service='backup_service',
        basis='selected target detail: checksum verified, prior drill, archive path and retention; same production recovery domain healthy',
        inference='operational target restore path; archive-specific authorization not directly observed')


def infer_restore(facts,meta,cutoff,linked,observations):
    if not facts or facts['service']!='backup_service' or meta['origin']!=facts['service']:return None
    if max(timestamp(meta['captured_at']),facts['target_drill_at'])>cutoff:return None
    if not linked:return None
    eligible=[o for o in observations if max(o.available,o.observed)<=cutoff]
    # An explicit target block/disabled configuration outranks capability inference.
    if any(o.state in {'BLOCKED','DISABLED'} for o in eligible):return None
    when=timestamp(meta['captured_at'])
    return Observation(meta['file_id'],meta['file_path'],'console:selected-target/drill/checksum/domain',
        when,when,'backup_service',facts['resource'],'BACKUP_ARCHIVE','ACTIVE',set(linked),
        {'restore_block_supported':True,'prediction_inference':facts,'_source_origin':meta['origin']},
        kind='prediction_inference')
