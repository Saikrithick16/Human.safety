import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

fig, ax = plt.subplots(1, 1, figsize=(22, 16))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('#0d1b2a')
ax.set_facecolor('#0d1b2a')

# Colors
bg_color    = '#0d1b2a'
box_bg      = '#112240'
box_border  = '#00d4ff'
header_bg   = '#0a3d6b'
text_color  = '#ffffff'
pk_color    = '#ffd700'
fk_color    = '#00ff88'
rel_color   = '#00d4ff'
line_color  = '#00d4ff'

def draw_entity(ax, x, y, w, h, title, fields):
    # Shadow
    shadow = FancyBboxPatch((x+0.07, y-0.07), w, h,
                            boxstyle="round,pad=0.05",
                            linewidth=0, facecolor='#000000', alpha=0.4, zorder=1)
    ax.add_patch(shadow)
    # Body
    body = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.05",
                          linewidth=2, edgecolor=box_border,
                          facecolor=box_bg, zorder=2)
    ax.add_patch(body)
    # Header bar
    row_h = h / (len(fields) + 1)
    header = FancyBboxPatch((x, y + h - row_h), w, row_h,
                            boxstyle="round,pad=0.03",
                            linewidth=0, facecolor=header_bg, zorder=3)
    ax.add_patch(header)
    # Title
    ax.text(x + w/2, y + h - row_h/2, title,
            ha='center', va='center', fontsize=9, fontweight='bold',
            color=box_border, zorder=4, fontfamily='monospace')
    # Divider line under header
    ax.plot([x, x+w], [y + h - row_h, y + h - row_h], color=box_border, lw=1, zorder=4)
    # Fields
    for i, field in enumerate(fields):
        fy = y + h - row_h * (i + 2) + row_h/2
        # Alternating row shade
        if i % 2 == 0:
            row_rect = FancyBboxPatch((x+0.02, fy - row_h/2 + 0.02), w-0.04, row_h-0.04,
                                     boxstyle="square,pad=0",
                                     linewidth=0, facecolor='#0d2137', alpha=0.5, zorder=3)
            ax.add_patch(row_rect)
        col = pk_color if '🔑' in field or '(PK)' in field else (fk_color if '(FK)' in field else text_color)
        ax.text(x + 0.18, fy, field, ha='left', va='center',
                fontsize=6.5, color=col, zorder=4, fontfamily='monospace')

def draw_relation(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=line_color, lw=1.5,
                                connectionstyle='arc3,rad=0.0'),
                zorder=1)
    mx, my = (x1+x2)/2, (y1+y2)/2
    if label:
        ax.text(mx, my+0.2, label, ha='center', va='bottom',
                fontsize=6.5, color=rel_color, style='italic', zorder=5)

# ─── Table definitions ────────────────────────────────────────────────
entities = {
    'users': {
        'pos': (1.0, 9.5), 'w': 3.8, 'h': 4.0,
        'fields': [
            'user_id        [PK]',
            'email',
            'password_hash',
            'full_name',
            'created_at',
            'is_active',
            'last_login',
        ]
    },
    'user_phone_numbers': {
        'pos': (6.2, 11.5), 'w': 3.8, 'h': 3.2,
        'fields': [
            'phone_id       [PK]',
            'user_id        [FK]',
            'phone_number',
            'is_primary',
            'added_at',
        ]
    },
    'camera_sessions': {
        'pos': (1.0, 4.5), 'w': 3.8, 'h': 3.8,
        'fields': [
            'session_id     [PK]',
            'user_id        [FK]',
            'start_time',
            'end_time',
            'camera_mode',
            'total_frames',
            'status',
        ]
    },
    'events': {
        'pos': (6.2, 5.8), 'w': 3.8, 'h': 3.5,
        'fields': [
            'event_id       [PK]',
            'session_id     [FK]',
            'user_id        [FK]',
            'event_type',
            'message',
            'confidence',
            'timestamp',
        ]
    },
    'alerts': {
        'pos': (11.4, 5.8), 'w': 3.8, 'h': 3.8,
        'fields': [
            'alert_id       [PK]',
            'event_id       [FK]',
            'user_id        [FK]',
            'alert_type',
            'delivery_method',
            'recipient_address',
            'delivery_status',
            'timestamp',
        ]
    },
    'alert_escalations': {
        'pos': (1.0, 0.4), 'w': 3.8, 'h': 3.6,
        'fields': [
            'escalation_id  [PK]',
            'user_id        [FK]',
            'event_id       [FK]',
            'alert_type',
            'current_level',
            'status',
            'start_time',
            'response_time',
        ]
    },
    'captured_images': {
        'pos': (6.2, 0.4), 'w': 3.8, 'h': 3.0,
        'fields': [
            'image_id       [PK]',
            'session_id     [FK]',
            'user_id        [FK]',
            'image_data',
            'captured_at',
        ]
    },
    'sensor_readings': {
        'pos': (11.4, 0.4), 'w': 3.8, 'h': 3.8,
        'fields': [
            'reading_id     [PK]',
            'user_id        [FK]',
            'accel_x/accel_y/accel_z',
            'gyro_x/gyro_y/gyro_z',
            'fall_detected',
            'confidence',
            'recorded_at',
        ]
    },
}

