import requests

def get_song_lyrics(song_title, api_token):
    base_url = "https://api.genius.com"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    search_url = base_url + "/search"
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
        lyrics_response = requests.get(song_url, headers=headers)
        return lyrics_response.text
    else:
        return "Lyrics not found"

def main():
    song_title = input("Enter the song title: ")
    api_token = "7BUjs-LqTGZ1MxOcoPoSQh9XQ-OGNnwZ9s1_kaTYoTezILHEKfsax7tduZZBNR4N"  # Replace with your actual Genius API token

    lyrics = get_song_lyrics(song_title, api_token)
    print("Lyrics:")
    print(lyrics)

if __name__ == "__main__":
    main()
