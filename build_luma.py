"""LUMA GALLERIA — original architectural concept, metres, Y-up.
One shared layout creates the editable GLB, scene JSON and matching SVG plan.
No surveyed reconstruction or engineering certification is implied.
Python 3.9+; no third-party dependencies.
"""
import math,json,struct,pathlib
P=pathlib.Path(__file__).parent
objects=[];rooms=[];fronts=[];signs=[]
materials={
 'limestone':([.50,.46,.37,1],.9,0), 'stone_light':([.64,.60,.50,1],.9,0),
 'bronze':([.22,.14,.065,1],.37,.65), 'charcoal':([.075,.105,.105,1],.62,.3),
 'terrazzo':([.82,.82,.77,1],.85,0), 'oak':([.55,.36,.19,1],.72,0),
 'glass':([.54,.78,.81,.25],.08,.1), 'roof_glass':([.21,.48,.56,.42],.13,.15),
 'solar':([.035,.065,.09,1],.25,.45), 'roof_metal':([.20,.27,.26,1],.6,.35), 'water':([.14,.51,.54,.78],.13,.3), 'leaf':([.055,.18,.065,1],.95,0),
 'leaf_light':([.12,.27,.09,1],1,0), 'soil':([.18,.14,.10,1],1,0),
 'text':([.90,.81,.61,1],.45,.15), 'white':([.94,.93,.87,1],.7,0),
 'seat':([.33,.39,.36,1],.85,0), 'paving':([.65,.68,.64,1],1,0),
 'path':([.79,.78,.70,1],1,0), 'grass':([.17,.25,.13,1],1,0),
 'light':([1,.77,.39,1],.3,0), 'clay':([.62,.38,.26,1],.9,0),
 'shop_blue':([.36,.51,.54,1],.7,0), 'shop_rose':([.61,.43,.39,1],.8,0)
}
def obj(name,pos,size,mat='limestone',cat='interior',shape='cube',rot=None,unit=None):
    o=dict(name=name,position=pos,size=size,material=mat,category=cat,shape=shape,rotation=rot or [0,0,0])
    if unit:o['unit']=unit
    objects.append(o)
def box(n,x,y,z,w,h,d,m='limestone',c='interior',rot=None,unit=None):obj(n,[x,y,z],[w,h,d],m,c,rot=rot,unit=unit)
def cyl(n,x,y,z,r,h,m='bronze',c='interior'):obj(n,[x,y,z],[r*2,h,r*2],m,c,'cylinder')
def ball(n,x,y,z,r,m='leaf',c='site'):obj(n,[x,y,z],[r*2,r*2,r*2],m,c,'sphere')
def beam(n,a,b,r=.10,m='bronze',cat='roof'):
    # Local Y cylinder rotates about X then Z to match segment.
    dx=b[0]-a[0];dy=b[1]-a[1];dz=b[2]-a[2];l=math.sqrt(dx*dx+dy*dy+dz*dz)
    rot=[math.atan2(dz,math.sqrt(dx*dx+dy*dy)),0,-math.atan2(dx,dy)]
    obj(n,[(a[i]+b[i])/2 for i in range(3)],[r*2,l,r*2],m,cat,'cylinder',rot)
def sign(text,x,y,z,width,rotation=0,cat='signage'):
    signs.append(dict(text=text,position=[x,y,z],width=width,rotation=rotation,category=cat))
def wall(n,x1,z1,x2,z2,h=5.2,c='interior'):
    box(n,(x1+x2)/2,h/2,(z1+z2)/2,abs(x2-x1) or .22,h,abs(z2-z1) or .22,'limestone',c)
def tree(n,x,z,scale=1,cat='site'):
    cyl(n+' planter',x,.38,z,1.1*scale,.76,'stone_light',cat)
    cyl(n+' soil',x,.77,z,.95*scale,.025,'soil',cat)
    cyl(n+' trunk',x,2*scale,z,.13*scale,3*scale,'oak',cat)
    for i,(dx,dy,dz,r) in enumerate([(-.6,3.3,0,1.25),(.6,3.8,.2,1.30),(0,4.6,-.1,1.2)]):ball(n+' crown '+str(i),x+dx*scale,dy*scale,z+dz*scale,r*scale,'leaf_light' if i==2 else 'leaf',cat)
def bench(n,x,z,rotation=0,cat='furniture'):
    for i in range(5):box(n+' oak slat '+str(i),x,.52,z+(i-2)*.13,2.8,.09,.10,'oak',cat,rot=[0,rotation,0])
    for dx in [-1,1]:box(n+' base',x+dx,.25,z,.18,.5,.65,'charcoal',cat)
