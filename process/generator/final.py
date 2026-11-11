"""The locked hematite logo: E2 emblem + B2 wordmark (Inter Display SemiBold Italic) with C2-light cuts and the S6 shard i-dot.
Cuts are baked into the outlines (no masks): each glyph contour is flattened and the facet polygons are subtracted."""
import os, math, emblem, wordmark as W, facets as F, dots as D, shards as SH
FONT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts','InterDisplay-SemiBoldItalic.otf')
TRACK=-22
TEXT='hematite'
def ladder_c2(d=45, a=45):
    TL,BR=90+a,270+a
    L={0:[(TL,d,(0,.5),(.7,1)),(BR,d,(0,.45),(0,.3)),(BR,d,(.55,1),(0,.3))],
       2:[(BR,d,(0,.36),(0,.3)),(BR,d,(.36,.68),(0,.3)),(BR,d,(.68,1),(0,.3))],
       3:[(BR,d,(.6,1),(0,.3))],
       4:[(TL,d,None,(.6,1))],5:[(TL,d),(BR,d,None,(0,.3))],6:[(TL,d,None,(.6,1))]}
    return L
CUTS=ladder_c2()
DOT=SH.shard(**[s for s in SH.SHARDS if s[0]=='S6'][0][2])
DOT_SCALE=1.22
SAMPLES=24

# ---- geometry helpers --------------------------------------------------------
def area(P): return sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))/2
def inside_convex(p, C):
    s=1 if area(C)>0 else -1; n=len(C)
    for i in range(n):
        a,b=C[i],C[(i+1)%n]
        if s*((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))<=1e-9: return False
    return True
def pip(p, polys):
    c=False
    for P in polys:
        n=len(P)
        for i in range(n):
            a,b=P[i],P[(i+1)%n]
            if (a[1]>p[1])!=(b[1]>p[1]):
                x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
                if x>p[0]: c=not c
    return c
def seg_x(a,b,c,d):
    r=(b[0]-a[0],b[1]-a[1]); s=(d[0]-c[0],d[1]-c[1]); den=r[0]*s[1]-r[1]*s[0]
    if abs(den)<1e-12: return None
    t=((c[0]-a[0])*s[1]-(c[1]-a[1])*s[0])/den; u=((c[0]-a[0])*r[1]-(c[1]-a[1])*r[0])/den
    if 0<t<1 and 0<=u<1: return t,u
    return None
def perim(C):
    L=[0]
    for i in range(len(C)): a,b=C[i],C[(i+1)%len(C)]; L.append(L[-1]+math.hypot(b[0]-a[0],b[1]-a[1]))
    return L
def at_perim(C,L,s):
    s%=L[-1]
    for i in range(len(C)):
        if L[i]<=s<=L[i+1]:
            a,b=C[i],C[(i+1)%len(C)]; t=(s-L[i])/(L[i+1]-L[i]) if L[i+1]>L[i] else 0
            return (a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]))
def arc(C,L,s0,s1,forward):
    """points of C's boundary strictly between perimeter positions s0 and s1"""
    T=L[-1]; out=[]
    if forward:
        e=s1 if s1>=s0 else s1+T
        for i in range(2*len(C)):
            v=L[i%len(C)]+(T if i>=len(C) else 0)
            if s0<v<e: out.append(C[i%len(C)])
    else:
        e=s1 if s1<=s0 else s1-T
        for i in range(2*len(C)-1,-1,-1):
            v=L[i%len(C)]-(T if i<len(C) else 0)
            if e<v<s0: out.append(C[i%len(C)])
    return out
