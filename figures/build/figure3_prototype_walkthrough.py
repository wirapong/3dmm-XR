"""
Rebuild Figure 3: Interactive Prototype Walk-Through
For Qianqian He et al. — Informatics (MDPI) XR Special Issue

Address proofreading comments:
2. Larger text (base >= 13pt bold)
3. No overlapping labels
4. Nothing cut off - panels sized to content
5. Legend for colors/arrows/symbols added
6. Italics removed (plain bold everywhere)
7. Font: Palatino, Bold weight throughout

v2: fix Panel D fork arrows, XYZ gizmo spacing, Legend 3x3 grid
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Circle,
                                Rectangle, Ellipse)
import matplotlib as mpl

# --- Global style: Palatino Bold ---
mpl.rcParams['font.family'] = 'Palatino'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['font.size'] = 13

FONT = 'Palatino'
BOLD = {'family': FONT, 'weight': 'bold'}

# Color palette
C_HEADER   = '#1F5D9C'
C_HEADER_D = '#0F3E70'
C_PANEL_BG = '#EEF4FB'
C_TIME_BG  = '#FFF7D6'
C_TIME_BD  = '#B7900B'
C_METRIC   = '#1F8B4C'
C_ACCENT   = '#F0A500'
C_TEXT     = '#111111'
C_ARROW    = '#1F5D9C'

FIG_W_IN = 24
FIG_H_IN = 12
fig, ax = plt.subplots(figsize=(FIG_W_IN, FIG_H_IN), dpi=200)
ax.set_xlim(0, 240)
ax.set_ylim(0, 120)
ax.set_aspect('equal')
ax.axis('off')

ax.text(120, 116, 'Interactive Prototype Walk-Through',
        ha='center', va='center', fontsize=22, **BOLD, color=C_TEXT)


def panel(ax, x, y, w, h, letter, title):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.4,rounding_size=1.2",
                       linewidth=2, edgecolor=C_HEADER, facecolor=C_PANEL_BG)
    ax.add_patch(p)
    hdr_h = 5.5
    hdr = FancyBboxPatch((x+1, y+h-hdr_h-1), w-2, hdr_h,
                         boxstyle="round,pad=0.15,rounding_size=0.8",
                         linewidth=1.5, edgecolor=C_HEADER_D, facecolor=C_HEADER)
    ax.add_patch(hdr)
    ax.text(x+w/2, y+h-hdr_h/2-1, title,
            ha='center', va='center', fontsize=15, **BOLD, color='white')
    ax.text(x+2, y+h-hdr_h-3.5, f'({letter})',
            ha='left', va='center', fontsize=15, **BOLD, color=C_HEADER)


def rbox(ax, x, y, w, h, text, fc='white', ec='#666666', tc=C_TEXT,
         fontsize=13, lw=1.5, rs=0.6, ha='center', va='center'):
    b = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.2,rounding_size={rs}",
                       linewidth=lw, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    if text:
        ax.text(x+w/2, y+h/2, text, ha=ha, va=va, fontsize=fontsize, **BOLD, color=tc)


def sqbox(ax, x, y, w, h, text, fc='white', ec='#666666', tc=C_TEXT, fontsize=13, lw=1.5):
    r = Rectangle((x, y), w, h, linewidth=lw, edgecolor=ec, facecolor=fc)
    ax.add_patch(r)
    if text:
        ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fontsize, **BOLD, color=tc)


def big_arrow(ax, x1, y1, x2, y2, color=C_ARROW, lw=3.5):
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='-|>', mutation_scale=28,
                        color=color, linewidth=lw)
    ax.add_patch(a)


def small_arrow(ax, x1, y1, x2, y2, color='#111111', lw=2):
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle='-|>', mutation_scale=18,
                        color=color, linewidth=lw)
    ax.add_patch(a)


def time_box(ax, x, y, w, h, top_lbl, big_val, sub_lbl):
    rbox(ax, x, y, w, h, '', fc=C_TIME_BG, ec=C_TIME_BD, lw=1.8, rs=0.6)
    ax.text(x+w/2, y+h-1.6, top_lbl, ha='center', va='top', fontsize=13, **BOLD, color=C_TEXT)
    ax.text(x+w/2, y+h/2-0.3, big_val, ha='center', va='center', fontsize=22, **BOLD, color=C_METRIC)
    ax.text(x+w/2, y+1.4, sub_lbl, ha='center', va='bottom', fontsize=11.5, **BOLD, color='#444444')


# Panel geometry
P_W = 50
P4_W = 65      # Panel D wider to fit fork + engines symmetrically
P_H = 82
P_Y = 20
P1_X = 3
P2_X = 58
P3_X = 113
P4_X = 168

# ============ PANEL A ============
panel(ax, P1_X, P_Y, P_W, P_H, 'a', 'Step 1: Select Input Image')

dot_y = P_Y + P_H - 12.5
for i, dc in enumerate(['#E74C3C', '#F1C40F', '#27AE60']):
    ax.add_patch(Circle((P1_X+3.5+i*1.5, dot_y), 0.55, facecolor=dc, edgecolor='#333', linewidth=0.6))
ax.text(P1_X+10, dot_y, 'Open File...', ha='left', va='center', fontsize=13, **BOLD, color=C_TEXT)

tn_w, tn_h = 12, 10
tn_gap = 1.2
tn_x0 = P1_X + 4
tn_y0 = P_Y + P_H - 27
for i in range(3):
    for j in range(2):
        idx = j*3 + i + 1
        tx = tn_x0 + i*(tn_w+tn_gap)
        ty = tn_y0 - j*(tn_h+tn_gap)
        selected = (idx == 3)
        fc = '#FFF3CD' if selected else '#E8E8E8'
        ec = C_ACCENT if selected else '#999999'
        lw = 2.5 if selected else 1.2
        sqbox(ax, tx, ty, tn_w, tn_h, '', fc=fc, ec=ec, lw=lw)
        ax.add_patch(Circle((tx+tn_w/2, ty+tn_h/2+0.6), 2.0,
                            facecolor='#BFC9D6', edgecolor='#666', linewidth=0.8))
        ax.text(tx+tn_w/2, ty+1.2, f'IMG_{idx:02d}', ha='center', va='bottom',
                fontsize=11.5, **BOLD, color=C_TEXT)
# 'Selected' label placed above IMG_03 (top row, rightmost) - explicit coords to avoid mismatch
sel_tx = tn_x0 + 2*(tn_w+tn_gap) + tn_w/2
sel_ty = tn_y0 + tn_h + 1.2
ax.text(sel_tx, sel_ty, 'Selected', ha='center', va='bottom',
        fontsize=10.5, **BOLD, color=C_ACCENT)

info_y = tn_y0 - 2*(tn_h+tn_gap) - 8
rbox(ax, P1_X+4, info_y, 26, 8, '', fc='white', ec=C_HEADER, lw=1.8)
ax.text(P1_X+5.5, info_y+5.2, 'Selected: IMG_03.jpg',
        ha='left', va='center', fontsize=12, **BOLD, color=C_TEXT)
ax.text(P1_X+5.5, info_y+2.5, '1920 x 1080 px',
        ha='left', va='center', fontsize=11.5, **BOLD, color='#555555')
rbox(ax, P1_X+32, info_y+1, 14, 6, 'Open', fc='#1A5276', ec='#154360', tc='white', fontsize=13)

ax.text(P1_X + P_W/2, info_y-4, 'User selects a single face image',
        ha='center', va='center', fontsize=12, **BOLD, color='#333333')
ax.text(P1_X + P_W/2, info_y-7, 'Supports JPG, PNG, BMP',
        ha='center', va='center', fontsize=11.5, **BOLD, color='#555555')

time_box(ax, P1_X+3, P_Y+3, P_W-6, 11,
         'Step Time', '< 100 ms', '(file I/O + UI render)')

# ============ PANEL B ============
panel(ax, P2_X, P_Y, P_W, P_H, 'b', 'Step 2: Align & Pre-process')

ax.text(P2_X+11, P_Y+P_H-14, 'Input', ha='center', va='center', fontsize=13, **BOLD, color=C_TEXT)
ax.add_patch(Circle((P2_X+11, P_Y+P_H-22), 5.8, facecolor='#FFF3CD', edgecolor=C_ACCENT, linewidth=2))
ax.text(P2_X+11, P_Y+P_H-28.5, 'Face image', ha='center', va='top', fontsize=11.5, **BOLD, color='#333333')
ax.text(P2_X+11, P_Y+P_H-30.7, '(unconstrained)', ha='center', va='top', fontsize=11, **BOLD, color='#555555')

small_arrow(ax, P2_X+18, P_Y+P_H-22, P2_X+27, P_Y+P_H-22, lw=2.5)
ax.text(P2_X+22.5, P_Y+P_H-18, 'dlib + align', ha='center', va='center',
        fontsize=11.5, **BOLD, color='#333333')

ax.text(P2_X+37, P_Y+P_H-14, 'Aligned (120 x 120)', ha='center', va='center', fontsize=13, **BOLD, color=C_TEXT)
r = FancyBboxPatch((P2_X+31, P_Y+P_H-28), 12, 12,
                   boxstyle="round,pad=0.15,rounding_size=0.6",
                   linewidth=2, edgecolor='#1ABC9C', facecolor='#E8F8F5')
ax.add_patch(r)

np.random.seed(3)
cx, cy = P2_X+37, P_Y+P_H-22
for angle in np.linspace(-np.pi, np.pi, 24):
    dx = 3.5*np.cos(angle); dy = 4*np.sin(angle)
    ax.add_patch(Circle((cx+dx, cy+dy), 0.22, facecolor='#0E7C66', edgecolor='none'))
for pt in [(-1.5, 1.5),(1.5,1.5),(0,0),(-1.2,-2),(0,-2),(1.2,-2)]:
    ax.add_patch(Circle((cx+pt[0], cy+pt[1]), 0.22, facecolor='#0E7C66', edgecolor='none'))
ax.text(P2_X+37, P_Y+P_H-30, 'Landmark grid ROI',
        ha='center', va='top', fontsize=11.5, **BOLD, color='#333333')

ax.text(P2_X+P_W/2, P_Y+P_H-38, '4-Channel Input Composition',
        ha='center', va='center', fontsize=13, **BOLD, color=C_TEXT)
ch_y = P_Y + P_H - 47
ch_w, ch_h = 7, 7
plus_w = 2.5
cx0 = P2_X + 4
labels = [('R', '#E74C3C'), ('G', '#27AE60'), ('B', '#2E86C1')]
xcur = cx0
for i, (lbl, col) in enumerate(labels):
    rbox(ax, xcur, ch_y, ch_w, ch_h, lbl, fc=col, ec='#333333', tc='white', fontsize=15, lw=1.5, rs=0.4)
    xcur += ch_w
    ax.text(xcur+plus_w/2, ch_y+ch_h/2, '+', ha='center', va='center', fontsize=18, **BOLD, color=C_TEXT)
    xcur += plus_w
rbox(ax, xcur, ch_y, ch_w+3, ch_h, 'Mask', fc='#F0B27A', ec='#B25E00', tc='white', fontsize=13, lw=1.5, rs=0.4)
ax.text(xcur+(ch_w+3)/2, ch_y-2, '(sigma = 2 px)', ha='center', va='top', fontsize=11, **BOLD, color='#333333')

time_box(ax, P2_X+3, P_Y+3, P_W-6, 11,
         'Step Time', '~ 50 ms', '(HOG detect + 68 landmarks)')

# ============ PANEL C ============
panel(ax, P3_X, P_Y, P_W, P_H, 'c', 'Step 3: 3D Mesh Preview')

sqbox(ax, P3_X+3, P_Y+P_H-38, P_W-6, 28, '', fc='#1A1A2E', ec='#555555', lw=1.5)

mesh_cx = P3_X + P_W/2 + 2
mesh_cy = P_Y + P_H - 24
for r_ratio in [0.35, 0.55, 0.75, 1.0]:
    e = Ellipse((mesh_cx, mesh_cy), 16*r_ratio, 20*r_ratio,
                fill=False, edgecolor='#00FF88', linewidth=1.0)
    ax.add_patch(e)
for ang in np.linspace(0, 180, 7)[1:-1]:
    e = Ellipse((mesh_cx, mesh_cy), 16*np.abs(np.cos(np.radians(ang))), 20,
                fill=False, edgecolor='#00FF88', linewidth=0.7, angle=0)
    ax.add_patch(e)

ax.text(P3_X+4.5, P_Y+P_H-13, '3DMM', ha='left', va='top', fontsize=13, **BOLD, color='#00FF88')
params_txt = 'Shape: 40\nExpr: 10\nPose:   6\nLight:   5\nCam:    1'
ax.text(P3_X+4.5, P_Y+P_H-16, params_txt, ha='left', va='top',
        fontsize=11, **BOLD, color='#DDDDDD', linespacing=1.35)

# XYZ axis gizmo — larger, well spaced
gx, gy = P3_X+P_W-10, P_Y+P_H-14.5
AL = 4.2
ax.add_patch(FancyArrowPatch((gx, gy),(gx+AL, gy), arrowstyle='-|>', mutation_scale=16, color='#FF4444', linewidth=2.4))
ax.add_patch(FancyArrowPatch((gx, gy),(gx, gy+AL), arrowstyle='-|>', mutation_scale=16, color='#44FF44', linewidth=2.4))
ax.add_patch(FancyArrowPatch((gx, gy),(gx-AL*0.72, gy-AL*0.72), arrowstyle='-|>', mutation_scale=16, color='#4488FF', linewidth=2.4))
ax.text(gx+AL+0.9, gy, 'X', fontsize=13, **BOLD, color='#FF7070', va='center', ha='left')
ax.text(gx, gy+AL+0.9, 'Y', fontsize=13, **BOLD, color='#70FF70', ha='center', va='bottom')
ax.text(gx-AL*0.72-0.9, gy-AL*0.72-0.9, 'Z', fontsize=13, **BOLD, color='#70AAFF', ha='right', va='top')

btn_x = P3_X + P_W - 12
rbox(ax, btn_x, P_Y+P_H-22, 9, 3.5, 'Rotate', fc=C_HEADER, ec=C_HEADER_D, tc='white', fontsize=11, lw=1.2)
rbox(ax, btn_x, P_Y+P_H-27, 9, 3.5, 'Zoom',   fc=C_HEADER, ec=C_HEADER_D, tc='white', fontsize=11, lw=1.2)
rbox(ax, btn_x-1.2, P_Y+P_H-32, 10.5, 3.5, 'Export OBJ', fc='#27AE60', ec='#1a6b3c', tc='white', fontsize=11, lw=1.2)

time_box(ax, P3_X+3, P_Y+16, P_W-6, 10.5,
         'Inference Latency', '35 ms', '(RTX 4090, batch size = 1)')

rbox(ax, P3_X+3, P_Y+3.5, P_W-6, 10, '',
     fc='#EBF5FB', ec=C_HEADER, lw=1.8)
ax.text(P3_X+P_W/2, P_Y+9.8, 'Reconstruction Accuracy',
        ha='center', va='center', fontsize=13, **BOLD, color=C_TEXT)
ax.text(P3_X+P_W/2, P_Y+5.6, 'R2 = 0.854     |     MAPE = 10.6 %',
        ha='center', va='center', fontsize=14, **BOLD, color=C_HEADER)

# ============ PANEL D ============
panel(ax, P4_X, P_Y, P4_W, P_H, 'd', 'Step 4: Export to XR Engines')

mesh_x = P4_X + 2
mesh_y = P_Y + P_H - 26
rbox(ax, mesh_x, mesh_y, 15, 9, 'Reconstructed\nMesh (OBJ)',
     fc='#DAE8FC', ec='#1a5276', fontsize=12, lw=1.8)

small_arrow(ax, mesh_x+15.5, mesh_y+4.5, mesh_x+20, mesh_y+4.5, lw=2.5)

bl_x = mesh_x + 20.5
rbox(ax, bl_x, mesh_y, 15, 9, 'Blender 3.6 LTS\nAuto Bridge',
     fc='#E67E22', ec='#B25E00', tc='white', fontsize=12, lw=1.8)

# export arrow to FBX (label placed clearly above, well clear of box)
small_arrow(ax, bl_x+15.5, mesh_y+4.5, bl_x+18.7, mesh_y+4.5, lw=2.5)
ax.text(bl_x+17.1, mesh_y+10.6, 'export', ha='center', va='bottom',
        fontsize=11, **BOLD, color='#333333')

fbx_x = bl_x + 19.5
rbox(ax, fbx_x, mesh_y, 10, 9, '.FBX\nAsset',
     fc='#D5E8D4', ec='#2d6a4f', fontsize=13, lw=2)

# Recentre FBX cluster: shift .FBX box to center of panel horizontally so fork stays inside
# (already placed above; if too far right, we accept and rely on wider panel P4_W=65)

# ---- Unity + Unreal engine boxes, positioned symmetrically under FBX ----
fbx_bot_x = fbx_x + 5          # bottom-center of .FBX Asset
fbx_bot_y = mesh_y

engine_w = 20            # widened to fit 'Unreal Engine 5.3' comfortably
engine_h = 8
# Anchor fork centre to panel centre (not FBX centre) so both engines fit inside
fork_cx = P4_X + P4_W/2
spread = 12                    # half-distance between engine centers
u_cx  = fork_cx - spread       # Unity center x
ue_cx = fork_cx + spread       # Unreal center x
u_x   = u_cx  - engine_w/2
ue_x  = ue_cx - engine_w/2
u_y   = mesh_y - 22

rbox(ax, u_x, u_y, engine_w, engine_h, 'Unity 2022 LTS',
     fc='#F5F5F5', ec='#333333', fontsize=12, lw=2)
ax.text(u_cx, u_y-2.2, 'VR / AR / MR runtime', ha='center', va='top',
        fontsize=11, **BOLD, color='#444444')

rbox(ax, ue_x, u_y, engine_w, engine_h, 'Unreal Engine 5.3',
     fc='#1A1A2E', ec='#555555', tc='white', fontsize=12, lw=2)
ax.text(ue_cx, u_y-2.2, 'VR / AR / MR runtime', ha='center', va='top',
        fontsize=11, **BOLD, color='#444444')

# ---- Clean fork: FBX -> L-elbow to fork_cx -> horizontal bar -> Unity + Unreal ----
jy_bar = u_y + engine_h + 5    # horizontal branch bar y (above engines)
jy_elb = fbx_bot_y - 3         # elbow y just below FBX

# 1) vertical from FBX bottom to elbow
ax.plot([fbx_bot_x, fbx_bot_x], [fbx_bot_y, jy_elb],
        color='#111111', linewidth=1.8, solid_capstyle='round', zorder=3)
# 2) horizontal from FBX-bottom-x to fork centre
ax.plot([fbx_bot_x, fork_cx], [jy_elb, jy_elb],
        color='#111111', linewidth=1.8, solid_capstyle='round', zorder=3)
# 3) vertical from elbow down to branch bar
ax.plot([fork_cx, fork_cx], [jy_elb, jy_bar],
        color='#111111', linewidth=1.8, solid_capstyle='round', zorder=3)
# 4) horizontal branch bar spanning Unity center to Unreal center
ax.plot([u_cx, ue_cx], [jy_bar, jy_bar],
        color='#111111', linewidth=1.8, solid_capstyle='round', zorder=3)
# 5) single junction dot at intersection
ax.add_patch(Circle((fork_cx, jy_bar), 0.55, facecolor='#111111',
                    edgecolor='none', zorder=4))
# 6) arrows down into each engine top
small_arrow(ax, u_cx,  jy_bar, u_cx,  u_y+engine_h+0.2, lw=1.8)
small_arrow(ax, ue_cx, jy_bar, ue_cx, u_y+engine_h+0.2, lw=1.8)

time_box(ax, P4_X+3, P_Y+3, P4_W-6, 13,
         'Round-trip (image -> FBX)', '< 0.9 s',
         '(one-click Blender bridge -> FBX -> engine)')

# ============ Inter-panel arrows ============
arrow_y = P_Y + 55
big_arrow(ax, P1_X+P_W-1, arrow_y, P2_X+1, arrow_y)
big_arrow(ax, P2_X+P_W-1, arrow_y, P3_X+1, arrow_y)
big_arrow(ax, P3_X+P_W-1, arrow_y, P4_X+1, arrow_y)

# ============ LEGEND — 3-col x 3-row grid ============
leg_y = 2
leg_h = 14
lg = FancyBboxPatch((3, leg_y), 234, leg_h,
                    boxstyle="round,pad=0.3,rounding_size=1",
                    linewidth=1.8, edgecolor='#666666', facecolor='#FAFAFA')
ax.add_patch(lg)
ax.text(6, leg_y+leg_h-2.2, 'Legend', ha='left', va='top', fontsize=14, **BOLD, color=C_TEXT)


def leg_swatch(ax, x, y, kind, fc=None, ec=None):
    if kind == 'rect':
        ax.add_patch(FancyBboxPatch((x, y-1.6), 4, 3.2,
                    boxstyle="round,pad=0.1,rounding_size=0.4",
                    linewidth=1.2, edgecolor=ec, facecolor=fc))
    elif kind == 'text':
        ax.text(x+2, y, '42', ha='center', va='center',
                fontsize=15, **BOLD, color=fc)
    elif kind == 'chan_R':
        for i, (c, l) in enumerate([('#E74C3C','R'),('#27AE60','G'),('#2E86C1','B')]):
            rbox(ax, x+i*1.8, y-1.5, 1.6, 3, l, fc=c, ec='#333', tc='white', fontsize=10, lw=0.8, rs=0.25)
    elif kind == 'chan_M':
        rbox(ax, x, y-1.5, 4, 3, 'Mask', fc='#F0B27A', ec='#B25E00', tc='white', fontsize=10, lw=0.8, rs=0.25)
    elif kind == 'axis':
        gx0, gy0 = x+1.3, y-1.1
        ax.add_patch(FancyArrowPatch((gx0, gy0),(gx0+2.2, gy0), arrowstyle='-|>', mutation_scale=11, color='#E74C3C', linewidth=1.6))
        ax.add_patch(FancyArrowPatch((gx0, gy0),(gx0, gy0+2.2), arrowstyle='-|>', mutation_scale=11, color='#27AE60', linewidth=1.6))
        ax.add_patch(FancyArrowPatch((gx0, gy0),(gx0-1.6, gy0-1.6), arrowstyle='-|>', mutation_scale=11, color='#2E86C1', linewidth=1.6))
    elif kind == 'arrow_blue':
        ax.add_patch(FancyArrowPatch((x, y),(x+4, y), arrowstyle='-|>', mutation_scale=18, color=C_ARROW, linewidth=3))
    elif kind == 'arrow_black':
        ax.add_patch(FancyArrowPatch((x, y),(x+4, y), arrowstyle='-|>', mutation_scale=14, color='#111111', linewidth=1.8))


col_x = [16, 96, 172]
label_off = 7.0
row_y = [leg_y+leg_h-6.0, leg_y+leg_h-9.5, leg_y+leg_h-13.0]

legend_grid = [
    ('rect', C_HEADER,  C_HEADER_D, 'Panel header / UI button'),
    ('rect', C_TIME_BG, C_TIME_BD,  'Timing / metric box'),
    ('text', C_METRIC,  None,       'Large green number = performance value'),
    ('rect', '#FFF3CD', C_ACCENT,   'Yellow border = selected / highlighted'),
    ('chan_R', None,    None,       'R / G / B = image colour channels'),
    ('chan_M', None,    None,       'Mask = Gaussian face mask (sigma = 2 px)'),
    ('axis',   None,    None,       'X (red) / Y (green) / Z (blue) = 3D axes'),
    ('arrow_blue',  C_ARROW,  None, 'Blue arrow = workflow order between steps'),
    ('arrow_black', '#111111', None,'Black arrow = intra-step data flow'),
]

for idx, (kind, fc, ec, label) in enumerate(legend_grid):
    r_i = idx // 3
    c_i = idx % 3
    cx = col_x[c_i]
    cy = row_y[r_i]
    leg_swatch(ax, cx, cy, kind, fc=fc, ec=ec)
    off = label_off + (0.8 if kind == 'chan_R' else 0)
    ax.text(cx+off, cy, label, ha='left', va='center', fontsize=11.5, **BOLD, color=C_TEXT)

out_png = '/tmp/Figure3_prototype.png'
out_pdf = '/tmp/Figure3_prototype.pdf'
plt.savefig(out_png, dpi=400, bbox_inches='tight', facecolor='white')
plt.savefig(out_pdf, bbox_inches='tight', facecolor='white')
print(f"Saved: {out_png}")
print(f"Saved: {out_pdf}")
