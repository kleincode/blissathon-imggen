import requests
import json
from imagen2.gen_img import gen_img
from gemini.ask_gemini import ask_gemini
import random

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYjdlZjNhNThiYWEwZmIzZTUwYjYyMGYyOTMyZjRkZCIsInN1YiI6IjY2NTA2MmQxMjExNzQ3MDM5YzBhNmY5ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.b8QUETEl3f5oFskPLLP2T0D9sGB4Zac7aaYabYUblE8"
}

possible_movies = []

for year in range(2010, 2025):
    response = requests.request("GET", f"https://api.themoviedb.org/3/discover/movie?primary_release_year={year}&vote_average.gte=8&vote_count.gte=400", headers=headers)

    movies = json.loads(response.text)["results"]

    movies.sort(key=lambda x: x["vote_average"], reverse=True)
    movies = list(filter(lambda x: x["original_language"] in ["de", "en"], movies))
    possible_movies.extend(movies)

print("loaded ", len(possible_movies), "movies")

success = False

while not success:
    movie = random.choice(possible_movies)
    title = movie["original_title"]
    description = movie["overview"]
    prompt = ask_gemini("Describe an imaginary film poster. The poster should include the title of the film in big letters. :\nTitle: " + title +"\nDescription: " + description)
    success = gen_img(prompt, 4)