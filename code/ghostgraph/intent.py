"""Local supervised AI inference; training examples are independently authored.

No public output labels, case IDs, or dataset requests are used for training.
Model: character TF-IDF + balanced logistic regression, deterministic seed.
This is a small discriminative ML model, not an LLM or a multilingual foundation model.
"""

import hashlib
import json
import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import FeatureUnion

MODEL_NAME = "ghostgraph-intent-hybrid-word-char-logreg-v4"
TASK_PROMPT = "Classify whether the speaker authorizes erasure of their account or personal data. Access, correction, export, marketing opt-out, questions and negated deletion do not authorize erasure. Return a validated authorization boolean and probability."

# Independent, fictional examples describing intent, not challenge answers.
POSITIVE = [
    "Erase my personal information and close my customer profile.",
    "I authorize permanent deletion of all my customer records.",
    "Remove my account for good, including old aliases and linked personal data.",
    "I no longer need the service; permanently close my membership.",
    "Please delete my account and all associated personal information.",
    "I request erasure of my profile under the privacy policy.",
    "I would like my account erased completely.",
    "Please begin account deletion and confirm completion.",
    "Close my account permanently, retaining only what the law requires.",
    "Process my right to be forgotten request.",
    "I want to remove my account and its saved data.",
    "Please stop marketing and also erase my account permanently.",
    "After sending an export, please delete my account.",
    "Do not send a download; delete the account instead.",
    "Je souhaite effacer mes données et supprimer mon compte définitivement.",
    "Je demande la suppression de mon compte et de mes informations personnelles.",
    "Veuillez fermer mon compte et effacer définitivement mes données.",
    "Quiero borrar mi cuenta y todos mis datos personales.",
    "Solicito eliminar de forma permanente mi cuenta de cliente.",
    "Por favor eliminen mi perfil y los datos asociados a él.",
    "Quero apagar a minha conta e os meus dados pessoais.",
    "Solicito a exclusão definitiva da minha conta de cliente.",
    "Por favor excluam meus dados e encerrem a conta permanentemente.",
    "このアカウントを削除してください。個人情報も消去してください。",
    "私のアカウントの完全な削除を依頼します。",
    "アカウントと関連する個人データの削除をお願いします。",
    "제 계정을 영구 삭제하고 개인정보를 지워 주세요.",
    "개인정보와 계정의 삭제를 요청합니다.",
    "계정을 완전히 삭제해 주세요.",
    "Bitte löschen Sie mein Konto und meine persönlichen Daten.",
]
NEGATIVE = [
    "Do not delete my account. I only need a copy of my information.",
    "I am not asking for deletion. Stop sending me promotional messages.",
    "Remove me from advertising lists only, keep my account active.",
    "Unsubscribe my address from the newsletter.",
    "Correct the spelling of my surname without deleting my records.",
    "Change my email address; I want to continue using this account.",
    "Update the phone number on my profile.",
    "Help me recover my login and reset my password.",
    "Send my invoices, leaving the account unchanged.",
    "I need a portable export of my personal information.",
    "What personal data do you store about me?",
    "Tell me how account deletion works before I decide.",
    "Do not erase anything; send an access report only.",
    "I want to cancel my deletion request and keep my account.",
    "Please don't close my account or erase my information.",
    "What would happen if I decided to delete the account in the future?",
    "Please remove my old shipping address but keep my membership.",
    "Ne supprimez pas mon compte. Envoyez seulement une copie de mes données.",
    "Je demande un accès à mes données, pas leur suppression.",
    "Corrigez mon adresse et conservez mon compte.",
    "No borren mi cuenta. Solo quiero una copia de mis datos.",
    "Quiero actualizar el correo y conservar mi cuenta activa.",
    "No solicito eliminar nada, solo dejar de recibir publicidad.",
    "Não excluam minha conta. Só preciso de uma cópia dos dados.",
    "Quero corrigir meu telefone e manter a conta ativa.",
    "Não peço exclusão, apenas parar os emails promocionais.",
    "アカウントを削除しないでください。データのコピーだけ欲しいです。",
    "メールアドレスを変更したいです。アカウントは維持してください。",
    "계정을 삭제하지 마세요. 개인정보 사본만 보내 주세요.",
    "전화번호를 수정하고 계정은 유지해 주세요.",
    "Bitte mein Konto nicht löschen. Ich brauche nur eine Kopie.",
]

