import os, board as B
OUT=os.environ['OUT']; os.makedirs(OUT+'/svg',exist_ok=True)
files={}
def save(name, svg):
    open(f'{OUT}/svg/{name}.svg','w').write(svg); files[name]=svg; return svg
def img(svg, h, extra=''):
    import base64
    return f'<img style="max-height:{h}px;max-width:88%;{extra}" src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}">'
css='''*{box-sizing:border-box}body{margin:0;background:#EEEEF0;font-family:Inter,system-ui,sans-serif;color:#151515;padding:44px}
h1{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}.sub{color:#666;font-size:14px;margin-bottom:34px}
.sec{background:#fff;border-radius:18px;padding:28px 30px;margin-bottom:26px}.sec h2{font-size:19px;margin:0 0 4px}.sec .d{font-size:13px;color:#777;margin-bottom:20px}
.row{display:flex;gap:14px;align-items:stretch;margin-bottom:14px}.card{border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.dark{background:#09090B}.light{background:#fff;border:1px solid #e3e3e6}.cap{position:absolute;left:12px;bottom:9px;font-size:11px;color:#888}
.lab{width:230px;flex:none;padding-top:6px}.lab b{display:block;font-size:15px;margin-bottom:4px}.lab span{font-size:12.5px;color:#777;line-height:1.4}
.tag{display:inline-block;font-size:11px;background:#EEF2F6;color:#3A4856;border-radius:20px;padding:2px 9px;margin-top:8px}'''
H=[f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>',
   '<h1>hematite.gg — round 1</h1><div class="sub">Emblem clean-up and six wordmark directions. Flat only. Steel #C4D4E0 on night #09090B, iron #2E3A46 on white, haze #8A9BAB for ".gg". 11 Nov 2026.</div>']
# 01 emblem
H.append('<div class="sec"><h2>01 — Emblem</h2><div class="d">E0 is today\'s mark with the 3 px stroke baked in (identical look). E1 keeps the silhouette but makes the cleft exactly 45° / 67.5° with a constant gap. E2 snaps every edge to a 22.5° grid: more crystal, less hand-cut. Real sizes on the right: 64, 32, 16 px.</div>')
for k,lab,txt in [('current','E0 · Today, stroke baked in','No visual change; one clean path per shard.'),('clean','E1 · Clean-up (recommended)','Exact 45° / 67.5° cleft, constant gap, tidy points.'),('grid','E2 · Crystal grid','Every edge on 22.5°. Sharper, more symmetric.')]:
    s=save(f'emblem-{k}-steel',B.emb_svg(k,B.STEEL)); si=save(f'emblem-{k}-iron',B.emb_svg(k,B.IRON))
    small=''.join(img(s,h,'margin:0 10px') for h in (64,32,16))
    smalll=''.join(img(si,h,'margin:0 10px') for h in (64,32,16))
    H.append(f'<div class="row"><div class="lab"><b>{lab}</b><span>{txt}</span></div><div class="card dark" style="width:300px;height:230px">{img(s,170)}</div><div class="card dark" style="flex:1;height:230px">{small}</div><div class="card light" style="flex:1;height:230px">{smalll}</div></div>')
H.append('</div>')
# 02 directions
H.append('<div class="sec"><h2>02 — Wordmark directions</h2><div class="d">Each drawn from the font\'s outlines, not typed. Shard i-dot everywhere; "cuts" are 45° chamfers on stem tops, like the shard tips. All with the E1 emblem. Right column: the wordmark at 28 px, roughly a header size.</div>')
for k in B.SPECS:
    sp=B.SPECS[k]
    d=save(f'horizontal-{k}-color-dark',B.wm(k,B.STEEL,B.HAZE,lockup='h'))
    l=save(f'horizontal-{k}-color',B.wm(k,B.IRON,B.HAZE_D,lockup='h'))
    sm=save(f'wordmark-{k}-color-dark',B.wm(k,B.STEEL,B.HAZE))
    fav=' <span class="tag">favourite</span>' if k=='A2' else (' <span class="tag">alternative</span>' if k=='B1' else '')
    H.append(f'<div class="row"><div class="lab"><b>{sp["label"]}</b><span>{sp["note"]}</span>{fav}</div><div class="card dark" style="flex:1.3;height:170px">{img(d,92)}</div><div class="card light" style="flex:1.3;height:170px">{img(l,92)}</div><div class="card dark" style="flex:.8;height:170px">{img(sm,28)}</div></div>')
