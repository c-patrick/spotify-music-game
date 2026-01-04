from spotify_helper import get_playlist_tracks
from qr_generator import generate_qr_code
from pdf_generator import generate_pdf
import os

# import json

# Prompt the user for the playlist URL at runtime
PLAYLIST_URL = input("Enter Spotify playlist URL: ").strip()

if not PLAYLIST_URL:
    raise SystemExit("No playlist URL provided. Exiting.")

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

    # Create output folder for combined PDF
    combined_folder = "output/combined_cards"
    os.makedirs(combined_folder, exist_ok=True)

    # Generate full cards PDF with vector fronts + embedded QR backs
    generate_pdf(
        tracks=tracks,
        qr_folder=QR_FOLDER,
        output_path=OUTPUT_PATH,
    )

    # print(json.dumps(tracks[0], indent=2)) # For debugging, example track data:
    # {
    #     "title": "Ain't No Mountain High Enough",
    #     "artist": "Marvin Gaye",
    #     "url": "https://open.spotify.com/track/7tqhbajSfrz2F7E1Z75ASX",
    #     "year": 1967
    # }

    print(f"PDF with vector cards generated at {OUTPUT_PATH}")
