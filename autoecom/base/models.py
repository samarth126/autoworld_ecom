from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify




class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True, null=False)
    phone_no=models.CharField(max_length=11, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects=UserManager()
    REQUIRED_FIELDS=[]
    
# class Tri(models.Model):
#     name=models.CharField(max_length=10)
    
class TypeOfVehicle(models.Model):
    type_of=models.CharField(max_length=200, unique=True, null=False)
    slug=models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.type_of)
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.type_of)
    
class Manufacturer(models.Model):
    name_of_Manufacturer=models.CharField(max_length=200, unique=True, blank=False)
    vehicaltype=models.ForeignKey(TypeOfVehicle, on_delete=models.RESTRICT)
    slug=models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name_of_Manufacturer)
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.name_of_Manufacturer)


class CarModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.RESTRICT)
    model_name=models.CharField(max_length=200, blank=False, unique=True)
    slug=models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.model_name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return str(self.model_name)
    
class Year(models.Model):
    carmodel=models.ForeignKey(CarModel, on_delete=models.RESTRICT)
   
    Year=models.CharField(max_length=200, blank=True, null=True)
    slug=models.SlugField(blank=True, null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carmodel', 'Year'], name='name of constraint')
        ]
        
    
    
    
    def save(self, *args, **kwargs):
        
        self.slug=slugify(self.Year)
        
        super().save(*args, **kwargs)
    def __str__(self):
        # test=[]
        # test=self.Year
        # test2
        return str(self.Year)+str(self.carmodel)
    
      
class Category(MPTTModel):
    
    name=models.CharField(max_length=245, unique=True)
    slug=models.SlugField(max_length=255, unique=True)
    image=models.ImageField(
        
        verbose_name='category image',
        help_text="upload a category image",
        upload_to="images/",
        null=True,
        blank=True,
        
    )
    parent=TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active=models.BooleanField(default=True)
    
    class MPTTMeta:
        order_insertion_by=['name']
        
    def save(self, *args, **kwargs):
        
        self.slug=slugify(self.name)
        
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])
    
    def __str__(self):
        return str(self.name)
class Product(models.Model):
    # product_type=models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    vehicaltype=models.ForeignKey(TypeOfVehicle, blank=False, on_delete=models.RESTRICT)
    manufacturer=models.ForeignKey(Manufacturer, blank=False, on_delete=models.RESTRICT)
    vmodel=models.ForeignKey(CarModel, blank=False, on_delete=models.RESTRICT)
    myear=models.ForeignKey(Year, on_delete=models.RESTRICT)
    brand=models.CharField(max_length=200, blank=True, null=True )
    
    category=models.ForeignKey(Category, on_delete=models.RESTRICT)
    title=models.CharField(max_length=255, help_text=('required'))
    desc=models.TextField(blank=True, null=True, verbose_name=('desciptions'))
    
    regular_price=models.DecimalField(max_digits=6, decimal_places=1)
    descount_price=models.DecimalField(max_digits=6, decimal_places=1, blank=True )
    is_active=models.BooleanField(default=True)
    
    slug=models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
   
    
    def __str__(self):
        return str(self.title)
    
    
class ProductImage(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image=models.ImageField(
        verbose_name='image',
        help_text="upload a product image",
        upload_to="images/",
        null=True,
        blank=True,
        
    )
    is_feature=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name=models.CharField(max_length=20, null=True)
    last_name=models.CharField(max_length=20, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)







class Order(models.Model):
    Customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    status=models.BooleanField(default=False, null=True , blank=False)
    payment_status=models.BooleanField(default=False, null=True , blank=False)
    cod=models.BooleanField(default=False, null=True , blank=False)
    price=models.FloatField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.order_item_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.order_item_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class shipping_address(models.Model):
    Customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    Order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    country=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    zipcode=models.CharField(max_length=200, null=False, default=0)
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.address




class Order_item(models.Model):
    Order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    Product=models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
  

    @property
    def get_total(self):
        total = self.Product.regular_price * self.quantity
        return total


class Message(models.Model):
    Customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    real_message = models.TextField(blank=True, null=True)


class Support(models.Model):
    sender=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    s_name=models.TextField(null=True)
    s_email=models.EmailField(null=False)
    s_message=models.TextField(null=True)
    s_detail=models.CharField(max_length=20,null=True)
    s_created_at=models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return str(self.s_name)


class Contact(models.Model):
    name=models.CharField(max_length=20,null=True)
    email=models.CharField(max_length=20,null=True)
    phone_no=models.CharField(max_length=20,null=True)
    message=models.TextField(null=True)

    def _str_(self):
        return str(self.name)


class Transaction(models.Model):
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    bank_name=models.CharField(max_length=50)
    txn_id=models.CharField(max_length=200)
    txn_amt=models.CharField(max_length=20)
    txn_date=models.CharField(max_length=50)
    bank_txn_id=models.CharField(max_length=30)

    def __str__(self):
        return str(self.order)



# Create your models here.
