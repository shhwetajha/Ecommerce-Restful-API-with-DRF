from django.urls import path,include
from products.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
router=routers.DefaultRouter()
router.register('prodetail',Productdetail,basename='prodetail')

prod_router=routers.NestedDefaultRouter(router,'prodetail',lookup='product')
prod_router.register('ReviewRatingg',ReviewRatingg,basename='ReviewRatingg')


urlpatterns=[
    path('categorydetaillist/',categorydetaillist.as_view(),name='categorydetaillist'),
    path('categorydetaillist/<category_slug>/',categorydetailget.as_view()),
    path('single_product/<category_slug>/<slug>/',single_productdet.as_view()),
    path('reviewratingregister/<single_productid>/',reviewratingregister.as_view()),
    path('search/',search.as_view()),
    path('',include(router.urls)),
    path('',include(prod_router.urls)),
]
