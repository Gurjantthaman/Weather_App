from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API key (replace with your own API key)
API_KEY = "2b6ca8a7ac342cfbfd622209e101eba2"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            # Making the API request
            complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
            response = requests.get(complete_url)
            data = response.json()

            if data["cod"] == "404":
                error_message = "City not found! Please try again."
            else:
                main = data["main"]
                weather_data = {
                    "city": city,
                    "temperature": main["temp"],
                    "pressure": main["pressure"],
                    "humidity": main["humidity"],
                    "description": data["weather"][0]["description"],
                }
                weather = weather_data
        else:
            error_message = "Please enter a city name."

    return render_template("weather.html", weather=weather, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
