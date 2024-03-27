import razorpay
from django.conf import settings
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

default_app_config='fapp.apps'