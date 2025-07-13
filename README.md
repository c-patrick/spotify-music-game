# Spotify Music Game

This Python project generates printable game cards from a Spotify playlist. The aim of the game is to guess the year the song was released (bonus points for also guessing the artist and title!), then to prepare a timeline.

Each card displays a song's title, artist, and year on one side, and a scannable Spotify QR code on the other — ready for the DJ to scan.

## Example Card Layout

- **Front:** Song title, artist, release year (with bold box and crop marks).
- **Back:** Centered Spotify QR code (no crop marks).

Cards are arranged 2×5 per A4 page and exported as a PDF with front and back pages aligned for double-sided printing.

---

## Features

- Reads a public Spotify playlist using the Spotify API.
- Extracts track title, artist, and release year.
- Generates vector QR codes for each song.
- Dynamically adjusts font sizes to fit long titles.
- Exports well-aligned front/back printable PDF with crop marks.

---

## Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

You'll need:
* `spotipy`
* `segno`
* `PyMuPDF` (installed as fitz)
* `Pillow`


## Setup

Create a .env file in the project root with your Spotify credentials:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

Replace the `PLAYLIST_URL` in main.py with a public playlist of your choice.

## Usage

Run the generator with:

```
python main.py
```

This will:

1) Fetch tracks from the playlist.
2) Generate QR codes and card images.
3) Build a multi-page vector PDF in output/cards_vector.pdf.

Cards are arranged for double-sided printing (fronts then mirrored backs).

## How to Play

Shuffle the printed cards and try to place songs in chronological order on the table. Flip to scan the QR code and check the correct year. If a player guesses the incorrect year, the opponent can steal the card by correctly guessing the artist, title and placing the card in the right place on the timeline.

## Project Structure
```
spotify-music-game/
├── main.py
├── output
│   ├── cards
│   └── combined_cards
├── pdf_generator.py
├── qr_generator.py
├── README.md
├── requirements.txt
└── spotify_helper.py
```