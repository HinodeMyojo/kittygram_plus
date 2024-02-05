from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from cats.views import CatViewSet


router = DefaultRouter()
router.register('cats', CatViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]