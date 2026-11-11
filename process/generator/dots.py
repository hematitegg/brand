"""i-dot shapes for round 2. Each returns an SVG path for glyph g (from facets.layout)."""
import math, emblem, wordmark as W, facets as F
SLANT=math.tan(math.radians(9.0))   # Inter Display Italic leans about 9-10 deg
def hull(P):
    P=sorted(set(P))
    if len(P)<3: return P
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def place(polys, g, H, shear=True, dy=0, scale_w=1.0):
    """polys: unit shapes, y up, height 1 centred at 0. Placed at the font's dot centre with height H."""
    x0,y0,x1,y1=g['dot']; cx=(x0+x1)/2+g['x']; cy=(y0+y1)/2+dy
    out=''
    for P in polys:
        Q=[(cx+(x*scale_w)*H+(y*H*SLANT if shear else 0), cy+y*H) for x,y in P]
        out+=F.poly_d(Q)
    return out
def unit_from_emblem(polys):
    allp=[p for P in polys for p in P]; x0,y0,x1,y1=W.bbox(allp); h=y1-y0; mx=(x0+x1)/2; my=(y0+y1)/2
    return [[((x-mx)/h, -(y-my)/h) for x,y in P] for P in polys]
E2=emblem.build('grid')
def exploded(gap=0.16):
    L,R=unit_from_emblem(E2)
    return [[(x-gap/2*0.7,y+gap/2*0.7) for x,y in L],[(x+gap/2*0.7,y-gap/2*0.7) for x,y in R]]
def reg(n, r=0.5, rot=0):
    return [[(r*math.cos(math.radians(rot+360*i/n)), r*math.sin(math.radians(rot+360*i/n))) for i in range(n)]]
def split(P, deg=67.5, gap=0.09):
    """split a convex unit polygon by a line through the centre at deg (from horizontal) with a gap"""
    r=math.radians(deg); d=(math.cos(r),math.sin(r)); n=(-d[1],d[0])
    return [F.clip(P,n,gap/2), F.clip(P,(-n[0],-n[1]),gap/2)]
def chip(g, depth, normal=135, lift=None):
    """the piece a facet cut takes off the top of the i stem; lift=None -> at the dot position"""
    pts=g['pts']; top=max(p[1] for p in pts)
    reg_=pts   # whole stem: its straight edges carry no intermediate points
    Hh=hull(reg_); r=math.radians(normal); n=(math.cos(r),math.sin(r))
    s=max(n[0]*p[0]+n[1]*p[1] for p in pts)
    C=F.clip(Hh,n,s-depth)
    if lift is None:
        x0,y0,x1,y1=g['dot']; cx=(x0+x1)/2; cy=(y0+y1)/2
        bx0,by0,bx1,by1=W.bbox(C); C=[(x-(bx0+bx1)/2+cx, y-(by0+by1)/2+cy) for x,y in C]
    else:
        C=[(x+n[0]*lift, y+n[1]*lift) for x,y in C]
    return F.poly_d(C,g['x'])
SQ=[(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]
def octa(): return reg(8,0.54,22.5)
def rhomb(): return [[(0,.5),(.32,0),(0,-.5),(-.32,0)]]

# key: (label, function(g, xh, H) -> d, extra facet on the i or None)
def DOTS(H):
    return [
     ('D1','E2 left shard',     lambda g: place(unit_from_emblem([E2[0]]),g,H*1.55,shear=False), None),
     ('D2','E2 right shard',    lambda g: place(unit_from_emblem([E2[1]]),g,H*1.45,shear=False), None),
     ('D3','E2 emblem',         lambda g: place(unit_from_emblem(E2),g,H*1.6,shear=False), None),
     ('D4','E2 emblem, opened', lambda g: place(exploded(),g,H*1.6,shear=False), None),
     ('D5','crystal (quartz)',  lambda g: place([[(0,.5),(.2,.3),(.2,-.3),(0,-.5),(-.2,-.3),(-.2,.3)]],g,H*1.55), None),
     ('D6','kite',              lambda g: place([[(.02,.5),(.26,.08),(-.02,-.5),(-.22,.02)]],g,H*1.45), None),
     ('D7','wedge',             lambda g: place([[(-.02,.5),(.26,-.5),(-.26,-.26)]],g,H*1.3), None),
     ('D8','needle',            lambda g: place([[(0,.5),(.11,.08),(0,-.5),(-.11,-.08)]],g,H*1.8), None),
     ('D9','parallelogram',     lambda g: place([[(-.34,-.5),(.12,-.5),(.34,.5),(-.12,.5)]],g,H*1.05), None),
     ('D10','octagon',          lambda g: place(octa(),g,H*1.05), None),
     ('D11','octagon, cleft',   lambda g: place(split(octa()[0]),g,H*1.2), None),
     ('D12','rhombus, cleft',   lambda g: place(split(rhomb()[0]),g,H*1.45), None),
     ('D13','chip from the stem', lambda g: chip(g,75), (135,75)),
     ('D14','cracked stem',     lambda g: chip(g,105,lift=34), (135,105)),
     ('D15','square, 22.5° turn', lambda g: place(reg(4,0.62,22.5),g,H*1.0), None),
     ('D16','cut square',       lambda g: place([[(-.5,-.5),(.5,-.5),(.5,.16),(.16,.5),(-.5,.5)]],g,H*0.95), None),
    ]
