"""
Rebuild Figure 4 - Two Panels (RMSE + Percentage improvement) for
Qianqian He et al. — Informatics MDPI submission.

Proofreading fixes:
1. Overlap between "4.125" bar-label and legend box — resolved by raising
   y-axis headroom + placing legend outside plot area (bbox_to_anchor).
2. En dash (U+2013) between numbers in yaw-interval labels.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Helvetica'
mpl.rcParams['font.size'] = 13
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'

# Data (verified from vision)
CATEGORIES = ['Frontal', '0\u201330\u00b0', '30\u201360\u00b0', '60\u201390\u00b0']

# Panel A: baseline vs proposed
BASELINE = [2.512, 2.845, 3.420, 4.125]
PROPOSED = [2.456, 2.580, 2.712, 2.890]

# Panel B: percent improvement
PCT_IMPROV = [2.2, 9.3, 20.7, 29.9]

# Colors
C_BASE   = '#7F8C8D'
C_PROP   = '#2E86C1'
C_ORANGE = '#E67E22'

fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=200)

# ================== Panel A ==================
ax = axes[0]
x = np.arange(len(CATEGORIES))
width = 0.36

bars_base = ax.bar(x - width/2, BASELINE, width,
                   color=C_BASE, edgecolor='#333333', linewidth=1.2,
                   label='Single-modality baseline (RGB only)')
bars_prop = ax.bar(x + width/2, PROPOSED, width,
                   color=C_PROP, edgecolor='#154360', linewidth=1.2,
                   label='Proposed 3DMM\u2013CNN (RGB + landmark mask)')

# Add value labels above each bar
for b, v in zip(bars_base, BASELINE):
    ax.text(b.get_x() + b.get_width()/2, v + 0.08, f'{v:.3f}',
            ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#222222')
for b, v in zip(bars_prop, PROPOSED):
    ax.text(b.get_x() + b.get_width()/2, v + 0.08, f'{v:.3f}',
            ha='center', va='bottom', fontsize=11.5, fontweight='bold', color='#0F3E70')

ax.set_xticks(x)
ax.set_xticklabels(CATEGORIES, fontsize=12.5, fontweight='bold')
ax.set_xlabel('Yaw interval', fontsize=13.5, fontweight='bold', labelpad=8)
ax.set_ylabel('RMSE (lower is better)', fontsize=13.5, fontweight='bold', labelpad=8)
ax.set_title('(A) Absolute RMSE across yaw strata',
             fontsize=15, fontweight='bold', pad=14)

# Extra headroom so legend never overlaps top bar (4.125)
ax.set_ylim(0, 5.8)
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis='y', labelsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# Legend BELOW the plot area (bbox_to_anchor) — no overlap with any bar
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          ncol=1, fontsize=11.5, frameon=True, edgecolor='#666666',
          fancybox=False)

# ================== Panel B ==================
ax = axes[1]
bars = ax.bar(x, PCT_IMPROV, 0.55, color=C_ORANGE,
              edgecolor='#B25E00', linewidth=1.2)

for b, v in zip(bars, PCT_IMPROV):
    ax.text(b.get_x() + b.get_width()/2, v + 0.7, f'{v:.1f}%',
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='#333333')

ax.set_xticks(x)
ax.set_xticklabels(CATEGORIES, fontsize=12.5, fontweight='bold')
ax.set_xlabel('Yaw interval', fontsize=13.5, fontweight='bold', labelpad=8)
ax.set_ylabel('RMSE reduction over baseline (%)',
              fontsize=13.5, fontweight='bold', labelpad=8)
ax.set_title('(B) Percentage improvement from landmark-mask fusion',
             fontsize=15, fontweight='bold', pad=14)

ax.set_ylim(0, 38)
ax.set_yticks([0, 5, 10, 15, 20, 25, 30, 35])
ax.tick_params(axis='y', labelsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.set_axisbelow(True)

# Extra space below Panel A for its legend
plt.tight_layout(rect=[0, 0.02, 1, 0.98])
plt.subplots_adjust(bottom=0.22, wspace=0.22)

# Save
out_png = '/tmp/Figure4_two_panels.png'
out_pdf = '/tmp/Figure4_two_panels.pdf'
plt.savefig(out_png, dpi=400, bbox_inches='tight', facecolor='white')
plt.savefig(out_pdf, bbox_inches='tight', facecolor='white')
print(f'Saved: {out_png}')
print(f'Saved: {out_pdf}')

# Verify text characters contain en dash
import subprocess
r = subprocess.run(['file', out_png], capture_output=True, text=True)
print(r.stdout.strip())
