"""GitHub assets: the org avatar (P1, the emblem as contribution squares in GitHub green) and the
org README header (H3: GitHub's contribution grid with activity at both ends, the two-tone logo in the middle).
Writes brand/github/."""
import os, math, random, subprocess
import final as FN, export as EX
ROOT=os.environ.get('BRAND', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
OUT=os.path.join(ROOT,'github')
# GitHub's own contribution colours (levels 0-4) and canvases
GREEN={'dark':['#161B22','#0E4429','#006D32','#26A641','#39D353'],'light':['#EFF2F5','#ACEEBB','#4AC26B','#2DA44E','#116329']}
CANVAS={'dark':'#0D1117','light':'#FFFFFF'}
LOGO={'dark':EX.COL2['color-dark'],'light':EX.COL2['color']}

def coverage(polys, x0, y0, x1, y1, n=5):
    c=sum(FN.pip((x0+(i+.5)*(x1-x0)/n, y0+(j+.5)*(y1-y0)/n), polys) for i in range(n) for j in range(n))
    return c/(n*n)
def level(v): return 4 if v>0.75 else 3 if v>0.45 else 2 if v>0.2 else 1

def sample_cells(E, rows, phase):
    """contribution cells covering the emblem; phase shifts the sampling grid sideways by a fraction of a cell"""
    x0,y0,x1,y1=FN.bbox(E); cs=(y1-y0)/rows
    cols=math.ceil((x1-x0)/cs)+2; ox=(x0+x1)/2-cols*cs/2+phase*cs
    cells={}
    for r in range(rows):
        for c in range(cols):
            v=coverage(E, ox+c*cs, y1-(r+1)*cs, ox+(c+1)*cs, y1-r*cs)
            if v>0.08: cells[(r,c)]=level(v)
    return cells

def avatar_svg(rows=14, cell=10, gap=2, pad=8, margin=2):
    """P1: the emblem in contribution cells. The cleft is widened (gap 17) so it survives as a row of empty cells.
    Centred on the lit cells: the sampling grid is nudged sideways until the lit width has the same parity as the
    lit height, so the empty cells split evenly on all four sides."""
    E=FN.emblem_polys('grid',17.0)
    best=None
    for i in range(20):
        ph=((i+1)//2)*0.05*(1 if i%2 else -1)          # 0, +0.05, -0.05, +0.1, ... (closest to the original first)
        cells=sample_cells(E,rows,ph)
        rs=[r for r,_ in cells]; cs_=[c for _,c in cells]
        lh=max(rs)-min(rs)+1; lw=max(cs_)-min(cs_)+1
        if (lh-lw)%2==0: best=(cells,min(rs),min(cs_),lh,lw); break
    cells,r0,c0,lh,lw=best
    n=max(lh,lw)+2*margin
    offr=(n-lh)//2-r0; offc=(n-lw)//2-c0
    W=n*(cell+gap)-gap+2*pad; pal=GREEN['dark']
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}"><rect width="{W}" height="{W}" fill="{CANVAS["dark"]}"/>']
    for r in range(n):
        for c in range(n):
            lv=cells.get((r-offr,c-offc),0)
            s.append(f'<rect x="{pad+c*(cell+gap)}" y="{pad+r*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{pal[lv]}"/>')
    return ''.join(s)+'</svg>'

W,H,STEP,CELL=1280,400,18,14
def header_svg(theme, seed=11, logo_width=620):
    """H3: activity towards the left and right ends, an empty grid in the middle, the horizontal two-tone logo on top."""
    parts=EX.layout_parts()['horizontal']; allp=[p for v in parts.values() for p in v]
    x0,y0,x1,y1=FN.bbox(allp); k=logo_width/(x1-x0); lh=(y1-y0)*k; lx=(W-logo_width)/2; ly=(H-lh)/2
    cols,rows=W//STEP,H//STEP; ox=(W-(cols*STEP-(STEP-CELL)))/2; oy=(H-(rows*STEP-(STEP-CELL)))/2
    rnd=random.Random(seed); pal=GREEN[theme]
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{CANVAS[theme]}"/>']
    for r in range(rows):
        for c in range(cols):
            x=ox+c*STEP; y=oy+r*STEP; mx=x+CELL/2; my=y+CELL/2
            inside=(lx-36<=mx<=lx+logo_width+36) and (ly-30<=my<=ly+lh+30)
            p=0.0 if inside else max(0.0, 0.7-1.6*min(mx,W-mx)/W)
            lv=rnd.choice([1,1,1,2,2,3,4]) if rnd.random()<p else 0
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{pal[lv]}"/>')
    g=f'<g transform="translate({lx:.1f},{ly:.1f}) scale({k:.5f}) translate({-x0:.1f},{y1:.1f})">'
    for r in ('emblem','letters','dot'): g+=f'<path d="{FN.to_d(parts[r])}" fill="{LOGO[theme][r]}"/>'
    return ''.join(s)+g+'</g></svg>'

def png(svg, path, w):
    subprocess.run(['rsvg-convert','-w',str(w),'-o',path],input=svg.encode(),check=True)

def main():
    os.makedirs(OUT,exist_ok=True)
    a=avatar_svg(); open(f'{OUT}/hematite-github-avatar.svg','w').write(a)
    png(a,f'{OUT}/hematite-github-avatar-1024.png',1024); png(a,f'{OUT}/hematite-github-avatar-460.png',460)
    for t in ('dark','light'):
        h=header_svg(t); open(f'{OUT}/hematite-github-header-{t}.svg','w').write(h)
        png(h,f'{OUT}/hematite-github-header-{t}@2x.png',2560)
    print('github assets ->',OUT)
if __name__=='__main__': main()
