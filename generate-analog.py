import os

from reportlab.lib.colors import black, gray
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# === Configuration ===

# Font file paths (adjust if necessary)
font_dir = "fonts"
inter_regular_path = os.path.join(font_dir, "Inter-Regular.ttf")
inter_bold_path = os.path.join(font_dir, "Inter-Bold.ttf")

# Register fonts
pdfmetrics.registerFont(TTFont("Inter-Regular", inter_regular_path))
pdfmetrics.registerFont(TTFont("Inter-Bold", inter_bold_path))

# Ensure output directories exist
os.makedirs("cards", exist_ok=True)
os.makedirs("sheets", exist_ok=True)

# Layout constants
layout = {
    "card_width": 3 * inch,
    "card_height": 5 * inch,
    "top_margin": 0.3 * inch,
    "left_margin": 0.25 * inch,
    "right_margin": 0.25 * inch,
    "circle_radius": 0.055 * inch,
    "circle_offset": 0.18 * inch,
    "line_spacing": 0.43 * inch,
}

# === Drawing Logic ===


def draw_card_to_canvas(c, title, layout):
    c.setFont("Inter-Bold", 12)
    c.setFillColor(black)

    line_length = (
        layout["card_width"]
        - layout["left_margin"]
        - layout["right_margin"]
        - 0.4 * inch
    )
    c.drawString(
        layout["left_margin"], layout["card_height"] - layout["top_margin"], title
    )

    # Small top-right circles
    small_circle_radius = layout["circle_radius"] / 1.5
    circle_spacing = 0.13 * inch
    circle_x = (
        layout["left_margin"]
        + layout["circle_offset"]
        + layout["circle_radius"]
        + line_length
        + small_circle_radius * 3
    )
    circle_y_top = layout["card_height"] - layout["top_margin"] + 0.12 * inch

    for i in range(3):
        c.circle(circle_x, circle_y_top - i * circle_spacing, small_circle_radius)

    # Date line
    bottom_circle_y = circle_y_top - 2 * circle_spacing
    line_y = bottom_circle_y - small_circle_radius
    line_end_x = (
        layout["left_margin"]
        + layout["circle_offset"]
        + layout["circle_radius"]
        + line_length
    )
    line_start_x = line_end_x - 0.75 * inch
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(line_start_x, line_y, line_end_x, line_y)

    # Task section
    task_start_y = line_y - 0.4 * inch
    for i in range(10):
        y = task_start_y - i * layout["line_spacing"]
        cx = layout["left_margin"] + layout["circle_radius"]
        cy = y + 2

        c.setStrokeColor(black)
        c.circle(cx, cy, layout["circle_radius"])
        c.line(cx, cy - layout["circle_radius"], cx, cy + layout["circle_radius"])

        c.setStrokeColor(gray)
        c.line(
            layout["left_margin"] + layout["circle_offset"] + layout["circle_radius"],
            y,
            layout["left_margin"]
            + layout["circle_offset"]
            + layout["circle_radius"]
            + line_length,
            y,
        )


# === PDF Creation Functions ===


def create_individual_card(title, layout):
    path = f"cards/{title.lower()}_card_3x5.pdf"
    c = canvas.Canvas(path, pagesize=(layout["card_width"], layout["card_height"]))
    draw_card_to_canvas(c, title, layout)
    c.showPage()
    c.save()
    print(f"Saved: {path}")
    return path


def create_4up_sheet(title, layout):
    path = f"sheets/{title.lower()}_4up_letter.pdf"
    letter_width, letter_height = 8.5 * inch, 11 * inch
    c = canvas.Canvas(path, pagesize=(letter_width, letter_height))

    positions = [
        (0.5 * inch, 0.5 * inch),
        (4.5 * inch, 0.5 * inch),
        (0.5 * inch, 5.5 * inch),
        (4.5 * inch, 5.5 * inch),
    ]

    for x, y in positions:
        c.saveState()
        c.translate(x, y)
        draw_card_to_canvas(c, title, layout)
        c.restoreState()

    c.showPage()
    c.save()
    print(f"Saved: {path}")
    return path


# === Execution ===

titles = ["Today", "Next", "Someday"]
for title in titles:
    create_individual_card(title, layout)
    create_4up_sheet(title, layout)
