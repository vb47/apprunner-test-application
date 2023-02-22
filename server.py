from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import requests
from bs4 import BeautifulSoup
import os

def hello_world(request):
    name = os.environ.get('NAME')
    if name == None or len(name) == 0:
        name = "world"
    message = "Hello, " + name + "!\n"
    return Response(message)

def get_weather_data(request):
    # enter city name
    city = "lucknow"

    # create url
    url = "https://www.google.com/search?q="+"weather"+city

    # requests instance
    html = requests.get(url).content

    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    
    # get the temperature
    temp = soup.find('span', attrs={'id': 'wob_tm'}).text
    str = "Temperature is"+ temp
    return Response(str)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(get_weather_data, route_name='hello')
        
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
