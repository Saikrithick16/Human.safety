import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'

# All rows: (S.No, Field Name, Description, Sample Data)
rows = [
    # ── USERS ──
    ("",  "Table: users", "", ""),
    ("1",  "User Id",          "Unique ID for each user",                    "101"),
    ("2",  "Email",            "User email address",                         "asokan@gmail.com"),
    ("3",  "Password",         "Argon2id hashed password",                   "$argon2id$v=19$..."),
    ("4",  "Full Name",        "Full name of the guardian",                  "Asokan K"),
    ("5",  "Created At",       "Account creation timestamp",                 "2026-03-01 10:30:00"),
    ("6",  "Is Active",        "Whether the account is active",              "True"),
    ("7",  "Last Login",       "Last successful login timestamp",            "2026-03-06 09:00:00"),
    # ── USER_PHONE_NUMBERS ──
    ("",   "Table: user_phone_numbers", "", ""),
    ("8",  "Phone Id",         "Unique phone record ID",                     "201"),
    ("9",  "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("10", "Phone Number",     "Emergency contact (E.164 format)",           "+919487416630"),
    ("11", "Is Primary",       "Whether this is the primary number",         "True"),
    ("12", "Added At",         "Timestamp when number was added",            "2026-03-01 10:35:00"),
    # ── CAMERA_SESSIONS ──
    ("",   "Table: camera_sessions", "", ""),
    ("13", "Session Id",       "Unique session identifier",                  "5001"),
    ("14", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("15", "Start Time",       "Session start timestamp",                    "2026-03-06 09:00:00"),
    ("16", "End Time",         "Session end timestamp (NULL if active)",     "2026-03-06 09:30:00"),
    ("17", "Camera Mode",      "Mode: LIVE / MOCK / UPLOAD",                 "LIVE"),
    ("18", "Total Frames",     "Total frames processed in session",          "5400"),
    ("19", "Status",           "ACTIVE / STOPPED / ERROR",                  "STOPPED"),
    # ── EVENTS ──
    ("",   "Table: events", "", ""),
    ("20", "Event Id",         "Unique event identifier",                    "3001"),
    ("21", "Session Id (FK)",  "References camera_sessions(session_id)",     "5001"),
    ("22", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("23", "Event Type",       "FALL / NORMAL / CAPTURE / MANUAL_ALERT",    "FALL"),
    ("24", "Message",          "Human-readable event description",           "YOLO detected fall (conf: 0.87)"),
    ("25", "Confidence",       "AI confidence score (0.0 – 1.0)",           "0.87"),
    ("26", "Timestamp",        "When the event was detected",                "2026-03-06 09:15:32"),
    # ── ALERTS ──
    ("",   "Table: alerts", "", ""),
    ("27", "Alert Id",         "Unique alert identifier",                    "4001"),
    ("28", "Event Id (FK)",    "References events(event_id)",                "3001"),
    ("29", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("30", "Alert Type",       "EMAIL / SMS / VOICE / APP",                 "SMS"),
    ("31", "Message",          "Alert message body sent",                    "FALL DETECTED! Conf: 87%"),
    ("32", "Channel",          "Delivery channel: email / sms / voice",     "sms"),
    ("33", "Sent At",          "Timestamp when alert was dispatched",        "2026-03-06 09:15:33"),
    ("34", "Delivered",        "Whether delivery was confirmed",             "True"),
    # ── ALERT_ESCALATIONS ──
    ("",   "Table: alert_escalations", "", ""),
    ("35", "Escalation Id",    "Unique escalation ID (UUID)",                "a1b2c3d4-..."),
    ("36", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("37", "Event Id (FK)",    "References events(event_id)",                "3001"),
    ("38", "Alert Type",       "Type of alert that caused escalation",       "FALL"),
    ("39", "Current Level",    "Level 1=App, 2=SMS, 3=Voice, 4=Emergency",  "2"),
    ("40", "Status",           "ACTIVE / ACKNOWLEDGED / CANCELLED",         "ACKNOWLEDGED"),
    ("41", "Started At",       "Escalation start time",                      "2026-03-06 09:15:33"),
    ("42", "Acknowledged At",  "Time when guardian responded",               "2026-03-06 09:16:10"),
    ("43", "Response",         "Guardian's response message",                "I am checking now"),
    # ── CAPTURED_IMAGES ──
    ("",   "Table: captured_images", "", ""),
    ("44", "Image Id",         "Unique image identifier",                    "6001"),
    ("45", "Session Id (FK)",  "References camera_sessions(session_id)",     "5001"),
    ("46", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("47", "Image Data",       "Base64-encoded JPEG frame",                  "/9j/4AAQSkZJRgAB..."),
    ("48", "Captured At",      "Capture timestamp",                          "2026-03-06 09:15:35"),
    ("49", "Trigger",          "MANUAL / FALL_DETECTED / AUTO",             "FALL_DETECTED"),
    # ── SENSOR_READINGS ──
    ("",   "Table: sensor_readings", "", ""),
    ("50", "Reading Id",       "Unique reading identifier",                  "7001"),
    ("51", "User Id (FK)",     "References Users(user_id)",                  "101"),
    ("52", "Accel X",          "Accelerometer X-axis value (m/s²)",          "9.72"),
    ("53", "Accel Y",          "Accelerometer Y-axis value (m/s²)",          "-0.34"),
    ("54", "Accel Z",          "Accelerometer Z-axis value (m/s²)",          "0.21"),
    ("55", "Gyro X",           "Gyroscope X-axis value (°/s)",               "1.02"),
    ("56", "Gyro Y",           "Gyroscope Y-axis value (°/s)",               "-0.55"),
    ("57", "Gyro Z",           "Gyroscope Z-axis value (°/s)",               "0.13"),
    ("58", "Fall Detected",    "Whether sensor triggered a fall alert",      "True"),
    ("59", "Recorded At",      "Timestamp of sensor reading",                "2026-03-06 09:15:30"),
]

# ── layout ────────────────────────────────────────────────────────────
col_widths = [0.07, 0.22, 0.46, 0.25]   # fractions of total width
headers    = ["S.No", "Field Name", "Description", "Sample Data"]
row_height = 0.38   # inches per row
fig_width  = 14
n_rows     = len(rows) + 1  # +1 for header
fig_height = max(n_rows * row_height + 2.0, 12)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_xlim(0, 1)
ax.set_ylim(0, fig_height)
ax.axis('off')
fig.patch.set_facecolor('white')

# Title
ax.text(0.5, fig_height - 0.45,
        "3   DATABASE DESIGN", ha='center', fontsize=14, fontweight='bold')
ax.text(0.5, fig_height - 0.95,
        "3.1  DATA DICTIONARY", ha='center', fontsize=12, fontweight='bold')

# Table top-left x
tx = 0.03
tw = 0.94   # total table width
row_h_norm = row_height / fig_height

def col_x(col_idx):
    return tx + sum(col_widths[:col_idx]) * tw

table_top = fig_height - 1.45
table_top_norm = table_top / fig_height

def draw_row(row_idx, cells, is_header=False, is_section=False):
    y_top = table_top - row_idx * row_height
    y_bot = y_top - row_height
    y_mid = (y_top + y_bot) / 2

    # background
    bg = '#d0d0d0' if is_header else ('#e8e8e8' if is_section else 'white')
    ax.add_patch(plt.Rectangle((tx, y_bot / fig_height),
                                tw, row_height / fig_height,
                                transform=ax.transAxes if False else ax.transData,
                                color=bg, zorder=1))

    # Actually use data coords
    ax.fill_between([tx, tx+tw], [y_bot, y_bot], [y_top, y_top], color=bg, zorder=1)

    # horizontal lines
    lw_h = 1.5 if (is_header or row_idx == 0) else 0.4
    ax.plot([tx, tx+tw], [y_top, y_top], color='black', lw=lw_h, zorder=3)

    # vertical lines + text
    for ci, (text, cw) in enumerate(zip(cells, col_widths)):
        cx = col_x(ci)
        ax.plot([cx, cx], [y_bot, y_top], color='black', lw=0.8, zorder=3)
        # text
        fs  = 9 if is_header else (9 if is_section else 8.5)
        fw  = 'bold' if (is_header or is_section) else 'normal'
        ha  = 'center' if ci == 0 else 'left'
        xoff = 0 if ci == 0 else 0.008 * tw / col_widths[ci]
        ax.text(cx + cw * tw * (0.5 if ci == 0 else 0.02),
                y_mid, text,
                ha=ha, va='center', fontsize=fs, fontweight=fw,
                color='black', zorder=4,
                clip_on=True)

    # last vertical line
    ax.plot([tx+tw, tx+tw], [y_bot, y_top], color='black', lw=0.8, zorder=3)

# Draw header
draw_row(0, headers, is_header=True)

# Draw data rows
for i, row in enumerate(rows):
    sno, field, desc, sample = row
    is_section = (sno == "")
    if is_section:
        # merge all columns for section header
        cells = [field, "", "", ""]
    else:
        cells = [sno, field, desc, sample]
    draw_row(i + 1, cells, is_section=is_section)

# bottom border
y_bot_last = table_top - (len(rows) + 1) * row_height
ax.plot([tx, tx+tw], [y_bot_last, y_bot_last], color='black', lw=1.5)

plt.tight_layout(pad=0.5)
plt.savefig('/Users/saikrithick/Downloads/human_safety_ai/data_dictionary.png',
            dpi=180, bbox_inches='tight', facecolor='white')
print("Data dictionary image saved!")
