from django.urls import include, path
from rest_framework import routers

from book_shop.views import AuthorView, BookView, OrderView, PublisherView

router = routers.DefaultRouter()
router.register('author', AuthorView)
router.register('publisher', PublisherView)
router.register('book', BookView)
router.register('order', OrderView)


urlpatterns = [
    path('', include(router.urls)),
]
