import json

from src.api.accuweather_api import AccuWeatherAPI


class Weather:
    def __init__(self):
        self.cached_data = {}
        self.data_path = "data/"

        self.api = AccuWeatherAPI()

        self.load_cached_data("weather.json")
    
    def load_cached_data(self, file_name: str):
        file_path = self.data_path + file_name
        print(file_path)
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
            # setting new value if it didn't exist before 
            for index, value in data.items():
                if index not in self.cached_data.keys():
                    self.cached_data[index] = value

    def write_cached_data(self, file_name: str):
        file_path = self.data_path + file_name
        with open(file_path, 'w') as file:
            json.dump(self.cached_data, file)

    def get_weather(self, city_name: str):
        city_name = city_name.lower().strip()
        if city_name in self.cached_data.keys():
            return self.cached_data[city_name]
        
        response_data = self.api.get_weather(city_name)

        weather_data = {
            "temperature": response_data["Temperature"]["Metric"]["Value"],
            "wind": response_data["Wind"]["Speed"]["Metric"]["Value"],
        }

        if 0 < weather_data["temperature"] < 35 and weather_data["wind"] < 30:
            weather_data["text"] = f"Good weather - {response_data["WeatherText"]}"
        else:
            weather_data["text"] = f"Bad weather - {response_data["WeatherText"]}"

        self.cached_data[city_name] = weather_data
        self.write_cached_data("weather.json") # да я знаю что не надо много вызывать запись в файл, но у нас тут кол-во запросов ограничено так что мне лень придумывать систему лучше

        return weather_data


weather = Weather()