def storefront(n,x1,z1,x2,z2,unit):
    vertical=x1==x2;L=abs(z2-z1) if vertical else abs(x2-x1);cx=(x1+x2)/2;cz=(z1+z2)/2
    width=2.4; opening=L/2
    fronts.append(dict(unit=unit,a=[x1,z1],b=[x2,z2],door_center=[cx,cz],door_width=width))
    # Real transparent panes with double sliding-door leaves; bronze transoms/mullions.
    intervals=[(0,opening-width/2),(opening+width/2,L)]
    for j,(a,b) in enumerate(intervals):
        center=(a+b)/2
        box(n+' glazed pane '+str(j),cx if vertical else x1+center,2.15,z1+center if vertical else cz,.055 if vertical else b-a,4.2,b-a if vertical else .055,'glass','storefront',unit=unit)
    for j in [-1,1]:
        box(n+' sliding door '+str(j),cx if vertical else cx+j*.6,1.5,cz+j*.6 if vertical else cz,.06 if vertical else 1.18,3,1.18 if vertical else .06,'glass','storefront',unit=unit)
        box(n+' door pull '+str(j),cx+.07 if vertical else cx+j*.12,1.3,cz+j*.12 if vertical else cz+.07,.035,.45,.035,'bronze','details')
    for s in [0,opening-width/2,opening+width/2,L]:
        box(n+' bronze mullion',cx if vertical else x1+s,2.2,z1+s if vertical else cz,.1,4.4,.1,'bronze','storefront')
    for height in [.05,3.05,4.3]:box(n+' bronze transom',cx,height,cz,.12 if vertical else L,.085,L if vertical else .12,'bronze','storefront')
    box(n+' fascia',cx,4.75,cz,.22 if vertical else L,.80,L if vertical else .22,'charcoal','storefront')
    box(n+' warm lintel light',cx,4.24,cz,.12 if vertical else L-.2,.035,L-.2 if vertical else .12,'light','details')
    # Sign faces towards public gallery from the shop.
    if vertical:
        side=1 if x1 in [12,28] else -1
        sign(unit,cx+side*.14,4.6,cz,min(5.5,L-2),math.pi/2 if side>0 else -math.pi/2)
    else:sign(unit,cx,4.6,cz+.14,min(7,L-3),0)
def shop(name,rect,front,kind='retail',style='oak'):
    x1,z1,x2,z2=rect;rooms.append(dict(name=name,rect=rect,kind=kind,front=front))
    box(name+' floor',(x1+x2)/2,.035,(z1+z2)/2,x2-x1,.065,z2-z1,style,'floors',unit=name)
    for side,a,b in [('west',(x1,z1),(x1,z2)),('east',(x2,z1),(x2,z2)),('south',(x1,z1),(x2,z1)),('north',(x1,z2),(x2,z2))]:
        if side==front:storefront(name+' shopfront',*a,*b,name)
        elif a[0]==b[0] and a[0] in [0,74] and kind=='retail':
            x=a[0];L=z2-z1
            box(name+' exterior sill',x,1.66,(z1+z2)/2,.22,3.32,L,'limestone','exterior')
            box(name+' exterior header',x,4.97,(z1+z2)/2,.22,.46,L,'limestone','exterior')
            for z in [z1+.5,z2-.5]:box(name+' window stone jamb',x,4.03,z,.22,1.42,1,'limestone','exterior')
        else:wall(name+' '+side+' partition',*a,*b,c='exterior' if a[0]==b[0] and a[0] in [0,74] or a[1]==b[1] and a[1] in [0,100] else 'interior')
    if name=='THE GROVE':
        for a,b,c,d in [(0,89,1.2,100),(3.2,89,28,100),(1.2,89,3.2,97.8)]:box(name+' roof around hatch',(a+c)/2,5.32,(b+d)/2,c-a,.24,d-b,'roof_metal','roof')
        box('Maintenance access glazed hatch',2.2,5.43,98.9,2,.08,2.2,'roof_glass','roof')
    else:box(name+' roof',(x1+x2)/2,5.32,(z1+z2)/2,x2-x1+.18,.24,z2-z1+.18,'roof_metal','roof')
    # Retail fit-out is explicitly designed, with shelves and display islands.
    if kind=='retail':
        for z in [z1+2,z2-2]:
            box(name+' display plinth',(x1+x2)/2,.45,z,3,.9,1.35,'white','furniture')
            for dx in [-.8,0,.8]:box(name+' merchandise', (x1+x2)/2+dx,1.02,z,.45,.27,.6,'shop_blue' if style=='terrazzo' else 'shop_rose','furniture')
        bx=x1+1 if front=='east' else x2-1
        for y in [.6,1.25,1.9]:
            box(name+' wall shelf',bx,y,(z1+z2)/2,.65,.08,z2-z1-3,'oak','furniture')
            for z in range(int(z1)+3,int(z2)-2,2):box(name+' shelf product',bx,y+.17,z,.35,.25,.8,'white','furniture')
    elif kind=='dining':
        for x in [x1+5,x2-5]:
            for z in [z1+3,z2-3]:
                cyl(name+' table',x,.76,z,.85,.08,'oak','furniture')
                cyl(name+' table stem',x,.38,z,.09,.72,'charcoal','furniture')
                for dx in [-1.2,1.2]:box(name+' chair',x+dx,.45,z,.65,.85,.65,'seat','furniture')
    else:
        box(name+' reception',(x1+x2)/2,.55,(z1+z2)/2,3,1.1,1,'oak','furniture')

