from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
# Create your views here.
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        # default city
        city = "Kanpur"
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=93f6e53ce30ab47dd002844358975e1d'
    PARAMS = {'units':'metric'}

    # Make a request to the Unsplash API to get city images
    unsplash_access_key = 'fvmd0kWtqAo3ot5IAnEQCrhDdNgIPsrMO1uURubIXx4'
    endpoint = f'https://api.unsplash.com/search/photos'
    params = {
        'query': city,
        'client_id': 'fvmd0kWtqAo3ot5IAnEQCrhDdNgIPsrMO1uURubIXx4',
    }

    data = requests.get(endpoint, params=params).json()

    # Extract image URLs from the API response
    image_urls = []
    for photo in data['results']:
        image_urls.append(photo['urls']['raw'])
    if len(image_urls) == 0:    
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
    elif len(image_urls) > 0:
        image_url = image_urls[0]
    
    try: 
        data = requests.get(url,params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        Temperature = data['main']['temp']
        humidity = data['main']['humidity'] 

        date = datetime.date.today()
        context = {
            'description': description,
            'icon' : icon,
            'temperature' : Temperature,
            'humidity' : humidity,
            'date' : date,
            'city' : city,
            'exception_occured' : False,
            'image_url' : image_url
        }

        return render(request, 'index.html', context = context)
    except:
        exception_occured = True
        messages.error(request, "Entered City is not Available")
        date = datetime.date.today()
        context = {
            'description': 'N/A',
            'icon' : '01d',
            'temperature' : 'N/A',
            'humidity' : 'N/A',
            'date' : date,
            'city' : city,
            'exception_occured' : True,
            'image_url' : image_url
        }

        return render(request, 'index.html', context = context)
