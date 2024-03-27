from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('Cart',cart,basename='cart')
router.register('cartsecond',cartsecond,basename='cartsecond')

# nested router for cartitem
cart_router=routers.NestedDefaultRouter(router,'Cart',lookup='cart')
cart_router.register('item',cart_item,basename='cart_item')

# nested router for cartitemssecond
cart_secondrouter=routers.NestedDefaultRouter(router,'cartsecond',lookup='cartsecondid')
cart_secondrouter.register('itemsss',cart_itemsss,basename='cart_itemsss')



urlpatterns=[
    path('add_cart/<int:product_id>/',add_cart.as_view()),
    path('',include(router.urls)),
    path('',include(cart_router.urls)),
    path('',include(cart_secondrouter.urls)),
    path('decrement/<int:product_id>/<uuid:cart_id>/<int:item_id>/',cartdecrement.as_view()),
    path('increment/<int:product_id>/<uuid:cart_id>/<int:item_id>/',view_increment.as_view()),
    path('delete/<int:product_id>/<uuid:cart_id>/<int:item_id>/',view_delete.as_view())
    # path('cartsecond',add_carting.as_view()),

]