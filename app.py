
import streamlit as st
import requests

st.set_page_config(
    page_title="Live Weather Dashboard",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Live Weather Dashboard")
st.write("Get current weather conditions for any city.")

city = st.text_input("Enter a city name", "Hyderabad")

if st.button("Get Weather"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        try:
            # Find the city's coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_response = requests.get(
                geo_url,
                params={"name": city, "count": 1, "language": "en"},
                timeout=10
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data.get("results"):
                st.error("City not found. Try another city.")
            else:
                place = geo_data["results"][0]
                latitude = place["latitude"]
                longitude = place["longitude"]

                # Get current weather
                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_response = requests.get(
                    weather_url,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": (
                            "temperature_2m,"
                            "relative_humidity_2m,"
                            "apparent_temperature,"
                            "wind_speed_10m,"
                            "weather_code"
                        ),
                        "timezone": "auto"
                    },
                    timeout=10
                )
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                current = weather_data["current"]

                st.subheader(
                    f"📍 {place['name']}, "
                    f"{place.get('country', '')}"
                )
                st.caption(
                    f"Updated: {current['time'].replace('T', ' ')}"
                )

                col1, col2 = st.columns(2)
                col1.metric(
                    "Temperature",
                    f"{current['temperature_2m']} °C"
                )
                col2.metric(
                    "Feels Like",
                    f"{current['apparent_temperature']} °C"
                )

                col3, col4 = st.columns(2)
                col3.metric(
                    "Humidity",
                    f"{current['relative_humidity_2m']}%"
                )
                col4.metric(
                    "Wind Speed",
                    f"{current['wind_speed_10m']} km/h"
                )

                st.info(
                    "Weather code: "
                    + str(current["weather_code"])
                )

        except requests.RequestException:
            st.error(
                "Could not fetch weather data. "
                "Please check your connection and try again."
            )
        except (KeyError, ValueError, IndexError):
            st.error("Unexpected weather data received.")
