import os, tempfile, base64
OUT=os.environ['OUT']; os.environ['OUT']=tempfile.mkdtemp()
import round2 as R, dots as D, shards as SH
os.environ['OUT']=OUT; os.makedirs(OUT+'/svg',exist_ok=True)
STEEL,IRON=R.STEEL,R.IRON
L2=R.ladder(45,45)[1]          # C2 light
SIZE=1.22                       # D2 was 1.45x the font's dot
def save(n,s): open(f'{OUT}/svg/{n}.svg','w').write(s); return s
def dotfn(polys,k=SIZE): return lambda g: D.place(polys,g,R.H*k,shear=False)
def shape_svg(polys):
    d=''.join('M'+' L'.join(f'{x:.4f},{-y:.4f}' for x,y in P)+'Z' for P in polys)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-0.6 -0.56 1.2 1.12"><path d="{d}" fill="{STEEL}"/></svg>'
items=[('D2','round 3 reference (E2 shard, 1.45x)',D.unit_from_emblem([D.E2[1]]),1.45)]+[(k,l,SH.shard(**kw),SIZE) for k,l,kw in SH.SHARDS]
H=[f'<html><head><meta charset="utf-8"><style>{R.css}.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}</style></head><body><h1>hematite — round 4</h1><div class="sub">Locked: E2 emblem, B2 wordmark, C2 light cuts. New shard i-dots in the spirit of D2, drawn fresh and a little smaller. 11 Nov 2026.</div>']
H.append('<div class="sec"><h2>01 — Shard i-dots</h2><div class="d">Each shard is cut only by facets on the 22.5° grid, like a grown crystal. Left in each card: the shard alone. Right: "tite" close-up and the whole word at 30 px. All at 1.22× the font\'s dot (D2 was 1.45×).</div><div class="grid3">')
for k,lab,polys,sz in items:
    a=save(f'shard-{k}',shape_svg(polys))
    det=R.wm({0:L2[4],1:L2[5],2:L2[6]},STEEL,dotfn(polys,sz),text='tite',ii=1)
    w=save(f'wordmark-{k}',R.wm(L2,STEEL,dotfn(polys,sz)))
    H.append(f'<div class="card dark" style="height:240px;gap:22px;padding:0 18px 16px"><div style="width:90px;display:flex;justify-content:center">{R.img(a,86)}</div><div style="display:flex;flex-direction:column;align-items:center;gap:14px;flex:1">{R.img(det,118)}{R.img(w,30)}</div><div class="cap"><b>{k}</b>{lab}</div></div>')
H.append('</div></div>')
H.append('<div class="sec"><h2>02 — In the lockup</h2><div class="d">With the E2 emblem, steel on night and iron on white.</div><div class="grid3">')
for k,lab,polys,sz in items:
    a=save(f'lockup-{k}',R.wm(L2,STEEL,dotfn(polys,sz),lockup=True)); b=save(f'lockup-{k}-iron',R.wm(L2,IRON,dotfn(polys,sz),lockup=True))
    H.append(f'<div style="display:flex;flex-direction:column;gap:8px"><div class="card dark" style="height:100px">{R.img(a,50)}<div class="cap"><b>{k}</b></div></div><div class="card light" style="height:100px">{R.img(b,50)}</div></div>')
H.append('</div></div></body></html>')
open(f'{OUT}/board.html','w').write(''.join(H))
