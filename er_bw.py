import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(24, 17))
ax.set_xlim(0, 24)
ax.set_ylim(0, 17)
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

def draw_table(ax, x, y, w, fields):
    row_h = 0.38
    h = row_h * (len(fields) + 1)
    # outer border
    ax.add_patch(FancyBboxPatch((x, y - h + row_h), w, h,
                                boxstyle="square,pad=0",
                                linewidth=1.8, edgecolor='black', facecolor='white', zorder=2))
    # header
    title = fields[0]
    ax.add_patch(FancyBboxPatch((x, y), w, row_h,
                                boxstyle="square,pad=0",
                                linewidth=0, facecolor='black', zorder=3))
    ax.text(x + w/2, y + row_h/2, title,
            ha='center', va='center', fontsize=9, fontweight='bold',
            color='white', zorder=4)
    # fields
    for i, field in enumerate(fields[1:]):
        fy = y - row_h * i
        if i > 0:
            ax.plot([x, x+w], [fy, fy], color='#cccccc', lw=0.6, zorder=3)
        bold = field.startswith('[PK]')
        italic = field.startswith('[FK]')
        clean = field.replace('[PK] ','').replace('[FK] ','')
        prefix = ''
        if bold:   prefix = 'PK'
        if italic: prefix = 'FK'
        # badge
        if prefix:
            bx = x + 0.08
            by = fy - row_h
            ax.add_patch(FancyBboxPatch((bx, by + 0.06), 0.36, 0.25,
                                        boxstyle="square,pad=0",
                                        linewidth=1, edgecolor='black',
                                        facecolor='black' if bold else 'white', zorder=4))
            ax.text(bx + 0.18, by + 0.185, prefix,
                    ha='center', va='center', fontsize=6, fontweight='bold',
                    color='white' if bold else 'black', zorder=5)
            tx = x + 0.52
        else:
            tx = x + 0.14
        ax.text(tx, fy - row_h/2,
                clean,
                ha='left', va='center', fontsize=8,
                fontweight='bold' if bold else 'normal',
                fontstyle='italic' if italic else 'normal',
                color='black', zorder=4)
    return h

# ── TABLE DATA ──────────────────────────────────────────────────────────
tables = {
    'users':              (1.0,  15.8, 4.2, ['users',
                           '[PK] user_id', 'email', 'password_hash',
                           'full_name', 'created_at', 'is_active', 'last_login']),
    'user_phone_numbers': (6.5,  15.8, 4.5, ['user_phone_numbers',
                           '[PK] phone_id', '[FK] user_id',
                           'phone_number', 'is_primary', 'added_at']),
    'camera_sessions':    (12.5, 15.8, 4.5, ['camera_sessions',
                           '[PK] session_id', '[FK] user_id',
                           'start_time', 'end_time', 'camera_mode',
                           'total_frames', 'status']),
    'alert_escalations':  (18.5, 15.8, 5.2, ['alert_escalations',
                           '[PK] escalation_id', '[FK] user_id',
                           '[FK] event_id', 'alert_type', 'current_level',
                           'status', 'start_time', 'response_time']),
    'events':             (1.0,   8.2, 4.2, ['events',
                           '[PK] event_id', '[FK] session_id',
                           '[FK] user_id', 'event_type', 'message',
                           'confidence', 'timestamp']),
    'alerts':             (6.5,   8.2, 4.5, ['alerts',
                           '[PK] alert_id', '[FK] event_id',
                           '[FK] user_id', 'alert_type', 'delivery_method',
                           'recipient_address', 'delivery_status', 'timestamp']),
    'captured_images':    (12.5,  8.2, 4.5, ['captured_images',
                           '[PK] image_id', '[FK] session_id',
                           '[FK] user_id', 'image_data', 'captured_at']),
    'sensor_readings':    (18.5,  8.2, 5.2, ['sensor_readings',
                           '[PK] reading_id', '[FK] user_id',
                           'accel_x', 'accel_y', 'accel_z',
                           'gyro_x', 'gyro_y', 'gyro_z',
                           'fall_detected', 'confidence', 'recorded_at']),
}

