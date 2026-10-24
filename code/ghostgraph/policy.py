"""Conditional policy evaluation. Unknown applicability never authorizes deletion."""
from dataclasses import dataclass, field, asdict
from .contract import read_csv, timestamp
from .evidence import truth, EMAIL, direct_identifiers, is_value

# Recognized supplied conditions. A changed policy sentence needs an explicit
# interpreter update; silently applying old semantics to new text is unsafe.
CONDITIONS={
 'SUPPORT_MESSAGE':'Conversation contains shared customer, agent, or order context that must be retained',
 'SUPPORT_ATTACHMENT':'Attachment belongs only to the deletion subject',
 'ANALYTICS_PROFILE':'Record is still attributable to a user',
 'PRODUCT_TELEMETRY':'Record is still attributable to a user',
 'EMAIL_DELIVERY_LOG':'Log contains a user email address',
 'SECURITY_AUDIT_LOG':'Record is within the supplied retention period',
 'LEGAL_HOLD_RECORD':'A supplied legal hold is active',
 'BACKUP_ARCHIVE':'Restore access can be blocked',
 'ACCOUNT_TOMBSTONE':'Account is deleted and only a stable internal user_id is needed to preserve references to retained records',
}
REQUIRED={'DELETE':'ABSENT','REDACT':'REDACTED','ANONYMIZE':'ANONYMIZED','RETAIN':'PRESENT'}
VERIFY={'DELETE':'VERIFY_RECORD_ABSENT','REDACT':'VERIFY_RECORD_REDACTED','ANONYMIZE':'VERIFY_RECORD_ANONYMIZED','RETAIN':'VERIFY_RECORD_PRESENT'}

@dataclass
class Decision:
    rule_id: str | None
    condition: str
    applicability: str
    policy_action: str | None
    treatment: str | None
    required_state: object
    observed_state: str
    remediation_required: bool | None
    verification_obligations: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    preserve: list = field(default_factory=list)

    def explain(self):return asdict(self)

