"""
Kiro Pet - one cute pixel buddy that walks around your Kiro window.

A single pixel-art mascot (rendered in smooth 16/32-bit style via Scale2x +
auto shading) patrols the border of the Kiro editor window, following it as
you move/resize Kiro and hiding when Kiro is gone. It naps when you go idle
and occasionally dashes. Pick which mascot you want from the chooser.

Mascots: MuvMuv (pup in a tabby hood), Lunar (panda-duck in an eggshell),
Any (bunny-poncho girl), Shiro (Shin-chan's dog), Goldie in a red shirt,
Goldie in brown overalls, LOLO (strawberry kitten), Butter bear (café bear),
Buriburizaemon (hero pig).

Usage:
    pythonw kiro_pet.py                 # opens the picker
    pythonw kiro_pet.py --mascot lunar  # skip the picker
    pythonw kiro_pet.py --target code   # follow another app instead of Kiro
    pythonw kiro_pet.py --free          # roam the whole screen

Controls:
    Left-drag   : pick it up
    Left-click  : poke it (it hops / new activity)
    Right-click : menu -> change buddy / Thai word / break interval / quit
"""

import argparse
import ctypes
from ctypes import wintypes
import os
import random
import time
import tkinter as tk

import sprites as S

# The HD grid from S.hd() is 2x the authored size, so scale 3/4 keeps the
# pet the same on-screen size with twice the pixel detail.
NUM, DEN = 3, 4
SIDE = max(S.W, S.H) * 2 * NUM // DEN    # square so the sprite fits when rotated
WIN_W = WIN_H = SIDE + 6                 # a little transparent margin
HALF = SIDE // 2                         # sprite half-extent (~18)
INSET = HALF + 4                         # keep the pet fully inside Kiro's edge
TRANSPARENT = S.TRANSPARENT
IDLE_SLEEP = 90                          # walker naps after this many idle seconds

# Desktop buddy: a bigger, free-roaming pal (~2x the walker).
D_NUM, D_DEN = 3, 2
DSCENE_W = S.SCENE_W * 2 * D_NUM // D_DEN    # 120
DSCENE_H = S.SCENE_H * 2 * D_NUM // D_DEN    # 84
DWIN_W = DSCENE_W + 8
DWIN_H = DSCENE_H + 8
BREAK_EVERY = 60 * 60                    # default: nudge for a break every 1 hour

# ------------------------------------------------------------------ Win32
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


class MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]


user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetForegroundWindow.restype = wintypes.HWND
user32.MonitorFromWindow.restype = ctypes.c_void_p
user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
user32.GetMonitorInfoW.argtypes = [ctypes.c_void_p, ctypes.POINTER(MONITORINFO)]
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int,
                                ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]

HWND_TOPMOST = wintypes.HWND(-1)
_SWP = 0x0001 | 0x0002 | 0x0010          # NOSIZE | NOMOVE | NOACTIVATE

user32.OpenInputDesktop.restype = wintypes.HANDLE
user32.OpenInputDesktop.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
user32.CloseDesktop.argtypes = [wintypes.HANDLE]


def keep_on_top(hwnd):
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, _SWP)


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]


def idle_seconds():
    """Seconds since the last keyboard/mouse input anywhere in the session."""
    li = LASTINPUTINFO()
    li.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if not user32.GetLastInputInfo(ctypes.byref(li)):
        return 0.0
    return max(0, kernel32.GetTickCount() - li.dwTime) / 1000.0


def is_locked():
    """True when the workstation is locked. When locked, the input desktop is
    the secure Winlogon desktop, which a normal process cannot open."""
    h = user32.OpenInputDesktop(0, False, 0x0001)   # DESKTOP_READOBJECTS
    if h:
        user32.CloseDesktop(h)
        return False
    return True


def work_area(hwnd):
    """Visible work area (minus taskbar) of the monitor holding hwnd."""
    hmon = user32.MonitorFromWindow(hwnd, 2)      # MONITOR_DEFAULTTONEAREST
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
        r = mi.rcWork
        return (r.left, r.top, r.right, r.bottom)
    return None


