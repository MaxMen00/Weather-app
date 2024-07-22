import httpx
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import numpy as np


def get_weather(lat, lon):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": float(lat),
        "longitude": float(lon),
        "hourly": "temperature_2m,weathercode"
    }
    response = openmeteo.weather_api(url, params=params)
    return response[0]


def get_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    response = httpx.get(url)

    data = response.json()
    if data:
        return data[0].get('lat'), data[0].get('lon')
    else:
        return None, None


def weather(city_name):
    lat, lon = get_coordinates(city_name)
    if lat and lon:
        response = get_weather(lat, lon)
        hourly = response.Hourly()
        hourly_temperature_2m = (hourly.Variables(
            0).ValuesAsNumpy()[::6]).astype(np.int32)
        weather_codes = (hourly.Variables(
            1).ValuesAsNumpy()[::6]).astype(np.int32)
        hourly_data = {
            "date": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                                  end=pd.to_datetime(
                                      hourly.TimeEnd(), unit="s", utc=True),
                                  freq=pd.Timedelta(hours=6), inclusive="left")
        }
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["weather_code"] = weather_codes
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe = hourly_dataframe.set_index(
            'date').resample('6h').mean()
        return hourly_dataframe
    else:
        return f"Coordinates for {city_name} not found."

# Функция для преобразования времени в нужный формат


def time_to_str(time):
    time = pd.to_datetime(time)
    day = time.day
    # Конвертируем номер месяца в название
    month = time.strftime("%B").capitalize()
    hour = time.hour
    period_dict = {
        0: "ночь",
        6: "утро",
        12: "день",
        18: "вечер"
    }
    period = period_dict.get(hour % 24 // 6 * 6, "неизвестное время суток")
    return f"{day} {month} {period}"


weather_code_dict = {
    0: "Чистое небо",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Оседающий изморозь",
    51: "Морось: слабая",
    53: "Морось: умеренная",
    55: "Морось: интенсивная",
    56: "Замерзающая морось: слабая",
    57: "Замерзающая морось: плотная интенсивность",
    61: "Дождь: слабый",
    63: "Дождь: умеренный",
    65: "Дождь: сильный",
    66: "Замерзающий дождь: слабой интенсивности",
    67: "Замерзающий дождь: сильной интенсивности",
    71: "Снегопад: слабый",
    73: "Снегопад: умеренный",
    75: "Снегопад: сильный",
    77: "Снежные зерна",
    80: "Ливневые дожди: слабые",
    81: "Ливневые дожди: умеренные",
    82: "Ливневые дожди: сильные",
    85: "Снежные ливни: слабые",
    86: "Снежные ливни: сильные",
    95: "Гроза: слабая или умеренная",
    96: "Гроза с небольшим градом",
    99: "Гроза с сильным градом",
}

images_code = {
    "Чистое небо": 'sun.svg',
    "Преимущественно ясно": 'sun.svg',
    "Переменная облачность": 'partly_cloudy.svg',
    "Пасмурно": 'cloudy.svg',
    "Туман": 'cloudy.svg',
    "Оседающий изморозь": 'NotFound',
    "Морось: слабая": 'NotFound',
    "Морось: умеренная": 'NotFound',
    "Морось: интенсивная": 'NotFound',
    "Замерзающая морось: слабая": 'NotFound',
    "Замерзающая морось: плотная интенсивность": 'NotFound',
    "Дождь: слабый": 'light_rain.svg',
    "Дождь: умеренный": 'heavy_rain.svg',
    "Дождь: сильный": 'heavy_rain.svg',
    "Замерзающий дождь: слабой интенсивности": 'hail.svg',
    "Замерзающий дождь: сильной интенсивности": 'hail.svg',
    "Снегопад: слабый": 'light_snow.svg',
    "Снегопад: умеренный": 'heavy_snow.svg',
    "Снегопад: сильный": 'heavy_snow.svg',
    "Снежные зерна": 'NotFound',
    "Ливневые дожди: слабые": 'heavy_rain.svg',
    "Ливневые дожди: умеренные": 'heavy_rain.svg',
    "Ливневые дожди: сильные": 'heavy_rain.svg',
    "Снежные ливни: слабые": 'NotFound',
    "Снежные ливни: сильные": 'NotFound',
    "Гроза: слабая или умеренная": 'thunderstorm.svg',
    "Гроза с небольшим градом": 'NotFound',
    "Гроза с сильным градом": 'NotFound'
}
# Функция для получения описания кода погоды


def code_to_description(code):
    return weather_code_dict.get(code, "Неизвестный код")


# Словарь перевода месяцев
month_translation = {
    "January": "Января",
    "February": "Февраля",
    "March": "Марта",
    "April": "Апреля",
    "May": "Мая",
    "June": "Июня",
    "July": "Июля",
    "August": "Августа",
    "September": "Сентября",
    "October": "Октября",
    "November": "Ноября",
    "December": "Декабря"
}

# Функция для перевода даты на русский язык


def translate_date(date_str):
    parts = date_str.split()
    day = parts[0]
    month = month_translation.get(parts[1], parts[1])
    return f"{day} {month}"

# Функция для преобразования данных


def convert_data(hourly_dataframe):
    # Применяем функцию преобразования времени к столбцу индекса
    hourly_dataframe.index = hourly_dataframe.index.map(time_to_str)

    # Применяем функцию преобразования кода к столбцу weather_code
    hourly_dataframe['weather_code'] = hourly_dataframe['weather_code'].map(
        code_to_description)

    return hourly_dataframe

# Функция для вычисления средних значений за день для непреобразованных данных


def daily_averages_raw(hourly_dataframe):
    # Преобразуем индекс в datetime, если он не является datetime
    if not pd.api.types.is_datetime64_any_dtype(hourly_dataframe.index):
        hourly_dataframe.index = pd.to_datetime(hourly_dataframe.index)

    # Группируем по дню и вычисляем средние значения для числовых столбцов
    daily_means = hourly_dataframe.groupby(hourly_dataframe.index.date).mean()

    # Для weather_code вычисляем наиболее часто встречающееся значение (мода)
    weather_mode = hourly_dataframe.groupby(hourly_dataframe.index.date)[
        'weather_code'].agg(lambda x: x.mode()[0])

    # Объединяем результаты
    daily_means['weather_code'] = weather_mode
    daily_means['weather_code'] = daily_means['weather_code'].map(
        code_to_description)

    # Переименовываем индекс в нужный формат
    daily_means.index = daily_means.index.map(
        lambda x: translate_date(x.strftime('%d %B')))

    return daily_means


def ret_daily_data(city_name):
    df = weather(city_name)
    daily_df = daily_averages_raw(df)
    daily_data = daily_df.reset_index().to_dict('records')
    for item in daily_data:
        item['weather_icon'] = images_code.get(
            item['weather_code'], 'NotFound')
    return daily_data