# 74 x 100 m one-level original scheme. Public spine and transverse gallery.
box('Site ground',37,-.36,42,110,.4,144,'grass','site')
box('Building foundation',37,-.12,50,74,.24,100,'charcoal','floors')
box('Continuous public terrazzo',37,.006,50,74,.025,100,'terrazzo','floors')
for x in [28,46]:box('Atrium inlaid bronze axis',x,.025,50,.08,.018,100,'bronze','details')
for z in [43,55]:box('Cross gallery inlay',37,.026,z,74,.018,.08,'bronze','details')
names=[['FORMA','ATELIER','NOMAD','ELEMENT'],['AURA','STUDIO 28','KIN','OBJECT'],['VERDE','MONO','FIELD','COMMON'],['LUMEN','COVE','ORA','THREAD']]
strips=[(0,12,'east','terrazzo'),(17,28,'east','oak'),(46,57,'west','oak'),(62,74,'west','terrazzo')]
for j,(x1,x2,front,style) in enumerate(strips):
    for i,(z1,z2) in enumerate([(17,30),(30,43),(55,72),(72,89)]):shop(names[j][i],[x1,z1,x2,z2],front,style=style)
shop('THE GROVE',[0,89,28,100],'east','dining')
shop('SOL TABLE',[46,89,74,100],'west','dining')
shop('GUEST SERVICES',[0,0,12,12],'north','services','terrazzo')
shop('RESTROOMS',[12,0,24,12],'north','services','terrazzo')
shop('MANAGEMENT',[50,0,62,12],'north','services','terrazzo')
shop('FAMILY LOUNGE',[62,0,74,12],'north','services','terrazzo')
# Front/back public facade and side cross-gallery entrances.
def facade(n,x1,z1,x2,z2,h=6.2,doors=False):
    vertical=x1==x2;L=abs(z2-z1) if vertical else abs(x2-x1);count=max(1,round(L/2.6))
    for i in range(count):
        a=L*i/count;b=L*(i+1)/count;center=(a+b)/2
        box(n+' glass bay '+str(i),x1 if vertical else x1+center,h/2,z1+center if vertical else z1,.07 if vertical else b-a-.10,h-.1,b-a-.10 if vertical else .07,'glass','exterior_glass')
    for i in range(count+1):box(n+' frame '+str(i),x1 if vertical else x1+L*i/count,h/2,z1+L*i/count if vertical else z1,.14,h,.14,'bronze','exterior')
    for y in [.05,3.1,h]:box(n+' transom',x1 if vertical else (x1+x2)/2,y,(z1+z2)/2 if vertical else z1,.17 if vertical else L,.14,L if vertical else .17,'bronze','exterior')
    if doors:
        cx=(x1+x2)/2;cz=(z1+z2)/2
        for k in [-1,1]:box(n+' entrance handle',cx+.09 if vertical else cx+k*.3,1.25,cz+k*.3 if vertical else cz-.09,.04,.8,.04,'bronze','details')
facade('Main south curtain wall',24,0,50,0,6.2,True)
facade('North dining lounge curtain wall',28,100,46,100,6.2,True)
facade('West cross gallery entrance',0,43,0,55,6.2,True)
facade('East cross gallery entrance',74,43,74,55,6.2,True)
# South public foyer ends, enclosing connection between amenities and shops.
facade('South west lobby strip',0,12,0,17,5.5)
facade('South east lobby strip',74,12,74,17,5.5)
box('Foyer west roof',12,5.55,14.5,24,.2,5,'roof_metal','roof')
box('Foyer east roof',62,5.55,14.5,24,.2,5,'roof_metal','roof')
for x in [26,48]:box('Entrance foyer glazed wing roof',x,6.2,8.5,4,.08,17,'roof_glass','roof')
# Exterior sandstone pilasters and clerestory ribbons across solid shop backs.
for x in [0,74]:
    for z in [17,30,43,55,72,89,100]:box('Exterior stone pilaster',x,2.7,z,.40,5.4,.40,'stone_light','exterior')
    for z1,z2 in [(17,30),(30,43),(55,72),(72,89)]:
        for y in [3.38,4.76]:box('Exterior clerestory transom',x+(-.15 if x==0 else .15),y,(z1+z2)/2,.08,.10,z2-z1-2,'bronze','exterior')
        for z in [z1+1,z2-1]:box('Exterior clerestory jamb',x+(-.15 if x==0 else .15),4.07,z,.08,1.4,.10,'bronze','exterior')
        box('Exterior clerestory glass',x+(-.20 if x==0 else .20),4.07,(z1+z2)/2,.06,1.30,z2-z1-2.1,'glass','exterior_glass')
        for y in [1.2,2.4,3.3]:box('Limestone horizontal joint',x+(-.12 if x==0 else .12),y,(z1+z2)/2,.016,.018,z2-z1-.4,'charcoal','exterior')
# Photovoltaic roof modules: a designed feature, not an energy performance claim.
for x in [6,68]:
    for z in [24,36,63,80]:
        for dx in [-1.7,1.7]:
            for dz in [-1.0,1.0]:
                box('Photovoltaic panel bronze border',x+dx,5.64,z+dz,3,.12,1.75,'charcoal','roof',rot=[-.12,0,0])
                box('Photovoltaic module',x+dx,5.72,z+dz,2.88,.018,1.6,'solar','roof',rot=[-.12,0,0])
                for cell in [-.7,0,.7]:box('Photovoltaic cell seam',x+dx+cell,5.74,z+dz,.015,.008,1.55,'bronze','roof',rot=[-.12,0,0])
