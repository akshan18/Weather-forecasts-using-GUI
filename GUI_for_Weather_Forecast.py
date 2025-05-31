from tkinter import *
from tkinter import messagebox
import requests
import json
import datetime
from PIL import ImageTk, Image
import os

# === API Key ===
api_key = "30046e1cc9370831a4aec77039cc2854"
#api_key = "enter_your_api_key"

# === Setup Window ===
root = Tk()
root.title("Weather App")
root.geometry("450x720")
root.config(bg="white")

# === Load Local Images ===
script_dir = os.path.dirname(__file__)
logo_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "logo.png")).resize((450, 160)))
sun_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "sun.png")).resize((100, 100)))
moon_img = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "moon.png")).resize((100, 100)))

# === Logo Display ===
logo_label = Label(root, image=logo_img, bg="white")
logo_label.place(x=0, y=550)

# === Date & Time ===
dt = datetime.datetime.now()
Label(root, text=dt.strftime('%A--'), bg='white', font=("bold", 15)).place(x=10, y=130)
Label(root, text=dt.strftime('%d %B'), bg='white', font=("bold", 15)).place(x=130, y=130)
Label(root, text=dt.strftime('%I : %M %p'), bg='white', font=("bold", 15)).place(x=10, y=160)

# === Time-based Theme (Sun/Moon) ===
hour_now = dt.hour
icon_label = Label(root, bg="white")
if 18 <= hour_now or hour_now < 6:
    icon_label.config(image=moon_img)
    icon_label.image = moon_img
else:
    icon_label.config(image=sun_img)
    icon_label.image = sun_img
icon_label.place(x=320, y=130)

# === Input Field ===
city_var = StringVar()
city_entry = Entry(root, textvariable=city_var, font=("Arial", 12))
city_entry.grid(row=0, column=0, columnspan=2, ipadx=30, ipady=10, pady=10, padx=10, sticky=W+E)

# === Search Button ===
Button(root, text="Search", font=("Arial", 10, "bold"), command=lambda: fetch_weather()).grid(row=0, column=2, padx=10)

# === Labels ===
lable_citi = Label(root, text="City", bg='white', font=("bold", 16))
lable_citi.place(x=10, y=60)

lable_country = Label(root, text="Country", bg='white', font=("bold", 16))
lable_country.place(x=135, y=60)

lable_lon = Label(root, text="Longitude", bg='white', font=("Helvetica", 12))
lable_lon.place(x=25, y=95)

lable_lat = Label(root, text="Latitude", bg='white', font=("Helvetica", 12))
lable_lat.place(x=150, y=95)

lable_temp = Label(root, text="...", bg='white', font=("Helvetica", 90), fg='black')
lable_temp.place(x=50, y=200)

weather_desc = Label(root, text="", bg="white", font=("Arial", 16, "italic"))
weather_desc.place(x=10, y=320)

weather_icon_label = Label(root, bg="white")
weather_icon_label.place(x=280, y=210)

Label(root, text="Humidity:", bg='white', font=("bold", 14)).place(x=10, y=370)
lable_humidity = Label(root, text="...", bg='white', font=("bold", 14))
lable_humidity.place(x=120, y=370)

Label(root, text="Max Temp:", bg='white', font=("bold", 14)).place(x=10, y=400)
max_temp = Label(root, text="...", bg='white', font=("bold", 14))
max_temp.place(x=120, y=400)

Label(root, text="Min Temp:", bg='white', font=("bold", 14)).place(x=10, y=430)
min_temp = Label(root, text="...", bg='white', font=("bold", 14))
min_temp.place(x=120, y=430)

note = Label(root, text="All temperatures in degree celsius", bg='white', font=("italic", 10))
note.place(x=95, y=510)

# === Fetch Weather Function ===
def fetch_weather():
    city = city_var.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url)
        api = response.json()
        print(json.dumps(api, indent=4))  # DEBUG: Print API response

        if response.status_code != 200 or "main" not in api:
            raise Exception(api.get("message", "City not found or API error"))

        # Weather Info
        weather = api['weather'][0]
        y = api['main']
        x = api['coord']
        z = api['sys']

        # Update GUI
        lable_citi.config(text=api['name'])
        lable_country.config(text=z['country'])
        lable_lon.config(text=f"Lon: {x['lon']}")
        lable_lat.config(text=f"Lat: {x['lat']}")
        lable_temp.config(text=f"{y['temp']}°")
        lable_humidity.config(text=f"{y['humidity']}%")
        max_temp.config(text=f"{y['temp_max']}°")
        min_temp.config(text=f"{y['temp_min']}°")
        weather_desc.config(text=weather['description'].title())

        # Weather Icon from OpenWeatherMap
        icon_code = weather['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url, stream=True).raw
        icon_img = Image.open(icon_data)
        icon_tk = ImageTk.PhotoImage(icon_img)
        weather_icon_label.config(image=icon_tk)
        weather_icon_label.image = icon_tk

        messagebox.showinfo("Success", f"Weather data for {city} loaded.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        weather_desc.config(text="❌ Failed to fetch data")
        lable_temp.config(text="...")
        weather_icon_label.config(image="")
        weather_icon_label.image = None

# === Main Loop ===
root.mainloop()