class PolicyEngine:
    def __init__(self,path):
        self.rules=read_csv(path)
        self.by_category={r['data_category']:r for r in self.rules}
        if len(self.by_category)!=len(self.rules):raise ValueError('overlapping rules require explicit resolution')
        if any(r['required_action'] not in REQUIRED for r in self.rules):raise ValueError('unsupported policy action')

    @staticmethod
    def condition(category,fields,state,cutoff):
        def flag(key):
            return truth(fields.get(key))
        if category=='SUPPORT_MESSAGE':
            if 'shared_context' in fields:return flag('shared_context')
            return True if fields.get('order_reference') else None
        if category=='SUPPORT_ATTACHMENT':
            if type(fields.get('subject_count')) is int:return fields['subject_count']==1
            return flag('subject_only')
        if category in {'ANALYTICS_PROFILE','PRODUCT_TELEMETRY'}:
            if state=='IDENTIFIABLE':return True
            if state=='ANONYMIZED':return False
            return flag('attributable')
        if category=='EMAIL_DELIVERY_LOG':
            if 'subject_email_present' in fields:return flag('subject_email_present')
            emails={e.casefold() for key in ['email','recipient_email','customer_email'] for e in EMAIL.findall(str(fields.get(key,'')))}
            if emails and fields.get('_subject_identifiers'):
                return bool(emails & set(fields['_subject_identifiers']))
            if state=='REDACTED':return False
            return None
        if category=='SECURITY_AUDIT_LOG':
            end=fields.get('retention_until') or fields.get('retained_until')
            start=fields.get('retention_from')
            if start and cutoff<timestamp(start):return False
            return cutoff<=timestamp(end) if end else None
        if category=='LEGAL_HOLD_RECORD':
            if flag('hold_active') is False:return False
            end=fields.get('hold_until') or fields.get('retained_until')
            start=fields.get('hold_from')
            if start and cutoff<timestamp(start):return False
            if end and cutoff>timestamp(end):return False
            return True if flag('hold_active') is True or end else None
        if category=='BACKUP_ARCHIVE':return True if state=='BLOCKED' else flag('restore_block_supported')
        if category=='ACCOUNT_TOMBSTONE':
            deleted=fields.get('account_status')=='DELETED' or flag('account_deleted') is True
            if flag('account_deleted') is False:return False
            return deleted and flag('stable_reference_required') if deleted else None
        return None

    def evaluate(self,category,state,fields,cutoff):
        if category=='DATA_FLOW':
            known=state in {'ACTIVE','DISABLED'}
            return Decision(None,'Observed live process configuration','SATISFIED' if known else 'UNKNOWN',None,'FLOW' if known else None,
                'DISABLED',state,state=='ACTIVE' if known else None,['VERIFY_DATA_FLOW_DISABLED'],
                [] if known else ['PROCESS_STATE_UNKNOWN'])
        rule=self.by_category.get(category)
        if not rule:return Decision(None,'No matching rule','UNKNOWN',None,None,None,state,None,issues=['POLICY_RULE_MISSING'])
        action=rule['required_action'];condition=rule['condition'];issues=[]
        stored_attribution=direct_identifiers(fields) or any(is_value(fields.get(k)) for k in ['user_id','customer_reference'])
        contradicts=(category in {'ANALYTICS_PROFILE','PRODUCT_TELEMETRY'} and state=='ANONYMIZED' and stored_attribution)
        contradicts=contradicts or (category=='ACCOUNT_TOMBSTONE' and state=='REDACTED' and direct_identifiers(fields))
        if contradicts:
            return Decision(rule['rule_id'],condition,'UNKNOWN',action,None,REQUIRED[action],
                'CONFLICT',None,[VERIFY[action]],['POLICY_STATE_FACT_CONFLICT'])
        if condition=='Always':app=True
        elif condition!=CONDITIONS.get(category):app=None;issues.append('UNSUPPORTED_POLICY_CONDITION')
        else:
            try:app=self.condition(category,fields,state,cutoff)
            except (ValueError,TypeError):app=None;issues.append('INVALID_POLICY_CONDITION_FACT')
        applicability='SATISFIED' if app is True else 'NOT_APPLICABLE' if app is False else 'UNKNOWN'
        preserve=[]
        if category=='ACCOUNT_TOMBSTONE':preserve=['stable internal subject reference','references to required retained records']
        if category=='SUPPORT_MESSAGE':preserve=['shared customer/agent/order context','other subjects\u2019 identifiers']
        if action=='RETAIN':preserve=['entire policy-required retained record']
        # Already-treated redaction/anonymization still needs verification. Its
        # success does not remove the original policy obligation.
        already=(action=='ANONYMIZE' and state=='ANONYMIZED') or (action=='REDACT' and state=='REDACTED')
        if app is False and already and category in {'ANALYTICS_PROFILE','PRODUCT_TELEMETRY','EMAIL_DELIVERY_LOG'}:app=True;applicability='SATISFIED'
        if app is not True:
            issues.append('POLICY_CONDITION_UNKNOWN' if app is None else 'NO_APPLICABLE_TREATMENT')
            # Preserve retained records conservatively; expired/missing conditions
            # never introduce an unsupported DELETE fallback.
            if category=='BACKUP_ARCHIVE':
                return Decision(rule['rule_id'],condition,applicability,action,None,
                    {'archive':'PRESENT','restore_access':'BLOCKED'},state,None,
                    ['VERIFY_RECORD_PRESENT','VERIFY_RESTORE_BLOCKED'],issues,preserve)
            return Decision(rule['rule_id'],condition,applicability,action,None,
                'PRESENT' if action=='RETAIN' else None,state,None,
                ['VERIFY_RECORD_PRESENT'] if action=='RETAIN' else [],issues,preserve)
        if category=='BACKUP_ARCHIVE':
            return Decision(rule['rule_id'],condition,applicability,action,'RESTORE',
                {'archive':'PRESENT','restore_access':'BLOCKED'},state,
                state=='ACTIVE' if state in {'ACTIVE','BLOCKED'} else None,
                ['VERIFY_RECORD_PRESENT','VERIFY_RESTORE_BLOCKED'],
                [] if state in {'ACTIVE','BLOCKED'} else ['RESTORE_STATE_UNKNOWN'],preserve)
        required=REQUIRED[action]
        known=state not in {'UNKNOWN','CONFLICT'}
        remediation=known and state!=required
        if action=='RETAIN' and remediation:
            issues.append('RETAINED_RECORD_MISSING');remediation=None
        if action in {'REDACT','ANONYMIZE'} and state=='ABSENT':
            issues.append('REQUIRED_RECORD_MISSING');remediation=None
        return Decision(rule['rule_id'],condition,applicability,action,action,required,state,
                        remediation if known else None,[VERIFY[action]],issues,preserve)
