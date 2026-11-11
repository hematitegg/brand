"""Social images in the website's language: night, a soft steel glow, the 64 px steel grid fading out, the two-tone logo.
Text is set in Inter and turned into outlines, so the SVGs need no fonts. Writes brand/social/."""
import os, subprocess
import final as FN, export as EX, wordmark as W
ROOT=os.environ.get('BRAND', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
OUT=os.path.join(ROOT,'social')
FONTS=os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts')
NIGHT='#09090B'; STEEL='#C4D4E0'; IRON='#2E3A46'; MUTED='#A1A1AA'; WHITE='#FFFFFF'
TAGLINE='Share your best moments, instantly.'

def text_group(text, font, px, x, y_base, fill, anchor='start', track=0):
    """text as outlined paths; px = font size, y_base = baseline in px"""
    d,_,_,w,_=W.build(text, os.path.join(FONTS,font), track=track, dot='font')
    s=px/1000; wpx=w*s
    x0={'start':x,'middle':x-wpx/2,'end':x-wpx}[anchor]
    return f'<g transform="translate({x0:.1f},{y_base:.1f}) scale({s:.5f})" fill="{fill}"><path d="{d}"/></g>', wpx

def lockup_group(cx, cy, width, layout='horizontal', cols=None, anchor='middle'):
    parts=EX.layout_parts()[layout]; cols=cols or EX.COL2['color-dark']
    allp=[p for v in parts.values() for p in v]; x0,y0,x1,y1=FN.bbox(allp); k=width/(x1-x0); h=(y1-y0)*k
    lx={'middle':cx-width/2,'start':cx,'end':cx-width}[anchor]; ly=cy-h/2
    g=f'<g transform="translate({lx:.1f},{ly:.1f}) scale({k:.5f}) translate({-x0:.1f},{y1:.1f})">'
    for r in ('emblem','letters','dot'): g+=f'<path d="{FN.to_d(parts[r])}" fill="{cols[r]}"/>'
    return g+'</g>', (lx,ly,lx+width,ly+h)

def backdrop(w, h, gx, gy, glow=0.10, grid=True, rx=None, ry=None):
    rx=rx or w*0.45; ry=ry or h*0.9
    s=f'''<defs><radialGradient id="glow" cx="{gx}" cy="{gy}" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({gx} {gy}) scale({rx} {ry}) translate({-gx} {-gy})">
<stop offset="0" stop-color="{STEEL}" stop-opacity="{glow}"/><stop offset="0.7" stop-color="{STEEL}" stop-opacity="0"/></radialGradient>
<radialGradient id="fade" cx="{gx}" cy="{gy}" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({gx} {gy}) scale({rx*1.15} {ry*1.15}) translate({-gx} {-gy})">
<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.75" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask></defs>
<rect width="{w}" height="{h}" fill="{NIGHT}"/>'''
    if grid:
        lines=''.join(f'<rect x="{x}" y="0" width="1" height="{h}"/>' for x in range(int(gx)%64,w,64))
        lines+=''.join(f'<rect x="0" y="{y}" width="{w}" height="1"/>' for y in range(int(gy)%64,h,64))
        s+=f'<g mask="url(#gridmask)" fill="{STEEL}" fill-opacity="0.07">{lines}</g>'
    s+=f'<rect width="{w}" height="{h}" fill="url(#glow)"/>'
    return s

def x_header(variant):
    w,h=1500,500
    if variant=='centre':      # logo and tagline in the middle
        bg=backdrop(w,h,750,230)
        lg,(_,_,_,ly1)=lockup_group(750,215,560)
        tg,_=text_group(TAGLINE,'Inter-Medium.ttf',30,750,ly1+62,MUTED,'middle',track=-10)
        body=bg+lg+tg
    elif variant=='right':     # weighted right, clear of the avatar at the bottom left
        bg=backdrop(w,h,1010,235,rx=620)
        lg,(lx0,_,_,ly1)=lockup_group(1010,205,500)
        tg,_=text_group(TAGLINE,'Inter-Medium.ttf',28,1010,ly1+58,MUTED,'middle',track=-10)
        body=bg+lg+tg
    elif variant=='logo':      # the logo alone
        bg=backdrop(w,h,750,250,glow=0.12)
        lg,_=lockup_group(750,245,600)
        body=bg+lg
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'

def avatar(variant):
    n=1000
    E=FN.emblem_polys('grid'); x0,y0,x1,y1=FN.bbox(E)
    eh=n*0.5; k=eh/(y1-y0); ew=(x1-x0)*k
    fill,bg,glow={'night':(STEEL,NIGHT,True),'iron':(WHITE,IRON,False),'steel':(IRON,STEEL,False)}[variant]
    back=backdrop(n,n,n/2,n/2,glow=0.16,grid=False,rx=n*0.55,ry=n*0.55) if glow else f'<rect width="{n}" height="{n}" fill="{bg}"/>'
    g=f'<g transform="translate({(n-ew)/2:.1f},{(n-eh)/2:.1f}) scale({k:.5f}) translate({-x0:.1f},{y1:.1f})" fill="{fill}"><path d="{FN.to_d(E)}"/></g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{n}" height="{n}">{back}{g}</svg>'

def png(svg, path, w):
    subprocess.run(['rsvg-convert','-w',str(w),'-o',path],input=svg.encode(),check=True)
def main():
    os.makedirs(OUT,exist_ok=True); n=0
    for v in ('centre','right','logo'):
        s=x_header(v); open(f'{OUT}/hematite-x-header-{v}.svg','w').write(s)
        png(s,f'{OUT}/hematite-x-header-{v}-1500x500.png',1500); png(s,f'{OUT}/hematite-x-header-{v}-3000x1000.png',3000); n+=3
    for v in ('night','iron','steel'):
        s=avatar(v); open(f'{OUT}/hematite-avatar-{v}.svg','w').write(s)
        png(s,f'{OUT}/hematite-avatar-{v}-400.png',400); png(s,f'{OUT}/hematite-avatar-{v}-1000.png',1000); n+=3
    print(n,'files ->',OUT)
if __name__=='__main__': main()
