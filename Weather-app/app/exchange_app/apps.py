from django.apps import AppConfig


class ExchangeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange_app'

    def ready(self):
        from exchange_app.tasks import add_cities_to_redis
        add_cities_to_redis.delay()
