"""
Smart Calculator Ultra — Premium Edition
3 Themes: Dark / Light / Red Neon
by kotan123
"""

import tkinter as tk
import math
import colorsys
import random


# ═══════════════════════════════════════════════════════════
#  THEMES
# ═══════════════════════════════════════════════════════════

THEMES = {
    "dark": {
        "name": "DARK",
        "bg":           "#08081a",
        "surface":      "#101028",
        "surface2":     "#181840",
        "border":       "#2a2a60",
        "text":         "#eef0ff",
        "subtext":      "#7070aa",
        "accent":       "#7a8fff",
        "accent2":      "#5a6adf",
        "green":        "#6fdd8b",
        "yellow":       "#ffc857",
        "red":          "#ff6b8a",
        "purple":       "#c49cff",
        "teal":         "#5cecc6",
        "orange":       "#ffaa5c",
        "num_bg":       "#141435",
        "num_glow":     "#4545a0",
        "func_bg":      "#0c1c30",
        "func_glow":    "#2a7090",
        "op_bg":        "#201540",
        "op_glow":      "#8055dd",
        "eq_bg":        "#2540dd",
        "eq_glow":      "#6090ff",
        "clear_bg":     "#102510",
        "clear_glow":   "#40cc60",
        "aux_bg":       "#151540",
        "aux_glow":     "#5060bb",
        "gradient_sat": 0.7,
        "gradient_val": 0.9,
        "orb_sat":      0.35,
        "orb_val":      0.10,
        "particle_sat": 0.5,
        "particle_val": 0.7,
    },
    "light": {
        "name": "LIGHT",
        "bg":           "#f0f2f8",
        "surface":      "#ffffff",
        "surface2":     "#e8eaf0",
        "border":       "#c0c4d8",
        "text":         "#1a1a2e",
        "subtext":      "#7878a0",
        "accent":       "#4060e0",
        "accent2":      "#3050c0",
        "green":        "#2da050",
        "yellow":       "#d09020",
        "red":          "#e04060",
        "purple":       "#7040c0",
        "teal":         "#209080",
        "orange":       "#d07020",
        "num_bg":       "#f5f6fc",
        "num_glow":     "#b0b8e0",
        "func_bg":      "#e8f0f8",
        "func_glow":    "#80a0d0",
        "op_bg":        "#f0e8f8",
        "op_glow":      "#a080d0",
        "eq_bg":        "#3858e0",
        "eq_glow":      "#6888ff",
        "clear_bg":     "#e8f8ea",
        "clear_glow":   "#50cc70",
        "aux_bg":       "#eaecf5",
        "aux_glow":     "#8890c0",
        "gradient_sat": 0.6,
        "gradient_val": 0.85,
        "orb_sat":      0.15,
        "orb_val":      0.88,
        "particle_sat": 0.4,
        "particle_val": 0.75,
    },
    "red": {
        "name": "NEON RED",
        "bg":           "#0a0008",
        "surface":      "#180810",
        "surface2":     "#250e18",
        "border":       "#501030",
        "text":         "#ffe8f0",
        "subtext":      "#aa5070",
        "accent":       "#ff2050",
        "accent2":      "#dd1840",
        "green":        "#ff6080",
        "yellow":       "#ff8840",
        "red":          "#ff1040",
        "purple":       "#ff40aa",
        "teal":         "#ff5070",
        "orange":       "#ff6030",
        "num_bg":       "#1a0510",
        "num_glow":     "#802040",
        "func_bg":      "#180818",
        "func_glow":    "#901848",
        "op_bg":        "#200a15",
        "op_glow":      "#cc2050",
        "eq_bg":        "#cc1030",
        "eq_glow":      "#ff4060",
        "clear_bg":     "#1a1008",
        "clear_glow":   "#ff8030",
        "aux_bg":       "#1a0a12",
        "aux_glow":     "#aa2050",
        "gradient_sat": 0.9,
        "gradient_val": 0.95,
        "orb_sat":      0.5,
        "orb_val":      0.12,
        "particle_sat": 0.7,
        "particle_val": 0.8,
    },
}


