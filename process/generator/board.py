import os, emblem, wordmark as W
STEEL='#C4D4E0'; IRON='#2E3A46'; HAZE='#8A9BAB'; HAZE_D='#7A8896'; NIGHT='#09090B'; WHITE='#FFFFFF'; STREAK='#C0503F'
IDF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','InterDisplay-SemiBoldItalic.otf')
SPECS={
 'A1':dict(label='A1 · Serif italic, drawn',note='DM Serif Text Italic as today, shard i-dot, no cuts',font='DMSerifText-Italic.ttf',gg='DMSerifText-Italic.ttf',track=-6,cuts=()),
 'A2':dict(label='A2 · Cleaved serif italic',note='A1 plus 45° cuts on the h and t tops',font='DMSerifText-Italic.ttf',gg='DMSerifText-Italic.ttf',track=-6,cuts=(0,4,6)),
 'A3':dict(label='A3 · Cleaved serif upright',note='DM Serif Text upright, 45° cuts, shard i-dot',font='DMSerifText-Regular.ttf',gg='DMSerifText-Regular.ttf',track=-10,cuts=(0,4,6)),
 'B1':dict(label='B1 · Faceted sans',note='Geist Bold, 45° cuts on h, t and i, shard i-dot',font='Geist-700.ttf',gg='Geist-500.ttf',track=-28,cuts=(0,4,5,6)),
 'B2':dict(label='B2 · Faceted sans italic',note='Inter Display SemiBold Italic, cuts, shard i-dot',font=IDF,gg=IDF,track=-22,cuts=(0,4,5,6)),
 'C1':dict(label='C1 · Technical mono',note='Geist Mono SemiBold, cuts, shard i-dot',font='GeistMono-600.ttf',gg='GeistMono-500.ttf',track=-40,cuts=(0,4,6)),
}
_n=[0]
def emb_group(kind, fill, h, x=0, ybottom=0):
    sh=emblem.build(kind); allp=[p for P in sh for p in P]; x0,y0,x1,y1=W.bbox(allp)
    s=h/(y1-y0); w=(x1-x0)*s
    g=f'<g transform="translate({x:.1f},{ybottom-h:.1f}) scale({s:.4f}) translate({-x0:.2f},{-y0:.2f})" fill="{fill}">'+''.join(f'<path d="{emblem.path(P)}"/>' for P in sh)+'</g>'
    return g,w
def emb_svg(kind, fill, pad=2):
    sh=emblem.build(kind); allp=[p for P in sh for p in P]; x0,y0,x1,y1=W.bbox(allp)
    d=''.join(f'<path d="{emblem.path(P)}"/>' for P in sh)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0-pad:.2f} {y0-pad:.2f} {x1-x0+2*pad:.2f} {y1-y0+2*pad:.2f}"><g fill="{fill}">{d}</g></svg>'
def wm(key, fg, ggc=None, dotc=None, gg=True, dot='shard', lockup=None, embc=None, emb_kind='clean', dot_scale=2.0, cut_angle=45):
    sp=SPECS[key]; _n[0]+=1; mid=f'm{_n[0]}'
    body,dotd,holes,w,m=W.build('hematite',sp['font'],track=sp['track'],dot=dot,cuts=sp['cuts'],dot_scale=dot_scale,cut_angle=cut_angle)
    if dot=='font':
        body,dotd,holes,w,m=W.build('hematite',sp['font'],track=sp['track'],dot='font',cuts=sp['cuts'],cut_angle=cut_angle)
    total=w
    g=f'<g mask="url(#{mid})"><path d="{body}" fill="{fg}"/></g>'
    if dotd: g+=f'<path d="{dotd}" fill="{dotc or fg}"/>'
    if gg:
        gd,_,_,gw,_=W.build('.gg',sp['gg'],track=sp['track'])
        gx=w+(14 if 'Mono' not in sp['font'] else -10)
        g+=f'<path d="{gd}" transform="translate({gx:.1f},0)" fill="{ggc or fg}"/>'; total=gx+gw
    mask=f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-300" y="-1500" width="{total+600}" height="3000"><rect x="-300" y="-1500" width="{total+600}" height="3000" fill="#fff"/><path d="{holes}" fill="#000"/></mask>'
    TOP, BOT = 770, 250   # ascender area / descender area (font units)
    if lockup is None:
        vb=(-20,-TOP,total+40,TOP+BOT); body_svg=mask+g
    elif lockup=='h':
        eh=TOP*1.12; eg,ew=emb_group(emb_kind, embc or fg, eh, 0, BOT*0.18)
        gap=ew*0.38
        body_svg=eg+f'<g transform="translate({ew+gap:.1f},0)">{mask}{g}</g>'
        vb=(-60,-eh+BOT*0.18-60,ew+gap+total+120,eh+BOT*0.85+120)
    elif lockup=='s':
        eh=TOP*1.5; eg,ew=emb_group(emb_kind, embc or fg, eh, (total-ew_guess(emb_kind,eh))/2, -TOP-180)
        body_svg=eg+mask+g
        vb=(-20,-TOP-180-eh-20,total+40,eh+180+TOP+BOT+40)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(f"{v:.1f}" for v in vb)}">{body_svg}</svg>'
def ew_guess(kind,h):
    sh=emblem.build(kind); allp=[p for P in sh for p in P]; x0,y0,x1,y1=W.bbox(allp); return (x1-x0)*h/(y1-y0)
