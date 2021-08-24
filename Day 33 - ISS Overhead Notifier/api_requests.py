import requests
from math import sin, cos, atan2, radians, sqrt
import config


class WebsiteRequests:
    def __init__(self) -> None:
        self.ip_address = self.get_public_ip_address()
        self.lon, self.lat = self.get_location()

    def check_daytime(self) -> tuple:
        """
        Uses https://sunrise-sunset.org/api to return the exact time of nautical dusk and dawn.
        """
        parameters = {"lat": self.lat, "lng": self.lon, "formatted": 0}
        response_sun = requests.get(
            url=" https://api.sunrise-sunset.org/json", params=parameters
        )
        response_sun.raise_for_status()

        night_end = response_sun.json()["results"]["nautical_twilight_begin"]
        night_end_time = night_end.split("T")[1].split(":")
        night_end_hour = int(night_end_time[0])
        night_end_minute = int(night_end_time[1])
        night_end_minutes = night_end_hour * 60 + night_end_minute

        night_begin = response_sun.json()["results"]["nautical_twilight_end"]
        night_begin_time = night_begin.split("T")[1].split(":")
        night_begin_hour = int(night_begin_time[0])
        night_begin_minute = int(night_begin_time[1])
        night_begin_minutes = night_begin_hour * 60 + night_begin_minute

        return night_begin_minutes, night_end_minutes

    def iss_nearby(self) -> tuple:
        """
        Uses http://open-notify.org/Open-Notify-API/ISS-Location-Now/ to determine if ISS is under 5 km away.
        distance analysis shouldn't be in this class but have it's own...
        """
        response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
        response_iss.raise_for_status()
        iss_lon = float(response_iss.json()["iss_position"]["longitude"])
        iss_lat = float(response_iss.json()["iss_position"]["latitude"])
        distance = self.get_distance(iss_lat, iss_lon)
        if distance < 5:
            return True, distance
        else:
            return False, distance

    def weather_is_okay(self) -> bool:
        """
        Uses https://openweathermap.org/api (Current Weather Data) to determine if the sky is clear.
        """
        current_weather = requests.get(
            url=f"http://api.openweathermap.org/data/2.5/weather?lat={self.lat}&"
            f"lon={self.lon}&appid={config.OPENWEATHER_APPID}"
        )
        current_weather.raise_for_status()
        sky_id = current_weather.json()["weather"][0]["id"]
        if 800 <= sky_id <= 803:
            return True
        else:
            return False

    def get_location(self) -> tuple:
        """
        Uses ipapi.co to geththe geo location of your pubic IP address.
        """
        location = requests.get(url=f"https://ipapi.co/{self.ip_address}/json/")
        my_lon = location.json()["longitude"]
        my_lat = location.json()["latitude"]
        return my_lon, my_lat

    def get_distance(self, iss_lat: float, iss_lon: float) -> float:
        """
        Calculates the distance between you and the ISS's projection on the surface of the earth.
        """
        R = 6373  # radius of the earth
        dlon = radians(iss_lon - self.lon)
        dlat = radians(iss_lat - self.lat)
        a = (sin(dlat / 2)) ** 2 + cos(self.lat) * cos(iss_lat) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c  # in km
        print(iss_lon, iss_lat, a, c, d)
        return d

    def get_public_ip_address(self) -> str:
        """
        Uses https://api.ipify.org to return your public IP address.
        """
        return requests.get("https://api.ipify.org").text