# ═══════════════════════════════════════════════════════════
#  COLOR HELPERS
# ═══════════════════════════════════════════════════════════

def hex2rgb(c):
    h = c.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def rgb2hex(r, g, b):
    r, g, b = max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b)))
    return f"#{r:02x}{g:02x}{b:02x}"

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex2rgb(c1)
    r2, g2, b2 = hex2rgb(c2)
    return rgb2hex(r1+(r2-r1)*t, g1+(g2-g1)*t, b1+(b2-b1)*t)


# ═══════════════════════════════════════════════════════════
#  FLOATING PARTICLES
# ═══════════════════════════════════════════════════════════

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "radius", "life", "decay", "hue", "hue_speed")

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.6, -0.1)
        self.radius = random.uniform(1.5, 4.5)
        self.life = 1.0
        self.decay = random.uniform(0.004, 0.012)
        self.hue = random.random()
        self.hue_speed = random.uniform(0.001, 0.006)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.003
        self.life -= self.decay
        self.hue = (self.hue + self.hue_speed) % 1.0
        return self.life > 0


class ParticleField(tk.Canvas):
    def __init__(self, parent, theme, **kw):
        super().__init__(parent, highlightthickness=0, bd=0, **kw)
        self.theme = theme
        self.particles = []
        self.orbs = []
        self.w = 480
        self.h = 860
        self._init_orbs()
        self._tick()

    def _init_orbs(self):
        self.orbs = []
        for _ in range(6):
            self.orbs.append({
                "x": random.uniform(40, self.w - 40),
                "y": random.uniform(40, self.h - 40),
                "vx": random.uniform(-0.25, 0.25),
                "vy": random.uniform(-0.25, 0.25),
                "r": random.uniform(70, 180),
                "hue": random.random(),
                "hs": random.uniform(0.0004, 0.002),
            })

    def set_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme["bg"])

    def burst(self, x, y, n=10):
        for _ in range(n):
            p = Particle(x + random.uniform(-15, 15), y + random.uniform(-8, 8))
            p.vx = random.uniform(-2.0, 2.0)
            p.vy = random.uniform(-2.5, 0.5)
            p.radius = random.uniform(2, 6)
            p.decay = random.uniform(0.012, 0.03)
            self.particles.append(p)

    def _tick(self):
        self.delete("all")
        T = self.theme

        for o in self.orbs:
            o["x"] += o["vx"]
            o["y"] += o["vy"]
            o["hue"] = (o["hue"] + o["hs"]) % 1.0
            if o["x"] < -50 or o["x"] > self.w + 50: o["vx"] *= -1
            if o["y"] < -50 or o["y"] > self.h + 50: o["vy"] *= -1
            r, g, b = colorsys.hsv_to_rgb(o["hue"], T["orb_sat"], T["orb_val"])
            c = rgb2hex(r*255, g*255, b*255)
            rad = o["r"]
            self.create_oval(o["x"]-rad, o["y"]-rad, o["x"]+rad, o["y"]+rad,
                             fill=c, outline="")

        if random.random() < 0.12:
            self.particles.append(Particle(random.uniform(0, self.w), self.h + 5))

        alive = []
        for p in self.particles:
            if p.update():
                r, g, b = colorsys.hsv_to_rgb(p.hue, T["particle_sat"],
                                               T["particle_val"] * p.life)
                c = rgb2hex(r*255, g*255, b*255)
                self.create_oval(p.x-p.radius, p.y-p.radius,
                                 p.x+p.radius, p.y+p.radius, fill=c, outline="")
                alive.append(p)
        self.particles = alive
        self.after(33, self._tick)


# ═══════════════════════════════════════════════════════════
#  NEON BUTTON
# ═══════════════════════════════════════════════════════════

