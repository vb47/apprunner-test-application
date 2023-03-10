import requests
from bs4 import BeautifulSoup
import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response




def get_data(request):
    resp = requests.get("https://news.ycombinator.com/")

    txt = ""

    if resp.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        soup=BeautifulSoup(resp.text,'html.parser')
        data = soup.find_all("span", {"class": "titleline"})

        for i in data[0:5]:
            txt = txt + i.text + "\n"
    
    return Response(txt)

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(get_data, route_name='hello')
        
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
