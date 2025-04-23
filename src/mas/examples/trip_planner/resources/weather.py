"""Weather resource"""

from pydantic import BaseModel

from mas.base_resource import BaseResource


class WeatherResource(BaseResource):
    """Weather resource for storing weather data."""

    # weather data
    class WeatherData(BaseModel):
        """Class to hold weather data."""

        latitude: float
        longitude: float
        date: str
        time: str
        temperature: str
        rain_chance: str
        precipitation_amount: str
        wind_speed: str

    def __init__(self, weather_data: WeatherData):
        """
        Initialise the WeatherResource with weather data.

        Args:
            weather_data (WeatherData): The weather data to be represented by the resource.
        """
        super().__init__(weather_data)
        self.weather_data = weather_data

    @staticmethod
    def get_model_type() -> type[WeatherData]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return WeatherResource.WeatherData