H.append('</div>')
# 03 i-dot
H.append('<div class="sec"><h2>03 — The i-dot</h2><div class="d">On A2 and B1: a single shard, the whole emblem in miniature, a plain cut rhombus, and the font\'s own dot.</div>')
for k in ('A2','B1'):
    cells=''
    for dot,lab in [('shard','shard'),('emblem','mini emblem'),('rhombus','rhombus'),('font','font dot')]:
        s=save(f'idot-{k}-{dot}',B.wm(k,B.STEEL,B.HAZE,dot=dot,gg=False))
        cells+=f'<div class="card dark" style="flex:1;height:150px">{img(s,74)}<div class="cap">{lab}</div></div>'
    H.append(f'<div class="row"><div class="lab"><b>{B.SPECS[k]["label"]}</b></div>{cells}</div>')
H.append('</div>')
# 04 .gg
H.append('<div class="sec"><h2>04 — ".gg"</h2><div class="d">Muted haze (today\'s idea), the same steel, and without — the short form for places where the domain is already clear.</div>')
for k in ('A2','B1'):
    cells=''
    for name,kw,lab in [('haze',dict(ggc=B.HAZE),'.gg in haze'),('same',dict(ggc=B.STEEL),'.gg in steel'),('none',dict(gg=False),'hematite alone')]:
        s=save(f'gg-{k}-{name}',B.wm(k,B.STEEL,**kw))
        cells+=f'<div class="card dark" style="flex:1;height:150px">{img(s,62)}<div class="cap">{lab}</div></div>'
    H.append(f'<div class="row"><div class="lab"><b>{B.SPECS[k]["label"]}</b></div>{cells}</div>')
H.append('</div>')
# 05 colour
H.append('<div class="sec"><h2>05 — Colour: steel vs. streak i-dot</h2><div class="d">Hematite is grey as a crystal but its streak (its powder) is blood-red, which gave it its name. Here the i-dot alone carries that red, #C0503F.</div>')
for k in ('A2','B1'):
    a=save(f'horizontal-{k}-streak-dark',B.wm(k,B.STEEL,B.HAZE,dotc=B.STREAK,lockup='h'))
    b=save(f'horizontal-{k}-streak',B.wm(k,B.IRON,B.HAZE_D,dotc='#A33A2C',lockup='h'))
    c=save(f'horizontal-{k}-steel',B.wm(k,B.STEEL,B.STEEL,lockup='h'))
    H.append(f'<div class="row"><div class="lab"><b>{B.SPECS[k]["label"]}</b></div><div class="card dark" style="flex:1;height:150px">{img(c,70)}<div class="cap">all steel</div></div><div class="card dark" style="flex:1;height:150px">{img(a,70)}<div class="cap">streak dot</div></div><div class="card light" style="flex:1;height:150px">{img(b,70)}<div class="cap">streak dot on white</div></div></div>')
H.append('</div>')
# 06 stacked
H.append('<div class="sec"><h2>06 — Stacked, for square formats</h2><div class="d">Emblem above "hematite", no ".gg".</div><div class="row">')
for k in ('A2','B1','C1'):
    s=save(f'stacked-{k}-color-dark',B.wm(k,B.STEEL,gg=False,lockup='s'))
    H.append(f'<div class="card dark" style="flex:1;height:300px">{img(s,210)}<div class="cap">{k}</div></div>')
H.append('</div></div></body></html>')
open(f'{OUT}/board.html','w').write(''.join(H)); print(len(files),'svgs')
