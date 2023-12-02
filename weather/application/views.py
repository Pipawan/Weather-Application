import datetime
from django.contrib import messages
import requests
from django.shortcuts import render
from rest_framework.decorators import api_view

API_KEY = "48a46c5cb3e524f78629f7640027e54e"

@api_view(['GET', 'POST'])
def Home(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'Pokhara')
    else:
        city = 'Pokhara'

    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    api_key = 'AIzaSyAjKmpX-AlozkXHCYClrk69w1VEZ94hM50'
    SEARCH_ENGINE_ID = '1311d4775e10a40ed'
    query = city + "1920*1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imagesize=xlarge"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        data = requests.get(city_url).json()
        image_url = data.get("items", [{}])[0].get('link', '')

        return render(request, 'application/home.html',
                      {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'exception_occured': False,
                       'image_url': image_url})

    except Exception as e:
        exception_occured = True
        messages.error(request, f"Error: {e}")
        day = datetime.date.today()
        return render(request, 'application/home.html',
                      {'description': '', 'icon': '', 'temp': '', 'day': day, 'exception_occured': True})
