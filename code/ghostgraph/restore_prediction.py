"""Target-scoped restore capability inference from recovery consoles.

A service's other restores never establish target eligibility. Require selected
archive integrity/path and either a chronologically valid target drill or
applicable live recovery controls. An earlier drill is service history only. This predicts recreation risk,
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
    created_match=re.search(r'(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s+\d{2}:\d{2}\s+UTC',inventory,re.I)
    created=None
    if created_match:
        try:created=datetime.strptime(created_match[1],'%d %b %Y').replace(tzinfo=timezone.utc).timestamp()
        except ValueError:return None
    if created is not None and created>timestamp(meta['captured_at']):return None
    target_drill_proven=created is not None and drilled>=created
    operational_controls=all(re.search(p,inventory,re.I) for p in [r'Customer.platform archives',r'Restore request',r'Service health'])
    if not target_drill_proven and not (created is not None and operational_controls):return None
    # These facts must coexist in the target detail panel and its service page.
    if not all(re.search(p,text,re.I) for p in [r'Vault Recovery Manager',r'Production',r'Healthy',r'Checksum\s+Verified',r'(?:s3|f3|£3)[:/]+',r'Retention end']):return None
    if re.search(r'(?:service\s+disabled|restore\s+(?:blocked|disabled)|access\s+denied)',text,re.I):return None
    return dict(resource=selected[0],target_drill_at=drilled if target_drill_proven else None,
        drill_history_at=drilled,archive_created_at=created,target_drill_proven=target_drill_proven,
        applicable_live_controls=operational_controls,service='backup_service',
        basis='selected target integrity/path and same live recovery domain; drill predating creation is historical context only',
        inference='operational target restore path; archive-specific authorization not directly observed')


def infer_restore(facts,meta,cutoff,linked,observations):
    if not facts or facts['service']!='backup_service' or meta['origin']!=facts['service']:return None
    if max(timestamp(meta['captured_at']),facts['drill_history_at'])>cutoff:return None
    if not linked:return None
    eligible=[o for o in observations if max(o.available,o.observed)<=cutoff]
    # An explicit target block/disabled configuration outranks capability inference.
    if any(o.state in {'BLOCKED','DISABLED'} for o in eligible):return None
    when=timestamp(meta['captured_at'])
    return Observation(meta['file_id'],meta['file_path'],'console:selected-target/drill/checksum/domain',
        when,when,'backup_service',facts['resource'],'BACKUP_ARCHIVE','ACTIVE',set(linked),
        {'restore_block_supported':True,'prediction_inference':facts,'_source_origin':meta['origin']},
        kind='prediction_inference')
