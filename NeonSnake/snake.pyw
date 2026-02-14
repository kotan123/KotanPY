import pygame
import sys
import random
import math
import json
import os
import array
from collections import deque

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# ── CONSTANTS ─────────────────────────────────────────────────────────────
CELL = 26
COLS, ROWS = 28, 23
SIDEBAR_W = 230
FIELD_W, FIELD_H = COLS * CELL, ROWS * CELL
WIDTH, HEIGHT = FIELD_W + SIDEBAR_W, FIELD_H
FPS = 60
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savedata.json")

# ── 10 THEMES ─────────────────────────────────────────────────────────────
def T(name, bg, grid, sh, sb, so, food, fs, bonus, wall, sbg, sbrd, txt, acc, dng, gold, silver, parts):
    return {"name":name,"bg":bg,"grid":grid,"snake_head":sh,"snake_body":sb,"snake_outline":so,
            "food":food,"food_shine":fs,"bonus":bonus,"wall":wall,"sidebar_bg":sbg,
            "sidebar_border":sbrd,"text":txt,"accent":acc,"danger":dng,"gold":gold,
            "silver":silver,"particles":parts}

THEMES = {
    "neon":      T("Neon",      (8,8,28),   (18,18,45),  (0,255,130),  (0,200,100),  (0,60,35),    (255,50,80),  (255,150,170),(255,215,0),  (70,70,120),  (12,12,38),  (0,255,130),  (220,220,255),(0,255,130),  (255,50,80),  (255,215,0),  (180,180,200),[(0,255,130),(255,50,80),(255,215,0),(0,180,255),(255,100,255)]),
    "cyberpunk": T("Cyberpunk", (15,5,25),  (30,10,45),  (255,0,200),  (180,0,150),  (80,0,60),    (0,255,255),  (150,255,255),(255,255,0),  (100,30,80),  (20,5,30),   (255,0,200),  (240,200,255),(255,0,200),  (255,60,60),  (255,255,0),  (200,180,220),[(255,0,200),(0,255,255),(255,255,0),(255,80,80),(200,0,255)]),
    "ocean":     T("Ocean",     (5,15,35),  (10,25,55),  (0,200,255),  (0,140,200),  (0,50,80),    (255,120,50), (255,180,130),(255,220,80), (40,80,120),  (5,12,32),   (0,200,255),  (200,230,255),(0,200,255),  (255,80,50),  (255,220,80), (160,190,210),[(0,200,255),(0,255,200),(255,120,50),(100,180,255),(0,255,150)]),
    "forest":    T("Forest",    (10,20,10), (18,35,18),  (120,255,60), (80,200,40),  (30,80,15),   (255,80,80),  (255,160,140),(255,200,50), (80,100,60),  (8,18,8),    (120,255,60), (210,240,200),(120,255,60), (255,80,80),  (255,200,50), (170,190,165),[(120,255,60),(255,200,50),(80,200,40),(200,255,100),(255,80,80)]),
    "retro":     T("Retro",     (20,12,28), (35,22,48),  (255,200,50), (220,160,30), (100,70,10),  (255,60,100), (255,140,170),(100,255,100),(100,70,110), (18,10,25),  (255,200,50), (255,230,200),(255,200,50), (255,60,100), (100,255,100),(200,180,170),[(255,200,50),(255,60,100),(100,255,100),(255,150,0),(200,100,255)]),
    "void":      T("Void",      (2,2,8),    (10,10,20),  (255,255,255),(160,160,180),(60,60,70),   (255,40,40),  (255,140,140),(255,200,0),  (50,50,60),   (4,4,12),    (255,255,255),(230,230,240),(255,255,255),(255,40,40),  (255,200,0),  (170,170,190),[(255,255,255),(255,40,40),(255,200,0),(140,140,180),(200,200,220)]),
    "sunset":    T("Sunset",    (25,8,15),  (40,15,25),  (255,140,0),  (255,100,0),  (120,50,0),   (255,50,120), (255,150,180),(255,230,80), (120,50,40),  (22,6,12),   (255,140,0),  (255,220,200),(255,140,0),  (255,50,120), (255,230,80), (200,170,160),[(255,140,0),(255,50,120),(255,230,80),(255,180,50),(255,80,180)]),
    "arctic":    T("Arctic",    (10,18,30), (18,28,45),  (130,220,255),(90,180,230), (40,80,110),  (255,100,100),(255,170,170),(200,255,200),(60,90,130),  (8,15,28),   (130,220,255),(220,235,255),(130,220,255),(255,100,100),(200,255,200),(180,200,220),[(130,220,255),(200,255,255),(255,100,100),(100,200,255),(180,230,255)]),
    "lavender":  T("Lavender",  (18,10,28), (30,18,45),  (180,120,255),(150,90,220), (70,40,110),  (255,180,80), (255,210,150),(120,255,180),(90,60,120),  (15,8,25),   (180,120,255),(230,215,255),(180,120,255),(255,100,80), (120,255,180),(190,175,210),[(180,120,255),(255,180,80),(120,255,180),(220,160,255),(255,120,200)]),
    "blood":     T("Blood",     (18,4,4),   (30,10,10),  (255,30,30),  (200,20,20),  (100,10,10),  (255,200,50), (255,230,150),(50,255,50),  (100,30,30),  (15,3,3),    (255,30,30),  (255,210,200),(255,30,30),  (255,200,50), (50,255,50),  (210,170,170),[(255,30,30),(255,100,50),(255,200,50),(200,50,50),(255,150,80)]),
}
THEME_ORDER = list(THEMES.keys())

current_theme_idx = 0
theme = dict(THEMES[THEME_ORDER[0]])

def set_theme(idx):
    global current_theme_idx, theme
    current_theme_idx = idx % len(THEME_ORDER)
    theme = dict(THEMES[THEME_ORDER[current_theme_idx]])

# ── DISPLAY ───────────────────────────────────────────────────────────────
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON SNAKE")
clock = pygame.time.Clock()

# ── FONTS — with fallback chain ───────────────────────────────────────────
def _pick_font(names, size, bold=False):
    """Try font names in order, return first that works (not default fallback)."""
    for name in names:
        f = pygame.font.SysFont(name, size, bold=bold)
        # Check it actually loaded (not the pygame default)
        if f.get_height() > 0:
            return f
    return pygame.font.SysFont(None, size, bold=bold)

_body_fonts = ["Segoe UI", "segoeui", "Arial", "Helvetica", "Verdana", "Tahoma"]
_mono_fonts = ["Consolas", "consolas", "Courier New", "Lucida Console", "monospace"]

font_xs    = _pick_font(_body_fonts, 16)
font_sm    = _pick_font(_body_fonts, 20)
font_md    = _pick_font(_body_fonts, 26, bold=True)
font_lg    = _pick_font(_body_fonts, 36, bold=True)
font_xl    = _pick_font(_body_fonts, 52, bold=True)
font_title = _pick_font(_body_fonts, 46, bold=True)
font_score = _pick_font(_mono_fonts, 34, bold=True)
font_hud   = _pick_font(_mono_fonts, 22)

# ── SOUNDS ────────────────────────────────────────────────────────────────
def _gen(freq, ms, vol=0.3, wave="square"):
    sr = 44100; n = int(sr*ms/1000); buf = array.array('h'); amp = int(32767*vol)
    for i in range(n):
        t = i/sr
        if wave == "square": v = amp if math.sin(2*math.pi*freq*t) >= 0 else -amp
        elif wave == "sine":  v = int(amp*math.sin(2*math.pi*freq*t))
        elif wave == "saw":   v = int(amp*(2*(freq*t%1)-1))
        else: v = 0
        v = int(v * min(1.0, (n-i)/(sr*0.05)))
        buf.append(v); buf.append(v)
    return pygame.mixer.Sound(buffer=buf)

snd_eat=_gen(600,80,0.2,"square"); snd_bonus=_gen(880,120,0.25,"sine")
snd_die=_gen(150,400,0.3,"saw");   snd_levelup=_gen(700,200,0.2,"sine")
snd_select=_gen(500,60,0.15,"square"); snd_powerup=_gen(1000,150,0.2,"sine")
snd_theme=_gen(440,100,0.12,"sine")