# Designed restroom fittings and guest lounge furniture.
for x in [13.5,16.5,19.5,22.5]:
    cyl('WC pedestal',x,.25,2.4,.28,.5,'white','furniture');cyl('WC bowl',x,.58,2.4,.42,.20,'white','furniture')
    box('WC tank',x,.8,1.9,.65,.65,.25,'white','furniture')
    if x<22.5:box('Restroom stall partition',x+1.5,1.1,2.5,.1,2.2,4,'stone_light','furniture')
    box('Restroom cubicle door',x,1.0,4.5,2.5,2,.08,'oak','furniture')
box('Restroom vanity',18,.65,8.4,9,1.3,.8,'stone_light','furniture')
for x in [14.5,18,21.5]:cyl('Restroom basin',x,1.36,8.4,.32,.1,'white','furniture')
box('Family lounge sofa',68,.55,4.2,6,1.1,1.2,'seat','furniture')
box('Family lounge low table',68,.36,6.5,2.8,.72,1.2,'oak','furniture')
# Main gabled glass atrium roof; real panels, purlins, ribs, ridge caps and columns.
eaves=6.2;ridge=9.0;half=9.0;pitch=math.atan2(ridge-eaves,half);slant=math.hypot(half,ridge-eaves)
for side in [-1,1]:
    x=37+side*half/2
    for j in range(20):
        box('Atrium glazed roof panel '+str(side)+'-'+str(j),x,(eaves+ridge)/2,j*5+2.5,slant-.08,.08,4.86,'roof_glass','roof',rot=[0,0,-side*pitch])
    for offset in [0,3,6,9]:
        xx=37+side*offset;yy=ridge-(ridge-eaves)*offset/half
        box('Longitudinal atrium purlin',xx,yy,50,.085,.12,100,'bronze','roof')
for z in range(0,101,10):
    beam('Atrium rafter west',[28,eaves,z],[37,ridge,z],.075)
    beam('Atrium rafter east',[37,ridge,z],[46,eaves,z],.075)
    beam('Atrium roof tie',[28,eaves-.1,z],[46,eaves-.1,z],.045)
    for x in [28,46]:cyl('Atrium bronze column',x,eaves/2,z,.15,eaves,'bronze','columns')
box('Atrium ridge cap',37,9.04,50,.2,.18,100,'bronze','roof')
# Gable end triangular glazing is a real triangle mesh, plus sloped frame.
for z in [0,100]:
    objects.append(dict(name='Glazed gable end',position=[0,0,0],size=[1,1,1],material='glass',category='exterior_glass',shape='gable',rotation=[0,0,0],points=[[28,6.2,z],[46,6.2,z],[37,9,z]]))
    beam('Gable edge',[28,6.2,z],[37,9,z],.075,'bronze','exterior');beam('Gable edge',[37,9,z],[46,6.2,z],.075,'bronze','exterior')
# Cross gallery gable roof arms meet the continuous central atrium.
for x1,x2 in [(0,28),(46,74)]:
    for side in [-1,1]:
        dz=3;rise=1.8;sl=math.hypot(6,rise);p=math.atan2(rise,6)
        for j in range(7):box('Cross-gallery glass roof',(x1+x2)/2 if False else x1+(j+.5)*(x2-x1)/7,7.1,49+side*3,(x2-x1)/7-.06,.07,sl,'roof_glass','roof',rot=[side*p,0,0])
        for x in [x1,x1+7,x1+14,x1+21,x2]:beam('Cross-gallery roof rib',[x,6.2,49+side*6],[x,8,49],.06)
    box('Cross-gallery ridge',(x1+x2)/2,8.05,49,x2-x1,.14,.17,'bronze','roof')
    for x in [x1,x2]:
        for z in [43,55]:cyl('Cross gallery column',x,3.1,z,.15,6.2,'bronze','columns')
# Glazed cross-gallery gable ends close the side entrance roof volumes.
for x in [0,74]:
    objects.append(dict(name='Cross-gallery glazed gable end',position=[0,0,0],size=[1,1,1],material='glass',category='exterior_glass',shape='gable',rotation=[0,0,0],points=[[x,6.2,43],[x,6.2,55],[x,8,49]]))
    beam('Cross-gallery gable frame',[x,6.2,43],[x,8,49],.06,'bronze','exterior')
    beam('Cross-gallery gable frame',[x,8,49],[x,6.2,55],.06,'bronze','exterior')
# Daylight ribbons over secondary galleries; no opaque roof across circulation.
for x in [14.5,59.5]:
    for z1,z2 in [(17,43),(55,89)]:
        box('Secondary-gallery skylight ribbon',x,5.8,(z1+z2)/2,5,.07,z2-z1,'roof_glass','roof')
        for z in range(z1,z2+1,4):box('Ribbon roof bronze rib',x,5.85,z,5,.1,.10,'bronze','roof')
        for dx in [-2.5,2.5]:box('Ribbon roof edge',x+dx,5.8,(z1+z2)/2,.12,.15,z2-z1,'bronze','roof')
