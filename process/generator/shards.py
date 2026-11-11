"""New shard i-dots, grown like a crystal: the intersection of half-planes whose normals sit on the 22.5 deg grid.
Each facet is set tangent to an ellipse (the shard's body); `trim` pulls single facets in to make it asymmetric."""
import math, facets as F
def shard(normals, axis=67.5, a=0.5, b=0.2, trim=None):
    u=(math.cos(math.radians(axis)),math.sin(math.radians(axis))); v=(-u[1],u[0])
    P=[(-2,-2),(2,-2),(2,2),(-2,2)]
    for nd in normals:
        n=(math.cos(math.radians(nd)),math.sin(math.radians(nd)))
        h=math.sqrt((a*(n[0]*u[0]+n[1]*u[1]))**2+(b*(n[0]*v[0]+n[1]*v[1]))**2)
        h*= (trim or {}).get(nd,1.0)
        P=F.clip(P,(-n[0],-n[1]),-h)        # keep n.p <= h
    xs=[p[0] for p in P]; ys=[p[1] for p in P]; H=max(ys)-min(ys); cx=(max(xs)+min(xs))/2; cy=(max(ys)+min(ys))/2
    return [[((x-cx)/H,(y-cy)/H) for x,y in P]]
D2N=[270,292.5,337.5,22.5,135,157.5]   # the facet directions of E2's right shard
SHARDS=[
 ('S1','D2 facets, grown',    dict(normals=D2N)),
 ('S2','four facets',         dict(normals=[270,337.5,22.5,157.5])),
 ('S3','five facets',         dict(normals=[270,337.5,22.5,135,180])),
 ('S4','slim blade',          dict(normals=[270,292.5,337.5,22.5,157.5],b=0.15)),
 ('S5','stout',               dict(normals=D2N,b=0.26)),
 ('S6','sharp tip',           dict(normals=[270,315,0,45,135,180],a=0.5,b=0.19)),
 ('S7','more lean',           dict(normals=D2N,axis=56.25,b=0.21)),
 ('S8','upright',             dict(normals=[270,315,22.5,157.5,202.5],axis=78.75,b=0.2)),
 ('S9','flat top',            dict(normals=D2N+[67.5],trim={67.5:0.74})),
 ('S10','kite shard',         dict(normals=[247.5,315,22.5,135],b=0.22)),
 ('S11','six facets, even',   dict(normals=[270,330,30,90,150,210],axis=67.5,b=0.2)),
 ('S12','tipped base',        dict(normals=[247.5,292.5,337.5,22.5,157.5],b=0.19)),
]
