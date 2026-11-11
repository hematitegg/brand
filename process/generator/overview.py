"""brand/overview.html: the locked system, built from the exported files."""
import os
ROOT=os.environ.get('BRAND', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
NIGHT='#09090B'; BG={'steel':NIGHT,'iron':'#FFFFFF','black':'#FFFFFF','white':'#2E3A46'}
def im(path,h,extra=''): return f'<img src="{path}" style="max-height:{h}px;max-width:86%;{extra}">'
css='''*{box-sizing:border-box}body{margin:0;background:#EEEEF0;font-family:Inter,system-ui,sans-serif;color:#151515;padding:44px}
h1{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}.sub{color:#666;font-size:14px;margin-bottom:34px}
.sec{background:#fff;border-radius:18px;padding:28px 30px;margin-bottom:26px}.sec h2{font-size:19px;margin:0 0 4px}.sec .d{font-size:13px;color:#777;margin-bottom:20px;line-height:1.45}
.row{display:flex;gap:14px;margin-bottom:14px}.card{border-radius:12px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex:1}
.b{border:1px solid #e3e3e6}.cap{position:absolute;left:12px;bottom:9px;font-size:11px;color:#8a8a92}
.sw{flex:1;border-radius:12px;height:110px;padding:14px;display:flex;flex-direction:column;justify-content:flex-end;font-size:12px}.sw b{font-size:14px}
.tab{display:flex;align-items:center;gap:8px;border-radius:8px;padding:7px 12px;width:240px;font-size:12.5px}'''
H=[f'<html><head><meta charset="utf-8"><style>{css}</style></head><body><h1>hematite — logo system</h1><div class="sub">Emblem E2 · wordmark B2 (Inter Display SemiBold Italic, drawn) · C2 light cuts at 45° · S6 shard i-dot. Flat only. 11 Nov 2026.</div>']
H.append(f'<div class="sec"><h2>01 — Primary logo</h2><div class="d">Horizontal lockup. Steel on night is the default; iron on white for light backgrounds.</div><div class="row"><div class="card" style="height:300px;background:{NIGHT}">{im("horizontal/svg/hematite-horizontal-steel.svg",110)}</div></div><div class="row"><div class="card b" style="height:200px;background:#fff">{im("horizontal/svg/hematite-horizontal-iron.svg",80)}</div><div class="card" style="height:200px;background:#2E3A46">{im("horizontal/svg/hematite-horizontal-white.svg",80)}</div></div></div>')
H.append('<div class="sec"><h2>02 — Lockups and colourways</h2><div class="d">horizontal/, stacked/, wordmark/, emblem/ · each in steel, iron, black and white · SVG + PNG 1x–4x.</div>')
for name,hh,ch in (('horizontal',54,130),('stacked',150,230),('wordmark',40,110),('emblem',110,180)):
    cells=''.join(f'<div class="card {"b" if BG[c]=="#FFFFFF" else ""}" style="height:{ch}px;background:{BG[c]}">{im(f"{name}/svg/hematite-{name}-{c}.svg",hh)}<div class="cap">{name} · {c}</div></div>' for c in ('steel','iron','black','white'))
    H.append(f'<div class="row">{cells}</div>')
H.append('</div>')
tabs=lambda bg,fg: f'<div class="tab" style="background:{bg};color:{fg}"><img src="favicon/favicon-32.png" style="width:16px;height:16px">hematite.gg</div>'
H.append(f'<div class="sec"><h2>03 — Favicons and app icons</h2><div class="d">favicon/: favicon.svg (iron on light tabs, steel on dark), favicon.ico 16/32/48 and PNGs in haze #8A9BAB, which reads on both. Up to 48 px the emblem uses a small-size cut with a wider cleft. app-icon/: 1024 px on night and on steel, square and rounded.</div><div class="row"><div class="card b" style="height:90px;background:#F2F2F4">{tabs("#fff","#333")}</div><div class="card" style="height:90px;background:#1C1C20">{tabs("#2A2A30","#ddd")}</div><div class="card b" style="height:90px;background:#fff;gap:18px">'+''.join(f'<img src="favicon/favicon-{s}.png" style="width:{s}px">' for s in (16,32,48,64))+f'</div></div><div class="row"><div class="card b" style="height:240px;gap:28px;background:#fff">{im("app-icon/hematite-app-icon-night-rounded-1024.png",170)}{im("app-icon/hematite-app-icon-steel-rounded-1024.png",170)}{im("favicon/apple-touch-icon.png",90,"border-radius:20px")}</div></div></div>')
sw=[('Steel','#C4D4E0','#151515','Brand colour on dark'),('Iron','#2E3A46','#fff','Brand colour on light'),('Haze','#8A9BAB','#151515','Secondary, favicons'),('Night','#09090B','#fff','Ground')]
H.append('<div class="sec"><h2>04 — Colours</h2><div class="row">'+''.join(f'<div class="sw" style="background:{c};color:{t};{"border:1px solid #ddd" if c=="#C4D4E0" else ""}"><b>{n}</b>{c} · {u}</div>' for n,c,t,u in sw)+'</div></div></body></html>')
open(f'{ROOT}/overview.html','w').write(''.join(H))
