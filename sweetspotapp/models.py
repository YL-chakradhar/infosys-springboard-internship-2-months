from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_no, first_name,last_name,city,state, address, pincode, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_no=phone_no,
            first_name=first_name,
            last_name=last_name,
            address=address,
            state=state,
            city=city,
            pincode=pincode,
            **extra_fields
        )
        user.set_password(password)#it is used to set the password and it is used to convert it into hash form
        user.save(using=self._db)# saving in thr database
        return user

    def create_superuser(self, email, phone_no, first_name,last_name,city,state, address, pincode, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True) 
        return self.create_user(email, phone_no, first_name,last_name,city,state, address, pincode, password=None, **extra_fields)

class Customer(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(unique=True,max_length=50)
    phone_no = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()#which contain methods for the creation of user and superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no', 'address', 'pincode','first_name','last_name','city','state']

    def __str__(self):
        return self.email 
class Store(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name
class Cake(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cakes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='cakes')

    def __str__(self):
        return self.name
class CakeCustomization(models.Model):
    Cake = models.ForeignKey('Cake', on_delete=models.CASCADE)
    Customer=models.ForeignKey('Customer',on_delete=models.CASCADE)
    message = models.CharField(max_length=50,blank=True)
    toppings = models.CharField(max_length=100, blank=True)
    shape = models.CharField(max_length=100, blank=True)
    egg_version = models.BooleanField(default=True)
class Cart(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    Customization=models.ForeignKey(CakeCustomization,on_delete=models.SET_NULL,null=True,default=None)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Order(models.Model):
    # Define choices for payment method
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    # Define choices for payment status
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    # Define choices for order status
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cake_customization = models.ForeignKey(CakeCustomization, on_delete=models.SET_NULL,null=True,default=None)
    items = models.ForeignKey(Cake,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES,default='other')

    def __str__(self):
        return f"Order {self.pk}"

    