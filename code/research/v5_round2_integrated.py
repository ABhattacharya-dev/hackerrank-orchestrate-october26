"""Research authorization layer over the unchanged frozen learned classifier.

No sample IDs, output labels or probe strings are consulted. Speech-act scope,
requester attribution and consent gates precede lexical/model classification.
"""
import re
from copy import deepcopy
from ghostgraph.intent import IntentClassifier,normalize

VERSION='authorization-scope-v5-research-2.1'
ERASURE=re.compile(r'\b(?:delet\w*|eras\w*|remov\w*|clos(?:e|ed|ing|ure)|erasure|right to be forgotten)\b',re.I)
OWN=re.compile(r'\b(?:my|own|this|personal|customer|account|profile|membership|registration)\b',re.I)
COMMAND=re.compile(r'^(?:(?:and|also|then|separately|instead|now)\s+)*(?:(?:can|could|would|will) you\s+)?(?:please\s+)?(?:permanently\s+)?(?:delete|erase|remove|close|process|begin|complete|finish|audit|verify|confirm|check|investigate|treat)\b',re.I)
SELF=re.compile(r'\b(?:i\s+(?:now\s+)?(?:want|wish|request|authorize|consent|ask|instruct|invoke|exercise|demand|adopt|confirm|would like|am requesting|am asking|am deleting|am erasing|am closing)|my instruction now is|this (?:message|request)\s+(?:is|repeats))\b',re.I)


def negative(clause):
    english=re.search(r"\b(?:do not|don't|dont|refuse|not asking|not requesting|without|never)\b",clause) and ERASURE.search(clause)
    english=english or re.search(r'\b(?:not|no)\s+(?:permission|consent|authoriz\w*)\b',clause)
    multilingual=any(re.search(p,clause) for p in [
        r'\bpas\s+(?:la\s+suppression|supprim\w*|effac\w*|fermer)',
        r'\bne\s+(?:supprim\w*|effac\w*|ferm\w*).{0,35}\bpas\b',
        r'\bno\s+(?:borren|borr\w*|eliminen|elimin\w*|solicito eliminar)',
        r'\bnão\s+(?:apag\w*|exclu\w*)',r'\bnicht\s+lösch\w*',
        r'削除しない|消去しない',r'삭제하지\s*마|지우지\s*마'])
    return bool(english or multilingual)


def affirmative(clause,context):
    if not ERASURE.search(clause):return False
    if not OWN.search(clause+' '+context):return False
    clause=re.sub(r'^if (?:possible|you can|you are able),?\s*','',clause)
    clause=re.sub(r'^(?:after|once)\b.{0,65}\b(?:export|download)\b[^,]*,\s*','',clause)
    return bool(COMMAND.search(clause.strip()) or re.search(r'\bthen\s+(?:permanently\s+)?(?:delete|erase|close)\b.{0,40}\b(?:my|this|the)\b',clause) or SELF.search(clause) or re.search(r'\bi\b.{0,70}\bwould like\b|\bthis repeats my (?:earlier|prior|previous) instruction\b',clause) or re.search(r'\b(?:account deletion|erasure) is authorized\b',clause))


