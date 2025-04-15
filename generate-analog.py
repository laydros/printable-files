from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, gray

# Output PDF path
output_path = "final_adjusted_today_card_3x5.pdf"

# Card size
card_width, card_height = 3 * inch, 5 * inch

# Create PDF canvas
c = canvas.Canvas(output_path, pagesize=(card_width, card_height))

# Layout constants
top_margin = 0.4 * inch
left_margin = 0.25 * inch
right_margin = 0.25 * inch
circle_radius = 0.06 * inch
circle_offset = 0.18 * inch
line_spacing = 0.43 * inch
line_length = card_width - left_margin - right_margin - 0.4 * inch

# Title text
c.setFont("Helvetica-Bold", 12)
c.setFillColor(black)
c.drawString(left_margin, card_height - top_margin, "Today")

# Small top-right indicator circles
small_circle_radius = circle_radius / 1.5
circle_spacing = 0.14 * inch
# Push them slightly to the right beyond task line end
circle_x_right = left_margin + circle_offset + circle_radius + line_length + small_circle_radius * 1.6
circle_y_top = card_height - top_margin + 0.12 * inch

# Draw 3 small top-right circles
for i in range(3):
    c.circle(circle_x_right, circle_y_top - i * circle_spacing, small_circle_radius)

# Draw "date line" aligned with bottom of lowest small circle and right-aligned with task lines
bottom_circle_y = circle_y_top - 2 * circle_spacing
line_y = bottom_circle_y - small_circle_radius
line_end_x = left_margin + circle_offset + circle_radius + line_length
line_start_x = line_end_x - 0.65 * inch
c.setStrokeColor(black)
c.setLineWidth(1)
c.line(line_start_x, line_y, line_end_x, line_y)

# Draw main checkbox/task lines
for i in range(10):
    y = card_height - top_margin - 0.45 * inch - i * line_spacing
    cx = left_margin + circle_radius
    cy = y + 2

    # Draw circle
    c.setStrokeColor(black)
    c.circle(cx, cy, circle_radius)

    # Vertical line inside circle
    c.line(cx, cy - circle_radius, cx, cy + circle_radius)

    # Task line
    c.setStrokeColor(gray)
    c.line(left_margin + circle_offset + circle_radius, y,
           left_margin + circle_offset + circle_radius + line_length, y)

# Finalize PDF
c.showPage()
c.save()

print(f"Saved to {output_path}")
