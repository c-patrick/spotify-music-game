import segno
import os


def generate_qr_code(url, index, output_folder="output/cards_back"):
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, f"qr_{index + 1}.pdf")
    qr = segno.make(url)
    qr.save(filename, scale=10, border=1)  # scale controls QR code size
    return filename
