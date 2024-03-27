from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from products.models import *
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin, DestroyModelMixin,ListModelMixin
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication 


# Create your views here.
# trial cart
class cart(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=cart.objects.all()
    serializer_class=cartserializer

class cart_item(ModelViewSet):
    serializer_class=cartaddserializer

    def get_queryset(self):
        return cart_added.objects.filter(cart_id=self.kwargs['cart_pk'])


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

class add_cart(APIView):
    def post(self,request,product_id):
        current_user=request.user
        Product=Products.objects.get(id=product_id)
        product_variation=[]
        if current_user.is_authenticated:
            print('yesssssssssssssssssssssssssssssssssssssssssssss')
            for i in request.data.POST:
                key=i
                value=request.data.POST[key]
                Variations=variations.objects.get(product=Product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(Variations)
                print(product_variation)

            cart_itemexist=cart_added.objects.filter(product=Product,user=request.user).exists()
            if cart_itemexist:
                product_var=[]
                var_id=[]
                cart_item=cart_added.objects.filter(product=Product,user=request.user)
                for i in cart_item:
                    var=i.variations.all()
                    product_var.append(var)
                    var_id.append(i.id)

                if product_variation in product_var:
                    Index=product_var.index(product_variation)
                    id=var_id[Index]

                    cart_item=cart_added.objects.get(id=id)
                    cart_item.quantity+=1
                    cart_item.save()
                else:           
                    serializer=cartaddserializer(data=request.data,context={'user':request.user,'Product':Product,'Product_variation':product_variation})
                    if serializer.is_valid():
                        return Response({'data':'product added successfully!'},status=status.HTTP_200_OK)
                    else:
                        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer=cartaddserializer(data=request.data,context={'user':request.user,'Product':Product,'Product_variation':product_variation})
                if serializer.is_valid():
                    return Response({'data':'cart item added successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class cartsecond(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=cartsecond.objects.all()
    serializer_class=cartsecondSerializer

    

class cart_itemsss(ModelViewSet):
    # authentication_classes=[AllowAny]
    # permission_clases=[IsAuthenticated]
    
    def get_queryset(self):
        return cart_itemsecond.objects.filter(cart_id=self.kwargs['cartsecondid_pk'])

    def get_serializer_class(self):       
        if self.request.method=='POST':           
            if self.request.user.is_authenticated:
                cart_id=self.kwargs['cartsecondid_pk']
                user=self.request.user
                cart_items=cart_itemsecond.objects.filter(cart_id=cart_id).exists()
                if cart_items:
                    cart_items=cart_itemsecond.objects.filter(cart_id=cart_id)
                    for item in cart_items:
                        item.user=user
                        item.save()
                print('*************************************************')
                print(self.request.user)               
                return authaddcartserializer
            return addcartingserializer
        elif self.request.method=='PATCH':
            return updateserializer
        return add_cartingserializer
    
    def get_serializer_context(self,**kwargs):
        return {'cart_id':self.kwargs['cartsecondid_pk'],'user':self.request.user}



# def add_kart(request,product_id):
#     current_user=request.user
#     products=Products.objects.get(id=product_id)


#     if current_user.is_authenticated:
#         product_variation=[]
#         if request.method=='POST':
#             for item in request.POST:
#                 key=item
#                 print(key)
#                 value=request.POST[key]
#                 print(value)
#                 try:
#                     Variation=variations.objects.get(product=products,variation_category__iexact=key,variation_value__iexact=value)
#                     product_variation.append(Variation)
#                     print(product_variation)
#                 except Exception as e:
#                     print(e)              
        
#         cart_item_exist=Kart_item.objects.filter(user=current_user,product=products).exists()
#         print("True")
#         if cart_item_exist:
#             cart_item=Kart_item.objects.filter(user=current_user,product=products)
#             ex_variations=[]
#             ex_var_id=[]
#             for item in cart_item:
#                 variation=item.variations.all()
#                 ex_variations.append(list(variation))
#                 ex_var_id.append(item.id)
#             print(ex_variations)
#             print(product_variation)

#             if product_variation in ex_variations:
#                 Index=ex_variations.index(product_variation)
#                 item_id=ex_var_id[Index]
#                 item=Kart_item.objects.get(product=products,id=item_id)
#                 item.quantity+=1
#                 item.save()
#                 print('Yes')
#             else:
#                 item=Kart_item.objects.create(product=products,user=current_user,quantity=1)
#                 if len(product_variation)>0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item=Kart_item.objects.create(product=products,user=current_user,quantity=1)
#             if len(product_variation)>0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')
#     else:
#         product_variation=[]
#         if request.method=='POST':
#             for item in request.POST:
#                 key=item
#                 value=request.POST[key]
#                 try:
#                     Variation=variations.objects.get(product=products,variation_category__iexact=key,variation_value__iexact=value)
#                     product_variation.append(Variation)
#                 except:
#                     pass
#         try:
#             cart=Kart.objects.get(kart_id=_kart_id(request))
#         except Kart.DoesNotExist:
#             cart=Kart.objects.create(kart_id=_kart_id(request))
#         cart.save()

#         Iscartitemexist=Kart_item.objects.filter(cart=cart,product=products).exists()
#         if Iscartitemexist:
#             cartitem=Kart_item.objects.filter(cart=cart,product=products)
#             ex_variation=[]
#             ex_id=[]
#             for item in cartitem:
#                 variationss=item.variations.all()
#                 ex_variation.append(list(variationss))
#                 ex_id.append(item.id)

#             if product_variation in ex_variation:
#                 Index=ex_variation.index(product_variation)
#                 item_id=ex_id[Index]
#                 items=Kart_item.objects.get(product=products,id=item_id)
#                 items.quantity+=1
#                 items.save()

#             else:
#                 cart_item=Kart_item.objects.create(product=products,cart=cart,quantity=1)
#                 if len(product_variation)>0:
#                     cart_item.variations.clear()
#                     cart_item.variations.add(*product_variation)
#                 cart_item.save()
#         else:
#             cart_item=Kart_item.objects.create(product=products,cart=cart,quantity=1)
#             if len(product_variation)>0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')
 
class cartdecrement(APIView):
    def post(self,request,product_id,cart_id=None,item_id=None):
        product=Products.objects.get(id=product_id)
        try:
            if request.user.is_authenticated:
                cart_items=cart_itemsecond.objects.get(user=request.user,product=product,id=item_id)
            else:
                cart_items=cart_itemsecond.objects.get(cart_id=cart_id,product=product,id=item_id)

            if cart_items.quantity > 1:
                cart_items.quantity-=1
                cart_items.save()
                return Response({'msg':'cart_item reduced successfully!'},status=status.HTTP_200_OK)
            else:
                cart_items.delete()
                return Response({'msg':'cart_item deleted successfully!'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg':e},status=status.HTTP_400_BAD_REQUEST)


class view_increment(APIView):
    def post(self,request,product_id,cart_id,item_id):
        try:
            if request.user.is_authenticated:
                cart_items=cart_itemsecond.objects.get(product_id=product_id,user=request.user,id=item_id)
            else:
                cart_items=cart_itemsecond.objects.get(product_id=product_id,cart_id=cart_id,id=item_id)
            cart_items.quantity+=1
            cart_items.save()
            return Response({'data':'item added successfully!'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)


class view_delete(APIView):
    def post(self,request,product_id,cart_id,item_id):
        try:
            if request.user.is_authenticated:
                cart_items=cart_itemsecond.objects.get(product_id=product_id,user=request.user,id=item_id)
            else:
                cart_items=cart_itemsecond.objects.get(product_id=product_id,cart_id=cart_id,id=item_id)
            cart_items.delete()
            return Response({'data':'item deleted successfully!'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':e},status=status.HTTP_400_BAD_REQUEST)


            

