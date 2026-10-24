"""Time-bounded alias resolution without name matching or resource-ID conventions."""

from collections import defaultdict

from .contract import read_csv, timestamp
from .evidence import identities


class IdentityIndex:
    def __init__(self, dataset):
        self.current = read_csv(dataset / "user_identities.csv")
        self.audit = read_csv(dataset / "user_audit_log.csv")
        self._cutoffs = {}

    def resolve(self, email, cutoff):
        if not hasattr(self, "_cutoffs"):
            self._cutoffs = {}
        if cutoff in self._cutoffs:
            by_user, owners = self._cutoffs[cutoff]
            return self._lookup(by_user, owners, email)
        by_user = defaultdict(set)
        for row in self.current:
            if timestamp(row["updated_at"]) <= cutoff:
                by_user[row["user_id"]].update(identities({k: row[k] for k in ["user_id", "email", "phone", "email_hash"]}))
        for row in self.audit:
            if timestamp(row["event_time"]) <= cutoff:
                by_user[row["user_id"]].update(identities([row["user_id"], row["old_value"], row["new_value"]]))
        owners = defaultdict(set)
        for uid, tokens in by_user.items():
            for token in tokens: owners[token].add(uid)
        self._cutoffs[cutoff] = by_user, owners
        return self._lookup(by_user, owners, email)

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