# Glazed roof upstands and perimeter parapets enclose the complete shell.
for x in [28,46]:
    for z1,z2 in [(17,43),(55,89)]:box('Atrium glazed clerestory upstand',x,5.7,(z1+z2)/2,.06,1.0,z2-z1,'roof_glass','roof')
for z in [43,55]:
    for x1,x2 in [(0,28),(46,74)]:box('Cross-gallery glazed clerestory upstand',(x1+x2)/2,5.7,z,x2-x1,1,.06,'roof_glass','roof')
for x in [12,17,57,62]:
    for z1,z2 in [(17,43),(55,89)]:box('Secondary glazed roof upstand',x,5.5,(z1+z2)/2,.06,.6,z2-z1,'roof_glass','roof')
for x in [0,74]:
    for z1,z2 in [(0,43),(55,100)]:box('Limestone roof parapet',x,5.48,(z1+z2)/2,.35,.58,z2-z1,'stone_light','roof')
for z in [0,100]:
    for x1,x2 in [(0,24 if z==0 else 28),(50 if z==0 else 46,74)]:box('End roof parapet',(x1+x2)/2,5.48,z,x2-x1,.58,.35,'stone_light','roof')
# Entrance canopy and sculptural masonry portals.
box('Entrance canopy floating bronze plate',37,4.95,-3.2,30,.28,6.4,'charcoal','roof')
for x in [22,52]:
    box('Entrance limestone pier',x,2.45,-4.8,.65,4.9,.65,'stone_light','exterior')
    box('Entrance canopy warm soffit line',x,4.78,-3.2,.045,.04,5.8,'light','roof')
box('Entrance stone sign band',37,5.72,-.20,26,.78,.38,'stone_light','exterior')
sign('LUMA GALLERIA',37,5.54,-.44,18,math.pi)
sign('A PLACE TO GATHER',37,3.75,-3.12,9,math.pi)
# North patios and exterior dining furniture; structural entrances remain clear.
for x1,x2 in [(2,27),(47,72)]:
    box('North restaurant terrace',(x1+x2)/2,-.025,106.5,x2-x1,.13,13,'paving','site')
    for x in [x1+5,x2-5]:
        for z in [104,109]:
            cyl('Terrace cafe table',x,.75,z,.9,.1,'oak','site');cyl('Terrace table stem',x,.36,z,.08,.7,'bronze','site')
            for dx in [-1.2,1.2]:box('Terrace cafe seat',x+dx,.45,z,.65,.85,.65,'seat','site')
            cyl('Terrace parasol mast',x,1.65,z,.04,3.3,'bronze','site')
            obj('Terrace parasol',[x,3.1,z],[4,.55,4],'white','site','cone')
# A landscaped urban forecourt, entry steps, paths, bollards and seat walls.
box('Main entrance plaza',37,-.05,-11,82,.15,22,'paving','site')
box('Entry approach stone runner',37,.02,-10,19,.05,20,'path','site')
for x in range(-2,79,4):box('Forecourt paver joint',x,.033,-11,.015,.008,22,'charcoal','site')
for z in range(-20,1,4):box('Forecourt paver joint',37,.033,z,82,.008,.015,'charcoal','site')
for x in [10,64]:
    box('Raised forecourt planting bed',x,.25,-11,11,.5,6,'stone_light','site')
    box('Planting bed soil',x,.51,-11,10.5,.025,5.5,'soil','site')
    for dx in [-3,3]:tree('Forecourt tree',x+dx,-11,.95)
    bench('Forecourt bench',x,-6.8,cat='site')
for x in [25,49]:
    for z in [-13,-7]:cyl('Entry bollard',x,.55,z,.10,1.1,'bronze','site')
for x in [-6,80]:
    box('Side entrance path',x,-.03,49,12,.12,16,'path','site')
    for z in [23,38,61,78,94]:tree('Perimeter tree',x,z,.9)
# Public atrium landscape, benches, water and café kiosks.
for x in [31.5,42.5]:
    for z in [24,68,84]:tree('Atrium olive',x,z,.65,'furniture')
    for z in [31,76]:bench('Atrium bench',x,z)
cyl('Atrium fountain limestone basin',37,.28,49,3,.55,'stone_light','furniture')
cyl('Atrium reflecting water',37,.58,49,2.75,.035,'water','furniture')
cyl('Fountain sculpture bronze base',37,.85,49,.5,.65,'bronze','furniture')
for i in range(3):beam('Sculpture rising bronze stem',[37,1,49],[36.1+i*.9,3.7+i*.5,49],.09,'bronze','furniture')
for x in [7,67]:
    box('Cross-gallery coffee kiosk',x,.7,49,4,1.4,2.4,'oak','furniture')
    box('Kiosk stone counter',x,1.45,49,4.2,.12,2.55,'stone_light','furniture')
    for dx in [-1,1]:cyl('Kiosk stool',x+dx,.45,51.2,.3,.9,'seat','furniture')
# Operational single-level lifts and an architectural stair to an unmodeled future level.
# Stair explicitly represents a concept feature; no disconnected usable upper floor claimed.
for x in [25.1,48.9]:
    box('Glazed lift enclosure',x,2.45,8,2.3,4.9,3.2,'glass','vertical')
    for dx in [-1.15,1.15]:box('Lift enclosure frame',x+dx,2.5,8,.08,5,3.2,'bronze','vertical')
    box('Lift back panel',x,2.3,9.55,2.15,4.6,.08,'charcoal','vertical')
    box('Lift doors',x,1.35,6.37,1.8,2.7,.07,'bronze','vertical')
