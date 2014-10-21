import json
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory
from kivy.uix.modalview import ModalView


__version__ = "0.1"


def locations_args_converter(index, data_item):
    city, country = data_item
    return {'location': (city, country)}


class LocationButton(ListItemButton):
    location = ListProperty()


class WeatherRoot(BoxLayout):

    carousel = ObjectProperty()
#    add_location_form = ObjectProperty()

    def __init__(self, **kargs):
        super(WeatherRoot, self).__init__(**kargs)
        self.store = JsonStore("weather_store.json")
        if self.store.exists('locations'):
            locations = self.store.get('locations')
#            current_location = locations['current_location']
#            self.change_location(current_location)
            for location in locations['locations']:
                self.carousel.add_widget(WeatherPage(location))
            self.carousel.index = 0
#        else:
#            Clock.schedule_once(lambda dt: self.show_add_location_form())

#    def change_location(self, location=None):
#        if location is not None:
#            self.current_weather.location = location
#            if location not in self.locations.locations_list.adapter.data:
#                self.locations.locations_list.adapter.data.append(location)
#                self.locations.locations_list._trigger_reset_populate()
#                self.store.put("locations", locations=list(self.locations.locations_list.adapter.data), current_location=location)
#        self.current_weather.location = location
#        self.forecast.location = location
#        self.current_weather.update_weather()
#        self.forecast.update_weather()
#        self.carousel.load_slide(self.current_weather)
#        if self.add_location_form is not None:
#            self.add_location_form.dismiss()

#    def show_add_location_form(self):
#        self.add_location_form = AddLocationForm()
#        self.add_location_form.open()


class AddLocationForm(ModalView):

    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        search_template = ("http://api.openweathermap.org/data/2.5/" +
                "find?q={}&type=like")
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def search_coordinates(self):
        search_template = ("http://api.openweathermap.org/data/2.5/" +
                           "find?lat={}&lon={}&cnt=10")
        coordinates = self.search_input.text.split(',')
        if len(coordinates) == 2:
            try:
                lat, lon = float(coordinates[0]), float(coordinates[1])
                search_url = search_template.format(lat, lon)
                request = UrlRequest(search_url, self.found_location)
            except ValueError:
                pass

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        if 'list' in data:
            cities = [(d['name'], d['sys']['country'])
                     for d in data['list']]
        else:
            cities = []
        self.search_results.item_strings = cities
        try:
            self.search_results.adapter.data.clear()
        except AttributeError:
            self.search_results.adapter.data = []
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class CurrentWeather(BoxLayout):
    location = ListProperty(['New York', 'US'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
            "weather?q={},{}&units={}")
        weather_url = weather_template.format(self.location[0],
                self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrived)

    def weather_retrived(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']


class WeatherPage(BoxLayout):
    location = ListProperty(['New York', 'US'])
    temp = NumericProperty()
    forecast_panel = ObjectProperty()
    
    def __init__(self, location=None, **kargs):
        super(WeatherPage, self).__init__(**kargs)
        if location is not None:
            self.location = location
        self.update_weather_today()
        self.update_weather_forecast()
        
    def update_weather_today(self):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
            "weather?q={},{}&units={}")
        weather_url = weather_template.format(self.location[0],
                self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrived_today)

    def weather_retrived_today(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
#        self.temp_min = data['main']['temp_min']
#        self.temp_max = data['main']['temp_max']

    def update_weather_forecast(self):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
            "forecast/daily?q={},{}&units={}&cnt=7")
        weather_url = weather_template.format(self.location[0],
            self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrived_forecast)
        
    def weather_retrived_forecast(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.forecast_panel.clear_widgets()
        for day in data['list']:
            box = Factory.ForecastBox()
            box.date = \
                datetime.datetime.fromtimestamp(day['dt']).strftime("%a %b %d")
#            box.conditions = day['weather'][0]['description']
            box.conditions_image = "http://openweathermap.org/img/w/{}.png".format(day['weather'][0]['icon'])
            box.temp_day = day['temp']['day']
#            box.temp_min = day['temp']['min']
#            box.temp_max = day['temp']['max']
            self.forecast_panel.add_widget(box)


class WeatherApp(App):
    def build_config(self, config):
        config.setdefaults('General', {'temp_type': 'Metric'})
        
    def on_pause(self):
        return True

    def build_settings(self, settings):
        settings.add_json_panel("Weather Settings", self.config, data="""
[
    {"type": "options",
     "title": "Temperature System",
     "section": "General",
     "key": "temp_type",
     "options": ["Metric", "Imperial"]}
]""")

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "temp_type":
            try:
                self.root.current_weather.update_weather()
                self.root.forecast.update_weather()
            except AttributeError:
                pass


class Forecast(BoxLayout):
    location = ListProperty(['New York', 'US'])
    forecast_container = ObjectProperty()
    
    def update_weather(self):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
            "forecast/daily?q={},{}&units={}&cnt=3")
        weather_url = weather_template.format(self.location[0],
            self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrived)
        
    def weather_retrived(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.forecast_container.clear_widgets()
        for day in data['list']:
            label = Factory.ForecastLabel()
            label.date = \
                datetime.datetime.fromtimestamp(day['dt']).strftime("%a %b %d")
            label.conditions = day['weather'][0]['description']
            label.conditions_image = "http://openweathermap.org/img/w/{}.png".format(day['weather'][0]['icon'])
            label.temp_min = day['temp']['min']
            label.temp_max = day['temp']['max']
            self.forecast_container.add_widget(label)


if __name__ == '__main__':
    WeatherApp().run()
