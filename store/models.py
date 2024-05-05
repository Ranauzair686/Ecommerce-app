from django.db import models
# Create your models here.
from django.contrib.auth.models import User    #1


#customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True , blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

#Product model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2) #have changed float firld to decimal field 
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)  # image we have to put image here 

    def __str__(self):
        return self.name
    #IMAGEERROR CLASS
    @property  #this will help us to acces this as an attribute rather than a method 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#Order model

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False,null=True,blank=False)
    tansaction_Id = models.CharField(max_length=200 , null=True)

    def __str__(self):
        return str(self.id)
    
    #this is for complete cart total it is dependent on single item total(def get_total) 
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    

    @property  #this is our logic for shipping addres to check that our order is physical or not 
    def shipping (self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True


        return shipping
    
    #this is for getting total item in cart will ruery and calculate all items 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
#order item model
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #this is for the total of every single item means according to quantity after this we can calculate cart total
    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total



#shipping nmodel 
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.address


