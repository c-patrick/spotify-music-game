from spotify_helper import get_playlist_tracks
from qr_generator import generate_qr_code
from pdf_generator import generate_pdf
import os

# Your playlist URL
PLAYLIST_URL = "{{YOUR_PLAYLIST_URL_HERE}}"

# Output variables
QR_FOLDER = "output/cards"
OUTPUT_PATH = "output/combined_cards/cards.pdf"


if __name__ == "__main__":
    tracks = get_playlist_tracks(PLAYLIST_URL)
    print(f"Fetched {len(tracks)} tracks.")

    # Create output folder for QR code PDFs
    qr_folder = "output/cards"
    os.makedirs(qr_folder, exist_ok=True)

    # Generate vector QR codes as PDF
    for idx, track in enumerate(tracks):
        print(
            f"Generating QR code for track {idx + 1}: {track['title']} - {track['artist']}"
        )
        generate_qr_code(track["url"], idx, output_folder=qr_folder)

    # Generate full cards PDF with vector fronts + embedded QR backs
    generate_pdf(
        tracks=tracks,
        qr_folder=QR_FOLDER,
        output_path=OUTPUT_PATH,
    )

    print(f"PDF with vector cards generated at {OUTPUT_PATH}")
