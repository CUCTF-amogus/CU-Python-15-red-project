from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


@dataclass
class Api:
    api_key: str
    location_url: str
    weather_url: str


@dataclass
class Config:
    api: Api


def load_config() -> Config:
    load_dotenv()

    return Config(
        api=Api(
        api_key=getenv("API_KEY"),
            location_url=getenv("LOCATION_URL"),
            weather_url=getenv("WEATHER_URL"),
        ),
    )


config: Config = load_config()
