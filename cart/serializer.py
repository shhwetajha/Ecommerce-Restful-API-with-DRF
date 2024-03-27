from rest_framework import serializers
from .models import *
from products.models import *
from fapp.serializers import *
from products.serializers import variationSerializer,variations_addedSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['first_name','last_name',]

class ProductSerial(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=['product_name','description','images','price']


class cartaddserializer(serializers.ModelSerializer):
    product=ProductSerial(many=False,read_only=True)
    user=UserProfileSerializer(many=False,read_only=True)
    variations=variationSerializer(many=True,read_only=True)
    sub_total=serializers.SerializerMethodField(method_name='total')
    class Meta:
        model= cart_added
        fields=['cart','product','user','variations','quantity','sub_total']

    def total(self,cart_add:cart_added):
        return cart_add.quantity*cart_add.product.price

class cartserializer(serializers.ModelSerializer):
    cart_id=serializers.UUIDField(read_only=True)
    cartt=cartaddserializer(many=True,read_only=True)
    grand_total=serializers.SerializerMethodField(method_name='main_total')
    class Meta:
        model=cart
        fields=['cart_id','cartt','grand_total']

    def main_total(self,carts:cart):
        cartlist=carts.cartt.all()
        total=sum(item.quantity*item.product.price for item in cartlist)
        return total
        





    # def validate(self,attrs):
    #     Product=self.context.get('Product')
    #     user=self.context.get('user')
    #     product_variation=self.context.get('Product_variation')
    

    #     if user.is_authenticated:
    #         cart_item=cart_added.objects.create(user=user,product=Product,quantity=1)
    #         if len(product_variation)>0:
    #             cart_item.variations.clear()
    #             cart_item.variations.add(*product_variation)
    #             print('****************')
    #         cart_item.save()
    #         return cart_item
    

          

    # def create(self,validate_data):
    #     Product=self.context.get('Product')
    #     user=self.context.get('user')
    #     product_variation=self.context.get('Product_variation')
    #     if user.is_authenticated:
    #         cart_item=cart_added.objects.create(user=user,product=Product,quantity=1)
    #         if len(product_variation)>0:
    #             cart_item.variations.clear()
    #             cart_item.variations.add(*product_variation)
    #             print('****************')
    #         cart_item.save()
    #         return cart_item
    

class addcartingserializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    variations_id=serializers.ListField(child=serializers.IntegerField(),write_only=True)
    # current_user=serializers.SerializerMethodField('_user')
    
    # def _user(self,obj):
    #     request=self.context.get('request',None)
    #     if request:
    #         print(request.user)
    #         return request.user

    def save(self,**kwargs):
        # user=self.context['cart_itemsss'].request.user()
        # print(user)
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        variations_id=self.validated_data['variations_id']
        print(variations_id)
        quantity=self.validated_data['quantity']
        data=self.validated_data
        print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        product_var=[]
        for i in variations_id:
            variations=variations_added.objects.get(id=i)
            product_var.append(variations)
            print(product_var)

        try:       
            cart_items=cart_itemsecond.objects.filter(cart_id=cart_id,product_id=product_id).exists()
            if cart_items:
                cart_items=cart_itemsecond.objects.filter(cart_id=cart_id,product_id=product_id)
                ex_var=[]
                ex_var_id=[]
                for item in cart_items:
                    variationss=item.variations.all()
                    ex_var.append(list(variationss))
                    print(ex_var)
                    ex_var_id.append(item.id)
                    print(ex_var_id)
                    print(product_var)
                    print(ex_var)
                    print('yesssssssssssssssssssssssg')
                try:
                    if product_var in ex_var:
                        print('yesssssssssssssssssssssss')
                        print("lllllllllllllllllllllllllllllllllllllllllll")
                        Index=ex_var.index(product_var)
                        varid=ex_var_id[Index]
                        print(varid)
                        cartitemss=cart_itemsecond.objects.get(id=varid)
                        print(cartitemss)
                        cartitemss.quantity+=quantity
                        cartitemss.save()
                        self.instance=cartitemss
                        return self.instance
                    else:
                        cart_items=cart_itemsecond.objects.create(cart_id=cart_id,product_id=product_id,quantity=quantity)
                        for var in data['variations_id']:
                            var_obj=variations_added.objects.get(id=var)               
                            cart_items.variations.add(var_obj)
                        cart_items.save()
                        self.instance=cart_items       
                    return self.instance
                except Exception as e:
                    print(e)
            else:              
                cart_items=cart_itemsecond.objects.create(cart_id=cart_id,product_id=product_id,quantity=quantity)
                for var in data['variations_id']:
                    var_obj=variations_added.objects.get(id=var)               
                    cart_items.variations.add(var_obj)
                cart_items.save()
                self.instance=cart_items       
            return self.instance
        except:
            pass

    
    class Meta:
        model=cart_itemsecond
        fields=['id','product_id','variations_id','quantity']
        depth=1

# OrderedDict([('product_id', 3), ('quantity', 1)])

class authaddcartserializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    # quantity=serializers.IntegerField()
    variations_id=serializers.ListField(child=serializers.IntegerField(),write_only=True)
    
   
    # def create(self,validated_data):
    #     cart_id=self.context['cart_id']
    #     user=self.context['user']
    #     print('************')

    #     cart_itemssexist=cart_itemsecond.objects.filter(cart_id=cart_id).exists()
    #     if cart_itemssexist:
    #         cart_itemss=cart_itemsecond.objects.filter(cart_id=cart_id)
    #         productt_var=[]
    #         varr_id=[]
                        
    #         for item in cart_itemss:
    #             variationss=item.variations.all()
    #             productt_var.append(list(variationss))
    #             varr_id.append(item.id)

    #         cart_itemsslogin=cart_itemsecond.objects.filter(user=user)                       
    #         product_var=[]
    #         vari_id=[]
                
    #         for item in cart_itemsslogin:
    #             variationss=item.variations.all()
    #             product_var.append(list(variationss))
    #             vari_id.append(item.id)

    #             for pro in product_var:
    #                 if pro in productt_var:
    #                     Index=productt_var.index(pro)
    #                     id=varr_id[Index]
    #                     cart_itemsecond.objects.get(id=id)
    #                     cart_itemsecond.quantity+=1
    #                     cart_itemsecond.user=user
    #                     cart_itemsecond.save()
                                                           
    #                 else:
    #                     cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
    #                     for item in cart_itemsss:
    #                         item.user=user
    #                         item.save()

    # def validate(self,attrs):
    #     product_id=attrs.get('product_id')
    #     cart_id=self.context.get('cart_id')
    #     user=self.context.get('user')
    #     cart_items=cart_itemsecond.objects.filter(cart_id=cart_id).exists()
    #     if cart_items:
    #         cart_items=cart_itemsecond.objects.filter(cart_id=cart_id)
    #         for item in cart_items:
    #             item.user=user
    #             item.save()
    #             print('ho gyaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    #     else:
    #         pass
                            
    def save(self,**kwargs):
        product_id=self.validated_data['product_id']
        variations_id=self.validated_data['variations_id']
        cart_id=self.context['cart_id']
        user=self.context['user']
        print(user)
        quantity=self.validated_data['quantity']
        data=self.validated_data

        # cart_itemssexist=cart_itemsecond.objects.filter(cart_id=cart_id).exists()
        # if cart_itemssexist:
        #     cart_itemss=cart_itemsecond.objects.filter(cart_id=cart_id)
        #     productt_var=[]
        #     varr_id=[]
                        
        #     for item in cart_itemss:
        #         variationss=item.variations.all()
        #         productt_var.append(list(variationss))
        #         varr_id.append(item.id)

        #     cart_itemsslogin=cart_itemsecond.objects.filter(user=user)                       
        #     product_var=[]
        #     vari_id=[]
                
        #     for item in cart_itemsslogin:
        #         variationss=item.variations.all()
        #         product_var.append(list(variationss))
        #         vari_id.append(item.id)

        #         for pro in product_var:
        #             if pro in productt_var:
        #                 Index=productt_var.index(pro)
        #                 id=varr_id[Index]
        #                 cart_itemsecond.objects.get(id=id)
        #                 cart_itemsecond.quantity+=len(pro)
        #                 cart_itemsecond.user=user
        #                 cart_itemsecond.save()
                                                           
        #             else:
        #                 cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
        #                 for item in cart_itemsss:
        #                     item.user=user
        #                     item.save()
                            
        product_variation=[]
        for i in variations_id:
            variations=variations_added.objects.get(id=i)
            product_variation.append(variations)

        try:
            cart_itemexist=cart_itemsecond.objects.filter(product_id=product_id,user=user).exists()
            if cart_itemexist:
                product_var=[]
                var_id=[]
                cart_item=cart_itemsecond.objects.filter(product_id=product_id,user=user)
                for item in cart_item:
                    variations=item.variations.all()
                    product_var.append(list(variations))
                    var_id.append(item.id)
                   
                if product_variation in product_var:
                    print('yess')
                    print(product_variation)
                    print(product_var)
                    Index=product_var.index(product_variation)
                    id=var_id[Index]
                    cart_items=cart_itemsecond.objects.get(id=id)
                    cart_items.quantity+=quantity
                    cart_items.save()
                    self.instance=cart_items
                    # cart_itemss=cart_itemsecond.objects.filter(user=user)                       
                    # product_var=[]
                    # vari_id=[]
                        
                    # for item in cart_itemss:
                    #     variationss=item.variations.all()
                    #     product_var.append(list(variationss))
                    #     vari_id.append(item.id)

                    # cart_itemsslogin=cart_itemsecond.objects.filter(cart_id=cart_id)                       
                    # productt_var=[]
                    # varr_id=[]
                        
                    # for item in cart_itemsslogin:
                    #     variationss=item.variations.all()
                    #     productt_var.append(list(variationss))
                    #     varr_id.append(item.id)

                    #     for pro in product_var:
                    #         if pro in productt_var:
                    #             Index=productt_var.index(pro)
                    #             id=var_id[Index]
                    #             cart_itemsecond.objects.get(id=id)
                    #             cart_itemsecond.quantity+=1
                    #             cart_itemsecond.user=user
                    #             cart_itemsecond.save()
                    #             self.instance=cart_itemsecond                                   
                    #         else:
                    #             cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
                    #             for item in cart_itemsss:
                    #                 item.user=user
                    #                 item.save()
                    #                 self.instance=item


                               
                    return self.instance
                else:
                    cart_items=cart_itemsecond.objects.create(product_id=product_id,user=user,cart_id=cart_id,quantity=quantity)
                    for i in data['variations_id']:
                        variations=variations_added.objects.get(id=i)
                        cart_items.variations.add(variations)
                        cart_items.save()
                        self.instance=cart_items
                        # cart_itemss=cart_itemsecond.objects.filter(user=user)                       
                        # product_var=[]
                        # vari_id=[]
                            
                        # for item in cart_itemss:
                        #     variationss=item.variations.all()
                        #     product_var.append(list(variationss))
                        #     vari_id.append(item.id)

                        # cart_itemsslogin=cart_itemsecond.objects.filter(cart_id=cart_id)                       
                        # productt_var=[]
                        # varr_id=[]
                        
                        # for item in cart_itemsslogin:
                        #     variationss=item.variations.all()
                        #     productt_var.append(list(variationss))
                        #     varr_id.append(item.id)

                        #     for pro in productt_var:
                        #         if pro in product_var:
                        #             Index=product_var.index(pro)
                        #             id=var_id[Index]
                        #             cart_itemsecond.objects.get(id=id)
                        #             cart_itemsecond.quantity+=1
                        #             cart_itemsecond.user=user
                        #             cart_itemsecond.save()
                        #             self.instance=cart_itemsecond

                                    
                        #         else:
                        #             cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
                        #             for item in cart_itemsss:
                        #                 item.user=user
                        #                 item.save()
                        #                 self.instance=item             
                    return self.instance
            else:
                cart_items=cart_itemsecond.objects.create(product_id=product_id,user=user,cart_id=cart_id,quantity=quantity)
                print('createeeeeeeee')
                for i in data['variations_id']:
                    variations=variations_added.objects.get(id=i)
                    cart_items.variations.add(variations)
                    cart_items.save()
                    # cart_itemss=cart_itemsecond.objects.filter(user=user)                       
                    # product_var=[]
                    # vari_id=[]
                        
                    # for item in cart_itemss:
                    #     variationss=item.variations.all()
                    #     product_var.append(list(variationss))
                    #     vari_id.append(item.id)

                    # cart_itemsslogin=cart_itemsecond.objects.filter(cart_id=cart_id)                       
                    # productt_var=[]
                    # varr_id=[]
                        
                    # for item in cart_itemsslogin:
                    #     variationss=item.variations.all()
                    #     productt_var.append(list(variationss))
                    #     varr_id.append(item.id)

                    #     for pro in productt_var:
                    #         if pro in product_var:
                    #             Index=product_var.index(pro)
                    #             id=var_id[Index]
                    #             cart_itemsecond.objects.get(id=id)
                    #             cart_itemsecond.quantity+=1
                    #             cart_itemsecond.user=user
                    #             cart_itemsecond.save()
                    #             self.instance=cart_itemsecond                            
                    #         else:
                    #             cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
                    #             for item in cart_itemsss:
                    #                 item.user=user
                    #                 item.save()
                                    # self.instance=item
                    self.instance=cart_items
            print("Doneeeeeeeeeeeeeee")
            return self.instance
        except:
            pass

        # cart_items=cart_itemsecond.objects.filter(cart_id=cart_id).exists()
        # if cart_items:
        #     product_vari=[]
        #     var_idd=[]
        #     cart_itemss=cart_itemsecond.objects.filter(product_id=product_id,cart_id=cart_id)
        #     for item in cart_itemss:
        #         variations=item.variations.all()
        #         product_vari.append(list(variations))
        #         var_idd.append(item.id)
        #     for pr in product_var:
        #         if pr in product_vari:
        #             Index=product_vari.index(pr)
        #             id=var_idd[Index]
        #             cart_itemsss=cart_itemsecond.objects.get(id=id)
        #             cart_itemsss.quantity+=1
        #             cart_itemsss.save()
        #             self.instance=cart_itemsss
        #             return self.instance
        #         else:
        #             cart_itemss=cart_itemsecond.objects.filter(product_id=product_id,cart_id=cart_id)
        #             for item in cart_itemss:
        #                 item.user=user
        #             item.save()
        #             self.instance=item
                    # return self.instance


    class Meta:
        model=cart_itemsecond
        fields=['id','product_id','variations_id','quantity']
        depth=1

class add_cartingserializer(serializers.ModelSerializer):
    product=ProductSerial(many=False,read_only=True)
    variations=variations_addedSerializer(many=True,read_only=True)

    class Meta:
        model=cart_itemsecond
        fields=['id','product','variations','quantity']
        depth=1




class cartsecondSerializer(serializers.ModelSerializer):
    cartsecond=add_cartingserializer(many=True,read_only=True)
    id=serializers.UUIDField(read_only=True)
    class Meta:
        model=cartsecond
        fields=['id','cartsecond',]



    
# cart_itemss=cart_itemsecond.objects.filter(user=user)                       
#                         product_var=[]
#                         var_id=[]
                        
#                         for item in cart_itemss:
#                             variationss=item.variations.all()
#                             product_var.append(list(variationss))
#                             var_id.append(item.id)

#                         cart_itemsslogin=cart_itemsecond.objects.filter(cart_id=cart_id)                       
#                         productt_var=[]
#                         varr_id=[]
                        
#                         for item in cart_itemsslogin:
#                             variationss=item.variations.all()
#                             productt_var.append(list(variationss))
#                             varr_id.append(item.id)

#                             for pro in productt_var:
#                                 if pro in product_var:
#                                     Index=product_var.index(pro)
#                                     id=var_id[Index]
#                                     cart_itemsecond.objects.get(id=id)
#                                     cart_itemsecond.quantity+=1
#                                     cart_itemsecond.user=user
#                                     cart_itemsecond.save()
#                                     self.instance=cart_itemsecond

                                    
#                                 else:
#                                     cart_itemsss=cart_itemsecond.objects.filter(cart_id=cart_id)
#                                     for item in cart_itemsss:
#                                         item.user=user
#                                         item.save()
#                                         self.instance=item


class updateserializer(serializers.ModelSerializer):
    class Meta:
        model= cart_itemsecond
        fields=['quantity']   