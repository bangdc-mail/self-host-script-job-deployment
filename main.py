import requests

API_KEY = "[YOUR_OPEN_WEATHER_API_HERE]"  # replace with your OpenWeatherMap API key
CITY = "Hanoi"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather():
    try:

        response = requests.get(URL)
        data = response.json()

        if response.status_code != 200:
            print("Error:", data.get("message", "Failed to fetch weather"))
            return

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        print(f"Weather in {CITY}:")
        print(f"Condition: {weather}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")

    except Exception as e:
        print("Something went wrong:", e)

def get_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        print(data["joke"])
    except Exception as e:
        print("Error fetching joke:", e)

import requests
import random

def get_random_pokemon():
    # As of now, there are ~1025 Pokémon in the API
    pokemon_id = random.randint(1, 1025)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data.")
        return
    
    data = response.json()
    
    name = data["name"].title()
    height = data["height"] / 10  # convert to meters
    weight = data["weight"] / 10  # convert to kg
    types = [t["type"]["name"] for t in data["types"]]
    abilities = [a["ability"]["name"] for a in data["abilities"]]
    
    print(f"Name: {name}")
    print(f"Height: {height} m")
    print(f"Weight: {weight} kg")
    print(f"Types: {', '.join(types)}")
    print(f"Abilities: {', '.join(abilities)}")



if __name__ == "__main__":
    # get_weather()
    # print("here's a random dad joke")
    # get_dad_joke()
    print("This is a test. And a pokemon detail:")
    get_random_pokemon()