# North-west maintenance stair sits within north dining room rear corner.
for i in range(28):box('Roof maintenance stair tread '+str(i+1),2.2,.095*(i+1),89.65+i*.35,2,.19*(i+1),.35,'charcoal','vertical')
for x in [1.1,3.3]:beam('Maintenance stair railing',[x,1,89.65],[x,6.3,99.1],.025,'bronze','vertical')
sign('DINING GARDEN',37,5.6,98.7,10,0)
sign('WEST GALLERY',8,4.8,49,7,math.pi/2)
sign('EAST GALLERY',66,4.8,49,7,-math.pi/2)

layout=dict(project='LUMA GALLERIA',design_status='Original architectural concept inspired by supplied mall plan; chosen dimensions, not surveyed reconstruction',units='metres',axes='X east, Y up, Z north',building_size=[74,100],floor_levels=[0],rooms=rooms,storefronts=fronts,signs=signs,objects=objects,public_spaces=[dict(name='Skylit atrium',rect=[28,0,46,100]),dict(name='Cross gallery',rect=[0,43,74,55]),dict(name='West gallery',rect=[12,17,17,89]),dict(name='East gallery',rect=[57,17,62,89]),dict(name='Entrance foyer',rect=[24,0,50,17])])
(P/'luma-layout.json').write_text(json.dumps(layout,indent=2))

# Geometry library with indexed triangles and per-vertex normals.
geos={}
def geo_cube():
    verts=[];norms=[];ids=[]
    fs=[([1,0,0],[[.5,-.5,-.5],[.5,.5,-.5],[.5,.5,.5],[.5,-.5,.5]]),([-1,0,0],[[-.5,-.5,.5],[-.5,.5,.5],[-.5,.5,-.5],[-.5,-.5,-.5]]),([0,1,0],[[-.5,.5,-.5],[-.5,.5,.5],[.5,.5,.5],[.5,.5,-.5]]),([0,-1,0],[[-.5,-.5,.5],[-.5,-.5,-.5],[.5,-.5,-.5],[.5,-.5,.5]]),([0,0,1],[[.5,-.5,.5],[.5,.5,.5],[-.5,.5,.5],[-.5,-.5,.5]]),([0,0,-1],[[-.5,-.5,-.5],[-.5,.5,-.5],[.5,.5,-.5],[.5,-.5,-.5]])]
    for n,vs in fs:
        s=len(verts)//3
        for v in vs:verts.extend(v);norms.extend(n)
        ids.extend([s,s+1,s+2,s,s+2,s+3])
    return verts,norms,ids
geos['cube']=geo_cube()
def geo_round(shape,N=20,M=12):
    vs=[];ns=[];ids=[]
    if shape=='sphere':
        for j in range(M+1):
            t=math.pi*j/M
            for i in range(N+1):
                a=2*math.pi*i/N;n=[math.sin(t)*math.cos(a),math.cos(t),math.sin(t)*math.sin(a)];vs.extend([q*.5 for q in n]);ns.extend(n)
        for j in range(M):
            for i in range(N):
                a=j*(N+1)+i;b=a+N+1
                if j>0:ids.extend([a,a+1,b])
                if j<M-1:ids.extend([a+1,b+1,b])
    else:
        for j,y in enumerate([-.5,.5]):
            r=.5 if shape=='cylinder' or j==0 else .03
            for i in range(N+1):
                a=2*math.pi*i/N;vs.extend([r*math.cos(a),y,r*math.sin(a)]);ns.extend([math.cos(a),0,math.sin(a)])
        for i in range(N):a=i;b=i+N+1;ids.extend([a,b,a+1,a+1,b,b+1])
        for j,y in enumerate([-.5,.5]):
            c=len(vs)//3;vs.extend([0,y,0]);ns.extend([0,-1 if j==0 else 1,0]);r=.5 if shape=='cylinder' or j==0 else .03
            for i in range(N+1):
                a=2*math.pi*i/N;vs.extend([r*math.cos(a),y,r*math.sin(a)]);ns.extend([0,-1 if j==0 else 1,0])
            for i in range(N):ids.extend([c,c+i+1,c+i+2] if j==0 else [c,c+i+2,c+i+1])
    return vs,ns,ids
for s in ['cylinder','sphere','cone']:geos[s]=geo_round(s)
for i,o in enumerate(objects):
    if o['shape']=='gable':
        name='gable'+str(i);o['shape']=name;points=o.pop('points');a=[points[1][j]-points[0][j] for j in range(3)];b=[points[2][j]-points[0][j] for j in range(3)];n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];l=math.sqrt(sum(v*v for v in n));geos[name]=([v for p in points for v in p],[v/l for v in n]*3,[0,1,2])
