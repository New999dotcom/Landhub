from django.db import models

# Create your models here.



class reg_form(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True)
    pwd = models.CharField(max_length=30)
    confirmpwd = models.CharField(max_length=30,null=True,blank=True)
    age = models.IntegerField()
    phone = models.IntegerField()
    place = models.CharField(max_length=200)
    genderchoice = (
        ('male','MALE'),
        ('female','FEMALE'),
    )
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    gend= models.CharField(max_length=10,choices=genderchoice,null=True,blank=True)
    
class property(models.Model):
    name= models.CharField(max_length=200)
    email = models.ForeignKey(reg_form,on_delete=models.CASCADE)
    phone = models.IntegerField()
    place = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    propertytype = models.CharField(max_length=200)
    propertychoice = (
        ('rent','RENT'),
        ('sale','SALE'),
    )
    prop= models.CharField(max_length=10,choices=propertychoice,null=True,blank=True)
    price = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200,null=True,blank=True)
    document = models.FileField(upload_to='documents/properties/', null=True, blank=True)  # For legal/property documents
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    area_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Property size
    is_furnished = models.BooleanField(default=False)  # Whether the property is furnished
    parking_space = models.BooleanField(default=False)  # Parking availability


class interested(models.Model):
    user=models.ForeignKey(reg_form,on_delete=models.CASCADE)
    propertyuser=models.ForeignKey(property,on_delete=models.CASCADE)
    interested=models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)  # 🔹 Optional message from user
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # 🔹 When the interest was registered
    

 
class Reviews(models.Model):
    user = models.ForeignKey('Reg_form', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Example: To store the rating (e.g., 1 to 5 stars)
    review_text = models.TextField()  # The review text itself
    created_at = models.DateTimeField(auto_now_add=True)  # To store when the review was created

    def _str_(self):
        return f"Review by {self.user.name} - Rating: {self.rating}"
    

# models.py
class BuyerReview(models.Model):
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyer Review by {self.buyer.name} (Rating: {self.rating})"    
    
class contactmessage(models.Model):
    user=models.ForeignKey(reg_form,on_delete=models.CASCADE,related_name='messages')
    name=models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)  # Field for admin reply
    replied_at = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"Message from {self.user.name} - {self.subject}"
    
from django.db import models
from django.utils.timezone import now

class ForumCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey('reg_form', on_delete=models.CASCADE)  # Link to reg_form model
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ForumCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    best_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL, related_name="best_for")

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey('reg_form', on_delete=models.CASCADE)  # Link to reg_form model
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    upvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Answer by {self.user.name} on {self.question.title}"

class AnswerUpvote(models.Model):
    user = models.ForeignKey('reg_form', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ("user", "answer")  # Prevent duplicate upvotes


    
class Notification(models.Model):
    """Stores notifications for users."""
    user = models.ForeignKey('reg_form', on_delete=models.CASCADE, related_name="notifications")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.user.name} - {self.message}"
    


class Wishlist(models.Model):
    user = models.ForeignKey(reg_form, on_delete=models.CASCADE)
    property = models.ForeignKey(property, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')


from django.contrib.auth.hashers import make_password, check_password

class Buyer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    pwd = models.CharField(max_length=128)  # Increased length for hashed password
    age = models.IntegerField()
    phone = models.IntegerField()
    place = models.CharField(max_length=200)
    
    # Gender choices
    gender_choices = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)
    
    # Image field
    image = models.ImageField(upload_to='buyer_images/', null=True, blank=True)
    
    # Buyer-specific fields
    buyer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    preferred_categories = models.CharField(max_length=200, null=True, blank=True)
    purchase_history = models.TextField(null=True, blank=True)

    def set_password(self, raw_password):
        self.pwd = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.pwd)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"  

from django.db import models
from .models import Buyer, reg_form, property as propertymodel

class Payment(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.ForeignKey(reg_form, on_delete=models.CASCADE)
    property = models.ForeignKey(propertymodel, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name} - {self.razorpay_payment_id}"



class SavedProperty(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(property, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'property')  # Prevent duplicates

    def __str__(self):
        return f"{self.buyer.name} saved {self.property.name}"    


class buyer_contactmessage(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)  # Using Buyer model
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} by {self.name} (Buyer)"    



from django.db import models


class Chat(models.Model):
    seller = models.ForeignKey('reg_form', on_delete=models.CASCADE)
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']     

    


    

    
    

    
    