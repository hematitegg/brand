"""Round 5: two-tone variants. Emblem and wordmark in separate colours; the i-dot follows the emblem or the wordmark."""
import os, base64
import final as FN
OUT=os.environ['OUT']; os.makedirs(OUT+'/svg',exist_ok=True)
C=dict(steel='#C4D4E0', iron='#2E3A46', haze='#8A9BAB', slate='#5F7385', white='#FFFFFF', zinc400='#A1A1AA', zinc500='#71717A',
       zinc900='#18181B', streak='#C0503F', streakdeep='#A33A2C')
NIGHT='#09090B'
NAMES=dict(steel='steel',iron='iron',haze='haze',slate='slate',white='white',zinc400='zinc-400',zinc500='zinc-500',zinc900='zinc-900',streak='streak',streakdeep='streak (deep)')
letters,dot,_=FN.wordmark_parts()
E=FN.emblem_polys('grid'); ex0,ey0,ex1,ey1=FN.bbox(E); s=820/(ey1-ey0); ew=(ex1-ex0)*s
EH=FN.transform(E,s,-ex0*s,-ey0*s-40); gap=ew*0.36
LET=FN.transform(letters,1,ew+gap,0); DOT=FN.transform(dot,1,ew+gap,0)
ALL=EH+LET+DOT
def lockup(em, wm, dt, wordmark_only=False):
    polys=(LET+DOT) if wordmark_only else ALL
    x0,y0,x1,y1=FN.bbox(polys)
    parts=([] if wordmark_only else [(EH,em)])+[(LET,wm),(DOT,dt)]
    body=''.join(f'<path d="{FN.to_d(p)}" fill="{c}"/>' for p,c in parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {-y1:.1f} {x1-x0:.1f} {y1-y0:.1f}">{body}</svg>'
def save(n,s): open(f'{OUT}/svg/{n}.svg','w').write(s); return s
def img(s,h): return f'<img style="max-height:{h}px;max-width:86%" src="data:image/svg+xml;base64,{base64.b64encode(s.encode()).decode()}">'
DARK=[('T1','steel','white'),('T2','white','steel'),('T3','steel','haze'),('T4','haze','steel'),('T5','steel','zinc400'),('T6','haze','white'),('T7','streak','steel'),('T8','streak','white')]
LIGHT=[('L1','iron','zinc900'),('L2','slate','iron'),('L3','iron','slate'),('L4','haze','iron'),('L5','streakdeep','iron'),('L6','iron','zinc500')]
ACCENT=[('A1','steel','white','dark'),('A2','white','steel','dark'),('A3','steel','streak','dark'),('A4','iron','slate','light'),('A5','iron','streakdeep','light'),('A6','slate','iron','light')]
css='''*{box-sizing:border-box}body{margin:0;background:#EEEEF0;font-family:Inter,system-ui,sans-serif;color:#151515;padding:44px}
h1{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}.sub{color:#666;font-size:14px;margin-bottom:34px;max-width:1100px;line-height:1.45}
.sec{background:#fff;border-radius:18px;padding:28px 30px;margin-bottom:26px}.sec h2{font-size:19px;margin:0 0 4px}.sec .d{font-size:13px;color:#777;margin-bottom:20px;max-width:1100px;line-height:1.45}
.row{display:flex;gap:14px;align-items:stretch;margin-bottom:14px}.card{border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex:1;height:130px}
.dark{background:#09090B}.light{background:#fff;border:1px solid #e3e3e6}.cap{position:absolute;left:12px;bottom:9px;font-size:11px;color:#8a8a92}
.lab{width:210px;flex:none;padding-top:4px}.lab b{display:block;font-size:15px;margin-bottom:4px}.lab span{font-size:12.5px;color:#777;line-height:1.4}
.chip{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px;border:1px solid rgba(0,0,0,.12)}'''
def chips(*ks): return ' '.join(f'<span class="chip" style="background:{C[k]}"></span>{NAMES[k]}' for k in ks)
H=[f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><h1>hematite — round 5: two-tone</h1><div class="sub">The locked logo (E2 · B2 · C2 light · S6) with the emblem and the wordmark in separate colours. In each row: the i-dot in the emblem\'s colour, then in the wordmark\'s, then the wordmark alone at header size. New colours for this round: slate #5F7385 (4.9:1 on white) and streak #C0503F / #A33A2C (the mineral\'s red powder). 11 Nov 2026.</div>']
for title,desc,rows,bg in (('01 — On dark','Night #09090B.',DARK,'dark'),('02 — On light','White.',LIGHT,'light')):
    H.append(f'<div class="sec"><h2>{title}</h2><div class="d">{desc}</div>')
    for k,em,wm in rows:
        a=save(f'{k}-{em}-{wm}-dot-emblem',lockup(C[em],C[wm],C[em])); b=save(f'{k}-{em}-{wm}-dot-wordmark',lockup(C[em],C[wm],C[wm]))
        w=lockup(C[em],C[wm],C[em],wordmark_only=True)
        H.append(f'<div class="row"><div class="lab"><b>{k}</b><span>emblem {chips(em)}<br>wordmark {chips(wm)}</span></div><div class="card {bg}">{img(a,60)}<div class="cap">dot = emblem</div></div><div class="card {bg}">{img(b,60)}<div class="cap">dot = wordmark</div></div><div class="card {bg}" style="flex:.55">{img(w,26)}<div class="cap">wordmark, dot = emblem</div></div></div>')
    H.append('</div>')
H.append('<div class="sec"><h2>03 — Accent dot only</h2><div class="d">Emblem and letters stay one colour; only the i-dot changes.</div>')
for i in range(0,len(ACCENT),3):
    cells=''
    for k,base,dt,bg in ACCENT[i:i+3]:
        s_=save(f'{k}-{base}-dot-{dt}',lockup(C[base],C[base],C[dt]))
        cells+=f'<div class="card {bg}">{img(s_,56)}<div class="cap">{k} · {NAMES[base]}, dot {NAMES[dt]}</div></div>'
    H.append(f'<div class="row">{cells}</div>')
H.append('</div></body></html>')
open(f'{OUT}/board.html','w').write(''.join(H))
