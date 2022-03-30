from xml.etree.ElementInclude import include
from . import views
from django.urls import path


urlpatterns = [
    path('login_user', views.login_user, name="login")
]
  