import math, emblem
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import os
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts')+'/'
_cache={}
def font(name):
    if name not in _cache:
        p = name if name.startswith('/') else FD+name
        _cache[name]=TTFont(p)
    return _cache[name]

def glyph_contours(f, ch):
    gs=f.getGlyphSet(); gn=f.getBestCmap()[ord(ch)]
    pen=DecomposingRecordingPen(gs); gs[gn].draw(pen)
    k=1000/f['head'].unitsPerEm
    cs=[]; cur=None
    for op,args in pen.value:
        args=tuple((x*k,y*k) for x,y in args)
        if op=='moveTo': cur=[(op,args)]
        elif op in ('closePath','endPath'): cur.append((op,args)); cs.append(cur); cur=None
        else: cur.append((op,args))
    return cs, gs[gn].width*k
def pts(c): return [p for op,a in c for p in a]
def bbox(ps):
    xs=[p[0] for p in ps]; ys=[p[1] for p in ps]; return min(xs),min(ys),max(xs),max(ys)
def cpath(c, dx, dy=0):
    s=[]
    for op,a in c:
        q=' '.join(f'{x+dx:.1f},{-(y+dy):.1f}' for x,y in a)
        s.append({'moveTo':'M','lineTo':'L','curveTo':'C','qCurveTo':'Q','closePath':'Z','endPath':''}[op]+q)
    # qCurveTo with >2 pts needs splitting; handle
    return ''.join(s)
def cpath_safe(c, dx):
    out=[]
    for op,a in c:
        if op=='qCurveTo' and len(a)>2:
            # implied on-curve points
            ctrl=a[:-1]; end=a[-1]
            for i,cp in enumerate(ctrl):
                if i<len(ctrl)-1:
                    nx=((cp[0]+ctrl[i+1][0])/2,(cp[1]+ctrl[i+1][1])/2)
                    out.append(f'Q{cp[0]+dx:.1f},{-cp[1]:.1f} {nx[0]+dx:.1f},{-nx[1]:.1f}')
                else:
                    out.append(f'Q{cp[0]+dx:.1f},{-cp[1]:.1f} {end[0]+dx:.1f},{-end[1]:.1f}')
        else:
            k={'moveTo':'M','lineTo':'L','curveTo':'C','qCurveTo':'Q','closePath':'Z','endPath':''}[op]
            out.append(k+' '.join(f'{x+dx:.1f},{-y:.1f}' for x,y in a))
    return ''.join(out)

SHARD_L = emblem.build('clean')[0]
EMB = emblem.build('clean')
def shape_path(polys, cx, cy, h, flipx=False):
    # polys in emblem coords (y down); place centred at (cx,cy) in font units (y up) with height h
    allp=[p for P in polys for p in P]; x0,y0,x1,y1=bbox(allp)
    s=h/(y1-y0); mx=(x0+x1)/2; my=(y0+y1)/2
    out=''
    for P in polys:
        q=[((x-mx)*s*(-1 if flipx else 1)+cx, -((y-my)*s)+cy) for x,y in P]
        out+='M'+' L'.join(f'{x:.1f},{-y:.1f}' for x,y in q)+'Z'
    return out, s
def rhombus(cx,cy,h,w):
    return f'M{cx:.1f},{-(cy+h/2):.1f} L{cx+w/2:.1f},{-cy:.1f} L{cx:.1f},{-(cy-h/2):.1f} L{cx-w/2:.1f},{-cy:.1f}Z'

def build(text, fontname, track=0, dot='shard', dot_scale=1.25, cuts=(), cut_angle=45, cut_band=40, kern=None, dot_dx=0):
    """returns (svg path d, mask polys d, width, metrics). Coordinates: font units, y down (svg)."""
    f=font(fontname); xh=f['OS/2'].sxHeight*1000/f['head'].unitsPerEm
    x=0; paths=[]; holes=[]; extra=[]
    for i,ch in enumerate(text):
        cs,adv=glyph_contours(f,ch)
        if ch=='i' and dot!='font':
            body=[c for c in cs if bbox(pts(c))[1] < xh*0.9]
            dots=[c for c in cs if bbox(pts(c))[1] >= xh*0.9]
            if dots:
                bx0,by0,bx1,by1=bbox(pts(dots[0])); cx=(bx0+bx1)/2+x+dot_dx; cy=(by0+by1)/2; dh=(by1-by0)*dot_scale
                if dot=='shard': d,_=shape_path([SHARD_L],cx,cy,dh)
                elif dot=='emblem': d,_=shape_path(EMB,cx,cy,dh*1.1)
                elif dot=='rhombus': d=rhombus(cx,cy,dh*0.85,dh*0.55)
                else: d=''
                extra.append(d)
            cs=body
        if i in cuts or ch in cuts:
            allp=[p for c in cs for p in pts(c)]; top=max(p[1] for p in allp)
            near=[p for p in allp if p[1]>top-cut_band]
            xl=min(p[0] for p in near); xr=max(p[0] for p in near)
            t=math.tan(math.radians(cut_angle))
            yl=lambda X: top-(xr-X)*t
            a=xl-30; b=xr+1
            holes.append(f'M{a+x:.1f},{-yl(a):.1f} L{b+x:.1f},{-yl(b):.1f} L{b+x:.1f},{-(top+400):.1f} L{a+x:.1f},{-(top+400):.1f}Z')
        for c in cs: paths.append(cpath_safe(c,x))
        x+=adv+track+(kern or {}).get(text[i:i+2],0)
    return ''.join(paths), ''.join(extra), ''.join(holes), x-track, dict(xh=xh, cap=f['OS/2'].sCapHeight)
