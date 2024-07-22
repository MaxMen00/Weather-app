from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from exchange_app.models import SearchHistory
from api.serializers import SearchHistorySerializer


class SearchHistoryList(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def city_search_stats(request):
    stats = SearchHistory.objects.values('city').annotate(
        count=Count('city')).order_by('-count')
    return Response(stats)
