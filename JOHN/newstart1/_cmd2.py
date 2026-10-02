import geometry_package.absolute_constants as ac
from universal_decoder import UniversalDecoder, UniverseState
obs={'engineering_active':False,'closure_gain':0.3,'closure_controller':True,'controller_strength':0.6}
ac.TAU_BEAT=getattr(ac,'TAU_BEAT',1.0)
ac.TAU_BREATH=getattr(ac,'TAU_BREATH',1.0)
d=UniversalDecoder()
s=UniverseState()
for i in range(1,9):
    s=d.step(s, observer_input=obs)
    print(f"step={i} closure_score_l2={s.closure_ledger.get('closure_score_l2')}")
