import math
L = [(65.5,65.5),(50.0529,102.5),(46.5,104),(34,84.5),(47,53.5),(54,47),(63.5,29.5),(77.5,16),(83,33),(84,47.5)]
R = [(73.4471,71.2321),(91.9471,53.2321),(98.9471,86.732),(89.4471,102.232),(72.4471,112.732),(55.5,113.733)]

def area(P):
    return sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))/2
def lines(P):
    n=len(P); out=[]
    for i in range(n):
        a,b=P[i],P[(i+1)%n]; d=(b[0]-a[0],b[1]-a[1]); l=math.hypot(*d)
        out.append(dict(p=((a[0]+b[0])/2,(a[1]+b[1])/2), d=(d[0]/l,d[1]/l), len=l))
    return out
def isect(l1,l2):
    (x1,y1),(dx1,dy1)=l1['p'],l1['d']; (x2,y2),(dx2,dy2)=l2['p'],l2['d']
    den=dx1*dy2-dy1*dx2
    if abs(den)<1e-9: return ((x1+x2)/2,(y1+y2)/2)
    t=((x2-x1)*dy2-(y2-y1)*dx2)/den
    return (x1+t*dx1,y1+t*dy1)
def verts(Ls):
    n=len(Ls); return [isect(Ls[i-1],Ls[i]) for i in range(n)]
def offset(Ls, o, sign):
    out=[]
    for l in Ls:
        nx,ny = l['d'][1]*sign, -l['d'][0]*sign
        out.append(dict(l, p=(l['p'][0]+nx*o,l['p'][1]+ny*o)))
    return out
def setangle(l, deg_from_h):
    # keep direction sense; set to given angle (screen coords, y down) nearest to current direction
    best=None
    for k in range(16):
        a=math.radians(deg_from_h+180*k/1) if False else None
    cands=[]
    for base in (deg_from_h, 180-deg_from_h, 180+deg_from_h, 360-deg_from_h):
        r=math.radians(base); cands.append((math.cos(r),math.sin(r)))
    d=max(cands,key=lambda c:c[0]*l['d'][0]+c[1]*l['d'][1])
    return dict(l,d=d)
def snap(l, step=22.5):
    ang=math.degrees(math.atan2(l['d'][1],l['d'][0]))
    a=round(ang/step)*step; r=math.radians(a)
    return dict(l,d=(math.cos(r),math.sin(r)))
def path(P, nd=2):
    return 'M'+' L'.join(f"{round(x,nd):g},{round(y,nd):g}" for x,y in P)+' Z'

def build(kind, gap=7.0):
    sL = 1 if area(L)>0 else -1; sR = 1 if area(R)>0 else -1
    LL, RL = lines(L), lines(R)
    # outward normal sign: for y-down coords with positive area (clockwise on screen) outward = (dy,-dx)
    LL, RL = offset(LL,1.5,sL), offset(RL,1.5,sR)   # expand the 3px stroke into the shape
    if kind=='current':
        return [verts(LL), verts(RL)]
    # left cleft edges: index 9 (J->A, 45deg) and 0 (A->B, 67.5); right: 5 (Q->K 67.5), 0 (K->L 45)
    # centre line of the cleft: through midpoint between bend points
    bL = isect(LL[9],LL[0]); bR = isect(RL[5],RL[0])
    c = ((bL[0]+bR[0])/2,(bL[1]+bR[1])/2)
    r45, r67 = math.radians(-45), math.radians(180-67.5)  # up-right 45, down-left 67.5
    d45=(math.cos(r45),math.sin(r45)); d67=(math.cos(r67),math.sin(r67))
    def side(d, sgn):  # line parallel to d through c offset by gap/2 to one side
        n=(-d[1]*sgn, d[0]*sgn); return (c[0]+n[0]*gap/2, c[1]+n[1]*gap/2)
    # left shard lies to the upper-left of the cleft
    LL[9]=dict(LL[9], d=(-d45[0],-d45[1]), p=side(d45,-1)); LL[0]=dict(LL[0], d=d67, p=side(d67,1))
    RL[0]=dict(RL[0], d=d45, p=side(d45,1)); RL[5]=dict(RL[5], d=(-d67[0],-d67[1]), p=side(d67,-1))
    if kind=='grid':
        LL=[snap(l) if i not in (0,9) else l for i,l in enumerate(LL)]
        RL=[snap(l) if i not in (0,5) else l for i,l in enumerate(RL)]
        # drop the bottom-right near-collinear edge pair handled by snapping
    return [verts(LL), verts(RL)]

def svg(kind, fill='#C4D4E0', bbox=True):
    sh=build(kind)
    return ''.join(f'<path d="{path(P)}" fill="{fill}"/>' for P in sh), sh
if __name__=='__main__':
    for k in ('current','clean','grid'):
        _,sh=build(k),None
        print(k,[ [ (round(x,1),round(y,1)) for x,y in P] for P in build(k)])