def subtract(contour, C, glyph):
    """contour minus convex polygon C; glyph = all contours of the glyph (for choosing the right arc)"""
    n=len(contour); L=perim(C)
    pts=[]   # (point, is_cross, perim_pos)
    for i in range(n):
        a,b=contour[i],contour[(i+1)%n]; pts.append((a,False,None))
        xs=[]
        for j in range(len(C)):
            r=seg_x(a,b,C[j],C[(j+1)%len(C)])
            if r: xs.append((r[0],L[j]+r[1]*(L[j+1]-L[j])))
        for t,s in sorted(xs): pts.append(((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])),True,s))
    if not any(c for _,c,_ in pts):
        return [] if all(inside_convex(p,C) for p,_,_ in pts) else [contour]
    # start at a vertex outside C
    st=next((i for i,(p,c,_) in enumerate(pts) if not c and not inside_convex(p,C)),None)
    if st is None: return []
    pts=pts[st:]+pts[:st]
    out=[]; inside=False; entry=None
    for p,c,s in pts+[pts[0]]:
        if c:
            if not inside: out.append(p); entry=s; inside=True
            else:
                fw=arc(C,L,entry,s,True); bw=arc(C,L,entry,s,False)
                def mid(path,s0,s1,f):
                    T=L[-1]
                    if f: m=(s0+((s1-s0)%T)/2)
                    else: m=(s0-((s0-s1)%T)/2)
                    return at_perim(C,L,m)
                use=fw if pip(mid(fw,entry,s,True),glyph) else bw
                out+=use; out.append(p); inside=False
        elif not inside: out.append(p)
    if out and out[-1]==out[0]: out.pop()
    return [out]

# ---- build ------------------------------------------------------------------------------------
def wordmark_polys():
    """list of polygons (font units, y up, baseline 0) for 'hematite' with cuts and the S6 dot"""
    G,w,xh=F.layout(TEXT,FONT,TRACK); polys=[]
    for i,g in enumerate(G):
        cs=[]
        for c in g['cs']:
            P=F.sample(c,SAMPLES)
            if math.dist(P[0],P[-1])<1e-6: P=P[:-1]
            cs.append(P)
        glyph=list(cs)
        bx0,by0,bx1,by1=g['bb']
        for fc in CUTS.get(i,[]):
            nd,dep=fc[0],fc[1]; xr=fc[2] if len(fc)>2 else None; yr=fc[3] if len(fc)>3 else None
            XR=(bx0+(bx1-bx0)*xr[0], bx0+(bx1-bx0)*xr[1]) if xr else (bx0-4,bx1+4)
            YR=(by0+(by1-by0)*yr[0], by0+(by1-by0)*yr[1]) if yr else (by0-4,by1+4)
            Cp=F.facet_poly(g['pts'],nd,dep,XR,YR,ybox=(by0-4,by1+4))
            if not Cp or len(Cp)<3: continue
            nxt=[]
            for P in cs: nxt+=subtract(P,Cp,glyph)
            cs=nxt; glyph=list(cs)
        polys+=[[(x+g['x'],y) for x,y in P] for P in cs]
        if g['ch']=='i':
            Hd=g['dot'][3]-g['dot'][1]; x0,y0,x1,y1=g['dot']; cx=(x0+x1)/2+g['x']; cy=(y0+y1)/2; h=Hd*DOT_SCALE
            polys+=[[(cx+x*h,cy+y*h) for x,y in P] for P in DOT]
    return polys, w
def emblem_polys(kind='grid', gap=7.0):
    sh=emblem.build(kind,gap)
    return [[(x,-y) for x,y in P] for P in sh]   # to y up
def bbox(polys):
    xs=[p[0] for P in polys for p in P]; ys=[p[1] for P in polys for p in P]; return min(xs),min(ys),max(xs),max(ys)
def transform(polys, s=1, dx=0, dy=0): return [[(x*s+dx,y*s+dy) for x,y in P] for P in polys]
def to_d(polys, nd=1):
    """y-up polygons to an SVG path (y down)"""
    return ''.join('M'+' '.join(f'{round(x,nd):g},{round(-y,nd):g}' for x,y in P)+'Z' for P in polys)
