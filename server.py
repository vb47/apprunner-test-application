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
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

    # this contains time and sky description
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    # format the data
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    # printing all the data
    str = "Temperature is"+ temp + "Time: " + time + "Sky Description: " + sky
    return Response(str)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(get_weather_data, route_name='hello')
        
        config.add_route('weather', '/weather')
        config.add_view(get_weather_data, route_name='weather')
        
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
