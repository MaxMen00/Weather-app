import redis
from django.conf import settings
"""Подключение к Reddis"""
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    db=0
)
