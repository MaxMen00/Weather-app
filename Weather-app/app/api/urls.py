from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import SearchHistoryList, city_search_stats

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search-history/', SearchHistoryList.as_view(),
         name='search-history'),
    path('search-stats/', city_search_stats, name='search-stats')
]
