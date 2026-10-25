"""Round-three prospective continuation probes, authored before correction.
These cover speech-act classes exposed by the public regression; they are not
independent evidence that those classes were discovered without public feedback.
"""
PROBES=[
 ('audit_earlier','I previously erased my membership. Please verify no personal records remain.',True),
 ('audit_inspect','My erasure request was rejected. Inspect whether my profile has already been removed.',True),
 ('audit_address','I changed my contact address before deleting my profile. Check for leftover copies.',True),
 ('residual','I was told my registration was deleted. Please handle the residual copies.',True),
 ('retained_ref','Please remove my identifying details, but keeping a stable reference is fine if dependent records require it.',True),
 ('limited_reference','My deleted membership still holds personal information. Keep only the required reference and remove everything else.',True),
 ('inquiry_prior','I previously erased my membership. How would verification work?',False),
 ('foreign_audit','My landlord erased his account. Please inspect his residual records.',False),
 ('cancel_audit','I previously requested deletion. Cancel the erasure instruction; do not delete my profile.',False),
 ('conditional_audit','Verify my profile is erased only after I give approval.',None),
 ('negative_scope','Keep the invoice if policy needs it. Erase my customer profile.',True),
 ('retention_not_consent','If I agree later, remove my name but keep the required reference.',None),
 ('quoted_audit','Translate "I deleted my account; inspect the residual copies" into Dutch.',False),
 ('future_audit','If I someday delete my profile, how can I audit it?',False),
 ('access_audit','Inspect my profile and send me a copy. I am not requesting erasure.',False),
 ('retention_question','Would you keep only an internal reference if I requested deletion?',False),
]
