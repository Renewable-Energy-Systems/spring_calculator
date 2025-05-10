"""spring_gui.py – Coil‑Spring Calculator  ✦  Dark Material 2025.05
===============================================================
Dark‑theme Tk‑inter desktop app for quick spring‑rate / force checks.

🔑  Key points
--------------
• Brand bar with logo (auto‑scaled) and titles, left‑aligned and vertically
  centred.
• Loads **assets/spring_sample.png**; auto‑resizes to ≤160 px height with
  Pillow (if available). Falls back to a vector sketch otherwise.
• Two‑column grid layout with sensible column weights so text and images
  stay centred / aligned on any DPI.
• Cyan‑accent Material palette, dark background, footer watermark.
• Same CLI fallback (`python spring_gui.py --cli`).

MIT Licence.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Optional

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ModuleNotFoundError:  # headless python
    tk = None  # type: ignore

# Pillow is optional – only needed for nicer image scaling
try:
    from PIL import Image, ImageTk  # type: ignore
except ModuleNotFoundError:
    Image = ImageTk = None  # type: ignore

# ────────────────────────────────────────────────────────────────
#  Engineering maths
# ────────────────────────────────────────────────────────────────

def spring_rate(G_pa: float, d_m: float, ID_m: float, n: float) -> float:
    D_mean = ID_m + d_m
    if d_m <= 0 or n <= 0 or D_mean <= 0:
        raise ValueError("d, n, and mean diameter must be positive")
    return (G_pa * d_m ** 4) / (8 * D_mean ** 3 * n)


def spring_force(k: float, Δ_m: float) -> float:
    return k * Δ_m

# ────────────────────────────────────────────────────────────────
#  Theme + assets
# ────────────────────────────────────────────────────────────────
_BG, _FG = "#2B2B2B", "#EEEEEE"
_ACCENT      = "#00BCD4"
_ACCENT_DARK = "#0097A7"
_ENTRY_BG    = "#3C3F41"
_FONT        = ("Segoe UI", 11)
_FONT_BIG    = ("Segoe UI Semibold", 13)
_FONT_TITLE  = ("Segoe UI Semibold", 16)

_ASSETS   = Path(__file__).with_suffix("").parent / "assets"
_LOGO_PNG = _ASSETS / "logo.png"
_SPRING_PNG = _ASSETS / "spring_sample.png"
_IMG_MAX_H = 160

# ────────────────────────────────────────────────────────────────
#  Fallback vector sketch (if PNG missing or Pillow absent)
# ────────────────────────────────────────────────────────────────

def _draw_sine_spring(canvas: "tk.Canvas") -> None:  # type: ignore[name-defined]
    w, h = int(canvas["width"]), int(canvas["height"])
    cx, cy = w // 2, h // 2 + 6
    turns, amp = 8, 20
    length = 260
    sx = cx - length // 2
    pts: list[float] = []
    for i in range(turns * 20 + 1):
        x = sx + (i / (turns * 20)) * length
        y = cy + amp * math.sin(i / 20 * math.pi)
        pts += [x, y]
    canvas.create_line(*pts, smooth=True, width=3, fill=_ACCENT)
    inner_R = 55
    canvas.create_oval(cx - inner_R, cy - inner_R, cx + inner_R, cy + inner_R,
                       outline=_ACCENT, dash=(4,3))
    canvas.create_text(cx, cy - inner_R - 14, text="ID", fill=_ACCENT, font=_FONT)
    canvas.create_line(cx + inner_R, cy, cx + inner_R + 28, cy, arrow=tk.LAST, fill=_ACCENT, width=2)
    canvas.create_text(cx + inner_R + 42, cy - 4, text="d", fill=_ACCENT, font=_FONT, anchor="w")
    canvas.create_text(sx + 6, cy - amp - 22, text="n coils", fill=_ACCENT, font=_FONT, anchor="w")

# ────────────────────────────────────────────────────────────────
#  GUI builder
# ────────────────────────────────────────────────────────────────

def _build_gui() -> Optional["tk.Tk"]:  # type: ignore[name-defined]
    if tk is None:
        return None

    root = tk.Tk()
    root.title("Coil‑Spring Calculator")
    root.configure(bg=_BG)
    root.resizable(False, False)

    # ttk style
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background=_BG)
    style.configure("TLabel", background=_BG, foreground=_FG, font=_FONT)
    style.configure("Header.TLabel", font=_FONT_TITLE, background=_BG, foreground=_FG)
    style.configure("Water.TLabel", font=("Segoe UI", 9), background=_BG, foreground="#777")
    style.configure("TEntry", fieldbackground=_ENTRY_BG, foreground=_FG, insertcolor=_FG)
    style.configure("Accent.TButton", font=_FONT_BIG, background=_ACCENT, foreground=_FG,
                    padding=(14,6), relief="flat")
    style.map("Accent.TButton", background=[("active", _ACCENT_DARK)])

    root.columnconfigure(0, weight=1)

    pad = {"padx":12, "pady":6}

    # ── Brand bar ──
    brand = ttk.Frame(root)
    brand.grid(row=0, column=0, sticky="ew", **pad)
    brand.columnconfigure(1, weight=1)

    # logo
    logo_img = None
    if _LOGO_PNG.exists():
        try:
            raw = tk.PhotoImage(file=_LOGO_PNG)
            # scale logo height to 80 px
            if raw.height() > 80:
                raw = raw.subsample(max(int(raw.height()/80),1))
            logo_img = raw
            ttk.Label(brand, image=logo_img).grid(row=0, column=0, rowspan=2, sticky="w")
        except Exception:
            logo_img = None

    ttk.Label(brand, text="Renewable Energy Systems Limited", style="Header.TLabel")\
        .grid(row=0, column=1, sticky="w", padx=(10,0))
    ttk.Label(brand, text="Spring Calculator", font=_FONT_BIG, foreground=_ACCENT)\
        .grid(row=1, column=1, sticky="w", padx=(10,0))

    # ── Illustration ──
    illus = ttk.Frame(root)
    illus.grid(row=1, column=0, sticky="ew", **pad)
    illus.columnconfigure(0, weight=1)

    img_tk = None
    if _SPRING_PNG.exists() and Image and ImageTk:
        try:
            img_pil = Image.open(_SPRING_PNG)
            if img_pil.height > _IMG_MAX_H:
                ratio = img_pil.width / img_pil.height
                img_pil = img_pil.resize((int(_IMG_MAX_H*ratio), _IMG_MAX_H), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            ttk.Label(illus, image=img_tk).grid()
        except Exception:
            img_tk = None

    if img_tk is None:
        canvas = tk.Canvas(illus, width=420, height=_IMG_MAX_H, bg=_BG, highlightthickness=0)
        canvas.grid()
        _draw_sine_spring(canvas)

    # ── Input grid ──
    form = ttk.Frame(root)
    form.grid(row=2, column=0, sticky="ew", **pad)
    form.columnconfigure(1, weight=1)

    fields = (
        ("Wire Ø  d  [mm]", "d"),
        ("Inner Ø  ID  [mm]", "ID"),
        ("Active coils  n", "n"),
        ("Shear modulus  G  [GPa]", "G"),
        ("Deflection  Δ  [mm] (optional)", "defl")
    )
    entries: dict[str, tk.Entry] = {}
    for r, (lbl, key) in enumerate(fields):
        ttk.Label(form, text=lbl).grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(form, width=18, style="TEntry")
        e.grid(row=r, column=1, sticky="ew", **pad)
        entries[key] = e
    entries["G"].insert(0, "77")

    # ── Separator & results ──
    ttk.Separator(root, orient="horizontal").grid(row=3, column=0, sticky="ew", padx=14, pady=(6,2))

    res = ttk.Frame(root)
    res.grid(row=4, column=0, sticky="ew")
    res.columnconfigure(1, weight=1)

    k_var = tk.StringVar(value="– –")
    F_var = tk.StringVar(value="– –")
    ttk.Label(res, text="Spring rate k").grid(row=0, column=0, sticky="w", **pad)
    ttk.Label(res, textvariable=k_var, font=_FONT_BIG, foreground=_ACCENT)\
        .grid(row=0, column=1, sticky="e", **pad)
    ttk.Label(res, text="Force F (if Δ > 0)").grid(row=1, column=0, sticky="w", **pad)
    ttk.Label(res, textvariable=F_var, font=_FONT_BIG, foreground=_ACCENT)\
        .grid(row=1, column=1, sticky="e", **pad)

    # ── Calculate button ──
    def _calc():
        try:
            d = float(entries["d"].get())/1e3
            ID = float(entries["ID"].get())/1e3
            n  = float(entries["n"].get())
            G  = float(entries["G"].get())*1e9
            Δ  = float(entries["defl"].get())/1e3 if entries["defl"].get().strip() else 0.0
        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numeric values")
            return
        try:
            k = spring_rate(G, d, ID, n)
            k_var.set(f"{k:,.2f} N/m")
            F_var.set(f"{spring_force(k, Δ):,.2f} N" if Δ else "– –")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(root, text="Calculate", style="Accent.TButton", command=_calc)\
        .grid(row=5, column=0, pady=(8,6))

    ttk.Label(root, text="Design & Developed by Pranay Kiran with ❤", style="Water.TLabel")\
        .grid(row=6, column=0, pady=(0,10))

    entries["d"].focus()

    # keep refs
    root.logo = logo_img
    root.spring_png = img_tk

    return root

# ────────────────────────────────────────────────────────────────
#  CLI fallback
# ────────────────────────────────────────────────────────────────

def _cli() -> None:
    pa = argparse.ArgumentParser()
    pa.add_argument("d", type=float, help="wire Ø mm")
    pa.add_argument("ID", type=float, help="inner Ø mm")
    pa.add_argument("n", type=float, help="active coils")
    pa.add_argument("-G", default=77.0, type=float, help="Shear modulus GPa (default 77.0)")
    pa.add_argument("-D", "--deflection", type=float, default=0.0, help="Deflection mm")
    args = pa.parse_args()

    try:
        # Basic validation for CLI
        if args.d <= 0 or args.ID < 0 or args.n <= 0 or args.G <= 0:
             print("Error: Wire diameter, active coils, and Shear modulus must be positive. Inner diameter must be non-negative.", file=sys.stderr)
             sys.exit(1)
        if args.d >= args.ID + args.d:
            print("Error: Wire diameter must be less than or equal to Inner diameter.", file=sys.stderr)
            sys.exit(1)

        k_val = spring_rate(args.G * 1e9, args.d / 1e3, args.ID / 1e3, args.n)
        print(f"k = {k_val:.2f} N/m")
        if args.deflection:
            print(f"F = {spring_force(k_val, args.deflection / 1e3):.2f} N")
    except ValueError as e:
         print(f"Calculation Error: {e}", file=sys.stderr)
         sys.exit(1)


# ────────────────────────────────────────────────────────────────────
#   Entry-point
# ────────────────────────────────────────────────────────────────────

def main() -> None:  # pragma: no cover
    if tk is None:
        sys.stderr.write("⚠️  tkinter unavailable – running CLI.\n")
        _cli()
    else:
        gui = _build_gui()
        if gui is not None:
            gui.mainloop()
        else: # Should not happen if tk is not None, but as a safeguard
             sys.stderr.write("⚠️  GUI failed to build – running CLI.\n")
             _cli()


if __name__ == "__main__":
    main()