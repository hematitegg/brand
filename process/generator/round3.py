import os, sys, tempfile
OUT=os.environ['OUT']
os.environ['OUT']=tempfile.mkdtemp()   # round2 builds its own board on import; keep that out of this folder
import round2 as R, dots as D
os.environ['OUT']=OUT; os.makedirs(OUT+'/svg',exist_ok=True)
STEEL,IRON=R.STEEL,R.IRON
def save(n,s): open(f'{OUT}/svg/{n}.svg','w').write(s); return s
DEPTHS=[('light',45,'Lighter cuts, depth 45'),('base',62,'As in round 2, depth 62'),('strong',80,'Deeper cuts, depth 80')]
Hh=[f'<html><head><meta charset="utf-8"><style>{R.css}</style></head><body><h1>hematite — round 3</h1><div class="sub">E2 emblem, B2 with C2 cuts (stem tops and feet, 45°). How deep the cuts go, and the sixteen i-dots again, now on C2. 11 Nov 2026.</div>']
Hh.append('<div class="sec"><h2>01 — C2 cut depth</h2><div class="d">Same cuts, three depths (font units; the stems are about 100 wide). Lockup on dark and white, and the wordmark large.</div>')
for k,d,txt in DEPTHS:
    L2=R.ladder(45,d)[1]
    a=save(f'c2-{k}-lockup',R.wm(L2,STEEL,R.DOT_DEFAULT,lockup=True)); b=save(f'c2-{k}-wordmark',R.wm(L2,STEEL,R.DOT_DEFAULT)); c=save(f'c2-{k}-lockup-iron',R.wm(L2,IRON,R.DOT_DEFAULT,lockup=True))
    Hh.append(f'<div class="row"><div class="lab"><b>C2 · {k}</b><span>{txt}</span></div><div class="card dark" style="flex:1;height:150px">{R.img(a,74)}</div><div class="card dark" style="flex:1.25;height:150px">{R.img(b,118)}</div><div class="card light" style="flex:1;height:150px">{R.img(c,74)}</div></div>')
Hh.append('</div>')
L2=R.ladder(45,62)[1]
Hh.append('<div class="sec"><h2>02 — i-dots on C2</h2><div class="d">The sixteen dots from round 2, now with C2\'s cuts. Large: "tite"; small: the whole word at 30 px.</div><div class="grid">')
for key,lab,fn,extra in D.DOTS(R.H):
    s=save(f'idot-{key}',R.wm(L2,STEEL,fn,extra_i=extra))
    det=R.wm({0:L2[4],1:L2[5],2:L2[6]},STEEL,fn,extra_i=extra,text='tite',ii=1)
    Hh.append(f'<div class="card dark" style="height:230px;flex-direction:column;gap:14px;padding-bottom:18px">{R.img(det,120)}{R.img(s,30)}<div class="cap"><b>{key}</b>{lab}</div></div>')
Hh.append('</div></div>')
Hh.append('<div class="sec"><h2>03 — Dots in the lockup, on white</h2><div class="d">Iron on white, to check each dot against the emblem.</div><div class="grid">')
for key,lab,fn,extra in D.DOTS(R.H):
    s=R.wm(L2,IRON,fn,extra_i=extra,lockup=True)
    Hh.append(f'<div class="card light" style="height:110px">{R.img(s,52)}<div class="cap" style="color:#999"><b style="color:#2E3A46">{key}</b></div></div>')
Hh.append('</div></div></body></html>')
open(f'{OUT}/board.html','w').write(''.join(Hh))
