from pathlib import Path
import tempfile
import unittest
import json
from ghostgraph.planner import build_decision,PlanningBlocked
from ghostgraph.contract import step,check_rows,ordered,canonical_json,write_csv,read_csv

class PlannerTests(unittest.TestCase):
    def request(self):return dict(case_id='test',audit_at='2026-01-02T00:00:00Z')
    def times(self):return {'evidence_1':0,'evidence_2':1}

    def test_complete_is_cited_verification_only(self):
        row,issues=build_decision('test',True,verification=[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')])
        self.assertEqual(row['deletion_status'],'COMPLETE');self.assertFalse(issues)
        self.assertFalse(check_rows([row],[self.request()],self.times()))

    def test_incomplete_has_full_future_sequence_without_mutating_inputs(self):
        finding=step('REPORT_REMAINING_RECORD','account_service','account_1','evidence_1')
        verify=step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')
        row,issues=build_decision('test',True,[finding],[step('DELETE_RECORD','account_service','account_1')],[verify])
        steps=json.loads(row['steps_json'])
        self.assertEqual(row['deletion_status'],'INCOMPLETE');self.assertFalse(issues)
        self.assertEqual(verify['evidence_id'],'evidence_1')
        self.assertEqual([s['evidence_id'] for s in steps],['evidence_1','',''])
        self.assertFalse(check_rows([row],[self.request()],self.times()))

    def test_non_deletion_is_empty(self):
        row,issues=build_decision('test',False)
        self.assertEqual(row['steps_json'],'[]');self.assertEqual(row['deletion_status'],'NOT_APPLICABLE')
        with self.assertRaises(PlanningBlocked):build_decision('test',False,verification=[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')])

    def test_incomplete_risk_cannot_be_padded_with_invented_remedy(self):
        finding=step('REPORT_RESTORE_RISK','backup_service','backup_1','evidence_1')
        with self.assertRaises(PlanningBlocked):build_decision('test',True,[finding])
        row,issues=build_decision('test',True,[finding],allow_partial=True)
        self.assertIn('FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION',[i['code'] for i in issues])
        self.assertEqual(len(json.loads(row['steps_json'])),1)

    def test_unresolved_proofs_block_complete_even_with_valid_steps(self):
        with self.assertRaises(PlanningBlocked):
            build_decision('test',True,verification=[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')],issues=['copy coverage unknown'])

    def test_deduplication_and_canonical_bytes_do_not_depend_on_input_order(self):
        a=step('VERIFY_RECORD_PRESENT','security_service','audit_record_1','evidence_2')
        b=step('VERIFY_RECORD_ABSENT','account_service','account_2','evidence_1')
        c=step('VERIFY_RECORD_PRESENT','security_service','audit_record_1','evidence_1')
        first,_=build_decision('test',True,verification=[a,b,c])
        second,_=build_decision('test',True,verification=[c,b,a])
        self.assertEqual(first,second)
        self.assertEqual(len(json.loads(first['steps_json'])),2)
        self.assertFalse(check_rows([first],[self.request()],self.times()))
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'output.csv';write_csv(path,[first]);data=path.read_bytes();write_csv(path,[second])
            self.assertEqual(path.read_bytes(),data);self.assertEqual(read_csv(path),[first])
            self.assertTrue(data.startswith(b'case_id,deletion_status,steps_json\n'))

    def test_contradictory_final_states_are_rejected(self):
        steps=[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1'),step('VERIFY_RECORD_PRESENT','account_service','account_1','evidence_1')]
        with self.assertRaises(PlanningBlocked):build_decision('test',True,verification=steps)
        with self.assertRaises(PlanningBlocked):build_decision('test',True,verification=steps,allow_partial=True)

    def test_complete_requires_citations_and_phase_groups_are_checked(self):
        with self.assertRaises(PlanningBlocked):build_decision('test',True,verification=[step('VERIFY_RECORD_ABSENT','account_service','account_1')])
        with self.assertRaises(PlanningBlocked):build_decision('test',True,verification=[step('DELETE_RECORD','account_service','account_1')],allow_partial=True)

    def test_invalid_id_and_execution_citation_rejected(self):
        with self.assertRaises(PlanningBlocked):build_decision('test',True,verification=[step('VERIFY_RECORD_PRESENT','invalid system','account_1','evidence_1')])
        with self.assertRaises(PlanningBlocked):build_decision('test',True,remediation=[step('DELETE_RECORD','account_service','account_1','evidence_1')])

    def test_registry_duplicates_and_nonstandard_json_are_rejected(self):
        row,_=build_decision('test',True,verification=[step('VERIFY_RECORD_PRESENT','account_service','account_1','evidence_1')])
        self.assertIn('UNKNOWN_RESOURCE_SYSTEM_PAIR',[e['code'] for e in check_rows([row],[self.request()],self.times(),known_resource_pairs=set())])
        duplicate=json.loads(row['steps_json']);duplicate.append(dict(duplicate[0],step_no=2));row['steps_json']=json.dumps(duplicate)
        self.assertIn('DUPLICATE_STEP',[e['code'] for e in check_rows([row],[self.request()],self.times())])
        for payload in ['[{"step_no":1,"step_no":2}]','[NaN]']:
            row['steps_json']=payload
            self.assertIn('INVALID_JSON',[e['code'] for e in check_rows([row],[self.request()],self.times())])

    def test_system_and_resource_order_is_lexicographic_not_numeric(self):
        items=[step('VERIFY_RECORD_PRESENT','z_service','record_2','evidence_1'),
               step('VERIFY_RECORD_PRESENT','a_service','record_2','evidence_1'),
               step('VERIFY_RECORD_PRESENT','a_service','record_10','evidence_1')]
        row,_=build_decision('test',True,verification=items)
        steps=json.loads(row['steps_json'])
        self.assertEqual([(s['system_id'],s['resource_id']) for s in steps],
                         [('a_service','record_10'),('a_service','record_2'),('z_service','record_2')])
        self.assertEqual([s['step_no'] for s in steps],[1,2,3])

    def test_post_remediation_checks_include_required_retained_record(self):
        obligation=dict(system='security_service',resource='audit_record_1',applicability='SATISFIED',
                        remediation_required=False,verification_obligations=['VERIFY_RECORD_PRESENT'])
        row,issues=build_decision('test',True,[step('REPORT_REMAINING_RECORD','account_service','account_1','evidence_1')],
            [step('DELETE_RECORD','account_service','account_1')],[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')],obligations=[obligation])
        steps=json.loads(row['steps_json'])
        retained=next(s for s in steps if s['resource_id']=='audit_record_1')
        self.assertEqual(retained['operation'],'VERIFY_RECORD_PRESENT');self.assertEqual(retained['evidence_id'],'')
        self.assertFalse(issues);self.assertFalse(check_rows([row],[self.request()],self.times()))

    def test_complete_cannot_use_future_check_as_current_proof(self):
        obligation=dict(system='security_service',resource='audit_record_1',applicability='SATISFIED',verification_obligations=['VERIFY_RECORD_PRESENT'])
        with self.assertRaises(PlanningBlocked):build_decision('test',True,
            verification=[step('VERIFY_RECORD_ABSENT','account_service','account_1','evidence_1')],obligations=[obligation])

    def test_required_remedy_is_not_replaced_by_its_verification(self):
        obligation=dict(system='integration_service',resource='data_flow_1',applicability='SATISFIED',treatment='FLOW',
                        remediation_required=True,verification_obligations=['VERIFY_DATA_FLOW_DISABLED'])
        with self.assertRaises(PlanningBlocked):build_decision('test',True,
            verification=[step('VERIFY_DATA_FLOW_DISABLED','integration_service','data_flow_1','evidence_1')],obligations=[obligation])

if __name__=='__main__':unittest.main()
