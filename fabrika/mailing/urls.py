from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'mails', views.MailViewSet,basename="mails")
router.register(r'users', views.UserViewSet,basename="users")
router.register(r'clients', views.ClientViewSet,basename="clients")

urlpatterns = [
    path('', include(router.urls)),
]
#urlpatterns = format_suffix_patterns(urlpatterns)