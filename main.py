from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode

def get_url(singer, song):
    base_url = "https://www.vagalume.com.br/"

    singer = unidecode(singer.lower().replace(" ", "-"))
    song = unidecode(song.lower().replace(" ", "-") + '.html')

    return f"{base_url}{singer}/{song}"

def get_song_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao buscar URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    lyrics_div = soup.find("div", {"id": "lyrics"})
    return lyrics_div.get_text(separator=" ", strip=True) if lyrics_div else None

def normalize_song(song):
    song = unidecode(song.lower())
    song = re.sub(r"[^\w\s]", " ", song)
    song = re.sub(r"\s+", " ", song).strip()
    return song

singers_songs = {
    "Titãs": ["Epitáfio", "Enquanto Houver Sol"],
    "Legião Urbana": ["Tempo Perdido", "Será"]
}

with open("corpus.txt", "w", encoding="utf-8") as f:
    for singer, songs in singers_songs.items():
        for song in songs:
            print(f"Baixando {song} de {singer}...")
            url = get_url(singer, song)
            song_lyrics = get_song_html(url)
            if song_lyrics:
                normalized = normalize_song(song_lyrics)
                f.write(f"{singer} - {song}\n")
                f.write(f"{normalized}\n\n")
