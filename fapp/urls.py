from django.urls import path
from .views import *

urlpatterns=[
    path('Registeration/',Registeration.as_view()),
    path('activation/<uid>/<token>',activation.as_view()),
    path('loginn/',view_login.as_view()),
    path('userprofile/',UserProfile.as_view()),
    path('userchangepassword/',UserChangePassword.as_view()),
    path('Forgotpasswordmail/',ForgotPasswordmail.as_view(),name="Forgotpasswordmail"),
    path('Forgotpassword/<uid>/<token>',ForgotPassword.as_view(),name="Forgotpassword"),
    ]