# Draw all entities
for name, e in entities.items():
    x, y = e['pos']
    draw_entity(ax, x, y, e['w'], e['h'], name, e['fields'])

# ─── Relationships ─────────────────────────────────────────────────────
# users → user_phone_numbers
draw_relation(ax, 4.8, 12.0, 6.2, 12.5, '1 : M  has')
# users → camera_sessions
draw_relation(ax, 2.9, 9.5, 2.9, 8.3, '1 : M  initiates')
# users → alert_escalations
draw_relation(ax, 1.5, 9.5, 1.5, 4.0, '1 : M')
ax.text(0.7, 6.2, '1:M\nassigned', ha='center', va='center', fontsize=6.5,
        color=rel_color, style='italic')
# users → sensor_readings
draw_relation(ax, 4.8, 10.0, 11.4, 3.0, '1 : M  records')
# camera_sessions → events
draw_relation(ax, 4.8, 6.5, 6.2, 7.0, '1 : M  generates')
# events → alerts
draw_relation(ax, 10.0, 7.5, 11.4, 7.5, '1 : M  triggers')
# camera_sessions → captured_images
draw_relation(ax, 3.5, 4.5, 6.2, 2.5, '1 : M  stores')
# users → alert_escalations line
draw_relation(ax, 2.0, 9.5, 2.0, 4.0, '')

# ─── Legend ──────────────────────────────────────────────────────────
leg_x, leg_y = 16.5, 13.5
leg_box = FancyBboxPatch((leg_x, leg_y - 3.0), 4.8, 3.4,
                         boxstyle="round,pad=0.1",
                         linewidth=1.5, edgecolor=box_border,
                         facecolor=box_bg, zorder=2)
ax.add_patch(leg_box)
ax.text(leg_x + 2.4, leg_y + 0.2, 'LEGEND', ha='center', va='center',
        fontsize=9, fontweight='bold', color=box_border)
ax.plot([leg_x+0.2, leg_x+1.0], [leg_y - 0.6, leg_y - 0.6], color=pk_color, lw=2)
ax.text(leg_x + 1.2, leg_y - 0.6, 'Primary Key (PK)', va='center', fontsize=7.5, color=pk_color)
ax.plot([leg_x+0.2, leg_x+1.0], [leg_y - 1.2, leg_y - 1.2], color=fk_color, lw=2)
ax.text(leg_x + 1.2, leg_y - 1.2, 'Foreign Key (FK)', va='center', fontsize=7.5, color=fk_color)
ax.annotate('', xy=(leg_x+1.0, leg_y-1.8), xytext=(leg_x+0.2, leg_y-1.8),
            arrowprops=dict(arrowstyle='->', color=line_color, lw=1.5))
ax.text(leg_x + 1.2, leg_y - 1.8, 'Relationship (1:M)', va='center', fontsize=7.5, color=text_color)
ax.text(leg_x + 0.2, leg_y - 2.4, '1:M = One to Many', va='center', fontsize=7.5, color=text_color)
ax.text(leg_x + 0.2, leg_y - 2.85, 'All relations via user_id FK', va='center', fontsize=7, color='#aaaaaa')

# ─── Title ───────────────────────────────────────────────────────────
ax.text(11, 15.5, 'Entity Relationship Diagram  —  Human Safety AI Database',
        ha='center', va='center', fontsize=15, fontweight='bold',
        color=box_border, fontfamily='monospace')

plt.tight_layout(pad=0.3)
plt.savefig('/Users/saikrithick/Downloads/human_safety_ai/er_diagram.png',
            dpi=180, bbox_inches='tight', facecolor=bg_color)
print("ER Diagram saved successfully!")
