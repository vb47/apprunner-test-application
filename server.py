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

def get_data(request):
    # the target we want to open	
	url='https://www.hindustantimes.com/'
	
	#open with GET method
	resp=requests.get(url)
	
	#http_respone 200 means OK status
	if resp.status_code==200:
		print("Successfully opened the web page")
		print("The news are as follow :-\n")
	
		# we need a parser,Python built-in HTML parser is enough .
		soup=BeautifulSoup(resp.text,'html.parser')	

		# l is the list which contains all the text i.e news
		l=soup.find("h3",{"class":"hdg3"})
	
		#now we want to print only the text part of the anchor.
		#find all the elements of a, i.e anchor
		str = ""
		for i in l.findAll("a"):
			str = str + i.text + " "
		return Response(str)
	else:
		return Response("Error: " + str(resp.status_code))

if __name__ == '__main__':
    port = int(os.environ.get("PORT"))
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(get_data, route_name='hello')
        
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', port, app)
    server.serve_forever()