class AuthorizationIntent:
    def __init__(self):
        self.base=IntentClassifier();self.cache={};self.cache_hits=0;self._scope_decisions=0
        self.training_hash=self.base.training_hash
    @property
    def scope_decisions(self):return self._scope_decisions+self.base.scope_decisions
    @property
    def calls(self):return self.base.calls
    @property
    def model(self):return self.base.model
    def classify(self,text):
        text=re.sub(r'\s+',' ',normalize(text)).strip().casefold()
        if text in self.cache:self.cache_hits+=1;return deepcopy(self.cache[text])
        decision,reason,evidence=self.decide(text)
        if isinstance(decision,dict):
            result=dict(decision);result['evidence']=evidence
            if result['low_confidence']:
                result['authorized']=False;result['ambiguous']=True
                result['decision_source']='uncertain frozen semantic fallback; authorization deferred'
        else:
            self._scope_decisions+=1
            result=dict(authorized=decision is True,probability=None,decision_source=reason,
                model='frozen local intent + '+VERSION,ambiguous=decision is None,low_confidence=decision is None,evidence=evidence)
        result['authorization_layer']=VERSION
        self.cache[text]=deepcopy(result)
        return deepcopy(result)
    def decide(self,text):
        quotes=re.findall(r'"([^"\n]+)"|“([^”\n]+)”',text)
        quoted=[''.join(q) for q in quotes]
        outside=re.sub(r'"[^"\n]+"|“[^”\n]+”',' ',text)
        endorsed=bool(quoted and re.search(r'\bi (?:confirm|adopt|authorize|endorse)\b',outside) and re.search(r'\b(?:my (?:own|instruction)|as my|this is my)\b',outside))
        clauses=[c.strip(' ,:-') for c in re.split(r'[.;!?]+|\b(?:but|however|instead|separately)\b',outside) if c.strip(' ,:-')]
        # Refer to input clauses rather than duplicating potentially sensitive text.
        evidence=[dict(source='request_text after normalization and quote masking',clause_index=i,negative=negative(c),affirmative=affirmative(c,outside)) for i,c in enumerate(clauses)]
        positive=[c for c in clauses if not negative(c) and affirmative(c,outside)]
        # Descriptive/inquiry speech is not an imperative embedded in it.
        inquiry=bool(re.search(r'\b(?:explain|explanation|how to|how do|how can|how would|information about|describe|consequences|before i (?:decide|choose|make a decision)|what (?:would happen|happens)|should i|will my)\b',outside))
        hypothetical=bool(re.search(r'\bif i\b.{0,55}\b(?:ever|someday|decid\w*|cho(?:ose|se)|opt|close|erase|delete)\b',outside))
        limited=[c for c in positive if re.search(r'\b(?:marketing|promotional|advertising|newsletter)\b',c) and not re.search(r'\b(?:delete|erase|close)\b.{0,35}\bmy (?:account|profile|personal)\b',c)]
        current=[c for c in positive if c not in limited if not re.search(r'\b(?:if|explain|explanation|how to|how do|how can|how would|information about|describe|consequences|before i|what happens|what would happen)\b',c)]
        third=bool(re.search(r"\b(?:another customer|someone else|as an observer|not my request|my (?:neighbor|neighbour|sister|brother|uncle|cousin|client|father|mother|friend)\b|their (?:account|profile)|his (?:account|profile)|her (?:account|profile))",outside))
        # Possessive head phrases may include modifiers; the foreign actor in
        # another clause must not own the requester's separate instruction.
        foreign_possessor=re.compile(r"\b(?:my\s+(?:own\s+)?[a-z]+(?:'s|’s)|another (?:person|customer|user)(?:'s|’s)?|their)\s+(?:[a-z]+\s+){0,3}(?:account|profile|membership|registration)\b")
        third=third or bool(foreign_possessor.search(outside))
        own_current=[c for c in current if re.search(r'\bmy (?:[a-z]+\s+){0,3}(?:account|profile|personal|membership|registration)\b',c) and not foreign_possessor.search(c)]
        if third and not own_current:
            delegated=bool(re.search(r'\b(?:authorized|verified|legal) (?:agent|representative)\b',outside))
            return (None if delegated else False),'third-party authority unverified' if delegated else 'third-party text does not authorize requester deletion',evidence
        if (hypothetical or inquiry) and not current:return False,'hypothetical/inquiry rather than current instruction',evidence
        # Confirmation gates are not satisfied by the imperative they qualify.
        condition=any(re.search(r'\b(?:if|only after|only once|once|until|unless)\b',c) and ERASURE.search(c) and not re.search(r'^(?:please )?(?:contact|let me know|send (?:a |me )?confirmation)',c) for c in clauses)
        procedural=bool(re.search(r'\b(?:export|download)\b',outside)) and not re.search(r'\b(?:if|confirm|approval|refund|parcel)\b',outside)
        polite=bool(re.search(r'\bif (?:possible|you can|you are able)\b',outside))
        legal=bool(re.search(r'\b(?:law|legally|retention|policy)\b',outside)) and not re.search(r'\b(?:i confirm|approval|refund|parcel)\b',outside)
        if condition and not (procedural or polite or legal):return None,'conditional consent not established as currently fulfilled',evidence
        cancellation=bool(re.search(r'\b(?:cancel|withdraw|rescind|revoke)\b.{0,55}\b(?:deletion|erasure|request to (?:close|erase|delete)|instruction)\b',outside))
        if cancellation and not own_current:return False,'erasure instruction cancelled',evidence
        temporary=bool(re.search(r'\b(?:temporar\w*|pause|suspend)\b',outside)) and bool(re.search(r'\b(?:account|profile|access|registration|membership)\b',outside))
        if temporary and not current:return False,'temporary access/deactivation preserves data',evidence
        if quoted and not endorsed and not current:
            if re.search(r'\b(?:translate|translation|render|summar\w*|quote|forwarded|ticket|sentence)\b',outside):return False,'quoted/forwarded content is not requester instruction',evidence
            return None,'unattributed quotation does not establish current consent',evidence
        if endorsed and any(ERASURE.search(q) and OWN.search(q) for q in quoted):return True,'requester explicitly adopts quoted own instruction',evidence
        account_refusal=any(negative(c) and re.search(r'\b(?:account|profile|membership|registration)\b',c) for c in clauses)
        account_request=any(re.search(r'\b(?:account|profile|membership|registration)\b',c) for c in current)
        if account_refusal and account_request and not re.search(r'\b(?:changed my mind|now (?:authorize|consent))\b',outside):
            return None,'contradictory consent for the same account scope',evidence
        if current or (polite and positive):return True,'unquoted current instruction; negation scoped to its own clause',evidence
        if limited:return False,'marketing-only scope does not authorize account erasure',evidence
        if any(negative(c) for c in clauses):return False,'explicit scoped refusal',evidence
        result=self.base.classify(outside)
        if result['authorized'] and result['decision_source']=='explicit erasure or completion/audit of prior erasure':
            return None,'erasure words without verified instruction frame',evidence
        return result,'frozen semantic fallback',evidence
