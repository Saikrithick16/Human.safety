import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'

fig, ax = plt.subplots(figsize=(22, 16))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('white')

# ── helpers ──────────────────────────────────────────────────────────
def ext_entity(x, y, w, h, label):
    """External entity = double-border rectangle"""
    ax.add_patch(FancyBboxPatch((x-0.12, y-0.12), w+0.24, h+0.24,
                                boxstyle="square,pad=0", lw=1.5, edgecolor='black', facecolor='#e8e8e8', zorder=2))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="square,pad=0", lw=1.5, edgecolor='black', facecolor='#e8e8e8', zorder=3))
    ax.text(x+w/2, y+h/2, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color='black', zorder=4, wrap=True,
            multialignment='center')

def process(x, y, r, label, num):
    """Process = circle with number"""
    circle = plt.Circle((x, y), r, color='white', ec='black', lw=2, zorder=2)
    ax.add_patch(circle)
    # Top half label (number)
    ax.plot([x-r, x+r], [y, y], color='black', lw=1, zorder=3)
    ax.text(x, y + r*0.45, num, ha='center', va='center',
            fontsize=9, fontweight='bold', color='black', zorder=4)
    ax.text(x, y - r*0.35, label, ha='center', va='center',
            fontsize=8, color='black', zorder=4, multialignment='center')

def datastore(x, y, w, h, label, num):
    """Data store = open-ended rectangle (two horizontal lines)"""
    ax.plot([x, x+w], [y+h, y+h], color='black', lw=2)
    ax.plot([x, x+w], [y, y], color='black', lw=2)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                lw=0, facecolor='#f5f5f5', zorder=2))
    ax.text(x + 0.25, y+h/2, num, ha='left', va='center',
            fontsize=8, fontweight='bold', color='black', zorder=3)
    ax.text(x + w/2 + 0.2, y+h/2, label, ha='center', va='center',
            fontsize=8.5, color='black', zorder=3)

def arrow(x1, y1, x2, y2, label='', color='black', lw=1.4, label_offset=(0.1, 0.12)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle='arc3,rad=0.0'))
    if label:
        mx = (x1+x2)/2 + label_offset[0]
        my = (y1+y2)/2 + label_offset[1]
        ax.text(mx, my, label, ha='center', va='center',
                fontsize=7.5, color='black', style='italic',
                bbox=dict(facecolor='white', edgecolor='none', pad=1))

# ── TITLE ─────────────────────────────────────────────────────────────
ax.text(11, 15.55, 'Human Safety AI — Level 1 Data Flow Diagram',
        ha='center', va='center', fontsize=16, fontweight='bold')
ax.plot([0.5, 21.5], [15.2, 15.2], color='black', lw=1.5)

# ═══════════════════════════════════════════════════════════════════
# EXTERNAL ENTITIES
# ═══════════════════════════════════════════════════════════════════
# E1 - Guardian/User  (top-left)
ext_entity(0.4, 12.5, 2.4, 1.2, "E1\nGuardian /\nUser")

# E2 - Camera Hardware (mid-left)
ext_entity(0.4, 8.8, 2.4, 1.2, "E2\nCamera\nHardware")

# E3 - IoT Sensor Device (bottom-left)
ext_entity(0.4, 5.5, 2.4, 1.2, "E3\nIoT Sensor\nDevice")

# E4 - Twilio Platform (right)
ext_entity(19.0, 9.6, 2.4, 1.2, "E4\nTwilio\nPlatform")

# E5 - SMTP Email (right-top)
ext_entity(19.0, 12.5, 2.4, 1.2, "E5\nSMTP Email\nServer")

# ═══════════════════════════════════════════════════════════════════
# PROCESSES
# ═══════════════════════════════════════════════════════════════════
# P1 - User Authentication (top area)
process(5.5, 13.1, 1.2, "User\nAuthentication", "P1")

# P2 - Camera & AI Monitoring (center-left)
process(9.5, 10.2, 1.3, "Camera &\nAI Monitoring", "P2")

# P3 - Fall Detection (center)
process(13.5, 10.2, 1.3, "Fall\nDetection\n(YOLO)", "P3")

# P4 - Alert Generation (center-right)
process(17.0, 12.2, 1.2, "Alert\nGeneration", "P4")

# P5 - Alert Escalation (right)
process(17.0, 8.5, 1.2, "Alert\nEscalation", "P5")

# P6 - Dashboard & Analytics (center-bottom)
process(11.0, 5.5, 1.2, "Dashboard\n& Analytics", "P6")

# ═══════════════════════════════════════════════════════════════════
# DATA STORES
# ═══════════════════════════════════════════════════════════════════
# D1 - Users / Auth Store
datastore(4.0, 10.0, 4.0, 0.7, "Users & Auth Store", "D1")

# D2 - Events & Sessions
datastore(8.0, 7.2, 4.5, 0.7, "Events & Sessions Log", "D2")

# D3 - Alerts Store
datastore(13.5, 7.2, 4.0, 0.7, "Alerts & Escalations", "D3")

# D4 - Captured Images
datastore(4.0, 6.5, 4.0, 0.7, "Captured Images", "D4")

# D5 - Sensor Readings
datastore(4.0, 5.0, 4.0, 0.7, "Sensor Readings", "D5")

