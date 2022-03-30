from django.urls import path
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info
        (title = 'TRIAL',
        default_version ='v1',
        description = "test description",
        terms_of_service = "http://www.faya.com/policies/terms",
        contact = openapi.Contact(email="thakurj007e@gmail.local"),
        license = openapi.License(name = 'BSD License'),),
    
    public = True,
    permission_classes = (permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout = 0), name = 'schema-swagger-ui'),
    path('redoc/' ,  schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema-redoc'),
    path('categories/' ,  CategoryView.as_view(), name='category'),
    path('products/' ,  ProductAPIView.as_view(), name = 'products'),
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="register"),
    path('email_verify/', VerifyEmail.as_view(), name="email_verify"),
    path('order/', OrderAPIView.as_view(), name="order"),
]