class NeonButton(tk.Canvas):
    def __init__(self, parent, text, bg, fg, glow, font_cfg,
                 command=None, pfield=None, btn_w=100, btn_h=66, corner=20):
        super().__init__(parent, width=btn_w, height=btn_h,
                         bg=parent["bg"], highlightthickness=0, bd=0)
        self.txt = text
        self.base_bg = bg
        self.fg = fg
        self.glow = glow
        self.fcfg = font_cfg
        self.cmd = command
        self.pfield = pfield
        self.bw = btn_w
        self.bh = btn_h
        self.cr = corner
        self.ht = 0.0
        self.ps = 1.0
        self.ripples = []
        self.hovering = False
        self.pressing = False
        self._draw()
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<ButtonRelease-1>", self._release)

    def update_colors(self, bg, fg, glow, parent_bg):
        self.base_bg = bg
        self.fg = fg
        self.glow = glow
        self.configure(bg=parent_bg)
        self._draw()

    def _rr(self, x0, y0, x1, y1, r, **kw):
        pts = [x0+r,y0, x1-r,y0, x1,y0, x1,y0+r, x1,y1-r, x1,y1,
               x1-r,y1, x0+r,y1, x0,y1, x0,y1-r, x0,y0+r, x0,y0]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self):
        self.delete("all")
        s = self.ps
        cx, cy = self.bw/2, self.bh/2
        hw = (self.bw/2 - 4) * s
        hh = (self.bh/2 - 4) * s
        x0, y0 = cx-hw, cy-hh
        x1, y1 = cx+hw, cy+hh
        r = self.cr * s
        parent_bg = self.configure("bg")[-1]

        # Neon outer glow
        if self.ht > 0:
            for i in range(5, 0, -1):
                g = lerp_color(parent_bg, self.glow, self.ht * 0.12 * (6-i)/5)
                self._rr(x0-i*2, y0-i*2, x1+i*2, y1+i*2, r+i, fill=g, outline="")

        # Shadow
        sh = lerp_color(self.base_bg, "#000000", 0.7)
        self._rr(x0+2, y0+3, x1+2, y1+3, r, fill=sh, outline="")

        # Body
        bg = lerp_color(self.base_bg, self.glow, self.ht * 0.22)
        self._rr(x0, y0, x1, y1, r, fill=bg, outline="")

        # Glass top
        glass = lerp_color(bg, "#ffffff", 0.06 + self.ht * 0.06)
        mid = y0 + (y1-y0) * 0.40
        self._rr(x0+2, y0+2, x1-2, mid, max(1, r-2), fill=glass, outline="")
        self.create_rectangle(x0+3, mid-4, x1-3, mid+1, fill=bg, outline="")

        # Bottom edge
        bot = lerp_color(bg, "#ffffff", 0.025)
        self.create_rectangle(x0+10, y1-5, x1-10, y1-2, fill=bot, outline="")

        # Ripples
        for rp in self.ripples:
            rx, ry, rad, a = rp
            if a > 0:
                rc = lerp_color(bg, "#ffffff", a * 0.3)
                self.create_oval(rx-rad, ry-rad, rx+rad, ry+rad, fill=rc, outline="")

        # Inner border
        if self.ht > 0.2:
            bc = lerp_color(bg, self.glow, (self.ht-0.2)*0.6)
            self._rr(x0+1, y0+1, x1-1, y1-1, max(1, r-1), fill="", outline=bc, width=1)

        # Text
        tx, ty = cx, cy + s
        ts = lerp_color(bg, "#000000", 0.5)
        self.create_text(tx+1, ty+1, text=self.txt, fill=ts, font=self.fcfg)
        tfg = lerp_color(self.fg, "#ffffff", self.ht * 0.35)
        self.create_text(tx, ty, text=self.txt, fill=tfg, font=self.fcfg)

    def _enter(self, e):
        self.hovering = True; self._anim_in()
    def _leave(self, e):
        self.hovering = False; self.pressing = False; self._anim_out()
    def _press(self, e):
        self.pressing = True
        self.ripples.append([e.x, e.y, 3, 0.65])
        self.ps = 0.90; self._draw(); self._anim_ripple()
        if self.pfield:
            try:
                ax = self.winfo_rootx() - self.pfield.winfo_rootx() + e.x
                ay = self.winfo_rooty() - self.pfield.winfo_rooty() + e.y
                self.pfield.burst(ax, ay, 6)
            except: pass
    def _release(self, e):
        if self.pressing:
            self.pressing = False; self._spring()
            if self.cmd: self.cmd()

    def _anim_in(self):
        if not self.hovering: return
        self.ht = min(1.0, self.ht + 0.12); self._draw()
        if self.ht < 1.0: self.after(16, self._anim_in)
    def _anim_out(self):
        if self.hovering: return
        self.ht = max(0, self.ht - 0.08); self._draw()
        if self.ht > 0: self.after(16, self._anim_out)
    def _spring(self):
        d = 1.0 - self.ps
        if abs(d) < 0.004: self.ps = 1.0; self._draw(); return
        self.ps += d * 0.28; self._draw(); self.after(16, self._spring)
    def _anim_ripple(self):
        alive = False
        for rp in self.ripples:
            rp[2] += 6; rp[3] -= 0.04
            if rp[3] > 0: alive = True
        self.ripples = [r for r in self.ripples if r[3] > 0]
        self._draw()
        if alive: self.after(16, self._anim_ripple)


