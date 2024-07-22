from rest_framework import serializers
from exchange_app.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['session_key', 'city', 'timestamp']
