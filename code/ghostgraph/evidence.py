"""Read-only adapters for the six participant evidence formats.

All observations preserve source locators and availability separately from event time.
No adapter reads sample_output.csv, organizer material, or files outside the manifest.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess

from .contract import read_csv, timestamp

EMAIL = re.compile(r"[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}", re.UNICODE)
USER = re.compile(r"\buser_[0-9]+\b")
HASH = re.compile(r"\b[0-9a-fA-F]{64}\b")
RESOURCE = re.compile(r"\b(?:account|analytics|search|support|export|data_flow|backup|audit_record|legal_hold|tombstone|marketing|cache|object|email_delivery)_[0-9]+\b")
PHONE = re.compile(r"\+\d[\d ()-]{6,}\d")
NULLS = {"", "null", "none", "[redacted]", "redacted", "no direct identifier"}
DEFAULTS = {
    "account": ("account_service", "USER_PROFILE"),
    "analytics": ("analytics_platform", "ANALYTICS_PROFILE"),
    "search": ("search_service", "SEARCH_INDEX_ENTRY"),
    "support": ("support_platform", "SUPPORT_MESSAGE"),
    "export": ("export_service", "USER_EXPORT"),
    "data_flow": ("integration_service", "DATA_FLOW"),
    "backup": ("backup_service", "BACKUP_ARCHIVE"),
    "audit_record": ("security_service", "SECURITY_AUDIT_LOG"),
    "legal_hold": ("finance_service", "LEGAL_HOLD_RECORD"),
    "tombstone": ("identity_service", "ACCOUNT_TOMBSTONE"),
    "marketing": ("marketing_platform", "MARKETING_PROFILE"),
    "cache": ("cache_service", "CACHE_ENTRY"),
    "object": ("object_storage", "SUPPORT_ATTACHMENT"),
    "email_delivery": ("email_delivery_service", "EMAIL_DELIVERY_LOG"),
}


def prefix(resource):
    return resource.rsplit("_", 1)[0]


def identities(value):
    """Extract complete strong identifiers, never names or numeric suffix matches."""
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    result = {s.casefold() for pattern in (EMAIL, USER, HASH) for s in pattern.findall(text)}
    result.update(re.sub(r"\D", "", s) for s in PHONE.findall(text))
    return result


def is_value(value):
    return value is not None and str(value).casefold() not in NULLS


def truth(value):
    if value is True or value == 1 or str(value).lower() == "true":
        return True
    if value is False or value == 0 or str(value).lower() == "false":
        return False
    return None


def flatten(data):
    out = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                out.update(flatten(value))
            elif not isinstance(value, list):
                out[key] = value
    return out


def direct_identifiers(data, *, include_reference=False):
    flat = flatten(data)
    keys = {"name", "full_name", "display_name", "email", "phone", "email_hash",
            "requester_name", "requester_email", "requester_phone", "customer_email",
            "owner_email", "owner_phone", "uploaded_by"}
    if include_reference:
        keys |= {"user_id", "customer_reference", "subject_reference"}
    return any(is_value(flat.get(k)) for k in keys)


@dataclass
class Observation:
    evidence_id: str
    source: str
    locator: str
    available: float
    observed: float
    system: str
    resource: str
    category: str
    state: str
    subject_tokens: set = field(default_factory=set)
    fields: dict = field(default_factory=dict)
    scope: str = "logical"
    quality: int = 2
    kind: str = "observation"

    @property
    def key(self):
        return self.system, self.resource


class EvidenceStore:
    def __init__(self, dataset, cache_dir=None):
        self.dataset = Path(dataset).resolve()
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.observations = []
        self.scopes = []
        self.claims = []
        self.links = []
        self.coverage = []
        self.manifest = read_csv(self.dataset / "evidence_files.csv")
        self.citation_times = {}
        self.hashes = {}
        self.by_token = defaultdict(list)
        self.by_resource = defaultdict(list)
        self.warnings = []
        self.extraction_stats = Counter()

    def add(self, meta, resource, fields, *, system=None, category=None, state=None,
            observed=None, locator="", scope="logical", quality=2, extra_tokens=()):
        if not resource or not RESOURCE.fullmatch(resource):
            return
        default_system, default_category = DEFAULTS[prefix(resource)]
        category = category or fields.get("record_type") or default_category
        system = system or fields.get("system") or default_system
        state = state or self.infer_state(fields, category)
        if state is None:
            return
        when = observed or fields.get("observed_at") or fields.get("recorded_at") or meta["captured_at"]
        obs = Observation(meta["file_id"], meta["file_path"], locator,
                          timestamp(meta["captured_at"]), timestamp(when), system, resource,
                          category, state, identities(fields) | set(extra_tokens), fields,
                          scope, quality)
        self.observations.append(obs)

    @staticmethod
    def infer_state(data, category):
        explicit = data.get("result")
        states = {"FOUND": "PRESENT", "NOT_FOUND": "ABSENT", "IDENTIFIABLE": "IDENTIFIABLE",
                  "ANONYMIZED": "ANONYMIZED", "REDACTED": "REDACTED", "ACTIVE": "ACTIVE",
                  "DISABLED": "DISABLED", "BLOCKED": "BLOCKED", "PRESENT": "PRESENT"}
        if explicit in states:
            return states[explicit]
        if category == "DATA_FLOW":
            enabled = truth(data.get("enabled"))
            return None if enabled is None else "ACTIVE" if enabled else "DISABLED"
        if category == "BACKUP_ARCHIVE":
            allowed = truth(data.get("restore_allowed"))
            return None if allowed is None else "ACTIVE" if allowed else "BLOCKED"
        if category in {"ANALYTICS_PROFILE", "PRODUCT_TELEMETRY"}:
            return "IDENTIFIABLE" if direct_identifiers(data, include_reference=True) else "ANONYMIZED"
        if category in {"SUPPORT_MESSAGE", "EMAIL_DELIVERY_LOG", "ACCOUNT_TOMBSTONE"}:
            return "IDENTIFIABLE" if direct_identifiers(data) or identities(data.get("message_text", "")) or identities(data.get("message_excerpt", "")) else "REDACTED"
        return "PRESENT"

    def load(self):
        adapters = {".json": self.json_file, ".sql": self.sql_file, ".log": self.log_file,
                    ".txt": self.text_file, ".pdf": self.document_file, ".png": self.document_file}
        for meta in self.manifest:
            path = (self.dataset / meta["file_path"]).resolve()
            if not path.is_relative_to(self.dataset / "evidence") or not path.is_file():
                raise ValueError("manifest path outside evidence or missing: " + meta["file_id"])
            self.citation_times[meta["file_id"]] = timestamp(meta["captured_at"])
            self.hashes[meta["file_path"]] = hashlib.sha256(path.read_bytes()).hexdigest()
            before = len(self.observations)
            scopes_before = len(self.scopes)
            adapters[path.suffix](path, meta)
            self.coverage.append(dict(evidence_id=meta["file_id"], format=path.suffix,
                                      observations=len(self.observations) - before,
                                      scopes=len(self.scopes) - scopes_before))
        self.activity_file()
        for obs in self.observations:
            self.by_resource[obs.key].append(obs)
            for token in obs.subject_tokens:
                self.by_token[token].append(obs)
        return self

    def record(self, data, meta, *, system=None, collection="", when=None, locator="", scope="logical"):
        resource = data.get("resource_id")
        if not resource:
            return
        fields = dict(data)
        category = fields.get("record_type")
        if "attachment" in collection or fields.get("storage_class") == "ticket_attachment":
            category = "SUPPORT_ATTACHMENT"
        if "contact" in collection:
            category = "SECONDARY_IDENTIFIER"
        if "tombstone" in collection:
            category = "ACCOUNT_TOMBSTONE"
        if prefix(resource) == "account" and fields.get("account_status") == "DELETED":
            category = "ACCOUNT_TOMBSTONE"
        state = None
        if "status_code" in fields:
            state = "ABSENT" if fields["status_code"] == 404 else "PRESENT" if fields["status_code"] == 200 else None
            fields.update(fields.get("profile") or {})
        if "hits" in fields:
            state = "PRESENT" if fields["hits"]["total"] else "ABSENT"
            documents = fields["hits"].get("documents", [])
            if documents:
                fields.update(documents[0])
        if "download_available" in fields and not truth(fields["download_available"]):
            # Unavailable download does not prove the stored export was deleted.
            fields["availability_only"] = True
        self.add(meta, resource, fields, system=system, category=category, state=state,
                 observed=fields.get("observed_at") or fields.get("recorded_at") or when,
                 locator=locator, scope=scope, quality=4)

    def json_file(self, path, meta):
        data = json.loads(path.read_text())
        if "service_exports" in data:
            for system, groups in data["service_exports"].items():
                for collection, records in groups.items():
                    for i, record in enumerate(records):
                        self.record(record, meta, system=system, collection=collection,
                                    locator=f"service_exports/{system}/{collection}/{i}")
        elif "snapshots" in data:
            for si, snapshot in enumerate(data["snapshots"]):
                for i, record in enumerate(snapshot["records"]):
                    self.record(record, meta, system=snapshot.get("data_store"),
                                collection=snapshot.get("collection", ""), when=snapshot.get("captured_at"),
                                locator=f"snapshots/{si}/records/{i}")
        else:
            for i, record in enumerate(data.get("records", [])):
                self.record(record, meta, collection=data.get("collection", ""),
                            when=data.get("captured_at") or data.get("exported_at"), locator=f"records/{i}")

    def sql_file(self, path, meta):
        conn = sqlite3.connect(":memory:")
        try:
            def authorizer(action, arg1, arg2, db, trigger):
                if action in {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH}:
                    return sqlite3.SQLITE_DENY
                if action == sqlite3.SQLITE_PRAGMA and (str(arg1).lower(), str(arg2).lower()) != ("foreign_keys", "on"):
                    return sqlite3.SQLITE_DENY
                if action == sqlite3.SQLITE_FUNCTION and str(arg2).lower() in {"load_extension", "writefile", "readfile"}:
                    return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
            conn.set_authorizer(authorizer)
            ticks = [0]
            def progress():
                ticks[0] += 1
                return int(ticks[0] > 10000)
            conn.set_progress_handler(progress, 1000)
            conn.executescript(path.read_text())
            conn.row_factory = sqlite3.Row
            tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            table_types = {"customer_profiles": "USER_PROFILE", "customer_search_documents": "SEARCH_INDEX_ENTRY",
                           "customer_analytics_profiles": "ANALYTICS_PROFILE", "support_records": "SUPPORT_MESSAGE",
                           "customer_exports": "USER_EXPORT", "connector_subscriptions": "DATA_FLOW",
                           "backup_restore_entries": "BACKUP_ARCHIVE", "security_audit_records": "SECURITY_AUDIT_LOG"}
            for table in tables:
                if table == "snapshot_scope":
                    continue
                quoted = '"' + table.replace('"', '""') + '"'
                records = [dict(row) for row in conn.execute("SELECT * FROM " + quoted)]
                system = None
                category = table_types.get(table)
                if table.startswith("customer_profiles"):
                    system, category = "account_service", "USER_PROFILE"
                if table == "search_documents_primary":
                    system, category = "search_service", "SEARCH_INDEX_ENTRY"
                keys = set()
                for i, row in enumerate(records):
                    record = json.loads(row["record_json"]) if "record_json" in row else row
                    if category:
                        record = dict(record, record_type=category)
                    self.record(record, meta, system=row.get("origin_system") or system,
                                collection=row.get("collection_name", table),
                                locator=f"table:{table}/resource:{row['resource_id']}", scope=table)
                    keys.add(row["resource_id"])
                # Full exported table permits absence only for independently linked resources.
                self.scopes.append(dict(meta=meta, table=table, resources=keys,
                                        system=system, category=category,
                                        generic=any("record_json" in r for r in records)))
        finally:
            conn.close()

    @staticmethod
    def parse_line(line):
        """Normalize JSON, logfmt, bracket, pipe, syslog and cloud escaped log lines."""
        time_match = re.match(r"(\d{4}-\d\d-\d\dT[\d:.]+Z)", line)
        if not time_match:
            return None
        rest = line[time_match.end():].strip()
        if rest.startswith("{"):
            data = json.loads(rest)
        else:
            rest = re.sub(r'\\+"', '"', rest)
            if "requestId=" in rest and "message=" in rest:
                envelope, payload = rest.split("message=", 1)
                rest = envelope + " " + (payload[1:-1] if payload.startswith('"') and payload.endswith('"') else payload)
            data = {}
            for key, quoted, plain in re.findall(r'([A-Za-z_][\w]*)=(?:"([^"\n]*)"|([^\s]+))', rest):
                data[key] = quoted if quoted else plain
            bracket = re.search(r"\[(?:INFO|WARN|DEBUG|ERROR)\] \[([^\]]+)\] \[([^\]]+)\] (\w+):", rest)
            if bracket:
                data.update(service=bracket[1], trace_id=bracket[2], event=bracket[3])
            if " | " in rest:
                parts = rest.split(" | ")
                if len(parts) >= 5:
                    data.update(service=parts[1], trace_id=parts[2], event=parts[3])
            syslog = re.search(r"<\d+>1 \S+ (\S+) (\S+) - -", rest)
            if syslog:
                data.update(service=syslog[1], trace_id=syslog[2])
            if "function" in data:
                data["service"] = data["function"]
            if "requestId" in data:
                data["trace_id"] = data["requestId"]
            # Escaped cloud message fields can be hidden inside the outer message token.
            for key, value in re.findall(r'([A-Za-z_][\w]*)="([^"\n]*)"', rest):
                data[key] = value
        data["event_time"] = time_match[1]
        return data

    def log_file(self, path, meta):
        content = path.read_text()
        is_readback = "readback" in content[:200]
        parsed = [(i, self.parse_line(line)) for i, line in enumerate(content.splitlines(), 1)]
        traces = defaultdict(set)
        for _, data in parsed:
            if data and data.get("trace_id"):
                traces[data["trace_id"]].update(identities(data))
        for i, data in parsed:
            if not data or not data.get("resource_id"):
                continue
            event = data.get("event", "")
            resource = data["resource_id"]
            state, category = None, None
            if event.endswith("_started") or event in {"connection_acquired", "cache_lookup", "dependency_retry", "dependency_recovered", "thumbnail_failed"}:
                continue
            if event == "record_lookup":
                state = self.infer_state(data, data.get("record_type", ""))
                category = data.get("record_type")
            elif event == "profile_lookup_completed":
                if data.get("http_status") == "404" or data.get("rows") == "0": state = "ABSENT"
                elif data.get("rows") == "1": state = "PRESENT"
            elif event == "index_query_completed":
                if data.get("result") in {"hit", "miss"}: state = "PRESENT" if data["result"] == "hit" else "ABSENT"
            elif event in {"message_pii_scan", "attachment_pii_scan", "analytics_identity_scan"}:
                state = "IDENTIFIABLE" if event != "attachment_pii_scan" else "PRESENT"
                if event == "attachment_pii_scan": category = "SUPPORT_ATTACHMENT"
            elif event in {"contact_lookup_completed", "contact_query_completed"}:
                category = "SECONDARY_IDENTIFIER"
                if data.get("rows") in {"0", "1"}: state = "PRESENT" if data["rows"] == "1" else "ABSENT"
            elif event == "deletion_marker_check":
                # Missing marker alone is not a state observation.
                continue
            elif event in {"analytics_profile_read", "analytics_profile_read_completed"}:
                state = "IDENTIFIABLE" if data.get("direct_identifiers") == "1" or direct_identifiers(data, include_reference=True) else "ANONYMIZED"
            elif event == "support_ticket_read_completed":
                state = "IDENTIFIABLE" if direct_identifiers(data) else "REDACTED"
            elif event == "message_read":
                state = "REDACTED" if data.get("message_text") == "[REDACTED]" else "IDENTIFIABLE"
            elif event in {"connector_heartbeat", "connector_config_loaded", "connector_config_read_completed"}:
                enabled = truth(data.get("enabled"))
                if enabled is not None: state = "ACTIVE" if enabled else "DISABLED"
            elif event in {"restore_candidate_evaluated", "restore_policy_read_completed", "restore_authorization_completed"}:
                if "restore_allowed" in data: state = "ACTIVE" if truth(data["restore_allowed"]) else "BLOCKED"
                elif data.get("decision") in {"deny", "allow"}: state = "BLOCKED" if data["decision"] == "deny" else "ACTIVE"
                elif "eligible" in data: state = "ACTIVE" if truth(data["eligible"]) else "BLOCKED"
            elif event in {"export_download_check_completed", "export_metadata_read_completed"}:
                if truth(data.get("available")): state = "PRESENT"
            elif event == "audit_record_read_completed" and data.get("rows") == "1":
                state = "PRESENT"
            if state:
                service = data.get("system") or data.get("service")
                if service in {"profile_service", "support_replica"}: service = "account_service" if service == "profile_service" else "support_platform"
                default = DEFAULTS.get(prefix(resource))
                if not default: continue
                if service not in {v[0] for v in DEFAULTS.values()}: service = default[0]
                self.add(meta, resource, data, system=service, category=category, state=state,
                         observed=data["event_time"], locator=f"line:{i}",
                         quality=5 if event.endswith("_read_completed") or is_readback else 3,
                         extra_tokens=traces.get(data.get("trace_id"), set()))

    def text_file(self, path, meta):
        for i, line in enumerate(path.read_text().splitlines(), 1):
            parts = [p.strip() for p in line.removeprefix("- ").split("|")]
            if len(parts) == 6 and RESOURCE.fullmatch(parts[2]):
                when, system, resource, category, result, subject = parts
                self.add(meta, resource, dict(record_type=category, result=result, subject_reference=subject),
                         system=system, category=category, observed=when, locator=f"line:{i}", quality=4)

    def extracted_text(self, path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        cache = self.cache_dir / (digest + ".txt") if self.cache_dir else None
        if cache and cache.exists():
            self.extraction_stats["cache_hits"] += 1
            return cache.read_text()
        command = ["pdftotext", "-layout", str(path), "-"] if path.suffix == ".pdf" else ["tesseract", str(path), "stdout"]
        self.extraction_stats["pdftotext_calls" if path.suffix == ".pdf" else "tesseract_calls"] += 1
        result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=True)
        if not result.stdout.strip():
            raise ValueError("empty document extraction: " + path.name)
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(result.stdout)
        return result.stdout

    def document_file(self, path, meta):
        text = self.extracted_text(path)
        # Conservative document extraction: explicit resource identifiers plus business facts.
        # Catalog links may later connect document references that are not canonical resource IDs.
        resources = set(RESOURCE.findall(text))
        for resource in sorted(resources):
            category = DEFAULTS[prefix(resource)][1]
            if prefix(resource) == "support" and path.suffix == ".pdf" and "attachment" in text.lower():
                category = "SUPPORT_ATTACHMENT"
            if prefix(resource) == "audit_record" and "retain until" in text.lower():
                category = "SECURITY_AUDIT_LOG"
            excerpt = text
            if path.suffix == ".png" and len(resources) > 1:
                # A screen can list unrelated customers. Never associate every
                # resource with every email elsewhere on the page.
                excerpt = "\n".join(line for line in text.splitlines() if resource in line)
                if not identities(excerpt): continue
            fields = {"document_excerpt": excerpt}
            state = "PRESENT"
            if category == "ANALYTICS_PROFILE": state = "IDENTIFIABLE"
            if category in {"SUPPORT_MESSAGE", "ACCOUNT_TOMBSTONE"}:
                state = "IDENTIFIABLE" if EMAIL.search(excerpt) or PHONE.search(excerpt) else "UNKNOWN"
            if category == "DATA_FLOW":
                if not ("Continuous" in text or "enabled" in text.lower()): continue
                state = "ACTIVE"
            if category == "BACKUP_ARCHIVE":
                # Archive existence doesn't prove restore authorization.
                continue
            self.add(meta, resource, fields, category=category, state=state,
                     locator="document:explicit-resource-reference", quality=1)
        self.documents = getattr(self, "documents", [])
        self.documents.append((meta, text))

    def activity_file(self):
        for row in read_csv(self.dataset / "system_activity.csv"):
            when = timestamp(row["event_time"])
            self.citation_times[row["activity_id"]] = when
            if row["event_type"] == "LINK_RESOURCE_IDENTITY":
                self.links.append((when, row["target_system"], row["resource_id"], identities(row["details"]), row["activity_id"]))
            else:
                self.claims.append(row)
        # Catalog may supply a canonical ID for a document's explicit reference.
        for when, system, resource, tokens, evidence_id in self.links:
            row = next(r for r in read_csv(self.dataset / "system_activity.csv") if r["activity_id"] == evidence_id)
            label = re.search(r"\(([^)]+)\)", row["details"])
            if not label: continue
            for meta, text in getattr(self, "documents", []):
                compatible_origin = meta["origin"] == system or (system == "export_service" and "CUSTOMER STATEMENT" in text and "statement" in text.lower())
                if not compatible_origin: continue
                if not re.search(r"(?<![\w])" + re.escape(label[1]) + r"(?![\w])", text): continue
                if resource in {o.resource for o in self.observations if o.evidence_id == meta["file_id"]}: continue
                category = DEFAULTS[prefix(resource)][1]
                if category == "BACKUP_ARCHIVE": continue
                state = "PRESENT"
                if category == "ACCOUNT_TOMBSTONE": state = "UNKNOWN"
                self.add(meta, resource, {"document_reference": label[1]}, system=system,
                         category=category, state=state, locator="document:catalog-reference",
                         quality=1)

    def summary(self):
        return {"files": len(self.manifest), "formats": dict(Counter(r["format"] for r in self.coverage)),
                "observations": len(self.observations), "file_coverage": self.coverage,
                "sql_scopes": len(self.scopes), "activity_claims": len(self.claims),
                "catalog_links": len(self.links)}
