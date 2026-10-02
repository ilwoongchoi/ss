import geometry_package.absolute_constants as ac
from universal_decoder import UniversalDecoder, UniverseState
obs={'engineering_active':False,'closure_gain':0.3,'closure_controller':True,'controller_strength':0.6}
ac.TAU_BEAT=getattr(ac,'TAU_BEAT',1.0)
ac.TAU_BREATH=getattr(ac,'TAU_BREATH',1.0)

def run_case(score_threshold, max_steps):
    d=UniversalDecoder()
    s,h=d.run_until_closed(state=UniverseState(), score_threshold=score_threshold, max_steps=max_steps, observer_input=obs)
    err=s.closure_ledger.get('error', {})
    print(f"threshold={score_threshold} max_steps={max_steps} steps_taken={len(h)} final_closure_score_l2={s.closure_ledger.get('closure_score_l2')} closure_backoff={s.closure_backoff} errors={{barnard:{err.get('barnard')}, sun:{err.get('sun')}, earth:{err.get('earth')}, moon:{err.get('moon')}, comag:{err.get('comag')}}}")

run_case(0.03,256)
run_case(0.02,512)
