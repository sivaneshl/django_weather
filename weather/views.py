from django.shortcuts import render
import requests
from django_weather.secrets import OWN_API_KEY
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    cities = City.objects.all()  # returns all the cities in the database

    if request.method == 'POST':    # only TRUE when the form is submitted
        form = CityForm(request.POST)   # add actual request data to form for processing
        form.save()    # will validate and save if valid

    form = CityForm()

    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city, OWN_API_KEY)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)