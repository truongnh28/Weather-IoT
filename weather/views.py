import requests
from django.shortcuts import render, redirect, get_object_or_404

from weather.forms import CityForm
from weather.models import City


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&lang={}&appid=3ef0842e0135e59e9325f8aea275151d'
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        name = city.name
        language = city.language.id
        unit = city.unit.id
        symbol = city.unit.symbol
        city_weather = requests.get(url.format(name, unit, language)).json()
        weather = {
            'city': name,
            'temperature': city_weather['main']['temp'],
            'unit': symbol,
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)

    message = ''
    message_class = ''

    if ('message' in request.session) and ('message_class' in request.session):
        message = request.session['message']
        message_class = request.session['message_class']
        request.session.clear()

    form = CityForm(initial={
        'language': 'en',
        'unit': 'standard'
    })
    context = {
        'form': form,
        'weather_data': weather_data,
    }

    if message and message_class:
        context['message'] = message
        context['message_class'] = message_class

    return render(request, 'weather/index.html', context)


def add(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&lang={}&appid=3ef0842e0135e59e9325f8aea275151d'
    form = CityForm(request.POST)
    err_msg = ''
    if form.is_valid():
        new_city = form.cleaned_data['name']
        language_id = form.cleaned_data['language'].id
        unit_id = form.cleaned_data['unit'].id
        existing_city_count = City.objects.filter(name=new_city).count()
        if existing_city_count == 0:
            r = requests.get(url.format(new_city, unit_id, language_id)).json()
            if r['cod'] == 200:
                form.save()
            else:
                err_msg = "City doesn't exist"

        else:
            err_msg = "City already exist in database"

    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = "City added successfully!"
        message_class = 'is-success'

    request.session["message"] = message
    request.session["message_class"] = message_class
    return redirect('index')


def delete(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')

