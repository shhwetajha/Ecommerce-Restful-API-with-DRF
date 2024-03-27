from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from products.models import Products



# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None,password2=None):
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError('user must have an username')
        # if password!=confirm_password:
        #    raise ValueError('password and confirm password must be same')
            

        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name, )
        
        user.set_password(password)
        # user.password=password
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(email=self.normalize_email(email),username=username,
                         first_name=first_name,last_name=last_name,password=password)
        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=100,blank=True)
    last_name=models.CharField(max_length=100,blank=True)
    username=models.CharField(max_length=50,unique=True,null=True,blank=True)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=100,blank=True)

    # required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']

    objects=MyAccountManager()

    def full_name(self):
        return f"{self.first_name}{self.last_name}"


    def __str__(self):
        return self.first_name
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

# any type of user can watch the module
    
class ProfilePicture(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField(max_length=200)
    profile_picture=models.ImageField(upload_to='profile',null=True,blank=True)


    def __str__(self):
        return self.name



class Orders(models.Model):
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETED='C'
    PAYMENT_STATUS_FAILED='F'




    PAYMENT_STATUS_CHOICES=[(PAYMENT_STATUS_PENDING,'pending'),
                        (PAYMENT_STATUS_COMPLETED,'completed'),
                        (PAYMENT_STATUS_FAILED,'cancelled')]


    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=100,choices=PAYMENT_STATUS_CHOICES,default='PAYMENT_STATUS_PENDING')
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    order_payment_id=models.CharField(max_length=100,null=True,blank=True)

    @property
    def total_price(self):
        itemss=self.items.all()
        order_total=sum([item.quantity*item.product.price for item in itemss])
        return order_total
    


    

    def __str__(self):
        return self.payment_status


    

class OrderItem(models.Model):
    order=models.ForeignKey(Orders,on_delete=models.PROTECT,related_name='items')
    product=models.ForeignKey(Products,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.product_name


class UserProfileModel(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user')
    address_line_1=models.CharField(max_length=100,null=True,blank=True)
    address_line_2=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    profile_picture=models.ImageField(upload_to='photos/userprofile',null=True,blank=True,default='None')
    created_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.first_name

    objects = models.Manager()