def edge_rot(nx, ny):
    """Rotation so the mascot's feet are on the frame, head pointing inward."""
    if ny == 1:
        return 0        # bottom edge -> upright
    if nx == -1:
        return 1        # left edge
    if ny == -1:
        return 2        # top edge -> upside-down
    return 3            # right edge


from thai_vocab import VOCAB as PHRASES   # basic Thai deck (Thai, rom, English)

FPS = 30
SPEAK_EVERY = 5 * 60 * FPS               # ~5 minutes
SPEAK_HOLD = int(8.5 * FPS)              # bubble stays ~8.5s


def _proc_name(pid):
    h = kernel32.OpenProcess(0x1000, False, pid)
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(512)
        size = wintypes.DWORD(512)
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return buf.value
    finally:
        kernel32.CloseHandle(h)
    return ""


def find_window_rect(name):
    name = name.lower()
    hits = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pn = _proc_name(pid.value).lower()
        n = user32.GetWindowTextLengthW(hwnd)
        tbuf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, tbuf, n + 1)
        title = tbuf.value.lower()
        if name in pn or (title and name in title):
            r = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(r))
            w, h = r.right - r.left, r.bottom - r.top
            if w > 250 and h > 200 and r.left > -30000:      # skip minimized
                hits.append((r.left, r.top, r.right, r.bottom, w * h))
        return True

    user32.EnumWindows(cb, 0)
    if not hits:
        return None
    hits.sort(key=lambda x: x[4])
    return hits[-1][:4]


def perimeter_point(rect, s):
    """(x, y, nx, ny, face) walking clockwise around the rectangle outline."""
    L, T, R, B = rect
    W, Hh = R - L, B - T
    P = 2 * (W + Hh)
    s %= P
    if s < W:
        return L + s, T, 0, -1, 1          # top, ->,  outward up
    s -= W
    if s < Hh:
        return R, T + s, 1, 0, 0           # right, v, outward right
    s -= Hh
    if s < W:
        return R - s, B, 0, 1, -1          # bottom, <-, outward down
    s -= W
    return L, B - s, -1, 0, 0              # left, ^, outward left


