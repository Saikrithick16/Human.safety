import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(20, 15))
ax.set_xlim(0, 20)
ax.set_ylim(0, 15)
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ── helpers ──────────────────────────────────────────────────────────
def box(x, y, w, h, label, sublabels=[], fill='white', lw=2, fontsize=10, bold=True, header_fill='black', header_text='white'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                linewidth=lw, edgecolor='black', facecolor=fill, zorder=2))
    header_h = 0.48
    ax.add_patch(FancyBboxPatch((x, y+h-header_h), w, header_h, boxstyle="square,pad=0",
                                linewidth=0, facecolor=header_fill, zorder=3))
    ax.text(x+w/2, y+h-header_h/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold' if bold else 'normal',
            color=header_text, zorder=4)
    if sublabels:
        step = (h - header_h) / (len(sublabels) + 0.5)
        for i, s in enumerate(sublabels):
            sy = y + h - header_h - step*(i+1) + step/2
            ax.text(x + w/2, sy, s, ha='center', va='center',
                    fontsize=8, color='black', zorder=4)
            if i < len(sublabels)-1:
                ax.plot([x+0.1, x+w-0.1], [y+h-header_h-step*(i+1), y+h-header_h-step*(i+1)],
                        color='#cccccc', lw=0.6, zorder=3)

def small_box(x, y, w, h, label, fontsize=7.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                linewidth=1, edgecolor='black', facecolor='#f0f0f0', zorder=4))
    ax.text(x+w/2, y+h/2, label, ha='center', va='center',
            fontsize=fontsize, color='black', zorder=5)

def arrow(x1, y1, x2, y2, label='', two_way=False):
    style = '<->' if two_way else '->'
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle=style, color='black', lw=1.5,
                                connectionstyle='arc3,rad=0.0'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.1, my, label, fontsize=7.5, color='black', style='italic',
                ha='left', va='center',
                bbox=dict(facecolor='white', edgecolor='none', pad=1))

# ── TITLE ────────────────────────────────────────────────────────────
ax.text(10, 14.6, 'Human Safety AI System — Architecture Diagram',
        ha='center', va='center', fontsize=15, fontweight='bold', color='black')
ax.plot([0.5, 19.5], [14.3, 14.3], color='black', lw=1.5)

# ── LAYER 1: USER ─────────────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((6.5, 13.2), 7, 0.85, boxstyle="square,pad=0",
                            linewidth=1.5, edgecolor='black', facecolor='#e8e8e8', zorder=2))
ax.text(10, 13.625, '👤  User / Browser  (Guardian / Caregiver)', ha='center', va='center',
        fontsize=10, fontweight='bold', color='black', zorder=3)

# ── LAYER 2: FRONTEND ─────────────────────────────────────────────────
box(1.0, 10.5, 18, 2.4, 'Frontend  —  React.js + Vite', fontsize=11, header_fill='black')
# sub-components
comps = ['Login /\nRegister', 'Dashboard\nUI', 'Camera Feed\nViewer', 'Alert\nHistory', 'Analytics\nCharts']
cw, gap = 2.8, 0.4
start_x = 1.3
for i, c in enumerate(comps):
    small_box(start_x + i*(cw+gap), 10.65, cw, 1.9, c, fontsize=8)

# ── ARROW: user → frontend ─────────────────────────────────────────
arrow(10, 13.2, 10, 12.9, 'HTTP / HTTPS', two_way=True)

# ── ARROW: frontend → backend ──────────────────────────────────────
arrow(10, 10.5, 10, 9.9, 'REST API + JWT', two_way=True)

# ── LAYER 3: BACKEND ─────────────────────────────────────────────────
box(1.0, 5.0, 18, 4.7, 'FastAPI Backend  —  Python  (Async REST API Server)', fontsize=11, header_fill='black')

# Auth Module
box(1.3, 5.15, 4.8, 3.87, 'Auth Module', fontsize=9,
    sublabels=['JWT Token Generator', 'Argon2id Password Hasher', 'users.json Store', 'Login / Register Endpoints'])

# Camera Module
box(6.5, 5.15, 6.0, 3.87, 'Camera Module', fontsize=9,
    sublabels=['Camera Manager (Thread)', 'Camera AI (OpenCV)', 'MediaPipe Pose Detector',
               'MockCamera Fallback', 'MJPEG Stream Endpoint', 'SharedState (In-Memory)'])

# Alert Engine
box(12.9, 5.15, 5.8, 3.87, 'Alert Escalation Engine', fontsize=9,
    sublabels=['Level 1 — App Notification (0s)', 'Level 2 — SMS Alert (30s)',
               'Level 3 — Voice Call (60s)', 'Level 4 — Emergency (120s)'])

# ── LAYER 4: EXTERNAL ────────────────────────────────────────────────
# Camera Hardware
box(0.5, 1.2, 4.0, 3.0, 'Camera Hardware', fontsize=9, header_fill='black',
    sublabels=['Physical USB/IP Camera', 'OpenCV Frame Capture', 'MockCamera (640×480)'])
arrow(2.5, 4.2, 4.5, 5.15, 'Video Frames')

# IoT Sensor Device
box(5.0, 1.2, 4.2, 3.0, 'IoT Sensor Device', fontsize=9, header_fill='black',
    sublabels=['Wearable IMU Sensor', 'Accel [ax,ay,az]', 'Gyro [gx,gy,gz]'])
arrow(7.1, 4.2, 8.0, 5.15, '/fall API POST')

# Twilio
box(10.2, 1.2, 4.2, 3.0, 'Twilio Platform', fontsize=9, header_fill='black',
    sublabels=['SMS Gateway', 'Voice Call (TwiML)', 'Multi-Number Dispatch'])
arrow(14.0, 7.5, 14.4, 7.5, 'SMS / Voice')
ax.annotate('', xy=(14.0, 7.5), xytext=(14.4, 7.5),
            arrowprops=dict(arrowstyle='<-', color='black', lw=1.3))
# re-draw properly
ax.annotate('', xy=(12.4, 2.8), xytext=(12.9, 6.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.3))
ax.text(12.0, 4.7, 'SMS /\nVoice', fontsize=7, color='black', style='italic', ha='center')

# SMTP
box(15.2, 1.2, 4.3, 3.0, 'SMTP Email Server', fontsize=9, header_fill='black',
    sublabels=['Email Alert Dispatch', 'Recipient Address', 'Alert Message Body'])
ax.annotate('', xy=(16.5, 4.2), xytext=(16.5, 5.15),
            arrowprops=dict(arrowstyle='<-', color='black', lw=1.3))
ax.text(16.8, 4.65, 'Email', fontsize=7, color='black', style='italic', ha='left')

# ── LAYER LABELS (left margin) ────────────────────────────────────────
for ly, lbl in [(13.6,'Layer 1\nUser'), (11.7,'Layer 2\nFrontend'),
                 (7.3,'Layer 3\nBackend'), (2.7,'Layer 4\nExternal')]:
    ax.text(0.15, ly, lbl, ha='center', va='center', fontsize=7.5,
            color='black', fontweight='bold', rotation=90,
            bbox=dict(facecolor='#e8e8e8', edgecolor='black', boxstyle='round,pad=0.3', lw=0.8))

plt.tight_layout(pad=0.3)
plt.savefig('/Users/saikrithick/Downloads/human_safety_ai/architecture_diagram.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Architecture diagram saved!")
