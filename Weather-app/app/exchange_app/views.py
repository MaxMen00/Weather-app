from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from googletrans import Translator

from exchange_app.redis_client import redis_client
from exchange_app.business_logic import ret_daily_data
from exchange_app.models import SearchHistory


translator = Translator()


def exchange(request):
    session_key = request.session.session_key
    if request.method == 'GET':
        if session_key:
            weather_hint_raw = SearchHistory.objects.values('city').filter(
                session_key=session_key).order_by('-timestamp')[0]
            weather_hint = translator.translate(
                weather_hint_raw.get('city'), dest='ru').text
            return render(
                request=request,
                template_name='weather_app/index.html',
                context={'weather_hint': weather_hint,
                         'weather_hint_raw': weather_hint_raw.get('city'),
                         'modal_window_key': True}
            )
        return render(request=request, template_name='weather_app/index.html')

    if request.method == 'POST':
        city_raw = str(request.POST.get('city'))
        city = translator.translate(city_raw, dest='en').text
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        SearchHistory.objects.create(session_key=session_key, city=city)

        return redirect(reverse('weather:weather_list', args=[city]))


def city_autocomplete(request):
    query = request.GET.get('query', '').lower()
    if not query:
        return JsonResponse([], safe=False)

    cities = redis_client.lrange('cities', 0, -1)
    filtered_cities = [city for city in cities if query in city.lower()]
    return JsonResponse(filtered_cities, safe=False)


def weather_list(request, city):
    weather_data = ret_daily_data(city)
    city_rus = translator.translate(city, dest='ru').text
    context = {'weather_list': weather_data,
               'city': city, 'city_rus': city_rus}
    return render(request=request,
                  template_name='weather_app/list.html', context=context)
