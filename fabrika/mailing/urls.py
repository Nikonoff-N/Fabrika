from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'mails', views.MailViewSet,basename="mails")
router.register(r'users', views.UserViewSet,basename="users")
router.register(r'clients', views.ClientViewSet,basename="clients")
#router.register(r'stats', views.MailStats, basename='stats')
urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.MailStats.as_view(), name="stats"),
    path('stats/<int:pk>', views.OneMailStats.as_view(), name="stats")
]
#urlpatterns = format_suffix_patterns(urlpatterns)