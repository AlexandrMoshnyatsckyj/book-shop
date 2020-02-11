from django.urls import path, include


urlpatterns = [
    path('api/', include('book_shop.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
