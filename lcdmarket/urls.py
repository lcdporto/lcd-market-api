"""
Url routing
"""

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from lcdmarket.api import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_nested import routers

# setting up api root routes
ROUTER = routers.DefaultRouter()
ROUTER.register(r'accounts', views.AccountViewSet, 'account')
ROUTER.register(r'products', views.ProductViewSet)
ROUTER.register(r'transfers', views.TransferViewSet)

urlpatterns = [
    url(r'^', include(ROUTER.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
