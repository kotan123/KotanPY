import customtkinter as ctk
import string, secrets, pyperclip, os, sys
import tkinter as tk
from PIL import Image, ImageTk

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BG_PATH  = os.path.join(BASE_DIR, "background.png")
ICON_ICO = os.path.join(BASE_DIR, "icon.ico")
ICON_PNG = os.path.join(BASE_DIR, "icon.png")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT       = "#00AAFF"
ACCENT_HOVER = "#2EC4FF"
BG_DARK      = "#080E1C"
CARD         = "#0B1528"
CARD_BORDER  = "#14263F"
WHITE        = "#F0F4FA"
DIM          = "#5C7599"
GREEN        = "#2EE88A"
ORANGE       = "#FFB347"
RED          = "#FF5252"

W, H = 480, 620


def strength(pw):
    s = 0
    n = len(pw)
    if n >= 8:  s += 1
    if n >= 12: s += 1
    if n >= 16: s += 1
    if n >= 20: s += 1
    if any(c in string.ascii_lowercase for c in pw): s += 1
    if any(c in string.ascii_uppercase for c in pw): s += 1
    if any(c in string.digits for c in pw):          s += 1
    if any(c in string.punctuation for c in pw):     s += 1
    if s <= 2:   return "Weak", RED, 1
    elif s <= 4: return "Fair", ORANGE, 2
    elif s <= 6: return "Strong", "#6DD98E", 3
    else:        return "Very Strong", GREEN, 4