heights = {}
centers = {}
for key, (x, y, w, fields) in tables.items():
    h = draw_table(ax, x, y, w, fields)
    heights[key] = h
    centers[key] = (x + w/2, y - h/2 + 0.38)

def conn(ax, x1, y1, x2, y2, label='', card1='1', cardM='M'):
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.4,
                                connectionstyle='arc3,rad=0.05'))
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.text(x1+0.15, y1+0.12, card1, fontsize=9, color='black', fontweight='bold')
    ax.text(x2-0.25, y2+0.12, cardM, fontsize=9, color='black', fontweight='bold')
    if label:
        ax.text(mx, my+0.18, label, fontsize=7.5, color='#333333',
                ha='center', style='italic',
                bbox=dict(facecolor='white', edgecolor='none', pad=1))

def right_of(key): x,y,w,f = tables[key]; return (x+w, y - heights[key]/2 + 0.38)
def left_of(key):  x,y,w,f = tables[key]; return (x,   y - heights[key]/2 + 0.38)
def bot_of(key):   x,y,w,f = tables[key]; h=heights[key]; return (x+w/2, y-h+0.38)
def top_of(key):   x,y,w,f = tables[key]; return (x+w/2, y+0.38)

# Relationships
conn(ax, *right_of('users'),         *left_of('user_phone_numbers'),  'has')
conn(ax, *right_of('user_phone_numbers'), *left_of('camera_sessions'), 'initiates')
conn(ax, *right_of('camera_sessions'),   *left_of('alert_escalations'),'escalates')
conn(ax, *bot_of('users'),           *top_of('events'),               'owns')
conn(ax, *bot_of('user_phone_numbers'), *top_of('alerts'),            'receives')
conn(ax, *bot_of('camera_sessions'), *top_of('captured_images'),      'stores')
conn(ax, *bot_of('alert_escalations'), *top_of('sensor_readings'),    'records')
conn(ax, *right_of('events'),        *left_of('alerts'),              'triggers')
conn(ax, *right_of('alerts'),        *left_of('captured_images'),     '')
conn(ax, *right_of('captured_images'), *left_of('sensor_readings'),   '')

# Title
ax.text(12, 16.65, 'Entity Relationship Diagram  —  Human Safety AI System',
        ha='center', va='center', fontsize=16, fontweight='bold', color='black')
ax.plot([1, 23], [16.4, 16.4], color='black', lw=1.5)

# Legend
lx, ly = 1.0, 2.5
ax.add_patch(FancyBboxPatch((lx, ly-1.4), 5.5, 1.9,
                            boxstyle="square,pad=0.05",
                            linewidth=1.2, edgecolor='black', facecolor='white', zorder=2))
ax.text(lx+2.75, ly+0.32, 'LEGEND', ha='center', fontsize=10, fontweight='bold')
ax.add_patch(FancyBboxPatch((lx+0.2, ly-0.2), 0.5, 0.25, boxstyle="square,pad=0",
             lw=1, edgecolor='black', facecolor='black', zorder=3))
ax.text(lx+0.45, ly-0.075, 'PK', ha='center', va='center', fontsize=7,
        color='white', fontweight='bold', zorder=4)
ax.text(lx+0.9, ly-0.07, '= Primary Key (underlined)', fontsize=8)
ax.add_patch(FancyBboxPatch((lx+0.2, ly-0.65), 0.5, 0.25, boxstyle="square,pad=0",
             lw=1, edgecolor='black', facecolor='white', zorder=3))
ax.text(lx+0.45, ly-0.52, 'FK', ha='center', va='center', fontsize=7,
        color='black', fontweight='bold', zorder=4)
ax.text(lx+0.9, ly-0.52, '= Foreign Key (italic)', fontsize=8)
ax.annotate('', xy=(lx+1.5, ly-0.95), xytext=(lx+0.2, ly-0.95),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
ax.text(lx+1.7, ly-0.91, '= One-to-Many (1:M)', fontsize=8)

plt.tight_layout(pad=0.4)
plt.savefig('/Users/saikrithick/Downloads/human_safety_ai/er_diagram_bw.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("B/W ER Diagram saved!")
