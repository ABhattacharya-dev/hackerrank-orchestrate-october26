import copy
import json
import unittest

from ghostgraph.contract import ordered, step, timestamp, validate_rows


class ValidationTests(unittest.TestCase):
    def fixture(self):
        request={'case_id':'test','audit_at':'2026-01-02T00:00:00Z'}
        steps=ordered([step('VERIFY_RECORD_ABSENT','account_service','account_91','evidence_1')])
        row=dict(case_id='test',deletion_status='COMPLETE',steps_json=json.dumps(steps))
        return request,row,{'evidence_1':timestamp('2026-01-01T00:00:00Z')}

    def test_future_citation_rejected(self):
        request,row,times=self.fixture()
        times['evidence_1']=timestamp('2026-01-03T00:00:00Z')
        with self.assertRaises(AssertionError): validate_rows([row],[request],times)

    def test_invalid_phase_state_and_extra_fields_rejected(self):
        request,row,times=self.fixture()
        for key,value in [('state','PRESENT'),('phase','FINDING'),('extra','unsupported')]:
            bad=copy.deepcopy(row);steps=json.loads(bad['steps_json']);steps[0][key]=value;bad['steps_json']=json.dumps(steps)
            with self.subTest(key=key),self.assertRaises(AssertionError):validate_rows([bad],[request],times)

    def test_missing_duplicate_or_unsorted_case_ids_rejected(self):
        request,row,times=self.fixture()
        for rows in [[],[row,row]]:
            with self.assertRaises(AssertionError):validate_rows(rows,[request],times)

    def test_non_deletion_must_have_no_steps(self):
        request,row,times=self.fixture()
        row['deletion_status']='NOT_APPLICABLE'
        with self.assertRaises(AssertionError):validate_rows([row],[request],times)


if __name__=='__main__':unittest.main()