# ═══════════════════════════════════════════════════════════════════
# ARROWS / DATA FLOWS
# ═══════════════════════════════════════════════════════════════════

# E1 → P1: Login / Register Request
arrow(2.8, 13.1, 4.3, 13.1, "Login / Register", label_offset=(0, 0.2))
# P1 → E1: JWT Token
arrow(4.3, 12.8, 2.8, 12.8, "JWT Token", label_offset=(0, -0.2))

# P1 → D1: Store user credentials
arrow(5.5, 11.9, 5.5, 10.7, "Store Credentials", label_offset=(0.9, 0))

# E2 → P2: Live Video Frames
arrow(2.8, 9.4, 8.2, 10.1, "Live Video Frames", label_offset=(0, 0.2))

# P2 → D2: Log session
arrow(9.5, 8.9, 9.5, 7.9, "Session Data", label_offset=(0.9, 0))

# P2 → D4: Save frame
arrow(8.5, 9.3, 6.5, 7.2, "Captured Frame", label_offset=(-0.3, 0.15))

# P2 → P3: Processed frames + keypoints
arrow(10.8, 10.2, 12.2, 10.2, "Keypoints /\nPose Data", label_offset=(0, 0.3))

# P3 → D2: Log fall event
arrow(13.5, 8.9, 11.5, 7.9, "Fall Event Log", label_offset=(0.2, 0.2))

# P3 → P4: Fall alert trigger
arrow(14.8, 10.8, 15.8, 11.4, "Fall Detected\n(confidence, time)", label_offset=(0.1, 0.25))

# P4 → D3: Store alert
arrow(16.0, 12.2, 17.5, 7.9, "Alert Record", label_offset=(0.8, 0))

# P4 → E5: Send email alert
arrow(18.2, 12.9, 19.0, 13.0, "Email Alert", label_offset=(0, 0.2))

# P4 → P5: Escalation trigger
arrow(17.0, 11.0, 17.0, 9.7, "Escalate if\nUn-acknowledged", label_offset=(1.2, 0))

# P5 → E4: SMS / Voice
arrow(18.2, 8.8, 19.0, 10.0, "SMS / Voice\nCall", label_offset=(0.5, 0.1))
arrow(19.0, 9.9, 18.2, 8.6, "Delivery\nStatus", label_offset=(-0.7, 0.1))

# E3 → P3: Sensor accel/gyro data
arrow(2.8, 6.0, 12.2, 9.8, "Accel / Gyro Data", label_offset=(0, 0.25))

# P3 → D5: Store sensor reading
arrow(12.5, 9.5, 7.0, 5.7, "Sensor Reading", label_offset=(0.2, 0.3))

# E1 → P6: View dashboard request
arrow(1.6, 12.5, 10.2, 6.5, "View Dashboard\nRequest", label_offset=(-0.9, 0))

# P6 → E1: Dashboard data response
arrow(10.5, 6.5, 2.0, 12.5, "Stats / Events /\nCamera Feed", label_offset=(-1.3, 0))

# D2 → P6: Event history
arrow(10.2, 7.2, 10.8, 6.7, "Event History", label_offset=(0.9, 0.1))

# D3 → P6: Alert history
arrow(13.5, 7.55, 12.2, 6.3, "Alert History", label_offset=(0.5, 0.25))

# ═══════════════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════════════
lx, ly = 0.4, 1.0
ax.text(lx, ly+1.8, 'Legend:', fontsize=9, fontweight='bold')

# External entity
ax.add_patch(FancyBboxPatch((lx, ly+1.0), 1.0, 0.6, boxstyle="square,pad=0",
                             lw=1.5, edgecolor='black', facecolor='#e8e8e8'))
ax.add_patch(FancyBboxPatch((lx+0.08, ly+1.08), 0.84, 0.44, boxstyle="square,pad=0",
                             lw=1, edgecolor='black', facecolor='#e8e8e8'))
ax.text(lx+1.2, ly+1.3, 'External Entity', fontsize=8.5, va='center')

# Process
circle2 = plt.Circle((lx+0.5, ly+0.3), 0.3, color='white', ec='black', lw=1.5, zorder=2)
ax.add_patch(circle2)
ax.plot([lx+0.2, lx+0.8], [ly+0.3, ly+0.3], color='black', lw=0.8)
ax.text(lx+1.2, ly+0.3, 'Process', fontsize=8.5, va='center')

# Data store
ax.plot([lx+3.5, lx+5.0], [ly+1.65, ly+1.65], color='black', lw=1.5)
ax.plot([lx+3.5, lx+5.0], [ly+1.15, ly+1.15], color='black', lw=1.5)
ax.text(lx+5.2, ly+1.4, 'Data Store', fontsize=8.5, va='center')

# Data flow
ax.annotate('', xy=(lx+5.0, ly+0.3), xytext=(lx+3.5, ly+0.3),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.3))
ax.text(lx+5.2, ly+0.3, 'Data Flow', fontsize=8.5, va='center')

plt.tight_layout(pad=0.5)
plt.savefig('/Users/saikrithick/Downloads/human_safety_ai/dfd_level1.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print("Level 1 DFD saved!")
