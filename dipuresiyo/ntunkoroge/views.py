from rest_framework import generics, status, views
from .serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from drf_yasg.utils import swagger_auto_schema
from .utils import Util
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.decorators import api_view
# from dipuresiyo.gmail import *
    
from django.conf import settings
from django.core.mail import send_mail


# GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
CREATE_USER_URL = "http://127.0.0.1:8000/account/signup"

class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = user.username +' Use link below to verify your email \n' + absurl

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        send_mail(subject=data['email_subject'], message=data['email_body'], from_email='thakurj007e@gmail.com', recipient_list=[data['to_email']])
        return Response(user_data, status=status.HTTP_201_CREATED)
        

class VerifyEmail(views.APIView):
    def get_verified(self , request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id='userid')
            if not user.is_verified:
                user.is_valified = True
                user.save()
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as Identifier :
            return Response({'error':'Activation expired'}, status = status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as Identifier :
            return Response({'error':'Invalid token'}, status = status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     auth_login(self.request, form.get_user())
    #     return HttpResponseRedirect(self.get_success_url())

class CategoryView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    # @swagger_auto_schema(operation_description="description")
    def category_list( request):
        categ = Category.objects.all()
        serialized_categ = CategorySerializer(categ)
        content={'category': serialized_categ}
        return Response( content)




class ProductAPIView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def get(self , request):
        products = Product.objects.all()
        seri = ProductSerializer(products, many=True)
        return Response(seri.data, status=status.HTTP_200_OK)

# @api_view(['GET', 'POST', 'DELETE'])
class OrderAPIView(generics.GenericAPIView):
    def order_details(request):
        order = Order.objects.filter(user = request.user)

        def get(request):
            if request.method == 'POST':
                new_order = Order.objects.filter(user = request.user, order_product = request.data['pro_id'])
                if new_order.exists() == False:
                    p = OrderSerializer(data = {
                        'user' : request.user.username,
                        'order_product': request.data['pro_id']
                    })
                    if p.is_valid():
                        p.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(p.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(request):
            bye_order = Order.objects.filter(user = request.user.id, order_product = request.data['pro_id'])
            if bye_order.exists():
                mumazi = bye_order.first()
                mumazi.delete()
                return Response(status=status.HTTP_200_OK)
        od = OrderSerializer(order, many=True)
        return Response(od.data)