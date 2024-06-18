import requests
from bs4 import BeautifulSoup

def get_song_lyrics(song_title, api_token):
    base_url = "https://api.genius.com"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    search_url = base_url + "/search?"
    params = {
        'q': song_title
    }
    response = requests.get(search_url, headers=headers, params=params)
    json_data = response.json()

    song_info = None
    for hit in json_data['response']['hits']:
        if song_title.lower() in hit['result']['title'].lower():
            song_info = hit
            break

    if song_info:
        song_url = song_info['result']['url']
        page = requests.get(song_url)
        html = BeautifulSoup(page.text, "html.parser")
        lyrics = html.find("div", class_="lyrics").get_text() if html.find("div", class_="lyrics") else "Lyrics not found"
        return lyrics
    else:
        return "Lyrics not found"

def SaveLyrics(lyrics, filename):
    with open(filename, "w") as file:
        file.write(lyrics)
    print(f"Lyrics saved to {filename}")

def main():
    song_title = input("Enter the song title: ")
    api_token = "7BUjs-LqTGZ1MxOcoPoSQh9XQ-OGNnwZ9s1_kaTYoTezILHEKfsax7tduZZBNR4N"    # Replace with your actual Genius API token

    lyrics = get_song_lyrics(song_title, api_token)
    SaveLyrics(lyrics, f"{song_title}.txt")

if __name__ == "__main__":
    main()