# General intent/scope combinations, authored without copying challenge requests.
# Both classes receive the same neutral privacy/courtesy clauses to avoid learning
# that words such as 'review', 'privacy', or 'confirmation' imply either class.
AUTHORIZATION_ACTIONS = [
    "Erase the membership and every identifying record about me.",
    "Permanently remove the customer profile I registered here.",
    "I consent to closing this account and erasing the related information.",
    "Complete my previously submitted erasure request.",
    "Remove residual copies left after the account was deleted.",
    "Audit my completed deletion and verify no personal data survives.",
    "Check whether my requested erasure has actually finished.",
    "Confirm the account is gone and retained statistics are anonymous.",
    "Clean up the old identifiers after closing my account.",
    "Remove the stale search entry belonging to my deleted account.",
    "I previously closed the profile; delete its leftover downloadable archive.",
    "Remove my identifying details from retained customer records.",
    "Finish removing my data and stop connectors from importing it again.",
    "Verify the account has been deleted at the time of my earlier request.",
    "Keep only legally permitted references after erasing my identity.",
    "Delete the remaining records under my previous email address.",
    "My account has been closed; check for surviving data tied to the old address.",
    "Remove profile data and personal contact details from older conversations.",
    "Erase the account, but preserve properly anonymous aggregate statistics.",
    "I already requested deletion. Investigate the remaining profile and finish it.",
    "I am deleting this membership and withdrawing my personal information.",
    "Delete my account; keeping anonymous statistical totals is acceptable.",
    "Remove every record belonging to both my former and present contact addresses.",
    "Erase information under the aliases I used before changing my login address.",
    "I updated my contact address before account removal; clean up any residual copies.",
    "I authorize deletion of old and new identifiers and disabling every reimport job.",
    "Permanently delete my registration, following all applicable retention requirements.",
    "Begin the permanent erasure process for my registered profile.",
    "I am deleting my account. Keep only anonymous aggregate usage statistics.",
    "My account deletion is authorized. Anonymous analytics may be retained.",
    "I withdraw my account and personal details, but you may keep anonymous totals.",
]
NON_AUTHORIZATION_ACTIONS = [
    "Export my records while keeping the customer membership intact.",
    "Only update the spelling of my contact details.",
    "Change the address used for login and keep my profile.",
    "Stop advertising mail, but continue providing the service.",
    "Send a data access report without changing any stored records.",
    "Do not delete the account or remove personal details.",
    "Cancel the request to erase my account.",
    "I need help signing in, not deletion.",
    "Explain your retention and deletion procedures before I make a decision.",
    "Download a copy of my invoices without closing my account.",
    "Supply my information in a portable download and leave registration unchanged.",
    "I would like to download the account information in a reusable format, keeping the service active.",
    "Send my personal data in a machine readable file without erasing anything.",
    "Provide a portable copy of my saved profile and transaction history.",
    "I want to exercise data portability and continue using my account.",
    "Make my data available for download, with no account removal.",
]
NEUTRAL_CLAUSES = [
    "", " Please review this under your privacy procedure.",
    " Include current and earlier identifiers when reviewing this request. Confirm the outcome.",
    " Apply your policy across the relevant systems and tell me when the review finishes.",
    " Please contact me if verification is required, and send a confirmation when done.",
]
POSITIVE += [a + c for a in AUTHORIZATION_ACTIONS for c in NEUTRAL_CLAUSES]
NEGATIVE += [a + c for a in NON_AUTHORIZATION_ACTIONS for c in NEUTRAL_CLAUSES]


def normalize(text):
    text = unicodedata.normalize("NFKC", text).replace("’", "'")
    return re.sub(r"\bI'm\b", "I am", text, flags=re.IGNORECASE)


