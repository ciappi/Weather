import json
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import (ObjectProperty, ListProperty,
                             StringProperty, NumericProperty)
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory
from kivy.uix.popup import Popup


__version__ = "0.2dev"


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
        self.locations = {}
        self.store = JsonStore("weather_store.json")
        if self.store.exists('locations'):
            locations = self.store.get('locations')
            for location in locations['locations']:
                location = tuple(location)
                self.locations[location] = WeatherPage(location)
                self.carousel.add_widget(self.locations[location])
            current_location = tuple(locations['current_location'])
            self.carousel.load_slide(self.locations[current_location])
        else:
            Clock.schedule_once(lambda dt: self.show_add_location_form())

    def update_weather(self):
        for location in self.locations:
            self.locations[location].update_weather()

    def remove_location(self, location=None):
        if location is None:
            location = self.carousel.current_slide.location
        location = tuple(location)
        if location in self.locations:
#            if self.carousel.previous_slide is None:
#                self.carousel.load_next()
#            else:
#                self.carousel.load_previous()
            self.carousel.remove_widget(self.locations.pop(location))

    def add_location(self, location=None):
        location = tuple(location)
        if location is not None:
            if location not in self.locations:
                self.locations[location] = WeatherPage(location)
                self.carousel.add_widget(self.locations[location])
                self.store.put("locations",
                               locations=list(self.locations.keys()),
                               current_location=location)
        self.carousel.load_slide(self.locations[location])
        if self.add_location_form is not None:
            self.add_location_form.dismiss()

    def show_add_location_form(self):
        self.add_location_form = Popup(title="Add Location...",
                                       size_hint=(.8, .6),
                                       content=AddLocationForm())
        self.add_location_form.open()


class AddLocationForm(BoxLayout):

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


class WeatherPage(BoxLayout):
    location = ListProperty(['New York', 'US'])
    temp = NumericProperty()
    forecast_panel = ObjectProperty()
    condition_image = StringProperty()
    conditions = StringProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    humidity = NumericProperty()
    pressure = NumericProperty()

    def __init__(self, location=None, **kargs):
        super(WeatherPage, self).__init__(**kargs)
        if location is not None:
            self.location = location
        self.update_weather()

    def update_weather(self):
        self.update_weather_today()
        self.update_weather_forecast()

    def update_weather_today(self):
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
                            "weather?q={},{}&units={}")
        weather_url = weather_template.format(self.location[0],
                                              self.location[1], 'metric')
        request = UrlRequest(weather_url, self.weather_retrived_today)

    def weather_retrived_today(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        conditions = data['weather'][0]['description']
        self.conditions = conditions[0].upper() + conditions[1:].lower()
        self.temp = data['main']['temp']
        self.condition_image = "http://openweathermap.org/img/w/{}.png".format(data['weather'][0]['icon'])
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.humidity = data['main']['humidity']
        self.pressure = data['main']['pressure']

    def update_weather_forecast(self):
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
                            "forecast/daily?q={},{}&units={}&cnt=7")
        weather_url = weather_template.format(self.location[0],
                                              self.location[1], 'metric')
        request = UrlRequest(weather_url, self.weather_retrived_forecast)

    def weather_retrived_forecast(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.forecast_panel.clear_widgets()
        for day in data['list']:
            box = Factory.ForecastBox()
            box.date = \
                datetime.datetime.fromtimestamp(day['dt']).strftime("%a %b %d")
            box.conditions_image = "http://openweathermap.org/img/w/{}.png".format(day['weather'][0]['icon'])
            box.temp_min = day['temp']['min']
            box.temp_max = day['temp']['max']
            self.forecast_panel.add_widget(box)


class Forecast(BoxLayout):
    location = ListProperty(['New York', 'US'])
    forecast_container = ObjectProperty()

    def update_weather(self):
        weather_template = ("http://api.openweathermap.org/data/2.5/" +
                            "forecast/daily?q={},{}&units={}&cnt=3")
        weather_url = weather_template.format(self.location[0],
                                              self.location[1], 'metric')
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


class WeatherApp(App):

    def build(self):
        self.icon = "imgs/icon.png"

    def on_pause(self):
        return True

    def open_settings(self, *largs):
        pass

    def on_stop(self):
        self.root.store.put("locations",
                            locations=list(self.root.locations.keys()),
                            current_location=self.root.carousel.current_slide.location)


if __name__ == '__main__':
    WeatherApp().run()