def gen_pw(length, upper, lower, digits, symbols):
    pool, req = "", []
    if upper:
        pool += string.ascii_uppercase
        req.append(secrets.choice(string.ascii_uppercase))
    if lower:
        pool += string.ascii_lowercase
        req.append(secrets.choice(string.ascii_lowercase))
    if digits:
        pool += string.digits
        req.append(secrets.choice(string.digits))
    if symbols:
        pool += string.punctuation
        req.append(secrets.choice(string.punctuation))
    if not pool:
        pool = string.ascii_letters + string.digits
        req = [secrets.choice(string.ascii_letters)]
    rest = max(0, length - len(req))
    c = req + [secrets.choice(pool) for _ in range(rest)]
    for i in range(len(c) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        c[i], c[j] = c[j], c[i]
    return "".join(c)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)
        if os.path.exists(ICON_ICO):
            self.iconbitmap(ICON_ICO)
        self._img = {}
        self.hist = []

        if os.path.exists(BG_PATH):
            raw = Image.open(BG_PATH).convert("RGBA")
            iw, ih = raw.size
            sc = max(W / iw, H / ih)
            nw, nh = int(iw * sc), int(ih * sc)
            raw = raw.resize((nw, nh), Image.LANCZOS)
            l, t = (nw - W) // 2, (nh - H) // 2
            bg = raw.crop((l, t, l + W, t + H))
            self._img["bg"] = ImageTk.PhotoImage(bg)
            lbl = tk.Label(self, image=self._img["bg"], bd=0, highlightthickness=0)
            lbl.place(x=0, y=0, relwidth=1, relheight=1)

        self._build()

    def _build(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=50, pady=(28, 32))

        # ---- Header ----
        hdr = ctk.CTkFrame(wrap, fg_color="transparent")
        hdr.pack(pady=(0, 18))
        if os.path.exists(ICON_PNG):
            ic = Image.open(ICON_PNG).resize((28, 28), Image.LANCZOS)
            self._img["ic"] = ctk.CTkImage(ic, ic, (28, 28))
            ctk.CTkLabel(hdr, image=self._img["ic"], text="").pack(side="left", padx=(0, 10))
        ctk.CTkLabel(hdr, text="Password Generator", fg_color="transparent",
                     font=ctk.CTkFont("Segoe UI", 18, "bold"), text_color=WHITE).pack(side="left")

        # ---- Output field ----
        self.pw_var = ctk.StringVar(value="")
        ctk.CTkEntry(wrap, textvariable=self.pw_var,
                     font=ctk.CTkFont("Consolas", 14, "bold"),
                     fg_color=CARD, border_width=1, border_color=CARD_BORDER,
                     text_color=WHITE, justify="center", corner_radius=10,
                     state="readonly", height=36).pack(fill="x", padx=4, pady=(0, 6))

        # strength bar
        sf = ctk.CTkFrame(wrap, fg_color="transparent")
        sf.pack(fill="x", pady=(0, 2))
        self._bars = []
        for i in range(4):
            b = ctk.CTkFrame(sf, fg_color="#162035", corner_radius=2, height=3)
            b.pack(side="left", fill="x", expand=True, padx=(0 if i == 0 else 3, 0))
            self._bars.append(b)
        self.str_lbl = ctk.CTkLabel(wrap, text="", font=ctk.CTkFont(size=10), text_color=DIM)
        self.str_lbl.pack(pady=(0, 14))

        # ---- Settings card ----
        sc = ctk.CTkFrame(wrap, fg_color=CARD, corner_radius=12,
                          border_width=1, border_color=CARD_BORDER)
        sc.pack(fill="x", pady=(0, 16))
        si = ctk.CTkFrame(sc, fg_color="transparent")
        si.pack(fill="x", padx=28, pady=(18, 18))

        # length
        lr = ctk.CTkFrame(si, fg_color="transparent")
        lr.pack(fill="x")
        ctk.CTkLabel(lr, text="Length", font=ctk.CTkFont(size=12), text_color=DIM).pack(side="left")
        self.len_lbl = ctk.CTkLabel(lr, text="16", width=26, corner_radius=4,
                                    font=ctk.CTkFont(size=12, weight="bold"), text_color=ACCENT,
                                    fg_color="#0A1420")
        self.len_lbl.pack(side="right")

        self.slider = ctk.CTkSlider(si, from_=4, to=64, number_of_steps=60,
                                    button_color=ACCENT, button_hover_color=ACCENT_HOVER,
                                    progress_color=ACCENT, fg_color="#162035", height=12,
                                    command=self._sl)
        self.slider.set(16)
        self.slider.pack(fill="x", pady=(6, 10))

        ctk.CTkFrame(si, fg_color=CARD_BORDER, height=1).pack(fill="x", pady=(0, 8))

        self.v_up  = ctk.BooleanVar(value=True)
        self.v_lo  = ctk.BooleanVar(value=True)
        self.v_dig = ctk.BooleanVar(value=True)
        self.v_sym = ctk.BooleanVar(value=True)

        g = ctk.CTkFrame(si, fg_color="transparent")
        g.pack(fill="x")
        g.columnconfigure((0, 1), weight=1)
        for i, (t, v) in enumerate([
            ("A-Z", self.v_up), ("a-z", self.v_lo),
            ("0-9", self.v_dig), ("!@#", self.v_sym)
        ]):
            ctk.CTkCheckBox(g, text=t, variable=v,
                            font=ctk.CTkFont(size=12), text_color=WHITE,
                            fg_color=ACCENT, hover_color=ACCENT_HOVER,
                            border_color="#253555", corner_radius=4,
                            border_width=2, checkbox_width=16, checkbox_height=16
                            ).grid(row=i // 2, column=i % 2, sticky="w", pady=4, padx=4)

        # ---- Buttons (inside settings card) ----
        ctk.CTkFrame(si, fg_color=CARD_BORDER, height=1).pack(fill="x", pady=(8, 10))
        br = ctk.CTkFrame(si, fg_color="transparent")
        br.pack()

        self.gen_btn = ctk.CTkButton(
            br, text="Generate",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0070CC", hover_color="#0090EE",
            text_color="#FFFFFF", corner_radius=6, height=28, width=110,
            border_width=0, command=self._gen
        )
        self.gen_btn.pack(side="left", padx=(0, 8))

        self.cp_btn = ctk.CTkButton(
            br, text="Copy",
            font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color="#162035",
            text_color="#6CB8E6", corner_radius=6, height=28, width=80,
            border_width=1, border_color="#1A3A58",
            command=self._cp
        )
        self.cp_btn.pack(side="left")

        # ---- History ----
        hdr_h = ctk.CTkFrame(wrap, fg_color="transparent")
        hdr_h.pack(fill="x", padx=6, pady=(0, 4))
        ctk.CTkLabel(hdr_h, text="Recent", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=DIM).pack(side="left")
        ctk.CTkButton(hdr_h, text="Clear", width=40, height=18,
                      font=ctk.CTkFont(size=10), fg_color="transparent",
                      hover_color="#162035", text_color=DIM, corner_radius=4,
                      command=self._clr).pack(side="right")
        hc = ctk.CTkFrame(wrap, fg_color=CARD, corner_radius=12,
                          border_width=1, border_color=CARD_BORDER)
        hc.pack(fill="both", expand=True)
        self.hbox = ctk.CTkTextbox(hc, fg_color="transparent",
                                   font=ctk.CTkFont("Consolas", 11),
                                   text_color=DIM, border_width=0,
                                   activate_scrollbars=False)
        self.hbox.pack(fill="both", expand=True, padx=16, pady=10)
        self.hbox.configure(state="disabled")

    def _sl(self, v):
        self.len_lbl.configure(text=str(int(v)))

    def _gen(self):
        pw = gen_pw(int(self.slider.get()),
                    self.v_up.get(), self.v_lo.get(),
                    self.v_dig.get(), self.v_sym.get())
        self.pw_var.set(pw)
        lbl, col, segs = strength(pw)
        for i, b in enumerate(self._bars):
            b.configure(fg_color=col if i < segs else "#162035")
        self.str_lbl.configure(text=lbl, text_color=col)
        self.hist.insert(0, pw)
        self.hist = self.hist[:5]
        self._uh()
        self.gen_btn.configure(fg_color="#0090EE")
        self.after(120, lambda: self.gen_btn.configure(fg_color="#0070CC"))

    def _cp(self):
        pw = self.pw_var.get()
        if pw:
            pyperclip.copy(pw)
            self.cp_btn.configure(text="Copied!", text_color=GREEN)
            self.after(1200, lambda: self.cp_btn.configure(
                text="Copy", text_color="#6CB8E6"))

    def _uh(self):
        self.hbox.configure(state="normal")
        self.hbox.delete("1.0", "end")
        for i, p in enumerate(self.hist, 1):
            self.hbox.insert("end", f"  {i}.  {p}\n")
        self.hbox.configure(state="disabled")

    def _clr(self):
        self.hist.clear()
        self._uh()


if __name__ == "__main__":
    App().mainloop()