# ------------------------------------------------------------------ Pet
class Pet:
    def __init__(self, mgr, mascot):
        self.mgr = mgr
        self.mascot = mascot
        self.s = 0.0
        self.speed = 1.4
        self.face = 1
        self.walk = 0.0
        self.blink = 0
        self.next_blink = random.randint(30, 120)
        self.pause = 0
        self.hop = 0
        self.rot = 0
        self.hidden = False
        self.cache = {}
        self.hwnd = None
        self.speak_t = SPEAK_EVERY - 25 * FPS    # first phrase ~25s after start
        self.bubble_hold = 0
        self.sleeping = False
        self.sprint = 0                          # frames left of a dash burst

        self.win = tk.Toplevel(mgr.root)
        self.win.overrideredirect(True)
        self.win.wm_attributes("-topmost", True)
        try:
            self.win.wm_attributes("-transparentcolor", TRANSPARENT)
        except tk.TclError:
            pass
        self.win.config(bg=TRANSPARENT)
        self.canvas = tk.Canvas(self.win, width=WIN_W, height=WIN_H,
                                bg=TRANSPARENT, highlightthickness=0, bd=0)
        self.canvas.pack()
        self.img_id = self.canvas.create_image(WIN_W // 2, WIN_H // 2, anchor="center")

        self.dragging = False
        self.moved = False
        self.dx = self.dy = 0
        self.canvas.bind("<Button-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.canvas.bind("<Button-3>", self._menu)

        # Thai speech bubble (its own borderless topmost window)
        self.bubble = tk.Toplevel(mgr.root)
        self.bubble.overrideredirect(True)
        self.bubble.wm_attributes("-topmost", True)
        self.bubble.configure(bg="#4a4363")               # acts as a thin border
        inner = tk.Frame(self.bubble, bg="#fffdf5")
        inner.pack(padx=1, pady=1)
        self.b_thai = tk.Label(inner, bg="#fffdf5", fg="#2a2540",
                               font=("Tahoma", 10, "bold"))
        self.b_thai.pack(padx=7, pady=(3, 0))
        self.b_eng = tk.Label(inner, bg="#fffdf5", fg="#7a7396",
                              font=("Segoe UI", 7))
        self.b_eng.pack(padx=7, pady=(0, 3))
        self.bubble.withdraw()

    def set_mascot(self, m):
        self.mascot = m

    def _say(self):
        th, rom, eng = random.choice(PHRASES)
        self.b_thai.config(text=th)
        self.b_eng.config(text=f"{rom}  —  {eng}" if rom else eng)
        self.bubble.deiconify()
        self.bubble.update_idletasks()
        self.bubble_hold = SPEAK_HOLD

    def _place_bubble(self):
        bw = self.bubble.winfo_width()
        bh = self.bubble.winfo_height()
        pxw = self.win.winfo_x()
        pyw = self.win.winfo_y()
        bx = pxw + WIN_W // 2 - bw // 2
        by = pyw - bh - 2
        rect = self.mgr.rect
        if rect and by < rect[1] + 2:                     # no room above -> below
            by = pyw + WIN_H + 2
        self.bubble.geometry(f"+{int(bx)}+{int(by)}")
        keep_on_top(self.bubble.winfo_id())

    # -- input --
    def _press(self, e):
        self.dragging = True
        self.moved = False
        self.dx, self.dy = e.x, e.y

    def _drag(self, e):
        self.moved = True
        x = self.win.winfo_pointerx() - self.dx
        y = self.win.winfo_pointery() - self.dy
        self.win.geometry(f"+{int(x)}+{int(y)}")

    def _release(self, e):
        self.dragging = False
        if not self.moved:               # a click (not a drag) -> new Thai word
            self.hop = 14
            self._say()

    def _menu(self, e):
        m = tk.Menu(self.win, tearoff=0)
        m.add_command(label="🎨  Change buddy…", command=self.mgr.open_picker)
        m.add_command(label="🗣️  Thai word now", command=self._say)
        buddy_on = self.mgr.deskbuddy is not None
        m.add_command(
            label="🖥️  Stop desktop buddy" if buddy_on else "🖥️  Start desktop buddy",
            command=self.mgr.toggle_deskbuddy)
        m.add_separator()
        m.add_command(label="👋  Quit", command=self.mgr.quit_all)
        m.tk_popup(e.x_root, e.y_root)

    # -- frame image (cached) --
    def _image(self, foot):
        closed = self.blink > 0 or self.sleeping
        key = (self.mascot, closed, foot, self.rot)
        img = self.cache.get(key)
        if img is None:
            grid = S.hd(S.build(self.mascot, blink=closed, foot=foot, rot=self.rot))
            img = S.make_photo(grid, NUM, DEN)
            self.cache[key] = img
        return img

    # -- per-frame update --
    def tick(self):
        # blink timer
        if self.blink > 0:
            self.blink -= 1
        else:
            self.next_blink -= 1
            if self.next_blink <= 0:
                self.blink = 6
                self.next_blink = random.randint(45, 150)
        if self.hop > 0:
            self.hop -= 1
        if self.hwnd is None:
            self.hwnd = self.win.winfo_id()

        rect = self.mgr.rect
        # shrink Kiro's rect so the pet walks fully inside it
        inset = None
        if rect is not None and rect[2] - rect[0] > 2 * INSET + 8 \
                and rect[3] - rect[1] > 2 * INSET + 8:
            inset = (rect[0] + INSET, rect[1] + INSET,
                     rect[2] - INSET, rect[3] - INSET)

        if not self.dragging:
            if inset is None:                    # Kiro not focused -> hide all
                if not self.hidden:
                    self.win.withdraw()
                    self.bubble.withdraw()
                    self.bubble_hold = 0
                    self.hidden = True
                return
            if self.hidden:
                self.win.deiconify()
                self.win.wm_attributes("-topmost", True)
                self.hidden = False
            # nap when the user has gone idle; wake with a hop when they return
            asleep = idle_seconds() >= IDLE_SLEEP
            if asleep and not self.sleeping:
                self.sleeping = True
                self.sprint = 0
                self.b_thai.config(text="Zzz…")
                self.b_eng.config(text="napping — move the mouse to wake me")
            elif not asleep and self.sleeping:
                self.sleeping = False
                self.bubble.withdraw()
                self.bubble_hold = 0
                self.hop = 14
            if self.sleeping:
                if not self.bubble.winfo_viewable():
                    self.bubble.deiconify()
                self.bubble_hold = 2          # keep the Zzz bubble pinned on
            # advance along the inset border
            if self.sleeping:
                pass
            elif self.pause > 0:
                self.pause -= 1
            else:
                if self.sprint > 0:
                    self.sprint -= 1
                elif random.random() < 0.0015:   # rare little dash burst
                    self.sprint = random.randint(45, 90)
                spd = 3.4 if self.sprint > 0 else self.speed
                self.s += spd
                self.walk += 1.0 if self.sprint > 0 else 0.5
                if self.sprint == 0 and random.random() < 0.004:
                    self.pause = random.randint(20, 70)
            px_, py_, nx, ny, _ = perimeter_point(inset, self.s)
            self.rot = edge_rot(nx, ny)          # feet on frame, head inward
            cx, cy = px_, py_
            if self.hop > 0:                      # hop INWARD (away from frame)
                hb = int(6 * (1 - ((self.hop - 7) / 7) ** 2))
                cx -= nx * hb
                cy -= ny * hb
            wx = cx - WIN_W / 2
            wy = cy - WIN_H / 2
            wl, wt, wr, wb = self.mgr.work        # keep whole pet on the monitor
            wx = min(max(wx, wl), wr - WIN_W)
            wy = min(max(wy, wt), wb - WIN_H)
            self.win.geometry(f"+{int(wx)}+{int(wy)}")
            keep_on_top(self.hwnd)

        # draw (rotation conveys the walk; image stays centered)
        foot = int(self.walk) % 2 if self.pause == 0 and not self.sleeping else 0
        self.canvas.itemconfig(self.img_id, image=self._image(foot))
        self.canvas.coords(self.img_id, WIN_W // 2, WIN_H // 2)

        # Thai vocab bubble (only counts down while visible / coding in Kiro)
        if not self.hidden and not self.sleeping:
            self.speak_t += 1
            if self.speak_t >= SPEAK_EVERY:
                self.speak_t = 0
                self._say()
        if self.bubble_hold > 0:
            self.bubble_hold -= 1
            self._place_bubble()
            if self.bubble_hold == 0:
                self.bubble.withdraw()


# ------------------------------------------------------------------ Picker
class Picker:
    def __init__(self, mgr):
        self.mgr = mgr
        self.thumbs = []
        self.win = tk.Toplevel(mgr.root)
        self.win.title("Pick your Kiro buddy")
        self.win.configure(bg="#f4f4f7")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self._close)
        tk.Label(self.win, text="Choose a buddy to walk around Kiro",
                 bg="#f4f4f7", fg="#333", font=("Segoe UI", 11, "bold")
                 ).grid(row=0, column=0, columnspan=3, pady=(12, 6))
        for i, m in enumerate(S.MASCOTS):
            grid = S.hd(S.build(m, face=1))
            img = S.make_photo(grid, 2, bg="#ffffff")
            self.thumbs.append(img)
            cell = tk.Frame(self.win, bg="#ffffff", bd=1, relief="solid")
            cell.grid(row=1 + i // 3, column=i % 3, padx=8, pady=8)
            b = tk.Button(cell, image=img, bg="#ffffff", bd=0,
                          activebackground="#eae6ff",
                          command=lambda m=m: self._choose(m))
            b.pack(padx=4, pady=(4, 0))
            tk.Label(cell, text=S.LABELS[m], bg="#ffffff", fg="#444",
                     font=("Segoe UI", 9)).pack(pady=(0, 4))
        self.win.update_idletasks()
        self._center()

    def _center(self):
        w = self.win.winfo_width()
        h = self.win.winfo_height()
        r = self.mgr.rect
        if r:                                       # center over Kiro's monitor
            cx, cy = (r[0] + r[2]) // 2, (r[1] + r[3]) // 2
        else:
            cx = self.win.winfo_screenwidth() // 2
            cy = self.win.winfo_screenheight() // 2
        self.win.geometry(f"+{cx - w // 2}+{cy - h // 2}")

    def _choose(self, mascot):
        self.mgr.choose(mascot)
        self._close()

    def _close(self):
        self.mgr.picker = None
        self.win.destroy()


# ------------------------------------------------------------------ DeskBuddy
class DeskBuddy:
    """A larger, free-standing pal that sits on the desktop (not focus-gated),
    shuffles through little 8-bit activities, shows how long you've been
    working since the last screen-lock, and reminds you when a break is due."""

    ACTION_EVERY = (5 * FPS, 10 * FPS)       # reshuffle the activity every 5-10s

    def __init__(self, mgr, mascot):
        self.mgr = mgr
        self.mascot = mascot
        self.action = random.choice(S.ACTIONS)
        self.action_t = random.randint(*self.ACTION_EVERY)
        self.blink = 0
        self.next_blink = random.randint(30, 120)
        self.frame = 0
        self.cache = {}
        self.break_flash = False
        self.face = 1
        self.wander_left = 0                  # +/- pixels still to stroll
        self.wander_t = random.randint(6 * FPS, 14 * FPS)

        self.win = tk.Toplevel(mgr.root)
        self.win.overrideredirect(True)
        self.win.wm_attributes("-topmost", True)
        try:
            self.win.wm_attributes("-transparentcolor", TRANSPARENT)
        except tk.TclError:
            pass
        self.win.config(bg=TRANSPARENT)
        self.canvas = tk.Canvas(self.win, width=DWIN_W, height=DWIN_H,
                                bg=TRANSPARENT, highlightthickness=0, bd=0)
        self.canvas.pack()
        self.img_id = self.canvas.create_image(DWIN_W // 2, DWIN_H // 2 - 4,
                                               anchor="center")

        # default position: bottom-right of the PRIMARY (main) screen
        sw = mgr.root.winfo_screenwidth()
        sh = mgr.root.winfo_screenheight()
        self.win.geometry(f"+{sw - DWIN_W - 48}+{sh - DWIN_H - 96}")

        self.dragging = False
        self.moved = False
        self.dx = self.dy = 0
        self.canvas.bind("<Button-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.canvas.bind("<Button-3>", self._menu)
        self.canvas.bind("<Enter>", self._hover_on)
        self.canvas.bind("<Leave>", self._hover_off)

        # always-visible working-time label
        self.label = tk.Toplevel(mgr.root)
        self.label.overrideredirect(True)
        self.label.wm_attributes("-topmost", True)
        self.label.configure(bg="#4a4363")
        li = tk.Frame(self.label, bg="#fffdf5")
        li.pack(padx=1, pady=1)
        self.label_txt = tk.Label(li, bg="#fffdf5", fg="#2a2540",
                                  font=("Segoe UI", 8, "bold"))
        self.label_txt.pack(padx=6, pady=2)

        # break countdown, shown on hover
        self.hover = tk.Toplevel(mgr.root)
        self.hover.overrideredirect(True)
        self.hover.wm_attributes("-topmost", True)
        self.hover.configure(bg="#4a4363")
        hi = tk.Frame(self.hover, bg="#fffdf5")
        hi.pack(padx=1, pady=1)
        self.hover_txt = tk.Label(hi, bg="#fffdf5", fg="#2a2540",
                                  font=("Segoe UI", 8, "bold"))
        self.hover_txt.pack(padx=7, pady=3)
        self.hover.withdraw()
        self._hovering = False

    def set_mascot(self, m):
        self.mascot = m
        self.cache.clear()

    # -- input --
    def _press(self, e):
        self.dragging = True
        self.moved = False
        self.dx, self.dy = e.x, e.y

    def _drag(self, e):
        self.moved = True
        x = self.win.winfo_pointerx() - self.dx
        y = self.win.winfo_pointery() - self.dy
        self.win.geometry(f"+{int(x)}+{int(y)}")

    def _shuffle(self):
        self.action = random.choice(S.ACTIONS)
        self.action_t = random.randint(*self.ACTION_EVERY)

    def _release(self, e):
        self.dragging = False
        if not self.moved:                    # a poke -> jump to a new activity
            self._shuffle()

    def _menu(self, e):
        m = tk.Menu(self.win, tearoff=0)
        m.add_command(label="🎨  Change buddy…", command=self.mgr.open_picker)
        m.add_command(label="🎲  New activity", command=self._shuffle)
        sub = tk.Menu(m, tearoff=0)
        for mins in (30, 45, 60, 90):
            mark = "●" if self.mgr.break_every == mins * 60 else "○"
            sub.add_command(label=f"{mark}  {mins} min",
                            command=lambda mm=mins: self.mgr.set_break(mm * 60))
        m.add_cascade(label="⏰  Break every…", menu=sub)
        m.add_command(label="🖥️  Stop desktop buddy",
                      command=self.mgr.toggle_deskbuddy)
        m.add_separator()
        m.add_command(label="👋  Quit", command=self.mgr.quit_all)
        m.tk_popup(e.x_root, e.y_root)

    def _hover_on(self, _):
        self._hovering = True

    def _hover_off(self, _):
        self._hovering = False
        self.hover.withdraw()

    # -- image (cached per action/blink/bob/face) --
    def _image(self, foot, bob):
        key = (self.mascot, self.action, self.blink > 0, foot, bob, self.face)
        img = self.cache.get(key)
        if img is None:
            grid = S.hd(S.build_scene(self.mascot, self.action,
                                      blink=self.blink > 0, foot=foot, bob=bob,
                                      face=self.face))
            img = S.make_photo(grid, D_NUM, D_DEN)
            self.cache[key] = img
        return img

    @staticmethod
    def _fmt(sec):
        sec = max(0, int(sec))
        h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    def _place_labels(self):
        x = self.win.winfo_x()
        y = self.win.winfo_y()
        self.label.update_idletasks()
        lw = self.label.winfo_width()
        lx = x + DWIN_W // 2 - lw // 2
        ly = y + DWIN_H - 6
        self.label.geometry(f"+{int(lx)}+{int(ly)}")
        keep_on_top(self.label.winfo_id())
        if self._hovering:
            self.hover.deiconify()
            self.hover.update_idletasks()
            hw = self.hover.winfo_width()
            hx = x + DWIN_W // 2 - hw // 2
            hy = y - self.hover.winfo_height() - 2
            self.hover.geometry(f"+{int(hx)}+{int(hy)}")
            keep_on_top(self.hover.winfo_id())

    def tick(self):
        self.frame += 1
        # blink
        if self.blink > 0:
            self.blink -= 1
        else:
            self.next_blink -= 1
            if self.next_blink <= 0:
                self.blink = 6
                self.next_blink = random.randint(45, 150)
        # shuffle activity
        self.action_t -= 1
        if self.action_t <= 0:
            self._shuffle()

        # little strolls around the desktop (not while napping or being held)
        walking = False
        if not self.dragging and self.action != "sleep":
            self.wander_t -= 1
            if self.wander_t <= 0:
                self.wander_t = random.randint(8 * FPS, 18 * FPS)
                if random.random() < 0.7:
                    self.wander_left = random.choice((-1, 1)) * random.randint(30, 110)
            if self.wander_left:
                walking = True
                step = 1 if self.wander_left > 0 else -1
                self.face = step
                x = self.win.winfo_x() + step
                sw = self.mgr.root.winfo_screenwidth()
                if 8 <= x <= sw - DWIN_W - 8:
                    self.win.geometry(f"+{x}+{self.win.winfo_y()}")
                    self.wander_left -= step
                else:
                    self.wander_left = 0

        worked = self.mgr.work_seconds()
        remaining = self.mgr.break_every - worked
        due = remaining <= 0

        # gentle idle bob + foot shuffle (quicker while strolling)
        bob = 1 if (self.frame // 16) % 2 else 0
        foot = (self.frame // (6 if walking else 20)) % 2
        self.canvas.itemconfig(self.img_id, image=self._image(foot, bob))

        # labels
        if due:
            self.label_txt.config(text=f"worked {self._fmt(worked)} · break time!",
                                  fg="#b83b3b")
        else:
            self.label_txt.config(text=f"worked {self._fmt(worked)}", fg="#2a2540")
        if self._hovering:
            doing = S.ACTION_LABELS[self.action]
            if due:
                self.hover_txt.config(text=f"{doing}\nBreak's overdue — go rest a bit 💤")
            else:
                self.hover_txt.config(text=f"{doing}\nNext break in {self._fmt(remaining)}")
        self._place_labels()
        keep_on_top(self.win.winfo_id())

    def destroy(self):
        for w in (self.hover, self.label, self.win):
            try:
                w.destroy()
            except tk.TclError:
                pass


# ------------------------------------------------------------------ Manager
class Manager:
    def __init__(self, target, free, mascot):
        self.target = target.lower()
        self.free = free
        self.me = os.getpid()
        self.root = tk.Tk()
        self.root.withdraw()
        self.rect = None if free else find_window_rect(self.target)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.work = (0, 0, sw, sh)          # visible monitor bounds (updated live)
        self.pet = None
        self.picker = None
        self.deskbuddy = None
        self.locked = False
        self.break_every = BREAK_EVERY
        self.last_unlock = time.monotonic()   # work timer resets on each unlock
        if mascot:
            self.choose(mascot)
        else:
            self.open_picker()
        self._poll()
        self._loop()

    def open_picker(self):
        if self.picker is None:
            self.picker = Picker(self)
        else:
            self.picker.win.lift()

    def choose(self, mascot):
        if self.pet is None:
            self.pet = Pet(self, mascot)
        else:
            self.pet.set_mascot(mascot)
        if self.deskbuddy is not None:
            self.deskbuddy.set_mascot(mascot)

    def toggle_deskbuddy(self):
        if self.deskbuddy is None:
            m = self.pet.mascot if self.pet else S.MASCOTS[0]
            self.deskbuddy = DeskBuddy(self, m)
        else:
            self.deskbuddy.destroy()
            self.deskbuddy = None

    def set_break(self, seconds):
        self.break_every = seconds

    def work_seconds(self):
        """Seconds worked since the last unlock (0 while locked / on a break)."""
        if self.locked:
            return 0
        return int(time.monotonic() - self.last_unlock)

    def quit_all(self):
        self.root.destroy()

    def _poll(self):
        # lock/unlock tracking for the desktop-buddy work timer
        locked = is_locked()
        if locked and not self.locked:
            self.locked = True                       # screen just locked -> break
        elif not locked and self.locked:
            self.locked = False
            self.last_unlock = time.monotonic()      # back to work -> reset timer

        if self.free:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.rect = (10, 10, sw - 10, sh - 60)
            self.work = (0, 0, sw, sh)
        else:
            # Only follow Kiro while it is the FOREGROUND window, so the pet
            # never floats over other apps. Track that exact window's rect.
            fg = user32.GetForegroundWindow()
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(fg, ctypes.byref(pid))
            if pid.value == self.me:
                pass                                    # interacting with pet
            elif self.target in _proc_name(pid.value).lower():
                r = wintypes.RECT()
                user32.GetWindowRect(fg, ctypes.byref(r))
                if r.left > -30000 and (r.right - r.left) > 250 and (r.bottom - r.top) > 150:
                    self.rect = (r.left, r.top, r.right, r.bottom)
                    wa = work_area(fg)
                    if wa:
                        self.work = wa
                else:
                    self.rect = None
            else:
                self.rect = None
        self.root.after(250, self._poll)

    def _loop(self):
        if self.pet is not None:
            self.pet.tick()
        if self.deskbuddy is not None:
            self.deskbuddy.tick()
        self.root.after(33, self._loop)

    def run(self):
        self.root.mainloop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mascot", choices=S.MASCOTS, default=None)
    ap.add_argument("--target", default="kiro")
    ap.add_argument("--free", action="store_true")
    a = ap.parse_args()
    Manager(a.target, a.free, a.mascot).run()


if __name__ == "__main__":
    main()
