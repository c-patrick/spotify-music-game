import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os

# Set your Spotify credentials here or use environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
)


def get_playlist_id(playlist_url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    return match.group(1) if match else None


def clean_track_title(name):
    # Remove anything in parentheses (e.g., "(Remastered 2009)")
    name = re.sub(r"\s*\(.*?\)", "", name)

    # Remove anything after a dash (e.g., "Song Title - Live at ...")
    name = re.sub(r"\s*-\s.*", "", name)

    # Optionally remove "feat." and similar trailing credits
    name = re.sub(r"\s*\b(feat\.?|ft\.?|with)\b.*", "", name, flags=re.IGNORECASE)

    return name.strip()


def get_playlist_tracks(playlist_url):
    playlist_id = get_playlist_id(playlist_url)
    if not playlist_id:
        raise ValueError("Invalid playlist URL")

    tracks = []
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        items = results["items"]
        if not items:
            break

        for item in items:
            track = item["track"]
            if track is None:
                continue

            title = clean_track_title(track["name"])
            artist = track["artists"][0]["name"]
            url = track["external_urls"]["spotify"]
            release_date = track["album"]["release_date"][:4]  # just year

            try:
                year = int(release_date)
            except ValueError:
                continue  # skip if year is missing or malformed

            tracks.append(
                {
                    "title": title,
                    "artist": artist,
                    "url": url,
                    "year": year,
                }
            )

        offset += limit

    # Sort by year, oldest first
    tracks.sort(key=lambda x: x["year"])
    return tracks
