from django.urls import path,include
from .views import *
from cart.views import cartsecond
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('cartsecond',cartsecond,basename='cartsecond')
router.register('profile_picture',profile_picture,basename='profile_picture')
router.register('view_Orders',view_Orders,basename='Orders')
# router.register('userprofile',UserProfileView,basename='userprofile')

cart_loginrouter=routers.NestedDefaultRouter(router,'cartsecond',lookup='cartsecondid')
cart_loginrouter.register('loginn',view_loginn,basename='loginn')


urlpatterns=[
    path('Registeration/',Registeration.as_view()),
    path('activation/<uid>/<token>',activation.as_view()),
    path('loginn/',view_login.as_view()),
    path('userprofile/',UserProfile.as_view()),
    path('userchangepassword/',UserChangePassword.as_view()),
    path('Forgotpasswordmail/',ForgotPasswordmail.as_view(),name="Forgotpasswordmail"),
    path('Forgotpassword/<uid>/<token>',ForgotPassword.as_view(),name="Forgotpassword"),
    path('userp',UserProfileAPiView.as_view(),name='UserProfile'),
    path('',include(router.urls)),
    path('',include(cart_loginrouter.urls))


    ]
