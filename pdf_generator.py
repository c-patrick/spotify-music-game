import fitz  # PyMuPDF
import os

PAGE_WIDTH = 595  # points, A4 width
PAGE_HEIGHT = 842  # points, A4 height

CARDS_PER_ROW = 2
CARDS_PER_COL = 5
CARDS_PER_PAGE = CARDS_PER_ROW * CARDS_PER_COL

CARD_WIDTH_PT = 270
CARD_HEIGHT_PT = 140

CARD_H_SPACING = 10
CARD_V_SPACING = 10

CROP_MARK_LEN = 10


def draw_crop_marks(page, x, y, w, h, color=(0.7, 0.7, 0.7), width=0.5):
    # Top-left
    page.draw_line((x - CROP_MARK_LEN, y), (x, y), color=color, width=width)
    page.draw_line((x, y - CROP_MARK_LEN), (x, y), color=color, width=width)
    # Top-right
    page.draw_line((x + w + CROP_MARK_LEN, y), (x + w, y), color=color, width=width)
    page.draw_line((x + w, y - CROP_MARK_LEN), (x + w, y), color=color, width=width)
    # Bottom-left
    page.draw_line((x - CROP_MARK_LEN, y + h), (x, y + h), color=color, width=width)
    page.draw_line((x, y + h + CROP_MARK_LEN), (x, y + h), color=color, width=width)
    # Bottom-right
    page.draw_line(
        (x + w + CROP_MARK_LEN, y + h), (x + w, y + h), color=color, width=width
    )
    page.draw_line(
        (x + w, y + h + CROP_MARK_LEN), (x + w, y + h), color=color, width=width
    )


def draw_card_front(page, x, y, card_data, card_num):
    crop_len = 10
    crop_color = (0.7, 0.7, 0.7)  # light grey
    crop_width = 0.5

    # Draw crop marks
    draw_crop_marks(
        page, x, y, CARD_WIDTH_PT, CARD_HEIGHT_PT, color=crop_color, width=crop_width
    )

    fontname = "helv"
    font = fitz.Font(fontname=fontname)

    # === 1. Draw YEAR box at top center ===
    year_text = str(card_data["year"])
    year_fontsize = 18
    box_padding_x = 8
    box_padding_y = 4

    font = fitz.Font(fontname="helv")

    text_width = font.text_length(year_text, year_fontsize)
    box_width = text_width + 2 * box_padding_x
    box_height = year_fontsize + 2 * box_padding_y

    box_x = x + (CARD_WIDTH_PT - box_width) / 2
    box_y = y + 15
    box_rect = fitz.Rect(box_x, box_y, box_x + box_width, box_y + box_height)

    page.draw_rect(box_rect, color=(0, 0, 0), fill=None, width=0.7)

    ascent = font.ascender / 1000 * year_fontsize
    descender = font.descender / 1000 * year_fontsize  # negative
    total_height = ascent - descender

    text_x = box_rect.x0 + (box_width - text_width) / 2
    text_y = box_rect.y0 + (box_height + year_fontsize) / 2 - 2

    page.insert_text(
        (text_x, text_y),
        year_text,
        fontsize=year_fontsize,
        fontname="helv",
        color=(0, 0, 0),
    )

    # === 2. Draw Title and Artist below year ===
    base_fontsize = 18
    min_fontsize = 8
    max_text_width = CARD_WIDTH_PT - 30  # 15pt padding

    title = card_data["title"]
    artist = card_data["artist"]

    fontsize = base_fontsize
    while fontsize >= min_fontsize:
        if font.text_length(title, fontsize) <= max_text_width:
            break
        fontsize -= 1

    content_y = box_y + box_height + 20

    title_width = font.text_length(title, fontsize)
    title_x = x + (CARD_WIDTH_PT - title_width) / 2
    page.insert_text(
        (title_x, content_y),
        title,
        fontsize=fontsize,
        fontname=fontname,
        color=(0, 0, 0),
    )

    artist_fontsize = 12
    artist_width = font.text_length(artist, artist_fontsize)
    artist_x = x + (CARD_WIDTH_PT - artist_width) / 2
    page.insert_text(
        (artist_x, content_y + 28),
        artist,
        fontsize=artist_fontsize,
        fontname=fontname,
        color=(0, 0, 0),
    )

    # === 3. Card number at bottom right ===
    card_num_fontsize = 12
    card_num_text = f"#{card_num}"
    card_num_width = font.text_length(card_num_text, card_num_fontsize)

    card_num_x = x + CARD_WIDTH_PT - 15 - card_num_width
    card_num_y = y + CARD_HEIGHT_PT - 15

    page.insert_text(
        (card_num_x, card_num_y),
        card_num_text,
        fontsize=card_num_fontsize,
        fontname=fontname,
        color=(0.5, 0.5, 0.5),
    )


def draw_card_back(page, x, y, qr_pdf_path):
    qr_doc = fitz.open(qr_pdf_path)
    qr_page = qr_doc.load_page(0)

    qr_height = CARD_HEIGHT_PT * 0.8
    qr_width = qr_height  # square

    qr_x = x + (CARD_WIDTH_PT - qr_width) / 2
    qr_y = y + (CARD_HEIGHT_PT - qr_height) / 2

    page.show_pdf_page(
        fitz.Rect(qr_x, qr_y, qr_x + qr_width, qr_y + qr_height), qr_doc, 0
    )

    qr_doc.close()


def generate_pdf(tracks, qr_folder, output_path):
    doc = fitz.open()

    total_cards = len(tracks)

    total_width = CARDS_PER_ROW * CARD_WIDTH_PT + (CARDS_PER_ROW - 1) * CARD_H_SPACING
    total_height = CARDS_PER_COL * CARD_HEIGHT_PT + (CARDS_PER_COL - 1) * CARD_V_SPACING

    margin_x = (PAGE_WIDTH - total_width) / 2
    margin_y = (PAGE_HEIGHT - total_height) / 2

    for i in range(0, total_cards, CARDS_PER_PAGE):
        fronts = tracks[i : i + CARDS_PER_PAGE]
        backs = [
            os.path.join(qr_folder, f"qr_{i + idx + 1}.pdf")
            for idx in range(len(fronts))
        ]

        # Front page
        front_page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        for idx, track in enumerate(fronts):
            row = idx // CARDS_PER_ROW
            col = idx % CARDS_PER_ROW
            x = margin_x + col * (CARD_WIDTH_PT + CARD_H_SPACING)
            y = margin_y + row * (CARD_HEIGHT_PT + CARD_V_SPACING)
            draw_card_front(front_page, x, y, track, i + idx + 1)
            draw_crop_marks(
                front_page,
                x,
                y,
                CARD_WIDTH_PT,
                CARD_HEIGHT_PT,
                color=(0.7, 0.7, 0.7),
                width=0.5,
            )

        # Back page (mirrored horizontally)
        back_page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        for idx, qr_path in enumerate(backs):
            row = idx // CARDS_PER_ROW
            col = CARDS_PER_ROW - 1 - (idx % CARDS_PER_ROW)  # horizontal mirror
            x = margin_x + col * (CARD_WIDTH_PT + CARD_H_SPACING)
            y = margin_y + row * (CARD_HEIGHT_PT + CARD_V_SPACING)
            draw_card_back(back_page, x, y, qr_path)

    doc.save(output_path)
    print(f"Saved PDF to {output_path}")