buf=b'';views=[];acs=[]
def accessor(vals,fmt,typ,ct):
    global buf
    buf+=b'\0'*((-len(buf))%4);off=len(buf);raw=struct.pack('<'+fmt*len(vals),*vals);buf+=raw;views.append(dict(buffer=0,byteOffset=off,byteLength=len(raw)))
    a=dict(bufferView=len(views)-1,componentType=ct,count=len(vals)//(3 if typ=='VEC3' else 1),type=typ)
    if typ=='VEC3':a.update(min=[min(vals[i::3]) for i in range(3)],max=[max(vals[i::3]) for i in range(3)])
    acs.append(a);return len(acs)-1
ga={k:(accessor(v,'f','VEC3',5126),accessor(n,'f','VEC3',5126),accessor(ix,'H','SCALAR',5123)) for k,(v,n,ix) in geos.items()}
matkeys=list(materials);mats=[]
for k,(color,rough,metal) in materials.items():
    m=dict(name=k,pbrMetallicRoughness=dict(baseColorFactor=color,roughnessFactor=rough,metallicFactor=metal))
    if color[3]<1:m.update(alphaMode='BLEND',doubleSided=True)
    if k=='light':m['emissiveFactor']=[1,.55,.14]
    mats.append(m)
meshdefs=[];meshmap={}
for o in objects:
    key=(o['shape'],o['material'])
    if key not in meshmap:
        a,n,i=ga[key[0]];meshmap[key]=len(meshdefs);meshdefs.append(dict(name=key[0]+' / '+key[1],primitives=[dict(attributes=dict(POSITION=a,NORMAL=n),indices=i,material=matkeys.index(key[1]))]))
def quat(e):
    x,y,z=[v/2 for v in e];c1,c2,c3=math.cos(x),math.cos(y),math.cos(z);s1,s2,s3=math.sin(x),math.sin(y),math.sin(z)
    return [s1*c2*c3+c1*s2*s3,c1*s2*c3-s1*c2*s3,c1*c2*s3+s1*s2*c3,c1*c2*c3-s1*s2*s3]
nodes=[];cats={}
for o in objects:
    nodes.append(dict(name=o['name'],mesh=meshmap[(o['shape'],o['material'])],translation=o['position'],scale=o['size'],rotation=quat(o['rotation']),extras=dict(category=o['category'],unit=o.get('unit'))))
    cats.setdefault(o['category'],[]).append(len(nodes)-1)
roots=[]
for cat,children in cats.items():roots.append(len(nodes));nodes.append(dict(name=cat.upper(),children=children,extras=dict(category=cat)))
buf+=b'\0'*((-len(buf))%4)
g=dict(asset=dict(version='2.0',generator='LUMA shared-layout concept builder',extras=dict(units='metres',design_status=layout['design_status'])),scene=0,scenes=[dict(name='LUMA GALLERIA',nodes=roots)],nodes=nodes,meshes=meshdefs,materials=mats,buffers=[dict(byteLength=len(buf))],bufferViews=views,accessors=acs)
js=json.dumps(g,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
blob=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(buf))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(buf),0x004e4942)+buf
(P/'luma-base.glb').write_bytes(blob)

