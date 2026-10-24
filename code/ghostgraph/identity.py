"""Time-bounded alias resolution without name matching or resource-ID conventions."""

from collections import defaultdict

from .contract import read_csv, timestamp
from .evidence import identities


class IdentityIndex:
    def __init__(self, dataset, store=None):
        self.current = read_csv(dataset / "user_identities.csv")
        self.audit = read_csv(dataset / "user_audit_log.csv")
        self._cutoffs = {}
        self.store = store
        self._provenance = {}

    def resolve(self, email, cutoff):
        if not hasattr(self, "_cutoffs"):
            self._cutoffs = {}
        if cutoff in self._cutoffs:
            by_user, owners = self._cutoffs[cutoff]
            return self._lookup(by_user, owners, email)
        by_user = defaultdict(set)
        proofs = defaultdict(list)
        def link(uid, values, source, locator, available, evidence_id=None):
            for token in identities(values):
                by_user[uid].add(token)
                proofs[(uid,token)].append(dict(source=source,locator=locator,available=available,evidence_id=evidence_id))
        for i,row in enumerate(self.current,2):
            if timestamp(row["updated_at"]) <= cutoff:
                link(row['user_id'],{k: row[k] for k in ["user_id", "email", "phone", "email_hash"]},'user_identities.csv',f'row:{i}',timestamp(row['updated_at']))
        for i,row in enumerate(self.audit,2):
            if timestamp(row["event_time"]) <= cutoff:
                link(row['user_id'],[row['user_id'],row['old_value'],row['new_value']],'user_audit_log.csv',f'row:{i}',timestamp(row['event_time']),row['audit_id'])
        store=getattr(self,'store',None)
        if store is not None:
            for when,system,resource,tokens,evidence_id in store.links:
                users={t for t in tokens if t.startswith('user_')}
                if when<=cutoff and len(users)==1:
                    link(next(iter(users)),list(tokens),'system_activity.csv',resource,when,evidence_id)
            for obs in store.observations:
                if max(obs.available,obs.observed)>cutoff:continue
                refs=identities({k:obs.fields[k] for k in ['user_id','customer_reference','subject_reference','subject_ref','subject_selector'] if k in obs.fields})
                users={t for t in refs if t.startswith('user_')}
                if len(users)!=1:continue
                values={k:obs.fields[k] for k in ['email','email_hash','phone','owner_email','requester_email','customer_email'] if k in obs.fields}
                link(next(iter(users)),[next(iter(users)),values],obs.source,obs.locator,max(obs.available,obs.observed),obs.evidence_id)
        owners = defaultdict(set)
        for uid, tokens in by_user.items():
            for token in tokens: owners[token].add(uid)
        self._cutoffs[cutoff] = by_user, owners
        if not hasattr(self,'_provenance'):self._provenance={}
        self._provenance[cutoff]=proofs
        return self._lookup(by_user, owners, email)

    def explain(self,email,cutoff):
        tokens,uid,note=self.resolve(email,cutoff)
        return dict(subject_id=uid,note=note,aliases=[dict(identifier=t,proofs=self._provenance.get(cutoff,{}).get((uid,t),[])) for t in sorted(tokens)] if uid else [])

    @staticmethod
    def _lookup(by_user, token_owners, email):
        email = email.casefold()
        owners = sorted(token_owners.get(email, set()))
        if len(owners) > 1:
            return {email}, None, "identifier belongs to multiple subjects; no automatic merge"
        if not owners:
            # A supplied request identifier is usable for direct evidence matching even
            # when the latest identity snapshot cannot legally establish earlier state.
            return {email}, None, "no eligible stable-subject identity link"
        uid = owners[0]
        # Shared historical identifiers are retrieval ambiguities, not automatic
        # edges to both subjects. Stable references or other unique identifiers
        # must supply the link instead.
        unique_tokens = {token for token in by_user[uid] if token_owners[token] == {uid}}
        return unique_tokens | {email}, uid, None
