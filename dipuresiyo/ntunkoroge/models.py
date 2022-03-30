from tabnanny import verbose
from unicodedata import category
from venv import create
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh_token.refresh),
            'access':str(refresh_token.access_token)
        }

class Category(models.Model):
    name = models.CharField(max_length = 255, db_index = True, null = False)
    slug = models.SlugField(max_length = 255, unique = True, null=True)
    description = models.TextField(max_length = 255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name        

class Product(models.Model):
    category = models.ForeignKey(Category , related_name = 'product',on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length = 222, null = False)
    slug = models.CharField(max_length = 222, unique = True, null=True)
    created_by = models.ForeignKey(User , on_delete = models.CASCADE , related_name = 'name', null=True)
    in_stock = models.IntegerField(default = 0)
    price = models.FloatField(default = 0)
    is_available = models.BooleanField(default = True)
    description = models.TextField(max_length = 255)
    image = models.ImageField(upload_to = 'images/')
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_by']
    # def img(self):
    #     try:
    #         url = self.image.url
    #     except:
    #         url = ''
    #     return url

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(User , on_delete = models.CASCADE , null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    is_received = models.BooleanField(default = False)
    product_ordered = models.ForeignKey(Product , on_delete = models.CASCADE , null = True, blank = True)

    def products_ordered(self):
        order_product = self.orderproduct_set.all()
        order_total = sum([product.total_price for product in order_product])
        return order_total

    def get_order_products(self):
        order_product = self.orderproduct_set.all()
        num_of_products = sum([product.quantity for product in order_product])
        return num_of_products
    
    def __str__(self):
        return "order"+ str(self.id)


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True , null = True)
    client = models.ForeignKey(User , on_delete = models.CASCADE , null = True, blank = True)
    order = models.ForeignKey(Order ,  on_delete = models.SET_NULL, blank = True , null = True)
    quantity = models.IntegerField(default = 0, blank = True , null = True)

    def total_price(self):
        total = self.product.price * self.quantity
        return total
