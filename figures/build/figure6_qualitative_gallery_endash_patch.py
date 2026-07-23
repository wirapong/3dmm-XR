"""
Figure 6 en-dash patch v3 - fixed bar geometry (reliable).

Use uniform bar dimensions across all 8 rows.
Erase generously to fully cover any original text/bar remnants.
"""

from PIL import Image, ImageDraw, ImageFont

SRC = '/tmp/fig6_original.png'
DST = '/tmp/Figure6_qualitative_gallery.png'

im = Image.open(SRC).convert('RGB')
W, H = im.size
print(f'source: {W}x{H}')

col_w = W // 3       # 1133
row_h = H // 8       # 1046

LABELS = [
    'frontal (<15\u00b0) \u2022 yaw=11.5\u00b0',
    'frontal (<15\u00b0) \u2022 yaw=12.9\u00b0',
    'small (15\u201330\u00b0) \u2022 yaw=20.7\u00b0',
    'small (15\u201330\u00b0) \u2022 yaw=18.7\u00b0',
    'moderate (30\u201360\u00b0) \u2022 yaw=30.9\u00b0',
    'moderate (30\u201360\u00b0) \u2022 yaw=30.7\u00b0',
    'profile (60\u201390\u00b0) \u2022 yaw=67.9\u00b0',
    'profile (60\u201390\u00b0) \u2022 yaw=65.6\u00b0',
]

font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 62)
draw = ImageDraw.Draw(im)

# Erase zone: fully cover any possible original label bar location
# Original bar was found at y=45-120 in some rows; erase from y=0 to be safe.
ERASE_Y_TOP = 0
ERASE_Y_BOT = 260
ERASE_X_LEFT = 20
ERASE_X_RIGHT = 1080

# Redraw bar: tight, matches original visual
BAR_Y_TOP = 60
BAR_Y_BOT = 145
BAR_X_LEFT = 40
BAR_X_RIGHT = 1050
TEXT_X = 55
TEXT_Y_OFFSET = 72   # y within row for text baseline top

# Sample a face-color per row from BELOW the label area so 'erase' looks natural (matches skin)
def sample_face_color(im, y_off):
    # Pick a patch from x=200..400, y=(row_h//2)..(row_h//2)+30
    from PIL import ImageStat
    patch = im.crop((200, y_off + row_h // 2, 400, y_off + row_h // 2 + 30))
    stat = ImageStat.Stat(patch)
    return tuple(int(v) for v in stat.mean[:3])

for i, label in enumerate(LABELS):
    y_off = i * row_h
    face_color = sample_face_color(im, y_off)
    # 1) Erase original bar region with a face-tone (natural blend, avoids black stripe artifacts)
    draw.rectangle(
        [ERASE_X_LEFT, y_off + ERASE_Y_TOP,
         ERASE_X_RIGHT, y_off + ERASE_Y_BOT],
        fill=face_color
    )
    # 2) Draw fresh label bar (opaque dark to match original look after semi-transparent overlay)
    #    Original bar looks ~50% opacity over faces => appears as very dark gray
    draw.rectangle(
        [BAR_X_LEFT, y_off + BAR_Y_TOP,
         BAR_X_RIGHT, y_off + BAR_Y_BOT],
        fill=(35, 35, 35)  # dark gray to match semi-transparent look
    )
    # 3) Draw label text white
    draw.text((TEXT_X, y_off + TEXT_Y_OFFSET), label, font=font, fill=(255, 255, 255))
    print(f'row {i+1}: patched')

im.save(DST, optimize=True)
print(f'saved: {DST}')

preview = im.copy()
preview.thumbnail((2400, 2400))
preview.save('/tmp/Figure6_preview.png')
print('preview saved')