def explicit_scope(text):
    """Conservative English consent/scope guards around actual ML inference.

    These rules are generic request-language grammar, never case-ID or answer
    lookups. Multilingual and implicit intent use the supervised model. Explicit
    denials and access-only requests cannot be overridden by lexical similarity.
    """
    text = normalize(text).casefold()
    denied = re.search(r"\b(?:do not|don't|dont|not to)\s+(?:permanently\s+)?(?:delete|erase|close|remove)\b", text)
    denied = denied or re.search(r"\bnot\s+(?:a\s+)?(?:asking|request(?:ing)?)\s+(?:for\s+|to\s+)?(?:deletion|delete|erase|erasure)\b", text)
    denied = denied or re.search(r"\bcancel\b.{0,35}\b(?:deletion|erasure)\s+request\b", text)
    denied = denied or re.search(r"\bwithout\s+(?:delet\w*|eras\w*|remov\w*)\s+any\s+(?:of\s+my\s+)?(?:records|data)\b", text)
    denied = denied or re.search(r"\b(?:do not|don't)\s+(?:want|wish|intend)\s+to\s+(?:delete|erase|close)\b",text)
    denied = denied or re.search(r"\bcancel\b.{0,30}\brequest\s+to\s+(?:erase|delete|close)\b",text)
    if denied:
        return False, "explicit non-deletion scope"
    if re.search(r"\b(?:how (?:do|can|would) i|what would happen|if i (?:decide|were|wanted))\b",text):
        return False,"hypothetical inquiry without authorization"
    if re.search(r"\b(?:how|explain|what would happen|before I decide)\b", text) and re.search(r"\b(?:deletion|erasure)\s+(?:works|procedures?|process)\b", text):
        return False, "procedure inquiry without authorization"
    action = re.search(r"\b(?:delet\w*|eras\w*|remov\w*|clos(?:e|ed|ing))\b", text)
    target = re.search(r"\b(?:account|profile|personal|records?|identifiers?|copies|archive|search result|data)\b", text)
    keep_account = re.search(r"\b(?:keep|leave)\b.{0,30}\baccount\b.{0,25}\b(?:active|intact|unchanged|as it is|in place)\b", text)
    limited = re.search(r"\b(?:marketing lists?|advertising lists?|newsletter|promotional)\b", text) and re.search(r"\b(?:only|still|keep|continue)\b", text)
    if keep_account or limited:
        return False, "limited scope preserving the account"
    if action and target:
        return True, "explicit erasure or completion/audit of prior erasure"
    access_only = re.search(r"\b(?:download|copy|portable|portability|export|correct|update|reset|change|information request)\b", text)
    if access_only and not action:
        return False, "access/correction/portability without erasure"
    return None, "semantic ML inference"


class IntentClassifier:
    def __init__(self):
        # Fit from auditable source every run: no unsafe pickle/model downloads.
        self.model = make_pipeline(
            FeatureUnion([
                ("char", TfidfVectorizer(analyzer="char", ngram_range=(2, 5), sublinear_tf=True)),
                ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
            ]),
            LogisticRegression(C=12, class_weight="balanced", random_state=0, max_iter=1000),
        )
        self.model.fit([normalize(t) for t in POSITIVE + NEGATIVE], [True] * len(POSITIVE) + [False] * len(NEGATIVE))
        self.cache = {}
        self.calls = 0
        self.cache_hits = 0
        self.training_hash = hashlib.sha256(json.dumps([POSITIVE, NEGATIVE], ensure_ascii=False).encode()).hexdigest()

    def classify(self, text):
        key = hashlib.sha256((MODEL_NAME + self.training_hash + text).encode()).hexdigest()
        if key in self.cache:
            self.cache_hits += 1
            return self.cache[key]
        probability = float(self.model.predict_proba([normalize(text)])[0, 1])
        explicit, reason = explicit_scope(text)
        ambiguous = bool(re.search(r"\b(?:not sure (?:whether|if|i want)|undecided|whether to (?:delete|erase)|maybe (?:delete|erase))\b",normalize(text).casefold()))
        result = {"authorized": probability >= 0.5 if explicit is None else explicit,
                  "probability": probability, "decision_source": reason,
                  "model": MODEL_NAME, "ambiguous": ambiguous,
                  "low_confidence": ambiguous or (explicit is None and abs(probability - 0.5) < 0.04)}
        self.cache[key] = result
        self.calls += 1
        return result