# SVG floor plan from the same metre-based room bounds and storefronts.
W=1200;H=1550;s=10;ox=180;oy=220
def xy(x,z):return ox+x*s,oy+(100-z)*s
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1550" viewBox="0 0 1200 1550">','<rect width="1200" height="1550" fill="#f3f1e9"/>','<style>text{font-family:Arial,sans-serif}.unit{font-size:12px;font-weight:600;letter-spacing:.6px}.dim{font-size:14px;fill:#68756d}.caption{font-size:13px;fill:#68756d}.small{font-size:10px;fill:#68756d}</style>','<text x="100" y="72" font-size="12" letter-spacing="4" fill="#607568">ORIGINAL ARCHITECTURAL CONCEPT</text>','<text x="100" y="120" font-size="39" fill="#233d32" letter-spacing="-1">LUMA GALLERIA</text>','<text x="100" y="153" class="caption">01 / GROUND FLOOR     •     74 × 100 m concept footprint     •     all dimensions in metres</text>']
def rect(x,z,w,d,fill,stroke='none',sw=1):
    px,py=xy(x,z+d);svg.append(f'<rect x="{px}" y="{py}" width="{w*s}" height="{d*s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(x1,z1,x2,z2,color='#555e55',sw=2,dash=None):
    a,b=xy(x1,z1),xy(x2,z2);svg.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{color}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def text(txt,x,z,cls='unit',color='#34473d'):
    px,py=xy(x,z);svg.append(f'<text x="{px}" y="{py}" text-anchor="middle" class="{cls}" fill="{color}">{txt}</text>')
rect(-4,-18,82,18,'#dadcd1');rect(0,0,74,100,'#ecece4','#596c5f',3)
rect(28,0,18,100,'#dde9e1');rect(0,43,74,12,'#dde9e1');rect(12,17,5,72,'#e6ebe5');rect(57,17,5,72,'#e6ebe5')
for r in rooms:
    x1,z1,x2,z2=r['rect'];fill='#d9d0bd' if r['kind']=='retail' else '#c5d4bd' if r['kind']=='dining' else '#d3d9df'
    rect(x1,z1,x2-x1,z2-z1,fill,'#626b61',2.3)
    text(r['name'],(x1+x2)/2,(z1+z2)/2+1)
    text(f'{(x2-x1)*(z2-z1):.0f} m²',(x1+x2)/2,(z1+z2)/2-1,'small')
for f in fronts:
    (x1,z1),(x2,z2)=f['a'],f['b'];line(x1,z1,x2,z2,'#67949b',3)
    cx,cz=f['door_center'];w=f['door_width']/2
    if x1==x2:
        line(cx,cz-w,cx,cz+w,'#f3f1e9',4);line(cx,cz-w,cx+1.2,cz-w,'#aa8855',1.5);line(cx,cz+w,cx+1.2,cz+w,'#aa8855',1.5)
    else:line(cx-w,cz,cx+w,cz,'#f3f1e9',4);line(cx-w,cz,cx-w,cz-1.2,'#aa8855',1.5);line(cx+w,cz,cx+w,cz-1.2,'#aa8855',1.5)
for x in [28,46]:
    for z in range(0,101,10):
        px,py=xy(x,z);svg.append(f'<circle cx="{px}" cy="{py}" r="3" fill="#92764c"/>')
for x in [31.5,42.5]:
    for z in [24,68,84]:
        px,py=xy(x,z);svg.append(f'<circle cx="{px}" cy="{py}" r="9" fill="#9aaf85" stroke="#658163"/>')
px,py=xy(37,49);svg.append(f'<circle cx="{px}" cy="{py}" r="30" fill="#8eb8b4" stroke="#8c9989" stroke-width="3"/>');text('WATER COURT',37,44.5,'small')
text('SKYLIT ATRIUM',37,61);text('18 m public spine',37,58.5,'small');text('ENTRANCE FOYER',37,14);text('DINING LOUNGE',37,94);text('WEST GALLERY',7,48);text('EAST GALLERY',67,48)
for x in [25.1,48.9]:rect(x-1.15,6.4,2.3,3.2,'#97a9ac','#546e6f',1);text('LIFT',x,8,'small')
for i in range(28):rect(1.2,89.475+i*.35,2,.35,'none','#68706c',.6)
rect(22,-6.4,30,6.4,'none','#937747',1);line(22,-6.4,52,-6.4,'#937747',1,'5 5');text('ENTRANCE CANOPY / FORECOURT',37,-10)
for x in [7,13,61,67]:
    px,py=xy(x,-11);svg.append(f'<circle cx="{px}" cy="{py}" r="15" fill="#9fb08d"/>')
# Public exterior glass and entrance thresholds agree with the 3D facade positions.
for a,b in [((24,0),(50,0)),((28,100),(46,100)),((0,43),(0,55)),((74,43),(74,55))]:line(*a,*b,'#67949b',3)
for cx,cz,vertical in [(37,0,False),(37,100,False),(0,49,True),(74,49,True)]:
    if vertical:line(cx,cz-1.6,cx,cz+1.6,'#f3f1e9',4)
    else:line(cx-2.4,cz,cx+2.4,cz,'#f3f1e9',4)
# Concept dimension chains and labelled widths, derived from model bounds.
line(0,104,74,104,'#8c968b',1)
for x in [0,12,17,28,46,57,62,74]:line(x,102,x,105,'#8c968b',1)
for a,b in zip([0,12,17,28,46,57,62],[12,17,28,46,57,62,74]):text(f'{b-a:.0f}',(a+b)/2,105,'dim')
text('74.0 m',(0+74)/2,112,'dim');line(-6,0,-6,100,'#8c968b',1);line(-8,0,-3,0,'#8c968b',1);line(-8,100,-3,100,'#8c968b',1)
px,py=xy(-9,50);svg.append(f'<text x="{px}" y="{py}" class="dim" text-anchor="middle" transform="rotate(-90 {px} {py})">100.0 m</text>')
svg.extend(['<path d="M1050 240 L1050 180 L1042 199 M1050 180 L1058 199" fill="none" stroke="#345343" stroke-width="2"/>','<text x="1050" y="163" text-anchor="middle" class="unit">N</text>','<text x="100" y="1410" class="caption">Retail  /  Dining  /  Guest amenities  /  Glass storefronts  /  Atrium landscape</text>','<text x="100" y="1450" class="caption">Chosen concept dimensions. Not a measured reconstruction of the supplied image.</text>','<text x="100" y="1474" class="caption">Single occupied level + designed skylight roof. Structural, accessibility and services design remain conceptual.</text>','<path d="M850 1410 H1050 M850 1405 V1415 M950 1405 V1415 M1050 1405 V1415" stroke="#345343" stroke-width="2"/>','<text x="850" y="1432" class="small">0</text><text x="950" y="1432" class="small">10</text><text x="1050" y="1432" class="small">20 m</text>','</svg>'])
(P/'luma-floorplan.svg').write_text('\n'.join(svg))
report=dict(project=layout['project'],rooms=len(rooms),storefronts=len(fronts),mesh_nodes=len(objects),categories={k:len(v) for k,v in cats.items()},building_footprint=[74,100],roof_ridge_height=9.0,units='metres; chosen original concept dimensions',all_dimensions_positive=all(all(n>0 for n in o['size']) for o in objects),glb_bytes=len(blob),source_plan_status='inspiration only; initial traced model preserved in preliminary/')
(P/'luma-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
