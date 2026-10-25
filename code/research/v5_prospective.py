"""Round-two prospective probes, frozen before ownership-scope correction.

First sealed evaluation exposed an adjective/third-party scope bug. Those first
40 probes are now observed regression for version two, never reported as unseen.
"""
PROSPECTIVE=[
 ('self_modifiers','My mother has a separate membership. Please erase my own online customer profile.',True,'self_scope'),
 ('self_active','I cannot authorize changes for my sister. Delete my active customer account.',True,'self_scope'),
 ('self_registered','My friend is keeping her registration. Permanently remove my registered personal profile.',True,'self_scope'),
 ('self_third_quote','A relative said "delete it". I now authorize erasure of my own business account.',True,'self_scope'),
 ('self_but','Do not change my uncle\'s details, but erase my own existing registration.',True,'self_scope'),
 ('foreign_coworker','Please erase my coworker\'s personal profile without asking them.',False,'third_party'),
 ('foreign_landlord','Remove my landlord\'s old customer account.',False,'third_party'),
 ('foreign_their','Delete their current personal profile; it is not my account.',False,'third_party'),
 ('foreign_another','Erase another person\'s registered account. I do not act for them.',False,'third_party'),
 ('delegated_client','I am a legal representative; remove my client\'s existing profile.',None,'third_party'),
 ('scoped_invoices','Do not delete the retained invoices. Please erase my own account and identifying data.',True,'negation'),
 ('scoped_export','Do not send me an export; erase my registered account now.',True,'negation'),
 ('same_scope_conflict','Do not erase my account. Delete my profile permanently.',None,'negation'),
 ('cancel_instruction','Revoke the instruction to erase my account and keep my membership.',False,'cancellation'),
 ('quote_summary','Summarize this example: "Delete my active account". It is not an instruction to act.',False,'quoted'),
 ('quote_endorse','I endorse the following as my instruction: "Erase my own profile permanently."',True,'quoted'),
 ('conditional_pending','Erase my profile only after I give approval; approval is still pending.',None,'conditional'),
 ('conditional_satisfied','The approval has been given. Please delete my own account now.',True,'conditional'),
 ('procedural_sequence','After providing my portable export, erase my registration permanently.',True,'export'),
 ('polite_request','If you are able, please close my own account permanently.',True,'conditional'),
 ('fr_scope','Je souhaite uniquement lire mes données, pas effacer mon profil.',False,'multilingual'),
 ('es_scope','No borren mi perfil; solo necesito una copia de mis datos.',False,'multilingual'),
 ('fr_current','Veuillez supprimer mon compte et mes données personnelles définitivement.',True,'multilingual'),
 ('ko_scope','계정을 삭제하지 마세요. 전화번호만 바꿔 주세요.',False,'multilingual'),
]