# ═══════════════════════════════════════════════════════════
#  GRADIENT BAR
# ═══════════════════════════════════════════════════════════

class GradientBar(tk.Canvas):
    def __init__(self, parent, theme, height=5, **kw):
        super().__init__(parent, height=height, highlightthickness=0, bd=0, **kw)
        self.theme = theme
        self.hue = 0.0
        self.bh = height
        self._tick()

    def set_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme["bg"])

    def _tick(self):
        self.delete("all")
        w = self.winfo_width() or 480
        T = self.theme
        for x in range(0, w, 2):
            h = (self.hue + x/w * 0.35) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, T["gradient_sat"], T["gradient_val"])
            c = rgb2hex(r*255, g*255, b*255)
            self.create_rectangle(x, 0, x+2, self.bh, fill=c, outline="")
        self.hue = (self.hue + 0.005) % 1.0
        self.after(40, self._tick)


# ═══════════════════════════════════════════════════════════
#  MAIN CALCULATOR
# ═══════════════════════════════════════════════════════════

class SmartCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Calculator")
        self.root.geometry("480x860")
        self.root.resizable(False, False)

        self.theme_name = "dark"
        self.T = THEMES["dark"]
        self.root.configure(bg=self.T["bg"])

        try: self.root.attributes("-alpha", 0.0)
        except: pass

        self.expression = ""
        self.just_calc = False
        self.font_size = 44.0
        self.target_fs = 44.0
        self.angle_mode = "rad"

        self._build()
        self._fade_in()

    def _build(self):
        T = self.T

        # Particles
        self.pfield = ParticleField(self.root, T, bg=T["bg"])
        self.pfield.place(x=0, y=0, relwidth=1, relheight=1)

        # Top gradient
        self.grad_top = GradientBar(self.root, T, height=4, bg=T["bg"])
        self.grad_top.place(x=0, y=0, relwidth=1)

        # Display
        self.disp_frame = tk.Frame(self.root, bg=T["bg"])
        self.disp_frame.place(x=20, y=12, width=440, height=175)

        # Title + theme switcher
        title_row = tk.Frame(self.disp_frame, bg=T["bg"])
        title_row.pack(fill="x", padx=8, pady=(8, 0))

        self.title_lbl = tk.Label(title_row, text="SMART CALC",
                                  font=("Segoe UI", 10, "bold"),
                                  fg=T["subtext"], bg=T["bg"], anchor="w")
        self.title_lbl.pack(side="left")

        theme_fr = tk.Frame(title_row, bg=T["bg"])
        theme_fr.pack(side="right")

        self.theme_btns = {}
        for tname, emoji in [("dark", "Dark"), ("light", "Light"), ("red", "Red")]:
            btn = tk.Label(theme_fr, text=emoji, font=("Segoe UI", 9, "bold"),
                           bg=T["surface2"], fg=T["subtext"],
                           cursor="hand2", padx=8, pady=1)
            btn.pack(side="left", padx=2)
            btn.bind("<Button-1>", lambda e, n=tname: self._switch_theme(n))
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=self.T["accent"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=self.T["subtext"]))
            self.theme_btns[tname] = btn

        # History
        self.hist_var = tk.StringVar(value="")
        self.hist_lbl = tk.Label(self.disp_frame, textvariable=self.hist_var,
                                 font=("Segoe UI", 13), fg=T["subtext"],
                                 bg=T["bg"], anchor="e")
        self.hist_lbl.pack(fill="x", padx=10, pady=(2, 0))

        # Display box
        self.disp_box = tk.Frame(self.disp_frame, bg=T["surface"],
                                 highlightbackground=T["border"],
                                 highlightthickness=2, relief="flat")
        self.disp_box.pack(fill="x", padx=5, pady=(4, 8), ipady=12)

        self.disp_var = tk.StringVar(value="0")
        self.disp_lbl = tk.Label(self.disp_box, textvariable=self.disp_var,
                                 font=("Segoe UI", 44, "bold"), fg=T["text"],
                                 bg=T["surface"], anchor="e", padx=15)
        self.disp_lbl.pack(fill="x")

        # Backspace
        self.del_lbl = tk.Label(self.disp_frame, text="⌫", font=("Segoe UI", 15),
                                fg=T["red"], bg=T["bg"], cursor="hand2")
        self.del_lbl.place(x=12, y=62)
        self.del_lbl.bind("<Button-1>", lambda e: self._backspace())

        # Mode bar
        self.mode_frame = tk.Frame(self.root, bg=T["bg"])
        self.mode_frame.place(x=25, y=192, width=430, height=28)

        self.mode_lbl = tk.Label(self.mode_frame, text="RAD",
                                 font=("Segoe UI", 9, "bold"),
                                 fg=T["teal"], bg=T["surface2"],
                                 padx=10, pady=2, cursor="hand2")
        self.mode_lbl.pack(side="left")
        self.mode_lbl.bind("<Button-1>", self._toggle_mode)

        self.theme_name_lbl = tk.Label(self.mode_frame, text="DARK",
                                       font=("Segoe UI", 9, "bold"),
                                       fg=T["accent"], bg=T["surface2"],
                                       padx=10, pady=2)
        self.theme_name_lbl.pack(side="right")

        # Separator
        self.sep = tk.Canvas(self.root, height=1, bg=T["bg"], highlightthickness=0, bd=0)
        self.sep.place(x=25, y=226, width=430)
        self.sep.create_line(0, 0, 430, 0, fill=T["border"])

        # Buttons
        self.btn_frame = tk.Frame(self.root, bg=T["bg"])
        self.btn_frame.place(x=10, y=234, width=460, height=610)

        for i in range(8): self.btn_frame.rowconfigure(i, weight=1)
        for j in range(4): self.btn_frame.columnconfigure(j, weight=1)

        self.buttons = []
        self._create_buttons()

        # Bottom gradient
        self.grad_bot = GradientBar(self.root, T, height=3, bg=T["bg"])
        self.grad_bot.place(x=0, rely=1.0, relwidth=1, anchor="sw")

        # Keyboard
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Return>", lambda e: self._calculate())
        self.root.bind("<BackSpace>", lambda e: self._backspace())
        self.root.bind("<Escape>", lambda e: self._clear())

    def _btn_layout(self):
        T = self.T
        return [
            ("sin",  T["func_bg"],  T["func_glow"], T["teal"],   0, 0),
            ("cos",  T["func_bg"],  T["func_glow"], T["teal"],   0, 1),
            ("tan",  T["func_bg"],  T["func_glow"], T["teal"],   0, 2),
            ("log",  T["func_bg"],  T["func_glow"], T["teal"],   0, 3),
            ("√",    T["func_bg"],  T["func_glow"], T["purple"], 1, 0),
            ("x²",   T["func_bg"],  T["func_glow"], T["purple"], 1, 1),
            ("xʸ",   T["func_bg"],  T["func_glow"], T["purple"], 1, 2),
            ("ln",   T["func_bg"],  T["func_glow"], T["teal"],   1, 3),
            ("π",    T["aux_bg"],   T["aux_glow"],  T["orange"], 2, 0),
            ("e",    T["aux_bg"],   T["aux_glow"],  T["orange"], 2, 1),
            ("!",    T["aux_bg"],   T["aux_glow"],  T["orange"], 2, 2),
            ("⌫",    T["aux_bg"],   T["red"],       T["red"],    2, 3),
            ("C",    T["clear_bg"], T["clear_glow"],T["green"],  3, 0),
            ("( )",  T["aux_bg"],   T["aux_glow"],  T["subtext"],3, 1),
            ("%",    T["aux_bg"],   T["aux_glow"],  T["subtext"],3, 2),
            ("÷",    T["op_bg"],    T["op_glow"],   T["yellow"], 3, 3),
            ("7",    T["num_bg"],   T["num_glow"],  T["text"],   4, 0),
            ("8",    T["num_bg"],   T["num_glow"],  T["text"],   4, 1),
            ("9",    T["num_bg"],   T["num_glow"],  T["text"],   4, 2),
            ("×",    T["op_bg"],    T["op_glow"],   T["yellow"], 4, 3),
            ("4",    T["num_bg"],   T["num_glow"],  T["text"],   5, 0),
            ("5",    T["num_bg"],   T["num_glow"],  T["text"],   5, 1),
            ("6",    T["num_bg"],   T["num_glow"],  T["text"],   5, 2),
            ("−",    T["op_bg"],    T["op_glow"],   T["yellow"], 5, 3),
            ("1",    T["num_bg"],   T["num_glow"],  T["text"],   6, 0),
            ("2",    T["num_bg"],   T["num_glow"],  T["text"],   6, 1),
            ("3",    T["num_bg"],   T["num_glow"],  T["text"],   6, 2),
            ("+",    T["op_bg"],    T["op_glow"],   T["yellow"], 6, 3),
            ("±",    T["num_bg"],   T["num_glow"],  T["subtext"],7, 0),
            ("0",    T["num_bg"],   T["num_glow"],  T["text"],   7, 1),
            (".",    T["num_bg"],   T["num_glow"],  T["text"],   7, 2),
            ("=",    T["eq_bg"],    T["eq_glow"],   "#ffffff",   7, 3),
        ]

    def _create_buttons(self):
        font = ("Segoe UI", 16, "bold")
        for (text, bg, glow, fg, row, col) in self._btn_layout():
            btn = NeonButton(self.btn_frame, text=text, bg=bg, fg=fg, glow=glow,
                             font_cfg=font, command=lambda t=text: self._on_btn(t),
                             pfield=self.pfield, btn_w=105, btn_h=68, corner=18)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.buttons.append((text, btn))

    # ── THEME ──

    def _switch_theme(self, name):
        if name == self.theme_name: return
        self.theme_name = name
        self.T = THEMES[name]
        T = self.T

        names = {"dark": "DARK", "light": "LIGHT", "red": "NEON RED"}
        self.theme_name_lbl.config(text=names[name], fg=T["accent"])

        self.root.configure(bg=T["bg"])
        self.pfield.set_theme(T)
        self.grad_top.set_theme(T)
        self.grad_bot.set_theme(T)

        for w in [self.disp_frame, self.mode_frame]:
            w.configure(bg=T["bg"])

        self.title_lbl.configure(bg=T["bg"], fg=T["subtext"])
        self.hist_lbl.configure(bg=T["bg"], fg=T["subtext"])
        self.disp_box.configure(bg=T["surface"], highlightbackground=T["border"])
        self.disp_lbl.configure(bg=T["surface"], fg=T["text"])
        self.del_lbl.configure(bg=T["bg"], fg=T["red"])
        self.mode_lbl.configure(bg=T["surface2"],
                                fg=T["teal"] if self.angle_mode == "rad" else T["yellow"])
        self.theme_name_lbl.configure(bg=T["surface2"])
        self.btn_frame.configure(bg=T["bg"])
        self.sep.configure(bg=T["bg"])
        self.sep.delete("all")
        self.sep.create_line(0, 0, 430, 0, fill=T["border"])

        for tbtn in self.theme_btns.values():
            tbtn.configure(bg=T["surface2"], fg=T["subtext"])

        layout = self._btn_layout()
        for i, (text, bg, glow, fg, row, col) in enumerate(layout):
            self.buttons[i][1].update_colors(bg, fg, glow, T["bg"])

    # ── ANIMATIONS ──

    def _fade_in(self):
        a = [0.0]
        def step():
            a[0] = min(1.0, a[0] + 0.07)
            try: self.root.attributes("-alpha", a[0])
            except: pass
            if a[0] < 1.0: self.root.after(16, step)
        step()

    def _flash(self, color):
        T = self.T
        intensity = [1.0]
        def step():
            intensity[0] = max(0, intensity[0] - 0.04)
            t = intensity[0]
            bc = lerp_color(T["border"], color, t)
            tc = lerp_color(T["text"], color, t * 0.5)
            self.disp_box.configure(highlightbackground=bc)
            self.disp_lbl.configure(fg=tc)
            if intensity[0] > 0:
                self.root.after(25, step)
            else:
                self.disp_box.configure(highlightbackground=T["border"])
                self.disp_lbl.configure(fg=T["text"])
        step()

    def _anim_font(self):
        ln = len(self.disp_var.get())
        if ln <= 7: self.target_fs = 44
        elif ln <= 10: self.target_fs = 36
        elif ln <= 14: self.target_fs = 30
        elif ln <= 20: self.target_fs = 24
        else: self.target_fs = 18
        self._smooth_font()

    def _smooth_font(self):
        d = self.target_fs - self.font_size
        if abs(d) < 0.5:
            self.font_size = self.target_fs
            self.disp_lbl.configure(font=("Segoe UI", int(self.font_size), "bold"))
            return
        self.font_size += d * 0.28
        self.disp_lbl.configure(font=("Segoe UI", int(self.font_size), "bold"))
        self.root.after(16, self._smooth_font)

    # ── INPUT ──

    def _toggle_mode(self, e=None):
        T = self.T
        if self.angle_mode == "rad":
            self.angle_mode = "deg"
            self.mode_lbl.config(text="DEG", fg=T["yellow"])
        else:
            self.angle_mode = "rad"
            self.mode_lbl.config(text="RAD", fg=T["teal"])

    def _on_key(self, e):
        k = e.char
        if k in "0123456789.": self._on_btn(k)
        elif k == "+": self._on_btn("+")
        elif k == "-": self._on_btn("−")
        elif k == "*": self._on_btn("×")
        elif k == "/": self._on_btn("÷")
        elif k == "%": self._on_btn("%")
        elif k == "^": self._on_btn("xʸ")
        elif k == "(": self._append("(")
        elif k == ")": self._append(")")
        elif k == "!": self._on_btn("!")

    def _on_btn(self, t):
        actions = {"C": self._clear, "=": self._calculate,
                   "±": self._negate, "( )": self._smart_parens}
        if t in actions: actions[t](); return

        inserts = {"sin":"sin(", "cos":"cos(", "tan":"tan(",
                   "√":"sqrt(", "log":"log10(", "ln":"log(",
                   "x²":"²", "xʸ":"^",
                   "π": str(round(math.pi, 10)),
                   "e": str(round(math.e, 10))}
        if t in inserts:
            if t in ("π", "e"): self._insert(inserts[t])
            else: self._append(inserts[t])
            return

        if t == "!": self._append("!"); return
        if t == "⌫": self._backspace(); return

        if t in "0123456789.": self._insert(t)
        elif t == "+": self._append("+")
        elif t == "−": self._append("-")
        elif t == "×": self._append("*")
        elif t == "÷": self._append("/")
        elif t == "%": self._append("%")

    def _insert(self, ch):
        if self.just_calc and ch in "0123456789.":
            self.expression = ""
        self.just_calc = False
        self._append(ch)

    def _append(self, ch):
        if self.just_calc and ch in "+-*/%^":
            self.just_calc = False
        if self.expression == "0" and ch not in ".+-*/%^)²!":
            self.expression = ""
        self.expression += ch
        self._update_disp()

    def _clear(self):
        self.expression = ""
        self.just_calc = False
        self.hist_var.set("")
        self.disp_var.set("0")
        self._flash(self.T["green"])
        self._anim_font()

    def _backspace(self):
        if not self.expression: return
        for tok in ["sin(", "cos(", "tan(", "sqrt(", "log10(", "log("]:
            if self.expression.endswith(tok):
                self.expression = self.expression[:-len(tok)]
                self._update_disp(); return
        self.expression = self.expression[:-1]
        self._update_disp()

    def _negate(self):
        if not self.expression: return
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression
        self._update_disp()

    def _smart_parens(self):
        o = self.expression.count("(")
        c = self.expression.count(")")
        last = self.expression[-1] if self.expression else ""
        if o <= c or last in "+-*/(^":
            self._append("(")
        else:
            self._append(")")

    def _update_disp(self):
        d = self.expression if self.expression else "0"
        self.disp_var.set(d.replace("*", "×").replace("/", "÷"))
        self._anim_font()

    # ── CALCULATE ──

    def _calculate(self):
        if not self.expression: return
        try:
            expr = self.expression
            diff = expr.count("(") - expr.count(")")
            if diff > 0: expr += ")" * diff

            while "!" in expr:
                idx = expr.index("!")
                j = idx - 1
                if j >= 0 and expr[j] == ")":
                    depth = 1; j -= 1
                    while j >= 0 and depth > 0:
                        if expr[j] == ")": depth += 1
                        elif expr[j] == "(": depth -= 1
                        j -= 1
                    j += 1
                    expr = expr[:j] + f"fact({expr[j:idx]})" + expr[idx+1:]
                else:
                    while j >= 0 and (expr[j].isdigit() or expr[j] == "."): j -= 1
                    j += 1
                    expr = expr[:j] + f"fact({expr[j:idx]})" + expr[idx+1:]

            expr = expr.replace("²", "**2").replace("^", "**").replace("%", "/100")

            if self.angle_mode == "deg":
                import re
                for fn in ["sin", "cos", "tan"]:
                    expr = re.sub(rf'{fn}\(', f'{fn}(rad(', expr)

            def fact(n): return math.factorial(int(n))
            def rad(x): return math.radians(x)

            ns = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
                  "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                  "abs": abs, "pi": math.pi, "e": math.e,
                  "asin": math.asin, "acos": math.acos, "atan": math.atan,
                  "fact": fact, "rad": rad, "math": math}

            result = eval(expr, {"__builtins__": {}}, ns)

            if isinstance(result, float):
                if result == int(result) and abs(result) < 1e15:
                    result = int(result)
                else:
                    result = round(result, 10)
                    s = f"{result:.10f}".rstrip("0").rstrip(".")
                    result = float(s) if "." in s else int(s)

            pretty = self.expression.replace("*", "×").replace("/", "÷")
            self.hist_var.set(f"{pretty} =")
            self.expression = str(result)
            self.disp_var.set(str(result))
            self.just_calc = True
            self._flash(self.T["accent"])
            self._anim_font()
            self.pfield.burst(240, 100, 20)

        except ZeroDivisionError:
            self._error("Cannot divide by zero")
        except Exception:
            self._error("Error")

    def _error(self, msg):
        self.hist_var.set("")
        self.disp_var.set(msg)
        self.expression = ""
        self.just_calc = False
        self._flash(self.T["red"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SmartCalculator().run()
