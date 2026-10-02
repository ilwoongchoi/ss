import pandas as pd
import numpy as np

df = pd.read_csv('FACE_FIELD_MAP.csv')
uniq = np.unique(df['score'].round(6))
print(len(uniq), 'unique scores')
print('first', uniq[:20])
print('last', uniq[-20:])
known = {0,0.0012,0.0067,0.012,0.01812,0.018359,0.018802,0.019245,0.020520,0.020958,0.021392,0.024117,0.02779,0.02887,0.029,0.0297,0.031}
others = [s for s in uniq if not any(abs(s-k)<1e-6 for k in known)]
print('other count', len(others))
# focus on nose region
nose = df[(df.x>=4)&(df.x<=12)&(df.y>=7)&(df.y<=14)]
nose_scores = np.unique(nose['score'].round(6))
print('nose unique scores', len(nose_scores))
print(nose_scores[:50])
print('sample points for nose scores not in known:')
for s in nose_scores:
    if not any(abs(s-k)<1e-6 for k in known):
        pts = nose[np.isclose(nose['score'], s, atol=1e-9)][['x','y']]
        print('score', s, 'count', len(pts), 'examples', pts.head().to_dict('records'))# light stress outside nose? find score around 0.012 with y<7 or x<4 or x>12
ls = df[np.isclose(df['score'],0.012,atol=5e-3)]
outs = ls[(ls.y<7)|(ls.x<4)|(ls.x>12)]
print('light stress candidates outside nose:', len(outs))
print(outs[['x','y','score']].head(20))