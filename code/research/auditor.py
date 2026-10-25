"""Experimental wrapper; never changes the production exporter or frozen files."""
from copy import copy
from ghostgraph.prediction import PredictionAuditor
from ghostgraph.contract import timestamp
from .linkage import graph

class ResearchAuditor(PredictionAuditor):
    def __init__(self,*args,graph_enabled=False,temporal_links=None):
        super().__init__(*args);self.graph_enabled=graph_enabled;self.temporal_links=temporal_links or {}
    def audit(self,request):
        original=self.store
        nodes,rejected=graph(original,self.identity,request,reverse=self.graph_enabled)
        tokens,uid,_=self.identity.resolve(request['email'],timestamp(request['audit_at']))
        scoped=copy(original);scoped.links=list(original.links)
        additions=[]
        allowed=set(nodes) if self.graph_enabled else set()
        temporal_proofs={}
        for link in self.temporal_links.get(request['case_id'],[]):
            if link['stage']=='corroborated_derived':
                key=link['system_id'],link['resource_id'];allowed.add(key)
                temporal_proofs[key]=dict(stage='corroborated_derived',available=link['available'],proofs=link['proofs'])
        for key in allowed:
            proof=nodes.get(key) or temporal_proofs.get(key)
            if proof and proof['stage']=='corroborated_derived':
                scoped.links.append((proof['available'],key[0],key[1],set(tokens),proof['proofs'][-1]['evidence_id']))
                additions.append(dict(system=key[0],resource=key[1],**proof,uncertainty='corroborated relationship, not state proof; structured copy semantics require review'))
        self.store=scoped
        try:row,diagnostic=super().audit(request)
        finally:self.store=original
        diagnostic['v3_graph_links']=additions
        diagnostic['v3_graph_rejections']=rejected
        return row,diagnostic
