import os, base64, math, emblem, wordmark as W, facets as F, dots as D
OUT=os.environ['OUT']; os.makedirs(OUT+'/svg',exist_ok=True)
FONT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','InterDisplay-SemiBoldItalic.otf')
TRACK=-22
STEEL='#C4D4E0'; IRON='#2E3A46'; NIGHT='#09090B'
# glyph index: h0 e1 m2 a3 t4 i5 t6 e7
def ladder(a=45, d=62):
    """cut sets at a base angle a (45 = like round 1). normals: top-left = 90+a, bottom-right = 270+a, top-right = 90-a, bottom-left = 270-a"""
    TL,BR,TR,BL=90+a,270+a,90-a,270-a
    L1={0:[(TL,d,(0,.5),(.7,1))],4:[(TL,d,None,(.6,1))],5:[(TL,d)],6:[(TL,d,None,(.6,1))]}
    L2={k:list(v) for k,v in L1.items()}
    L2[0]+= [(BR,d,(0,.45),(0,.3)),(BR,d,(.55,1),(0,.3))]
    L2[2]=[(BR,d,(0,.36),(0,.3)),(BR,d,(.36,.68),(0,.3)),(BR,d,(.68,1),(0,.3))]
    L2[3]=[(BR,d,(.6,1),(0,.3))]; L2[5]+= [(BR,d,None,(0,.3))]
    L3={k:list(v) for k,v in L2.items()}
    L3[0]+= [(TR,d*1.1,(.5,1),(.4,.8))]
    L3[1]=[(TR,d*1.1),(BL,d*1.1),(BR,d*0.9,(.5,1),(0,.4))]; L3[7]=list(L3[1])
    L3[2]+= [(TR,d*1.1,(.3,.66),(.5,1)),(TR,d*1.1,(.66,1),(.5,1)),(TL,d*0.9,(0,.36),(.5,1))]
    L3[3]+= [(TL,d*1.1,(0,.6),(.5,1)),(BL,d*1.1,(0,.5),(0,.5))]
    L3[4]+= [(BR,d,None,(0,.35))]; L3[6]+= [(BR,d,None,(0,.35))]
    L4={i:[(TL,d*1.2),(TR,d*1.2),(BR,d*1.2),(BL,d*1.2)] for i in range(8)}
    L4[0]+= [(BR,d*1.2,(0,.45),(0,.3))]; L4[2]+= [(BR,d*1.2,(0,.36),(0,.3)),(BR,d*1.2,(.36,.68),(0,.3))]
    return L1,L2,L3,L4
L1,L2,L3,L4=ladder()
_,_,L3s,_=ladder(22.5, 40)
_,_,L3t,_=ladder(67.5, 50)
L3t[2]=[f for f in L3t[2] if f[0] not in (157.5,337.5)]   # steep cuts run along the m's stems and eat them
VARS=[('C1','Round 1 cuts','Stem tops only (h, t, i), 45°.',L1),
      ('C2','+ feet','Stem feet too: h, m, a, i. Top and foot cuts are parallel.',L2),
      ('C3','+ curves','Facets on the e, a, m and h shoulders and the t hooks.',L3),
      ('C4','Faceted all round','Every letter cut on all four diagonals: crystal lettering.',L4),
      ('C5','C3 at 22.5°','Same cuts, shallow. Quieter, closer to type.',L3s),
      ('C6','C3 at 67.5°','Same cuts, steep: parallel to the emblem\'s cleft.',L3t)]
_n=[0]
def wm(facets, fg, dotfn=None, extra_i=None, lockup=False, embc=None, text='hematite', ii=5):
    _n[0]+=1; mid=f'm{_n[0]}'
    fc={k:list(v) for k,v in facets.items()}
    if extra_i: fc[ii]=fc.get(ii,[])+[extra_i]
    body,holes,dotd,w,Gl=F.build(text,FONT,TRACK,fc,dot=(lambda g,xh: dotfn(g)) if dotfn else None)
    g=''
    for j,(bd,hd) in enumerate(zip(body,holes)):
        if hd:
            m=f'{mid}g{j}'
            g+=f'<mask id="{m}" maskUnits="userSpaceOnUse" x="-300" y="-1500" width="{w+600}" height="3000"><rect x="-300" y="-1500" width="{w+600}" height="3000" fill="#fff"/><path d="{hd}" fill="#000"/></mask><path d="{bd}" fill="{fg}" mask="url(#{m})"/>'
        else:
            g+=f'<path d="{bd}" fill="{fg}"/>'
    g+=f'<path d="{dotd}" fill="{fg}"/>'
    TOP,BOT=800,60
    if not lockup:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 {-TOP} {w+80} {TOP+BOT+40}">{g}</svg>'
    sh=emblem.build('grid'); allp=[p for P in sh for p in P]; x0,y0,x1,y1=W.bbox(allp)
    eh=820; s=eh/(y1-y0); ew=(x1-x0)*s; gap=ew*0.36; yb=40
    em=f'<g transform="translate(0,{yb-eh:.1f}) scale({s:.4f}) translate({-x0:.2f},{-y0:.2f})" fill="{embc or fg}">'+''.join(f'<path d="{emblem.path(P)}"/>' for P in sh)+'</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 {yb-eh-60} {ew+gap+w+120} {eh+120}">{em}<g transform="translate({ew+gap:.1f},0)">{g}</g></svg>'
