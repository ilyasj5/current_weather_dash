import io

import requests
import tkinter as tk
from PIL import Image, ImageTk

localtime_label = None
temp_label = None
description_label = None
wind_speed_label = None
weather_icon_label = None
be_outside_decision_label = None
suggestion_label = None


def generate_suggestion(description):
    global suggestion_label
    description_lower = description.lower()

    if "rain" in description_lower:
        suggestion_label.config(text=f"Since they are calling for rain, I would suggest bringing an umbrella outside!")
    elif "snow" in description_lower:
        suggestion_label.config(text=f"Since it is snowing today, don't forget your winter gear!")
    elif "cloudy" in description_lower:
        suggestion_label.config(text=f"Clouds out right now, it may rain later!")
    else:
        suggestion_label.config(text=f"No form of precipitation right now, enjoy the weather outside! ")


def get_weather(city, api_key):
    global localtime_label, temp_label, description_label, wind_speed_label, weather_icon_label, be_outside_decision_label,suggestion_label
    base_url = "http://api.weatherstack.com/current?"
    complete_url = f"{base_url}access_key={api_key}&query={city}&units=f"

    response = requests.get(complete_url)
    be_outside_decision = False
    if response.status_code == 200:
        data = response.json()
        if 'error' not in data:
            local_time = data['location']['localtime']
            temp = data['current']['temperature']
            description = data['current']['weather_descriptions'][0]
            wind_speed = data['current']['wind_speed']
            wind_direction = data['current']['wind_dir']
            humidity = data['current']['humidity']
            visibility = data['current']['visibility']
            weather_icon_url = data['current']['weather_icons'][0]
            response = requests.get(weather_icon_url)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((50, 50), Image.LANCZOS)
            weather_icon = ImageTk.PhotoImage(img)
            weather_icon_label.config(image=weather_icon)
            weather_icon_label.image = weather_icon

            if temp > 50 & temp < 90:
                be_outside_decision = True

            if be_outside_decision:
                be_outside_decision_label.config(text=f"Since the current temperature is {temp}°F, it is considered nice out!")
            else:
                be_outside_decision_label.config(text=f"Since the current temperature is: {temp}, it is a bit chilly so if you "
                                                      f"decide to go outside, bundle up!")

            localtime_label.config(text=f"Local Time: {local_time}")
            temp_label.config(text=f"Temperature: {temp} °F")
            description_label.config(text=f"Weather Description: {description.capitalize()}")
            wind_speed_label.config(text=f"Wind Speed: {wind_speed} mph")
            weather_icon_label.config(text=f"Icon: {weather_icon}")
            generate_suggestion(description)
        else:
            print("Error:", data['error']['info'])
    else:
        print(f"Error: Unable to fetch weather data (Status Code: {response.status_code})")
        print("Response:", response.text)


def main():
    global localtime_label, temp_label, description_label, wind_speed_label, weather_icon_label, be_outside_decision_label, suggestion_label

    root = tk.Tk()
    root.title("Weather Dashboard")
    root.geometry("400x400")

    city_frame = tk.Frame(root)
    city_frame.pack(pady=10)

    city_label = tk.Label(city_frame, text="What City?")
    city_label.pack(side="left", padx=(10, 0))

    city_entry = tk.Entry(city_frame)
    city_entry.pack(side="left", padx=10)

    fetch_weather_button = tk.Button(root, text="Get Weather", command=lambda: get_weather(city_entry.get(), api_key))
    fetch_weather_button.pack(pady=10)

    localtime_label = tk.Label(root, text="")
    localtime_label.pack(pady=(10, 0))

    temp_label = tk.Label(root, text="")
    temp_label.pack()

    description_label = tk.Label(root, text="")
    description_label.pack()

    wind_speed_label = tk.Label(root, text="")
    wind_speed_label.pack()

    weather_icon_label = tk.Label(root, text="")
    weather_icon_label.pack()

    be_outside_decision_label = tk.Label(root, text="")
    be_outside_decision_label.pack()

    suggestion_label = tk.Label(root, text="")
    suggestion_label.pack()

    root.mainloop()

if __name__ == "__main__":
    api_key = "041881b7da552016755e237e9c83400e"
    main()




