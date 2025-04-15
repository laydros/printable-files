from reportlab.lib.colors import black, gray
from reportlab.lib.units import inch

# setup font
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register Inter fonts (update the paths if stored elsewhere)
pdfmetrics.registerFont(TTFont("Inter-Regular", "fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "fonts/Inter-Bold.ttf"))


# Output PDF path
today_card_path = "cards/today_card_3x5.pdf"
next_card_path = "cards/next_card_3x5.pdf"
someday_card_path = "cards/someday_card_3x5.pdf"

# Card size
card_width, card_height = 3 * inch, 5 * inch

# Create PDF canvas
c = canvas.Canvas(today_card_path, pagesize=(card_width, card_height))

# Layout constants
top_margin = 0.3 * inch  # reduced from 0.4
left_margin = 0.25 * inch
right_margin = 0.25 * inch
circle_radius = 0.06 * inch
circle_offset = 0.18 * inch
line_spacing = 0.43 * inch
line_length = card_width - left_margin - right_margin - 0.4 * inch

# Title text
c.setFont("Inter-Bold", 12)
# c.setFont("Helvetica-Bold", 12)
c.setFillColor(black)
c.drawString(left_margin, card_height - top_margin, "Today")

# Small top-right indicator circles
small_circle_radius = circle_radius / 1.5
circle_spacing = 0.14 * inch
circle_x_right = (
    left_margin
    + circle_offset
    + circle_radius
    + line_length
    + small_circle_radius * 1.6
)
circle_y_top = card_height - top_margin + 0.12 * inch

for i in range(3):
    c.circle(circle_x_right, circle_y_top - i * circle_spacing, small_circle_radius)

# Draw date line aligned with bottom of the lowest circle, right-aligned with task lines
bottom_circle_y = circle_y_top - 2 * circle_spacing
line_y = bottom_circle_y - small_circle_radius
line_end_x = left_margin + circle_offset + circle_radius + line_length
line_start_x = line_end_x - 0.75 * inch
c.setStrokeColor(black)
c.setLineWidth(1)
c.line(line_start_x, line_y, line_end_x, line_y)

# Vertical spacer between top items and task lines
task_start_y = line_y - 0.35 * inch  # additional vertical buffer

# Draw main checkbox/task lines
for i in range(10):
    y = task_start_y - i * line_spacing
    cx = left_margin + circle_radius
    cy = y + 2

    # Checkbox circle
    c.setStrokeColor(black)
    c.circle(cx, cy, circle_radius)

    # Vertical line inside circle
    c.line(cx, cy - circle_radius, cx, cy + circle_radius)

    # Task line
    c.setStrokeColor(gray)
    c.line(
        left_margin + circle_offset + circle_radius,
        y,
        left_margin + circle_offset + circle_radius + line_length,
        y,
    )

# Finalize and save
c.showPage()
c.save()

print(f"Saved to {today_card_path}")
