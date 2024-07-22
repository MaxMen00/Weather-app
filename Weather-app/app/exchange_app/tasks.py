from celery import shared_task
from exchange_app.redis_client import redis_client
city_name = 'city_name'

"""Таска запускается при старте Django,
смотрит содержание Redis на наличие таблицы cities,
если таблица существует то задача завершается, если таблицы нет,
то читает из файла города и пушит в Redis"""


@shared_task
def add_cities_to_redis():
    if not redis_client.exists('cities'):
        with open(city_name, 'r') as city:
            cities = []
            for _ in city:
                cities.append(_.rstrip('\n'))

        redis_client.rpush('cities', *cities)
        return 'Cities added to Redis'
    return 'Cities already exist in Redis'