# ── SAVE / LOAD ───────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE,"r") as f: return json.load(f)
        except: pass
    return {"scores":{"classic":[],"walls":[],"speed":[]},"theme":0}

def save_data(d):
    try:
        with open(SAVE_FILE,"w") as f: json.dump(d,f)
    except: pass

def add_score(mode,score):
    d=load_data()
    if mode not in d["scores"]: d["scores"][mode]=[]
    d["scores"][mode].append(score)
    d["scores"][mode]=sorted(d["scores"][mode],reverse=True)[:10]
    save_data(d)

def save_theme(idx):
    d=load_data(); d["theme"]=idx; save_data(d)

_saved=load_data(); set_theme(_saved.get("theme",0))

# ── HELPERS ───────────────────────────────────────────────────────────────
def clamp(v,lo,hi): return max(lo,min(hi,v))
def lerp(a,b,t): return a+(b-a)*t
def lerp_color(c1,c2,t): return tuple(clamp(int(c1[i]*(1-t)+c2[i]*t),0,255) for i in range(3))
def get_rainbow(t,off=0):
    return (int(127*math.sin(t*3+off)+128), int(127*math.sin(t*3+off+2.094)+128), int(127*math.sin(t*3+off+4.189)+128))

def ensure_visible(color, min_brightness=150):
    """Make sure a color is bright enough to read on dark backgrounds.
    Blends toward white if just scaling can't reach min_brightness."""
    r,g,b = color[:3]
    bri = r*0.299 + g*0.587 + b*0.114
    if bri >= min_brightness:
        return color
    # First try scaling up
    if bri > 15:
        factor = min_brightness / bri
        nr,ng,nb = min(255,int(r*factor)), min(255,int(g*factor)), min(255,int(b*factor))
        bri2 = nr*0.299 + ng*0.587 + nb*0.114
        if bri2 >= min_brightness * 0.9:
            return (nr,ng,nb)
    # Scaling not enough — blend toward white
    needed = (min_brightness - bri) / max(1, 255 - bri)
    t2 = max(0.0, min(1.0, needed * 1.3))
    return (min(255,int(r + (255 - r)*t2)),
            min(255,int(g + (255 - g)*t2)),
            min(255,int(b + (255 - b)*t2)))

def draw_text(surf, font, text, x, y, color, shadow=True, center=False):
    """Draw text with a dark shadow behind for readability."""
    s = font.render(text, True, color)
    dx = x - s.get_width()//2 if center else x
    if shadow:
        sh = font.render(text, True, (0,0,0))
        sh.set_alpha(160)
        surf.blit(sh, (dx+1, y+1))
        surf.blit(sh, (dx+2, y+2))
    surf.blit(s, (dx, y))
    return s.get_width(), s.get_height()

def draw_outlined_text(surf, font, text, x, y, color=(255,255,255), outline=(0,0,0), thickness=2, center=False):
    """Draw text with a solid outline around it."""
    s = font.render(text, True, color)
    o = font.render(text, True, outline)
    dx = x - s.get_width()//2 if center else x
    for ox2 in range(-thickness, thickness+1):
        for oy2 in range(-thickness, thickness+1):
            if ox2 != 0 or oy2 != 0:
                surf.blit(o, (dx+ox2, y+oy2))
    surf.blit(s, (dx, y))
    return s.get_width(), s.get_height()

def ease_out_elastic(t):
    if t<=0:return 0
    if t>=1:return 1
    return math.pow(2,-10*t)*math.sin((t-0.1)*5*math.pi)+1

def ease_out_back(t):
    c=1.70158; return 1+(c+1)*((t-1)**3)+c*((t-1)**2)

def ease_out_cubic(t): return 1-(1-t)**3
def ease_in_out_quad(t): return 2*t*t if t<0.5 else 1-(-2*t+2)**2/2

# ── GLOW (cached) ─────────────────────────────────────────────────────────
_glow_cache={}
def draw_glow(surf,cx,cy,radius,color,alpha=40):
    key=(radius,color[:3],alpha)
    if key not in _glow_cache:
        s=pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        for r in range(radius,0,-3):
            a=int(alpha*(r/radius)**0.5)
            pygame.draw.circle(s,(*color[:3],a),(radius,radius),r)
        _glow_cache[key]=s
    surf.blit(_glow_cache[key],(cx-radius,cy-radius),special_flags=pygame.BLEND_ADD)