def save(n,s): open(f'{OUT}/svg/{n}.svg','w').write(s); return s
def img(svg,h): return f'<img style="max-height:{h}px;max-width:90%" src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}">'
# dot size: the font's dot height
Gl,_,_=F.layout('hematite',FONT,TRACK); gi=Gl[5]; H=gi['dot'][3]-gi['dot'][1]
DOT_DEFAULT=lambda g: D.place(D.unit_from_emblem([D.E2[0]]),g,H*1.55,shear=False)
css='''*{box-sizing:border-box}body{margin:0;background:#EEEEF0;font-family:Inter,system-ui,sans-serif;color:#151515;padding:44px}
h1{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}.sub{color:#666;font-size:14px;margin-bottom:34px}
.sec{background:#fff;border-radius:18px;padding:28px 30px;margin-bottom:26px}.sec h2{font-size:19px;margin:0 0 4px}.sec .d{font-size:13px;color:#777;margin-bottom:20px;max-width:1100px;line-height:1.45}
.row{display:flex;gap:14px;align-items:stretch;margin-bottom:14px}.card{border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.dark{background:#09090B}.light{background:#fff;border:1px solid #e3e3e6}.cap{position:absolute;left:12px;bottom:9px;font-size:11.5px;color:#8a8a92}.cap b{color:#d0d6dc;font-weight:600;margin-right:6px}
.lab{width:220px;flex:none;padding-top:6px}.lab b{display:block;font-size:15px;margin-bottom:4px}.lab span{font-size:12.5px;color:#777;line-height:1.4}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}'''
Hh=[f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><h1>hematite — round 2</h1><div class="sub">E2 emblem, B2 (Inter Display SemiBold Italic) with more cuts, and 16 i-dots. No ".gg" this round. 11 Nov 2026.</div>']
# 01 emblem
e=save('emblem-E2-steel', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><g fill="{STEEL}">'+''.join(f'<path d="{emblem.path(P)}"/>' for P in emblem.build("grid"))+'</g></svg>')
Hh.append(f'<div class="sec"><h2>01 — Emblem E2</h2><div class="d">The crystal-grid emblem, every edge on 22.5°. It sets the angles for the cuts below.</div><div class="row"><div class="card dark" style="flex:1;height:200px">{img(e,170)}</div><div class="card dark" style="flex:1;height:200px">{img(e,64)}&nbsp;&nbsp;&nbsp;{img(e,32)}&nbsp;&nbsp;&nbsp;{img(e,16)}</div></div></div>')
# 02 cuts
Hh.append('<div class="sec"><h2>02 — More cuts</h2><div class="d">C1–C4 add cuts step by step at 45°. C5 and C6 take C3\'s cuts to the other two angles of the emblem\'s grid. Left: the lockup with E2. Right: the wordmark large, to see the cuts.</div>')
for k,lab,txt,fc in VARS:
    a=save(f'cuts-{k}-lockup',wm(fc,STEEL,DOT_DEFAULT,lockup=True))
    b=save(f'cuts-{k}-wordmark',wm(fc,STEEL,DOT_DEFAULT))
    c=save(f'cuts-{k}-lockup-iron',wm(fc,IRON,DOT_DEFAULT,lockup=True))
    Hh.append(f'<div class="row"><div class="lab"><b>{k} · {lab}</b><span>{txt}</span></div><div class="card dark" style="flex:1;height:150px">{img(a,74)}</div><div class="card dark" style="flex:1.25;height:150px">{img(b,118)}</div><div class="card light" style="flex:1;height:150px">{img(c,74)}</div></div>')
Hh.append('</div>')
# 03 dots
Hh.append('<div class="sec"><h2>03 — i-dots</h2><div class="d">Sixteen dots, all on C3 so the cuts stay constant. D1–D4 come from the emblem; D5–D12 are crystal shapes (sheared with the italic where that helps); D13 and D14 make the dot the piece the cut took off the stem.</div><div class="grid">')
for key,lab,fn,extra in D.DOTS(H):
    s=save(f'idot-{key}',wm(L3,STEEL,fn,extra_i=extra))
    det=wm({0:L3[4],1:L3[5],2:L3[6],3:L3[7]},STEEL,fn,extra_i=extra,text='tite',ii=1)
    Hh.append(f'<div class="card dark" style="height:230px;flex-direction:column;gap:14px;padding-bottom:18px">{img(det,120)}{img(s,30)}<div class="cap"><b>{key}</b>{lab}</div></div>')
Hh.append('</div></div>')
# 04 dots small
Hh.append('<div class="sec"><h2>04 — The same dots at header size</h2><div class="d">Wordmark at 32 px tall, about where it will live in the app.</div><div class="grid">')
for key,lab,fn,extra in D.DOTS(H):
    s=wm(L3,STEEL,fn,extra_i=extra)
    Hh.append(f'<div class="card dark" style="height:76px">{img(s,32)}<div class="cap"><b>{key}</b></div></div>')
Hh.append('</div></div></body></html>')
open(f'{OUT}/board.html','w').write(''.join(Hh))
