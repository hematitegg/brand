"""Facet cuts and i-dot shapes for round 2. All in font units, y up, then flipped for SVG."""
import math, wordmark as W, emblem

def sample(c, n=12):
    out=[]; cur=None
    for op,a in c:
        if op=='moveTo': cur=a[0]; out.append(cur)
        elif op=='lineTo': cur=a[0]; out.append(cur)
        elif op=='curveTo':
            p0=cur; p1,p2,p3=a[0],a[1],a[2]
            for i in range(1,n+1):
                t=i/n; u=1-t
                out.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
            cur=p3
        elif op=='qCurveTo':
            pts=list(a); ctrl=pts[:-1]; end=pts[-1]
            segs=[]
            for i,cp in enumerate(ctrl):
                nxt = end if i==len(ctrl)-1 else ((cp[0]+ctrl[i+1][0])/2,(cp[1]+ctrl[i+1][1])/2)
                segs.append((cp,nxt))
            for cp,nx in segs:
                p0=cur
                for i in range(1,n+1):
                    t=i/n; u=1-t
                    out.append((u*u*p0[0]+2*u*t*cp[0]+t*t*nx[0], u*u*p0[1]+2*u*t*cp[1]+t*t*nx[1]))
                cur=nx
    return out

def clip(poly, n, s):
    """keep part of convex poly where n.p >= s"""
    out=[]; m=len(poly)
    for i in range(m):
        a,b=poly[i],poly[(i+1)%m]
        da=n[0]*a[0]+n[1]*a[1]-s; db=n[0]*b[0]+n[1]*b[1]-s
        if da>=0: out.append(a)
        if (da>=0)!=(db>=0):
            t=da/(da-db); out.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
    return out

def facet_poly(pts, normal_deg, depth, xr=None, yr=None, ybox=None):
    """polygon (font units, y up) removing everything beyond support-depth along the normal"""
    r=math.radians(normal_deg); n=(math.cos(r),math.sin(r))
    P=pts
    if xr: P=[p for p in P if xr[0]<=p[0]<=xr[1]]
    if yr: P=[p for p in P if yr[0]<=p[1]<=yr[1]]
    if not P: return None
    s=max(n[0]*p[0]+n[1]*p[1] for p in P)
    x0,x1=(xr if xr else (-3000,6000)); y0,y1=(ybox if ybox else (-3000,3000))
    box=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    return clip(box,n,s-depth)

def poly_d(P, dx=0, dy=0):
    return 'M'+' L'.join(f'{x+dx:.1f},{-(y+dy):.1f}' for x,y in P)+'Z'

def layout(text, fontname, track):
    """per glyph: contours (dot removed for i), sampled points, x offset, dot bbox"""
    f=W.font(fontname); xh=f['OS/2'].sxHeight*1000/f['head'].unitsPerEm
    x=0; G=[]
    for ch in text:
        cs,adv=W.glyph_contours(f,ch)
        dotbb=None
        if ch=='i':
            dots=[c for c in cs if W.bbox(W.pts(c))[1]>=xh*0.9]
            cs=[c for c in cs if W.bbox(W.pts(c))[1]<xh*0.9]
            if dots: dotbb=W.bbox(sample(dots[0]))
        sp=[p for c in cs for p in sample(c)]
        G.append(dict(ch=ch,cs=cs,pts=sp,x=x,adv=adv,dot=dotbb,bb=W.bbox(sp)))
        x+=adv+track
    return G, x-track, xh

def build(text, fontname, track, facets, dot=None):
    """facets: {glyph index: [(normal_deg, depth, xr_frac, yr_frac), ...]} ; xr/yr fractions of glyph bbox or None.
    returns body d, holes d, dot d, width"""
    G,w,xh=layout(text,fontname,track)
    body=[]; holes=[]
    for i,g in enumerate(G):
        body.append(''.join(W.cpath_safe(c,g['x']) for c in g['cs'])); holes.append('')
        bx0,by0,bx1,by1=g['bb']
        for fc in facets.get(i,[]):
            nd,dep=fc[0],fc[1]; xr=fc[2] if len(fc)>2 else None; yr=fc[3] if len(fc)>3 else None
            XR=(bx0+(bx1-bx0)*xr[0], bx0+(bx1-bx0)*xr[1]) if xr else (bx0-4, bx1+4)
            YR=(by0+(by1-by0)*yr[0], by0+(by1-by0)*yr[1]) if yr else (by0-4, by1+4)
            P=facet_poly(g['pts'],nd,dep,XR,YR,ybox=(by0-4,by1+4))
            if P: holes[-1]+=poly_d(P,g['x'])
    dotd=''
    if dot:
        gi=[i for i,g in enumerate(G) if g['ch']=='i'][0]; g=G[gi]
        dotd=dot(g, xh)
    return body, holes, dotd, w, G