# ── PARTICLES ─────────────────────────────────────────────────────────────
class Particle:
    __slots__=['x','y','vx','vy','life','max_life','color','size','gravity','shape','rot','rotv','acurve']
    def __init__(self,x,y,color=None,spd=(1,6),life=(0.3,1.0),sz=(2,6),grav=0,shape="circle",acurve="linear"):
        self.x=x;self.y=y
        a=random.uniform(0,6.283); s=random.uniform(*spd)
        self.vx=math.cos(a)*s; self.vy=math.sin(a)*s
        self.life=random.uniform(*life); self.max_life=self.life
        self.color=color or random.choice(theme["particles"])
        self.size=random.uniform(*sz); self.gravity=grav
        self.shape=shape; self.rot=random.uniform(0,360); self.rotv=random.uniform(-300,300)
        self.acurve=acurve

    def update(self,dt):
        self.x+=self.vx*dt*60; self.y+=self.vy*dt*60
        self.vy+=self.gravity*dt*60; self.vx*=0.97; self.vy*=0.97
        self.rot+=self.rotv*dt; self.life-=dt
        return self.life>0

    def draw(self,surf):
        f=max(0,self.life/self.max_life)
        alpha=math.sin(f*math.pi) if self.acurve=="smooth" else f
        r=max(1,int(self.size*alpha))
        c=tuple(clamp(int(ch*alpha),0,255) for ch in self.color)
        ix,iy=int(self.x),int(self.y)
        if self.shape=="circle": pygame.draw.circle(surf,c,(ix,iy),r)
        elif self.shape=="spark":
            ex=self.x+self.vx*3; ey=self.y+self.vy*3
            pygame.draw.line(surf,c,(ix,iy),(int(ex),int(ey)),max(1,r//2))
        elif self.shape=="diamond":
            pygame.draw.polygon(surf,c,[(ix,iy-r),(ix+r,iy),(ix,iy+r),(ix-r,iy)])
        elif self.shape=="square":
            s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.rect(s,(*c,int(255*alpha)),(0,0,r*2,r*2))
            rot=pygame.transform.rotate(s,self.rot)
            surf.blit(rot,(ix-rot.get_width()//2,iy-rot.get_height()//2))
        elif self.shape=="star":
            pts=[]
            for i in range(8):
                a=self.rot/57.3+i*math.pi/4; rad=r if i%2==0 else r//2
                pts.append((ix+int(rad*math.cos(a)),iy+int(rad*math.sin(a))))
            if len(pts)>=3: pygame.draw.polygon(surf,c,pts)

particles=[]

def spawn_particles(x,y,count=12,color=None,**kw):
    for _ in range(count): particles.append(Particle(x,y,color,**kw))

def spawn_explosion(x,y,count=30,color=None):
    for _ in range(count):
        particles.append(Particle(x,y,color,spd=(2,9),life=(0.4,1.2),sz=(2,8),grav=0.15,
            shape=random.choice(["circle","diamond","spark","star"]),acurve="smooth"))

def spawn_firework(x,y,color=None):
    c=color or random.choice(theme["particles"])
    for _ in range(40):
        particles.append(Particle(x,y,c,spd=(3,10),life=(0.5,1.5),sz=(2,5),grav=0.2,shape="spark",acurve="smooth"))
    for _ in range(15):
        particles.append(Particle(x,y,(255,255,255),spd=(1,4),life=(0.3,0.8),sz=(1,3),shape="circle",acurve="smooth"))

def spawn_confetti(x,y,count=25):
    for _ in range(count):
        particles.append(Particle(x,y,random.choice(theme["particles"]),spd=(2,7),life=(0.8,2.0),
            sz=(3,7),grav=0.12,shape="square",acurve="smooth"))

def spawn_ring(x,y,radius=30,count=20,color=None):
    c=color or theme["accent"]
    for i in range(count):
        a=i*6.283/count; px=x+math.cos(a)*radius; py=y+math.sin(a)*radius
        p=Particle(px,py,c,spd=(0.5,2),life=(0.3,0.7),sz=(2,4),shape="circle",acurve="smooth")
        p.vx=math.cos(a)*2; p.vy=math.sin(a)*2; particles.append(p)

def spawn_spiral(x,y,count=30,color=None):
    c=color or theme["accent"]
    for i in range(count):
        a=i*0.5; r=i*0.8
        p=Particle(x+math.cos(a)*r,y+math.sin(a)*r,c,spd=(1,3),life=(0.4,1.0),sz=(2,5),shape="diamond",acurve="smooth")
        p.vx=math.cos(a+1.57)*2; p.vy=math.sin(a+1.57)*2; particles.append(p)

# ── FLOATING TEXT ─────────────────────────────────────────────────────────
class FloatingText:
    __slots__=['x','y','text','color','life','max_life','font','sa']
    def __init__(self,x,y,text,color=None,font=font_md,life=1.2):
        self.x=x;self.y=y;self.text=text;self.color=color or theme["accent"]
        self.life=life;self.max_life=life;self.font=font;self.sa=0.0

    def update(self,dt):
        self.y-=30*dt; self.life-=dt; self.sa=min(1.0,self.sa+dt*8)
        return self.life>0

    def draw(self,surf):
        f=max(0,self.life/self.max_life); alpha=clamp(int(255*f),0,255)
        sc=ease_out_back(min(1.0,self.sa))
        visible_c = ensure_visible(self.color, 160)
        s=self.font.render(self.text,True,visible_c)
        sh=self.font.render(self.text,True,(0,0,0))
        if 0.1<sc!=1.0:
            w=max(1,int(s.get_width()*sc)); h=max(1,int(s.get_height()*sc))
            s=pygame.transform.smoothscale(s,(w,h))
            sh=pygame.transform.smoothscale(sh,(w,h))
        s.set_alpha(alpha); sh.set_alpha(min(alpha,160))
        bx=self.x-s.get_width()//2; by=int(self.y)-s.get_height()//2
        surf.blit(sh,(bx+1,by+1))
        surf.blit(s,(bx,by))

floating_texts=[]

# ── SCREEN EFFECTS ────────────────────────────────────────────────────────
shake_timer=0.0; shake_intensity=0; flash_timer=0.0; flash_color=(255,255,255); slow_mo_timer=0.0

def trigger_shake(i=6,d=0.2):
    global shake_timer,shake_intensity; shake_timer=d; shake_intensity=i
def trigger_flash(c=(255,255,255),d=0.15):
    global flash_timer,flash_color; flash_timer=d; flash_color=c
def trigger_slow_mo(d=0.3):
    global slow_mo_timer; slow_mo_timer=d

# ── TRAIL ─────────────────────────────────────────────────────────────────
class Trail:
    __slots__=['x','y','life','color','size']
    def __init__(self,x,y,color,size=CELL//2):
        self.x=x;self.y=y;self.life=1.0;self.color=color;self.size=size
    def update(self,dt): self.life-=dt*2.5; return self.life>0
    def draw(self,surf):
        a=max(0,self.life); r=max(1,int(self.size*a*0.7))
        c=tuple(clamp(int(ch*a*0.4),0,255) for ch in self.color)
        pygame.draw.circle(surf,c,(int(self.x),int(self.y)),r)
trails=[]

# ── BACKGROUND STARS ──────────────────────────────────────────────────────
class Star:
    __slots__=['x','y','speed','bright','size','phase']
    def __init__(self):
        self.x=random.uniform(0,FIELD_W);self.y=random.uniform(0,FIELD_H)
        self.speed=random.uniform(3,12);self.bright=random.uniform(0.2,0.7)
        self.size=random.uniform(0.5,2.0);self.phase=random.uniform(0,6.283)
    def update(self,dt):
        self.y+=self.speed*dt
        if self.y>FIELD_H: self.y=-2; self.x=random.uniform(0,FIELD_W)
    def draw(self,surf,t):
        p=self.bright*(0.6+0.4*math.sin(t*2+self.phase))
        c=tuple(clamp(int(60*p),0,255) for _ in range(3))
        pygame.draw.circle(surf,c,(int(self.x),int(self.y)),max(1,int(self.size*p)))
bg_stars=[Star() for _ in range(45)]

# ── GAME MODES ────────────────────────────────────────────────────────────
MODES={"classic":{"name":"Classic","desc":"No walls, wrap around edges","walls":False},
       "walls":{"name":"Walls","desc":"Walls kill! Level obstacles","walls":True},
       "speed":{"name":"Speed","desc":"Starts fast, gets faster!","walls":False}}

def generate_walls(level):
    w=set()
    if level>=2:
        for i in range(5,10): w.add((i,8));w.add((COLS-1-i,ROWS-1-8))
    if level>=3:
        for i in range(8,16): w.add((14,i))
    if level>=4:
        for i in range(3,7): w.add((i,15));w.add((COLS-1-i,15))
    if level>=5:
        for i in range(6,18): w.add((i,5));w.add((i,ROWS-6))
    return w

# ── FOOD DRAWING ──────────────────────────────────────────────────────────
def draw_apple(surf,cx,cy,radius,t,fc,fs):
    pulse=1+0.12*math.sin(t*4.5); r=int(radius*pulse); bob=int(2*math.sin(t*3)); cy2=cy+bob
    draw_glow(surf,cx,cy2,r+12,fc,30); draw_glow(surf,cx,cy2,r+6,fc,20)
    ss=pygame.Surface((r*2+4,6),pygame.SRCALPHA); pygame.draw.ellipse(ss,(0,0,0,40),(0,0,r*2+4,6))
    surf.blit(ss,(cx-r-2,cy2+r))
    br=max(3,r-1)
    pygame.draw.circle(surf,fc,(cx-br//4,cy2),br); pygame.draw.circle(surf,fc,(cx+br//4,cy2),br)
    dk=tuple(max(0,c-50) for c in fc)
    pygame.draw.arc(surf,dk,(cx-br,cy2-br//2,br*2,br*2),3.5,5.8,2)
    so=2*math.sin(t*2); sr2=max(2,br//3); sx=cx-br//3+int(so); sy=cy2-br//3
    sh=pygame.Surface((sr2*2,sr2*2),pygame.SRCALPHA); pygame.draw.circle(sh,(*fs,180),(sr2,sr2),sr2)
    surf.blit(sh,(sx-sr2,sy-sr2)); pygame.draw.circle(surf,(255,255,255),(sx+1,sy+1),max(1,sr2//2))
    stx=cx; stt=cy2-br-3; stb=cy2-br//2
    pygame.draw.line(surf,(100,70,30),(stx,stb),(stx+1,stt),2)
    lsw=3*math.sin(t*2.5)
    lp=[(stx+1,stt+1),(stx+5+int(lsw),stt-3),(stx+8+int(lsw),stt+2),(stx+4,stt+3)]
    pygame.draw.polygon(surf,(50,180,50),lp); pygame.draw.line(surf,(80,220,80),lp[0],lp[2],1)

def draw_cherry(surf,cx,cy,radius,t,fc,fs):
    pulse=1+0.1*math.sin(t*5); r=max(3,int(radius*0.65*pulse))
    sway=2*math.sin(t*2.5); bob=int(1.5*math.sin(t*3.5))
    x1=cx-r-1+int(sway);x2=cx+r+1+int(sway*0.5);y1=cy+2+bob;y2=cy+bob
    draw_glow(surf,cx,cy,r+10,fc,25)
    st=(cx+int(sway*0.3),cy-r-6+bob)
    pygame.draw.line(surf,(90,60,25),st,(x1,y1-r//2),2)
    pygame.draw.line(surf,(90,60,25),st,(x2,y2-r//2),2)
    lp=[(st[0],st[1]),(st[0]+6+int(sway),st[1]-4),(st[0]+4,st[1]+2)]
    pygame.draw.polygon(surf,(50,170,50),lp)
    for xx,yy in [(x1,y1),(x2,y2)]:
        pygame.draw.circle(surf,fc,(xx,yy),r)
        dk=tuple(max(0,c-60) for c in fc); pygame.draw.arc(surf,dk,(xx-r,yy,r*2,r),0.3,2.8,2)
        shr=max(1,r//3); sh2=pygame.Surface((shr*2,shr*2),pygame.SRCALPHA)
        pygame.draw.circle(sh2,(*fs,200),(shr,shr),shr)
        surf.blit(sh2,(xx-r//3-shr,yy-r//3-shr)); pygame.draw.circle(surf,(255,255,255),(xx-r//3+1,yy-r//3+1),max(1,shr//2))

def draw_star_item(surf,cx,cy,radius,t,color,tf):
    pulse=1+0.2*math.sin(t*7); r=int(radius*pulse); rot=t*2
    draw_glow(surf,cx,cy,r+14,color,40); draw_glow(surf,cx,cy,r+8,color,25)
    pts=[];ipts=[]
    for i in range(10):
        a=rot+i*math.pi/5; rad=r if i%2==0 else r*0.45
        pts.append((cx+int(rad*math.cos(a)),cy-int(rad*math.sin(a))))
        rad2=r*0.6 if i%2==0 else r*0.25
        ipts.append((cx+int(rad2*math.cos(a)),cy-int(rad2*math.sin(a))))
    pygame.draw.polygon(surf,color,pts)
    pygame.draw.polygon(surf,tuple(min(255,c+60) for c in color),ipts)
    pygame.draw.polygon(surf,(255,255,240),pts,1)
    for i in range(3):
        sa=t*4+i*2.094
        pygame.draw.circle(surf,(255,255,200),(cx+int((r+6)*math.cos(sa)),cy+int((r+6)*math.sin(sa))),2)
    bw=CELL+4;bh=3;bx=cx-bw//2;by=cy+r+6
    pygame.draw.rect(surf,(40,40,40),(bx,by,bw,bh),border_radius=1)
    pygame.draw.rect(surf,color,(bx,by,int(bw*tf),bh),border_radius=1)

def draw_powerup_orb(surf,cx,cy,radius,t,tf):
    pulse=1+0.18*math.sin(t*6); r=int(radius*pulse); c=get_rainbow(t)
    draw_glow(surf,cx,cy,r+16,c,35)
    for i in range(12):
        a=t*3+i*math.pi/6; rc=get_rainbow(t,i*0.5)
        pygame.draw.circle(surf,rc,(cx+int((r+3)*math.cos(a)),cy+int((r+3)*math.sin(a))),2)
    pygame.draw.circle(surf,c,(cx,cy),r)
    lt=tuple(min(255,ch+80) for ch in c)
    pygame.draw.circle(surf,lt,(cx-r//4,cy-r//4),max(1,r//2))
    pygame.draw.circle(surf,(255,255,255),(cx-r//4,cy-r//4),max(1,r//4))
    txt=font_md.render("?",True,(255,255,255)); surf.blit(txt,(cx-txt.get_width()//2,cy-txt.get_height()//2))
    bw=CELL+4;bh=3;bx=cx-bw//2;by=cy+r+6
    pygame.draw.rect(surf,(40,40,40),(bx,by,bw,bh),border_radius=1)
    pygame.draw.rect(surf,c,(bx,by,int(bw*tf),bh),border_radius=1)

# ── GAME STATE ────────────────────────────────────────────────────────────
class Game:
    def __init__(self,mode="classic"):
        self.mode=mode; self.cfg=MODES[mode]; self.food_type="apple"; self.reset()

    def reset(self):
        cx2,cy2=COLS//2,ROWS//2
        self.snake=[(cx2,cy2),(cx2-1,cy2),(cx2-2,cy2)]
        self.direction=(1,0); self.input_queue=deque(maxlen=3)
        self.score=0; self.level=1; self.food=None; self.bonus=None; self.bonus_timer=0
        self.alive=True; self.win=False; self.move_timer=0
        self.combo=0; self.combo_timer=0; self.eaten_count=0; self.total_time=0
        self.speed_mult=3.0 if self.mode=="speed" else 1.0
        self.walls=set(); self.invuln_timer=0; self.rainbow_timer=0
        self.powerup=None; self.powerup_timer=0
        self.base_interval=0.12 if self.mode=="speed" else 0.15
        self.death_anim=0.0; self.eat_anim=0.0; self.levelup_anim=0.0
        self.food_type="apple"
        # Smooth movement interpolation
        self.move_progress=1.0  # 0..1, 1 means arrived
        self.prev_positions={}  # segment index -> previous (x,y)
        particles.clear(); floating_texts.clear(); trails.clear()
        self.place_food()

    @property
    def move_interval(self):
        return max(0.04,self.base_interval-(self.level-1)*0.008)/self.speed_mult

    def _free(self,extra=None):
        occ=set(self.snake)|self.walls
        if extra: occ|=extra
        return [(x,y) for x in range(COLS) for y in range(ROWS) if (x,y) not in occ]

    def place_food(self):
        f=self._free()
        if f: self.food=random.choice(f); self.food_type=random.choice(["apple","apple","cherry"])
        else: self.win=True; self.alive=False

    def place_bonus(self):
        f=self._free({self.food} if self.food else set())
        if f: self.bonus=random.choice(f); self.bonus_timer=6.0

    def place_powerup(self):
        f=self._free({self.food} if self.food else set())
        if f: self.powerup=random.choice(f); self.powerup_timer=8.0

    def update(self,dt):
        if not self.alive:
            self.death_anim=min(1.0,self.death_anim+dt*2.5); return

        self.total_time+=dt; self.move_timer+=dt; self.combo_timer-=dt
        self.eat_anim=max(0,self.eat_anim-dt*4)
        self.levelup_anim=max(0,self.levelup_anim-dt*2)

        if self.combo_timer<=0: self.combo=0
        if self.bonus:
            self.bonus_timer-=dt
            if self.bonus_timer<=0: self.bonus=None
        if self.powerup:
            self.powerup_timer-=dt
            if self.powerup_timer<=0: self.powerup=None
        if self.invuln_timer>0: self.invuln_timer-=dt
        if self.rainbow_timer>0: self.rainbow_timer-=dt

        # Smooth interpolation progress
        self.move_progress=min(1.0,self.move_progress+dt/self.move_interval)

        if self.move_timer>=self.move_interval:
            self.move_timer-=self.move_interval
            if self.input_queue:
                ndx,ndy=self.input_queue.popleft()
                dx,dy=self.direction
                if (ndx,ndy)!=(-dx,-dy): self.direction=(ndx,ndy)
            # Save positions before step for interpolation
            self.prev_positions={i:pos for i,pos in enumerate(self.snake)}
            self.step()
            self.move_progress=0.0

    def step(self):
        hx,hy=self.snake[0]; dx,dy=self.direction; nx,ny=hx+dx,hy+dy

        if self.cfg["walls"]:
            if nx<0 or nx>=COLS or ny<0 or ny>=ROWS:
                if self.invuln_timer<=0: self.die(); return
                else: nx%=COLS; ny%=ROWS
        else: nx%=COLS; ny%=ROWS

        if (nx,ny) in self.walls:
            if self.invuln_timer<=0: self.die(); return
        if (nx,ny) in self.snake[:-1]:
            if self.invuln_timer<=0: self.die(); return

        self.snake.insert(0,(nx,ny))
        trails.append(Trail(nx*CELL+CELL//2,ny*CELL+CELL//2,theme["snake_head"]))

        ate=False
        if (nx,ny)==self.food:
            snd_eat.play(); self.eaten_count+=1; self.combo+=1; self.combo_timer=3.0
            self.eat_anim=1.0; pts=10*self.level*max(1,self.combo); self.score+=pts
            fx=nx*CELL+CELL//2; fy=ny*CELL+CELL//2
            spawn_explosion(fx,fy,25,theme["food"]); spawn_ring(fx,fy,20,16,theme["food"])
            floating_texts.append(FloatingText(fx,fy-10,f"+{pts}",theme["accent"],font_md))
            if self.combo>1:
                floating_texts.append(FloatingText(fx,fy-30,f"x{self.combo} Combo!",theme["gold"],font_sm,1.5))
            if self.combo==5: spawn_firework(fx,fy,theme["gold"])
            if self.combo==10:
                spawn_confetti(fx,fy,40)
                floating_texts.append(FloatingText(fx,fy-50,"Unstoppable!",(255,100,255),font_lg,2.0))
            trigger_flash(theme["food"],0.08); self.place_food(); ate=True

            if self.eaten_count%8==0:
                self.level+=1; self.levelup_anim=1.0; snd_levelup.play()
                floating_texts.append(FloatingText(FIELD_W//2,FIELD_H//2,f"Level {self.level}!",theme["gold"],font_xl,2.0))
                spawn_firework(FIELD_W//2,FIELD_H//2,theme["gold"])
                spawn_firework(FIELD_W//4,FIELD_H//2,theme["accent"])
                spawn_firework(FIELD_W*3//4,FIELD_H//2,theme["particles"][2])
                trigger_shake(5,0.25); trigger_flash(theme["gold"],0.12)
                if self.cfg["walls"]: self.walls=generate_walls(self.level)
            if random.random()<0.3 and not self.bonus: self.place_bonus()
            if random.random()<0.15 and not self.powerup and self.level>=2: self.place_powerup()
        else: self.snake.pop()

        if self.bonus and (nx,ny)==self.bonus:
            snd_bonus.play(); p2=50*self.level; self.score+=p2
            bx2=nx*CELL+CELL//2; by2=ny*CELL+CELL//2
            spawn_firework(bx2,by2,theme["bonus"]); spawn_ring(bx2,by2,25,20,theme["bonus"])
            floating_texts.append(FloatingText(bx2,by2-10,f"+{p2}",theme["gold"],font_md))
            trigger_flash(theme["bonus"],0.1); self.bonus=None; ate=True

        if self.powerup and (nx,ny)==self.powerup:
            snd_powerup.play(); ptype=random.choice(["invuln","rainbow","shrink"])
            px2=nx*CELL+CELL//2; py2=ny*CELL+CELL//2
            if ptype=="invuln":
                self.invuln_timer=5.0
                floating_texts.append(FloatingText(px2,py2-10,"Shield!",(100,200,255),font_lg,1.8))
                spawn_spiral(px2,py2,35,(100,200,255)); spawn_ring(px2,py2,30,24,(100,200,255))
            elif ptype=="rainbow":
                self.rainbow_timer=6.0
                floating_texts.append(FloatingText(px2,py2-10,"Rainbow!",(255,100,255),font_lg,1.8))
                spawn_confetti(px2,py2,35); spawn_ring(px2,py2,30,24,(255,100,255))
            elif ptype=="shrink":
                if len(self.snake)>5:
                    rem=len(self.snake)//3
                    for seg in self.snake[-rem:]:
                        spawn_particles(seg[0]*CELL+CELL//2,seg[1]*CELL+CELL//2,3,theme["danger"],shape="spark")
                    self.snake=self.snake[:len(self.snake)-rem]
                    floating_texts.append(FloatingText(px2,py2-10,f"Trim -{rem}!",theme["danger"],font_lg,1.5))
                else:
                    bp=30*self.level; self.score+=bp
                    floating_texts.append(FloatingText(px2,py2-10,f"+{bp}",theme["gold"]))
                spawn_explosion(px2,py2,30,theme["danger"])
            trigger_flash(get_rainbow(pygame.time.get_ticks()/1000.0),0.1)
            self.powerup=None; ate=True

    def die(self):
        self.alive=False; self.death_anim=0.0; snd_die.play()
        hx,hy=self.snake[0]; cx2=hx*CELL+CELL//2; cy2=hy*CELL+CELL//2
        spawn_firework(cx2,cy2,theme["danger"])
        for i,(sx,sy) in enumerate(self.snake[:20]):
            for _ in range(3):
                particles.append(Particle(sx*CELL+CELL//2+random.randint(-5,5),
                    sy*CELL+CELL//2+random.randint(-5,5),theme["danger"],
                    spd=(1,5),life=(0.3+i*0.02,0.8+i*0.02),sz=(2,5),grav=0.15,shape="spark",acurve="smooth"))
        trigger_shake(14,0.5); trigger_flash(theme["danger"],0.18); trigger_slow_mo(0.4)

    def handle_input(self,key):
        m={pygame.K_UP:(0,-1),pygame.K_w:(0,-1),pygame.K_DOWN:(0,1),pygame.K_s:(0,1),
           pygame.K_LEFT:(-1,0),pygame.K_a:(-1,0),pygame.K_RIGHT:(1,0),pygame.K_d:(1,0)}
        if key in m: self.input_queue.append(m[key])

    def get_smooth_pos(self,idx):
        """Get interpolated pixel position for a segment."""
        cur=self.snake[idx]
        t2=ease_in_out_quad(min(1.0,self.move_progress))
        if idx in self.prev_positions:
            prev=self.prev_positions[idx]
            dx2=cur[0]-prev[0]; dy2=cur[1]-prev[1]
            # Handle wrap-around (don't interpolate across screen)
            if abs(dx2)>1 or abs(dy2)>1:
                return (cur[0]*CELL+CELL//2, cur[1]*CELL+CELL//2)
            px=lerp(prev[0],cur[0],t2)*CELL+CELL//2
            py=lerp(prev[1],cur[1],t2)*CELL+CELL//2
            return (px,py)
        return (cur[0]*CELL+CELL//2, cur[1]*CELL+CELL//2)

# ── DRAWING ───────────────────────────────────────────────────────────────
def draw_grid(surf):
    gc=theme["grid"]
    for x in range(0,FIELD_W,CELL): pygame.draw.line(surf,gc,(x,0),(x,FIELD_H))
    for y in range(0,FIELD_H,CELL): pygame.draw.line(surf,gc,(0,y),(FIELD_W,y))

def draw_snake(surf,game,t):
    n=len(game.snake)
    for i_rev,(sx,sy) in enumerate(reversed(game.snake)):
        idx=n-1-i_rev
        # Smooth position
        smx,smy=game.get_smooth_pos(idx)
        rw=CELL-2; rh=CELL-2

        if game.rainbow_timer>0:
            color=get_rainbow(t,idx*0.3); outline=tuple(max(0,c-60) for c in color)
        elif game.invuln_timer>0:
            p=0.5+0.5*math.sin(t*10); color=(int(100+100*p),int(200+55*p),255); outline=(40,80,130)
        elif idx==0:
            color=theme["snake_head"]; outline=theme["snake_outline"]
            if game.eat_anim>0:
                sc2=1+0.2*game.eat_anim; extra=int(rw*(sc2-1)/2); rw+=extra*2; rh+=extra*2
        else:
            frac=idx/max(1,n-1)
            color=lerp_color(theme["snake_head"],theme["snake_body"],frac)
            outline=theme["snake_outline"]

        rx=int(smx-rw//2); ry=int(smy-rh//2)
        rect=pygame.Rect(rx,ry,rw,rh)

        # Connector to next segment
        if idx<n-1:
            nmx,nmy=game.get_smooth_pos(idx+1)
            ddx=smx-nmx; ddy=smy-nmy
            if abs(ddx)<CELL*1.5 and abs(ddy)<CELL*1.5:
                mx2=(smx+nmx)/2; my2=(smy+nmy)/2
                cr=pygame.Rect(int(mx2-rw//2),int(my2-rh//2),rw,rh)
                pygame.draw.rect(surf,outline,cr.inflate(2,2),border_radius=3)
                pygame.draw.rect(surf,color,cr,border_radius=2)

        pygame.draw.rect(surf,outline,rect.inflate(2,2),border_radius=6)
        pygame.draw.rect(surf,color,rect,border_radius=5)

        # Body highlight
        if idx>0:
            hl=tuple(min(255,c+30) for c in color)
            hs2=pygame.Surface((rw//2-1,rh//2-1),pygame.SRCALPHA)
            pygame.draw.rect(hs2,(*hl,50),(0,0,rw//2-1,rh//2-1),border_radius=3)
            surf.blit(hs2,(rx+2,ry+2))

        # Head
        if idx==0:
            dx2,dy2=game.direction
            ecx=int(smx)+dx2*5; ecy=int(smy)+dy2*5
            ew=5
            e1x=ecx-4*abs(dy2); e1y=ecy-4*abs(dx2)
            e2x=ecx+4*abs(dy2); e2y=ecy+4*abs(dx2)
            pygame.draw.circle(surf,(255,255,255),(e1x,e1y),ew)
            pygame.draw.circle(surf,(255,255,255),(e2x,e2y),ew)
            pygame.draw.circle(surf,(10,10,30),(e1x+dx2*2,e1y+dy2*2),3)
            pygame.draw.circle(surf,(10,10,30),(e2x+dx2*2,e2y+dy2*2),3)
            pygame.draw.circle(surf,(255,255,255),(e1x+dx2*2-1,e1y+dy2*2-1),1)
            pygame.draw.circle(surf,(255,255,255),(e2x+dx2*2-1,e2y+dy2*2-1),1)

            if game.invuln_timer>0 or game.rainbow_timer>0:
                draw_glow(surf,int(smx),int(smy),22,color,35)

            # Tongue
            tp=math.sin(t*6)
            if tp>0.7:
                tl=int(4+3*(tp-0.7)/0.3)
                tx=int(smx)+dx2*(rw//2+tl); ty=int(smy)+dy2*(rh//2+tl)
                pygame.draw.line(surf,(255,60,80),(int(smx)+dx2*(rw//2),int(smy)+dy2*(rh//2)),(tx,ty),2)
                if tl>5:
                    f1=(tx+(abs(dy2)*3+dx2*2),ty+(abs(dx2)*3+dy2*2))
                    f2=(tx+(-abs(dy2)*3+dx2*2),ty+(-abs(dx2)*3+dy2*2))
                    pygame.draw.line(surf,(255,60,80),(tx,ty),f1,1)
                    pygame.draw.line(surf,(255,60,80),(tx,ty),f2,1)

def draw_walls(surf,game,t):
    wc=theme["wall"]
    for wx,wy in game.walls:
        rect=pygame.Rect(wx*CELL,wy*CELL,CELL,CELL)
        p=0.75+0.25*math.sin(t*1.5+wx*0.4+wy*0.3)
        c=tuple(clamp(int(ch*p),0,255) for ch in wc)
        pygame.draw.rect(surf,c,rect,border_radius=3)
        lt=tuple(min(255,ch+20) for ch in c)
        pygame.draw.line(surf,lt,(rect.left+2,rect.centery),(rect.right-2,rect.centery),1)
        pygame.draw.line(surf,lt,(rect.centerx,rect.top+2),(rect.centerx,rect.centery),1)
        pygame.draw.rect(surf,tuple(min(255,ch+10) for ch in c),rect,1,border_radius=3)

# ── SIDEBAR ───────────────────────────────────────────────────────────────
def draw_sidebar(surf,game,t):
    sb=pygame.Rect(FIELD_W,0,SIDEBAR_W,HEIGHT); pygame.draw.rect(surf,theme["sidebar_bg"],sb)
    bc=theme["sidebar_border"]
    for i in range(3):
        a=max(0,255-i*80); c2=tuple(clamp(int(c*a/255),0,255) for c in bc)
        pygame.draw.line(surf,c2,(FIELD_W+i,0),(FIELD_W+i,HEIGHT))

    x=FIELD_W+16; y=12
    # Sidebar title — use theme accent directly
    draw_text(surf,font_lg,"Neon",x,y,theme["accent"]); y+=34
    draw_text(surf,font_lg,"Snake",x,y,theme["accent"]); y+=44
    draw_text(surf,font_xs,f"Theme: {theme['name']}",x,y,theme["silver"]); y+=18
    dim_hint=lerp_color(theme["silver"],theme["sidebar_bg"],0.3)
    draw_text(surf,font_xs,"T = change theme",x,y,dim_hint); y+=22
    draw_text(surf,font_sm,f"Mode: {game.cfg['name']}",x,y,theme["gold"]); y+=28

    dc=lerp_color(theme["sidebar_bg"],theme["accent"],0.4)
    pygame.draw.line(surf,dc,(x,y),(x+SIDEBAR_W-32,y),1); y+=12

    # Score
    draw_text(surf,font_xs,"Score",x,y,theme["silver"]); y+=18
    sc_color=theme["text"]
    st=font_score.render(f"{game.score:,}",True,sc_color)
    if game.eat_anim>0:
        sc2=1+0.15*game.eat_anim
        st=pygame.transform.smoothscale(st,(max(1,int(st.get_width()*sc2)),max(1,int(st.get_height()*sc2))))
    st_sh=font_score.render(f"{game.score:,}",True,(0,0,0)); st_sh.set_alpha(120)
    if game.eat_anim>0:
        st_sh=pygame.transform.smoothscale(st_sh,(st.get_width(),st.get_height()))
    surf.blit(st_sh,(x+1,y+1)); surf.blit(st,(x,y)); y+=40

    # Level
    draw_text(surf,font_xs,"Level",x,y,theme["silver"]); y+=18
    lc=get_rainbow(t) if game.levelup_anim>0 else theme["accent"]
    draw_text(surf,font_hud,f"{game.level}",x,y,lc); y+=28

    # Length
    draw_text(surf,font_xs,"Length",x,y,theme["silver"]); y+=18
    draw_text(surf,font_hud,f"{len(game.snake)}",x,y,theme["text"]); y+=28

    # Combo
    if game.combo>1:
        draw_text(surf,font_xs,"Combo",x,y,theme["silver"]); y+=18
        cc=theme["gold"] if game.combo>=5 else theme["accent"]
        combo_ox=int(2*math.sin(t*12)) if game.combo>=5 else 0
        draw_text(surf,font_hud,f"x{game.combo}",x+combo_ox,y,cc); y+=26
        bw=SIDEBAR_W-36; frac=max(0,game.combo_timer/3.0)
        pygame.draw.rect(surf,tuple(max(0,c-150) for c in cc),(x,y,bw,4),border_radius=2)
        pygame.draw.rect(surf,cc,(x,y,int(bw*frac),4),border_radius=2); y+=14
    else: y+=58

    pygame.draw.line(surf,dc,(x,y),(x+SIDEBAR_W-32,y),1); y+=10
    draw_text(surf,font_xs,"Speed",x,y,theme["silver"]); y+=18
    bw=SIDEBAR_W-36; bh=8; spd=min(1.0,(1/game.move_interval)*10/100)
    pygame.draw.rect(surf,tuple(max(0,c-180) for c in theme["accent"]),(x,y,bw,bh),border_radius=3)
    bc2=theme["danger"] if spd>0.7 else theme["accent"]; fw=int(bw*spd)
    pygame.draw.rect(surf,bc2,(x,y,fw,bh),border_radius=3)
    if fw>4:
        sh2=pygame.Surface((fw-2,bh//2),pygame.SRCALPHA)
        pygame.draw.rect(sh2,(255,255,255,40),(0,0,fw-2,bh//2),border_radius=2)
        surf.blit(sh2,(x+1,y+1))
    y+=20

    if game.invuln_timer>0:
        draw_text(surf,font_xs,f"Shield {game.invuln_timer:.1f}s",x,y,(130,210,255)); y+=18
    if game.rainbow_timer>0:
        draw_text(surf,font_xs,f"Rainbow {game.rainbow_timer:.1f}s",x,y,get_rainbow(t)); y+=18

    y=HEIGHT-55; pygame.draw.line(surf,dc,(x,y),(x+SIDEBAR_W-32,y),1); y+=8
    m=int(game.total_time//60); s=int(game.total_time%60)
    draw_text(surf,font_sm,f"Time  {m:02d}:{s:02d}",x,y,theme["silver"]); y+=24
    dim_hint2=lerp_color(theme["silver"],theme["sidebar_bg"],0.3)
    draw_text(surf,font_xs,"P = Pause   Esc = Menu",x,y,dim_hint2)

# ── DEATH SCREEN ──────────────────────────────────────────────────────────
def draw_death_screen(surf,game,t):
    anim=ease_out_cubic(min(1.0,game.death_anim))
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,int(180*anim))); surf.blit(ov,(0,0))
    if anim<0.1: return
    cx2=FIELD_W//2; sl=int(30*(1-anim))

    # Title — "Game Over" / "You Win!"
    title_c = (255,215,0) if game.win else (255,80,80)
    title_txt = "You Win!" if game.win else "Game Over"
    ts=font_xl.render(title_txt,True,title_c)
    ts_sh=font_xl.render(title_txt,True,(0,0,0)); ts_sh.set_alpha(int(180*anim))
    ts.set_alpha(int(255*anim))
    surf.blit(ts_sh,(cx2-ts.get_width()//2+2,102-sl)); surf.blit(ts,(cx2-ts.get_width()//2,100-sl))

    # Score
    sse=ease_out_elastic(min(1.0,max(0,anim*2-0.3)))
    sc_c=(255,255,255)
    sc=font_lg.render(f"Score: {game.score:,}",True,sc_c)
    if sse>0.1:
        sc=pygame.transform.smoothscale(sc,(max(1,int(sc.get_width()*sse)),max(1,int(sc.get_height()*sse))))
    sc.set_alpha(int(255*anim)); surf.blit(sc,(cx2-sc.get_width()//2,180))

    # Info
    info_c=(200,200,220)
    info=font_md.render(f"Level {game.level}   |   Length {len(game.snake)}",True,info_c)
    info.set_alpha(int(255*anim)); surf.blit(info,(cx2-info.get_width()//2,230))
    m=int(game.total_time//60); s=int(game.total_time%60)
    tt=font_md.render(f"Time: {m:02d}:{s:02d}",True,info_c)
    tt.set_alpha(int(255*anim)); surf.blit(tt,(cx2-tt.get_width()//2,268))

    # High scores
    data=load_data(); ms=data["scores"].get(game.mode,[])
    if ms and anim>0.5:
        a2=min(1.0,(anim-0.5)*4)
        hs=font_sm.render("High Scores",True,(255,215,0)); hs.set_alpha(int(255*a2))
        surf.blit(hs,(cx2-hs.get_width()//2,315))
        score_colors=[(255,215,0),(200,200,220),(180,180,195),(160,160,175),(150,150,165)]
        for i,s2 in enumerate(ms[:5]):
            c=score_colors[min(i,4)]
            e=font_sm.render(f"{['1st','2nd','3rd','4th','5th'][i]}  {s2:,}",True,c)
            e.set_alpha(int(255*a2)); surf.blit(e,(cx2-e.get_width()//2,345+i*24))

    # Restart hint
    if anim>0.7:
        p=0.5+0.5*math.sin(t*4)
        rc=(int(140+115*p), int(140+115*p), int(140+115*p))
        draw_text(surf,font_md,"Enter = Restart   |   Esc = Menu",cx2,HEIGHT-70,rc,shadow=True,center=True)

# ── MENU ──────────────────────────────────────────────────────────────────
_menu_anim_sel = 0.0      # smooth Y position for selection highlight
_menu_anim_prev = -1      # previous selected index
_menu_anim_glow = 0.0     # glow pulse timer
_menu_arrow_phase = 0.0   # arrow bounce phase

def draw_menu(surf,selected,t):
    global _menu_anim_sel, _menu_anim_prev, _menu_anim_glow, _menu_arrow_phase
    surf.fill(theme["bg"]); cx2=WIDTH//2
    for star in bg_stars: star.draw(surf,t)

    # ── Title — white with thin black outline ──
    # Gentle float animation for title
    title_y = 35 + int(3 * math.sin(t * 1.2))
    glow_pulse = 12 + int(6 * math.sin(t * 2.0))
    draw_glow(surf, cx2, title_y + 25, 35, theme["accent"], glow_pulse)
    draw_outlined_text(surf, font_title, "Neon Snake", cx2, title_y,
                       color=(255,255,255), outline=(0,0,0), thickness=1, center=True)

    # Subtitle with fade-in feel
    sub_a = int(160 + 40 * math.sin(t * 1.5))
    sub_c = theme["silver"]
    sub_s = font_sm.render("A Classic Reimagined", True, sub_c)
    sub_s.set_alpha(sub_a)
    surf.blit(sub_s, (cx2 - sub_s.get_width()//2, 97 + int(2 * math.sin(t * 1.2 + 1))))

    # Theme indicator
    ti_c = lerp_color(theme["silver"], theme["bg"], 0.35)
    draw_text(surf, font_xs, f"Theme: {theme['name']}  |  T to change", cx2, 125, ti_c, shadow=True, center=True)

    # ── Menu items ──
    options=[("Classic Mode","No walls — snake wraps around"),
             ("Walls Mode","Walls are deadly + level obstacles"),
             ("Speed Mode","Start fast, get faster!"),
             ("Quit","Exit the game")]
    ITEM_H = 100
    sy = 160
    bw = 520; bh = 72

    # Smooth selection animation — lerp toward target Y
    target_y = sy + selected * ITEM_H
    if _menu_anim_prev == -1:
        _menu_anim_sel = float(target_y)
    else:
        _menu_anim_sel += (target_y - _menu_anim_sel) * 0.18

    # Detect selection change for burst
    if _menu_anim_prev != selected:
        sel_cy = sy + selected * ITEM_H + bh // 2
        for _ in range(8):
            particles.append(Particle(cx2 + random.randint(-80, 80), sel_cy + random.randint(-10, 10),
                theme["accent"], spd=(0.5, 2.5), life=(0.3, 0.7), sz=(1, 3), shape="circle", acurve="smooth"))
        _menu_anim_prev = selected

    # Glow and arrow phase
    _menu_anim_glow += 0.05
    _menu_arrow_phase += 0.07

    # Draw animated selection highlight (smooth box)
    anim_y = _menu_anim_sel - 4
    bx = cx2 - bw // 2
    by_smooth = int(anim_y)

    # Glow behind selected box
    glow_r = 40 + int(8 * math.sin(_menu_anim_glow * 2))
    draw_glow(surf, cx2, by_smooth + bh // 2, glow_r, theme["accent"], 18)

    # Selection box background
    bs = pygame.Surface((bw, bh), pygame.SRCALPHA)
    bg_a = int(160 + 30 * math.sin(_menu_anim_glow * 2))
    pygame.draw.rect(bs, (*theme["bg"][:3], bg_a), (0, 0, bw, bh), border_radius=12)
    surf.blit(bs, (bx, by_smooth))

    # Animated border — accent color with pulsing brightness
    bp = 0.5 + 0.5 * math.sin(_menu_anim_glow * 3)
    border_c = tuple(clamp(int(c + 30 * bp), 0, 255) for c in theme["accent"])
    pygame.draw.rect(surf, border_c, (bx, by_smooth, bw, bh), 2, border_radius=12)

    # Animated arrows on sides of selected item
    arrow_offset = int(4 * math.sin(_menu_arrow_phase * 3))
    arrow_c = theme["accent"]
    ax_left = bx - 18 + arrow_offset
    ax_right = bx + bw + 10 - arrow_offset
    ay = by_smooth + bh // 2
    # Left arrow ▸ (pointing right)
    pygame.draw.polygon(surf, arrow_c, [(ax_left, ay - 8), (ax_left + 10, ay), (ax_left, ay + 8)])
    # Right arrow ◂ (pointing left)
    pygame.draw.polygon(surf, arrow_c, [(ax_right + 10, ay - 8), (ax_right, ay), (ax_right + 10, ay + 8)])

    # Draw each item
    for i, (label, desc) in enumerate(options):
        y = sy + i * ITEM_H
        if i == selected:
            # White label — slightly scaled up with smooth feel
            scale_t = min(1.0, 0.8 + 0.2 * math.sin(_menu_anim_glow * 2))
            ls = font_lg.render(label, True, (255, 255, 255))
            lsx = cx2 - ls.get_width() // 2
            lsy = by_smooth + 8
            surf.blit(ls, (lsx, lsy))
            # Description
            ds = font_sm.render(desc, True, theme["silver"])
            surf.blit(ds, (cx2 - ds.get_width() // 2, by_smooth + 44))
        else:
            # Subtle hover proximity effect — items closer to selected are slightly brighter
            dist = abs(i - selected)
            base_bright = max(100, 155 - dist * 20)
            item_c = (base_bright, base_bright, base_bright + 15)
            ls = font_md.render(label, True, item_c)
            surf.blit(ls, (cx2 - ls.get_width() // 2, y + 10))
            desc_bright = max(70, 110 - dist * 15)
            ds = font_xs.render(desc, True, (desc_bright, desc_bright, desc_bright + 10))
            surf.blit(ds, (cx2 - ds.get_width() // 2, y + 40))

    # Decorative floating dots around menu area
    for i in range(3):
        dot_x = cx2 + int(280 * math.sin(t * 0.6 + i * 2.094))
        dot_y = 300 + int(80 * math.cos(t * 0.8 + i * 2.094))
        dot_a = int(40 + 30 * math.sin(t * 2 + i))
        dot_s = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(dot_s, (*theme["accent"][:3], dot_a), (3, 3), 3)
        surf.blit(dot_s, (dot_x - 3, dot_y - 3))

    # Controls hint
    hint_c = lerp_color(theme["silver"], theme["bg"], 0.4)
    draw_text(surf, font_xs, "Arrows / WASD = Move    Enter = Start    T = Theme",
              cx2, HEIGHT - 30, hint_c, shadow=True, center=True)

    # Subtle ambient particles
    if random.random() < 0.1:
        particles.append(Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT),
            random.choice(theme["particles"]), spd=(0.2, 1.0), life=(0.5, 1.5), sz=(1, 2), shape="circle", acurve="smooth"))

def draw_pause(surf,t):
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
    cx2=FIELD_W//2
    # On a dark overlay, just use bright white/themed colors directly
    p=0.5+0.5*math.sin(t*3)
    pc=(int(180+75*p), int(180+75*p), int(220+35*p))
    draw_text(surf,font_xl,"Paused",cx2,HEIGHT//2-60,pc,shadow=True,center=True)
    draw_text(surf,font_sm,"Press P or Space to resume",cx2,HEIGHT//2+20,(200,200,220),shadow=True,center=True)
    draw_text(surf,font_sm,"Esc = Back to menu",cx2,HEIGHT//2+50,(160,160,180),shadow=True,center=True)

def draw_levelup_overlay(surf,game,t):
    if game.levelup_anim<=0: return
    a=game.levelup_anim; sw=int(FIELD_H*(1-a))
    for i in range(3):
        ly=sw+i*2
        if 0<=ly<FIELD_H:
            al=int(80*a*(1-i*0.3))
            ls=pygame.Surface((FIELD_W,4),pygame.SRCALPHA); ls.fill((*theme["gold"][:3],al))
            surf.blit(ls,(0,ly))

# ── MAIN LOOP ─────────────────────────────────────────────────────────────
def main():
    global shake_timer,shake_intensity,flash_timer,slow_mo_timer

    state="menu"; menu_sel=0; game=None; mode_keys=["classic","walls","speed"]; dead_saved=False

    running=True
    while running:
        raw_dt=clock.tick(FPS)/1000.0; t=pygame.time.get_ticks()/1000.0
        if slow_mo_timer>0: slow_mo_timer-=raw_dt; dt=raw_dt*0.3
        else: dt=raw_dt

        particles[:]=[p for p in particles if p.update(dt)]
        floating_texts[:]=[ft for ft in floating_texts if ft.update(dt)]
        trails[:]=[tr for tr in trails if tr.update(dt)]
        for star in bg_stars: star.update(dt)
        if flash_timer>0: flash_timer-=dt

        if shake_timer>0:
            shake_timer-=dt; si=int(shake_intensity*(shake_timer/0.5 if shake_timer<0.5 else 1))
            ox=random.randint(-si,si) if si>0 else 0; oy=random.randint(-si,si) if si>0 else 0
        else: ox=oy=0

        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_t and state in ("menu","playing","paused"):
                    set_theme(current_theme_idx+1); save_theme(current_theme_idx)
                    snd_theme.play(); spawn_confetti(WIDTH//2,HEIGHT//2,20)

                if state=="menu":
                    if event.key in (pygame.K_UP,pygame.K_w): menu_sel=(menu_sel-1)%4; snd_select.play()
                    elif event.key in (pygame.K_DOWN,pygame.K_s): menu_sel=(menu_sel+1)%4; snd_select.play()
                    elif event.key==pygame.K_RETURN:
                        snd_select.play()
                        if menu_sel==3: running=False
                        else:
                            game=Game(mode_keys[menu_sel]); state="playing"; dead_saved=False
                            spawn_firework(FIELD_W//2,FIELD_H//2,theme["accent"])
                elif state=="playing":
                    if event.key==pygame.K_ESCAPE: state="menu"; _menu_anim_prev=-1; particles.clear(); floating_texts.clear(); trails.clear()
                    elif event.key in (pygame.K_p,pygame.K_SPACE): state="paused"
                    else: game.handle_input(event.key)
                elif state=="paused":
                    if event.key in (pygame.K_p,pygame.K_SPACE): state="playing"
                    elif event.key==pygame.K_ESCAPE: state="menu"; _menu_anim_prev=-1; particles.clear(); floating_texts.clear(); trails.clear()
                elif state=="dead":
                    if event.key==pygame.K_RETURN:
                        game.reset(); state="playing"; dead_saved=False
                        spawn_firework(FIELD_W//2,FIELD_H//2,theme["accent"])
                    elif event.key==pygame.K_ESCAPE: state="menu"; _menu_anim_prev=-1; particles.clear(); floating_texts.clear(); trails.clear()

        if state=="playing" and game:
            game.update(dt)
            if not game.alive and state=="playing":
                state="dead"
                if not dead_saved: add_score(game.mode,game.score); dead_saved=True
        elif state=="dead" and game: game.update(dt)

        screen.fill(theme["bg"])
        if state=="menu":
            draw_menu(screen,menu_sel,t)
            for p in particles: p.draw(screen)
        else:
            field=pygame.Surface((FIELD_W,FIELD_H)); field.fill(theme["bg"])
            for star in bg_stars: star.draw(field,t)
            draw_grid(field)
            if game:
                draw_walls(field,game,t)
                for tr in trails: tr.draw(field)
                if game.food:
                    fx2,fy2=game.food; fcx=fx2*CELL+CELL//2; fcy=fy2*CELL+CELL//2
                    if game.food_type=="cherry": draw_cherry(field,fcx,fcy,CELL//2,t,theme["food"],theme["food_shine"])
                    else: draw_apple(field,fcx,fcy,CELL//2,t,theme["food"],theme["food_shine"])
                if game.bonus:
                    bx2,by2=game.bonus
                    draw_star_item(field,bx2*CELL+CELL//2,by2*CELL+CELL//2,CELL//2,t,theme["bonus"],game.bonus_timer/6.0)
                if game.powerup:
                    px2,py2=game.powerup
                    draw_powerup_orb(field,px2*CELL+CELL//2,py2*CELL+CELL//2,CELL//2,t,game.powerup_timer/8.0)
                draw_snake(field,game,t); draw_levelup_overlay(field,game,t)
            for p in particles:
                if 0<=p.x<FIELD_W and 0<=p.y<FIELD_H: p.draw(field)
            for ft in floating_texts: ft.draw(field)
            if flash_timer>0:
                fa=int(60*(flash_timer/0.15))
                fs2=pygame.Surface((FIELD_W,FIELD_H),pygame.SRCALPHA); fs2.fill((*flash_color[:3],fa))
                field.blit(fs2,(0,0))
            screen.blit(field,(ox,oy))
            if game: draw_sidebar(screen,game,t)
            if state=="paused": draw_pause(screen,t)
            elif state=="dead": draw_death_screen(screen,game,t)

        pygame.display.flip()

    pygame.quit(); sys.exit()

if __name__=="__main__": main()
