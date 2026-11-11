"""Exports the locked hematite logo files into brand/ (one level above process/)."""
import os, subprocess, io
import final as FN
from PIL import Image
ROOT=os.environ.get('BRAND', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')))
COL={'steel':'#C4D4E0','iron':'#2E3A46','black':'#000000','white':'#FFFFFF'}
NIGHT='#09090B'; HAZE='#8A9BAB'
PX1={'emblem':512,'wordmark':128,'horizontal':160,'stacked':400}   # 1x heights in px

def layouts():
    W,w=FN.wordmark_polys()
    E=FN.emblem_polys('grid')
    ex0,ey0,ex1,ey1=FN.bbox(E)
    out={'wordmark':W,'emblem':FN.transform(E,1,-ex0,-ey0)}
    # horizontal: emblem 820 units tall, its base 40 below the baseline, gap 0.36 x emblem width
    s=820/(ey1-ey0); ew=(ex1-ex0)*s
    Eh=FN.transform(E,s,-ex0*s,-ey0*s-40)
    gap=ew*0.36
    out['horizontal']=Eh+FN.transform(W,1,ew+gap,0)
    # stacked: emblem 1155 units tall, centred over the wordmark, 180 above the ascender line (770)
    wx0,wy0,wx1,wy1=FN.bbox(W)
    s2=1155/(ey1-ey0); ew2=(ex1-ex0)*s2
    out['stacked']=FN.transform(E,s2,-ex0*s2+(wx0+wx1)/2-ew2/2,-ey0*s2+770+180)+W
    return out

def svg(polys, fill, h_px=None, pad=0, bg=None):
    x0,y0,x1,y1=FN.bbox(polys); w=x1-x0+2*pad; h=y1-y0+2*pad
    size=f' width="{w*h_px/h:.1f}" height="{h_px}"' if h_px else ''
    rect=f'<rect x="{x0-pad:.1f}" y="{-y1-pad:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0-pad:.1f} {-y1-pad:.1f} {w:.1f} {h:.1f}"{size}>{rect}<path d="{FN.to_d(polys)}" fill="{fill}"/></svg>'
def png(svgtext, path, h=None, w=None):
    args=['rsvg-convert']+(['-h',str(h)] if h else [])+(['-w',str(w)] if w else [])+['-o',path]
    subprocess.run(args,input=svgtext.encode(),check=True)
def mk(p): os.makedirs(p,exist_ok=True); return p

def main():
    L=layouts(); n=0
    for name,polys in L.items():
        for cw,fill in COL.items():
            base=f'hematite-{name}-{cw}'
            s=svg(polys,fill,PX1[name])
            open(os.path.join(mk(f'{ROOT}/{name}/svg'),base+'.svg'),'w').write(svg(polys,fill)); n+=1
            for k in (1,2,3,4):
                suf='' if k==1 else f'@{k}x'
                png(s,os.path.join(mk(f'{ROOT}/{name}/png/{k}x'),base+suf+'.png'),h=PX1[name]*k); n+=1
    # favicons: small-size cut (wider cleft) up to 48 px
    small=FN.emblem_polys('grid',11.0); big=FN.emblem_polys('grid')
    fav=mk(f'{ROOT}/favicon')
    def square(polys, size, fill, bg=None, scale=0.84, rounded=0):
        x0,y0,x1,y1=FN.bbox(polys); h=y1-y0; w=x1-x0; S=h/scale
        cx=(x0+x1)/2; cy=(y0+y1)/2
        r=f'<rect x="{cx-S/2:.2f}" y="{-cy-S/2:.2f}" width="{S:.2f}" height="{S:.2f}" rx="{S*rounded:.2f}" fill="{bg}"/>' if bg else ''
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx-S/2:.2f} {-cy-S/2:.2f} {S:.2f} {S:.2f}" width="{size}" height="{size}">{r}<path d="{FN.to_d(polys,2)}" fill="{fill}"/></svg>'
    # adaptive SVG favicon: iron on light tabs, steel on dark tabs
    x0,y0,x1,y1=FN.bbox(small); Sq=(y1-y0)/0.92; cx=(x0+x1)/2; cy=(y0+y1)/2
    open(f'{fav}/favicon.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx-Sq/2:.2f} {-cy-Sq/2:.2f} {Sq:.2f} {Sq:.2f}"><style>path{{fill:{COL["iron"]}}}@media (prefers-color-scheme:dark){{path{{fill:{COL["steel"]}}}}}</style><path d="{FN.to_d(small,2)}"/></svg>'); n+=1
    ico=[]
    for sz in (16,32,48,64,96,128):
        polys=small if sz<=48 else big
        p=f'{fav}/favicon-{sz}.png'; png(square(polys,sz,HAZE,scale=0.92),p,w=sz,h=sz); n+=1
        if sz<=48: ico.append(Image.open(p).convert('RGBA'))
    ico[-1].save(f'{fav}/favicon.ico',sizes=[(16,16),(32,32),(48,48)],append_images=ico[:-1]); n+=1
    for name,sz in (('apple-touch-icon',180),('android-chrome-192',192),('android-chrome-512',512)):
        png(square(big,sz,COL['steel'],bg=NIGHT,scale=0.62),f'{fav}/{name}.png',w=sz,h=sz); n+=1
    app=mk(f'{ROOT}/app-icon')
    for bgname,bg,fill in (('night',NIGHT,COL['steel']),('steel',COL['steel'],COL['iron'])):
        png(square(big,1024,fill,bg=bg,scale=0.6),f'{app}/hematite-app-icon-{bgname}-1024.png',w=1024,h=1024); n+=1
        png(square(big,1024,fill,bg=bg,scale=0.6,rounded=0.225),f'{app}/hematite-app-icon-{bgname}-rounded-1024.png',w=1024,h=1024); n+=1
    print(n,'files ->',ROOT)
if __name__=='__main__': main()
