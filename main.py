import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest


class WeatherRoot(BoxLayout):
    pass


class LocationButton(ListItemButton):
    pass


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
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                     for d in data['list']]
        else:
            cities = []
        self.search_results.item_strings = cities
        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class WeatherApp(App):
    pass


if __name__ == '__main__':
    WeatherApp().run()
