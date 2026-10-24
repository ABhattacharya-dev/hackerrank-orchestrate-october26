import json
from pathlib import Path
import tempfile
import unittest

from ghostgraph.contract import timestamp
from ghostgraph.evidence import EvidenceStore, identities


class IngestionTests(unittest.TestCase):
    def test_all_log_envelopes(self):
        formats = [
            '2026-01-01T00:00:00Z level=INFO service=account_service trace_id=x event=profile_lookup_completed resource_id=account_7 rows=1',
            '2026-01-01T00:00:00Z [INFO] [account_service] [x] profile_lookup_completed: resource_id="account_7" rows="1"',
            '2026-01-01T00:00:00Z | INFO | account_service | x | profile_lookup_completed | resource_id="account_7" rows="1"',
            '2026-01-01T00:00:00Z <15>1 node account_service x - - event="profile_lookup_completed" resource_id="account_7" rows="1"',
            '2026-01-01T00:00:00Z '+json.dumps(dict(service="account_service", trace_id="x", event="profile_lookup_completed",resource_id="account_7", rows="1")),
            r'2026-01-01T00:00:00Z requestId=x level=INFO function=account_service message="event=\"profile_lookup_completed\" resource_id=\"account_7\" rows=\"1\""',
        ]
        for line in formats:
            with self.subTest(line=line):
                parsed = EvidenceStore.parse_line(line)
                self.assertEqual(parsed["event"], "profile_lookup_completed")
                self.assertEqual(parsed["resource_id"], "account_7")
                self.assertEqual(parsed["rows"], "1")

    def test_identity_tokens_are_complete(self):
        tokens = identities("user_12, user_123, Ada Example, ADA@example.test, +44 (20) 1234-5678")
        self.assertIn("user_12", tokens)
        self.assertNotIn("user_1", tokens)
        self.assertNotIn("Ada Example", tokens)
        self.assertIn("ada@example.test", tokens)
        self.assertIn("442012345678", tokens)

    def test_timezone_required(self):
        with self.assertRaises(ValueError): timestamp("2026-01-01T00:00:00")
        self.assertEqual(timestamp("2026-01-01T00:00:00Z"),timestamp("2026-01-01T01:00:00+01:00"))

    def test_manifest_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"evidence_files.csv").write_text("file_id,file_path,origin,captured_at\nevidence_1,../outside.json,x,2026-01-01T00:00:00Z\n")
            with self.assertRaises(ValueError): EvidenceStore(root).load()


if __name__ == "__main__": unittest.main()
