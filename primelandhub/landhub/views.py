from django.shortcuts import render, redirect, HttpResponse
from .models import contactmessage  # Import the contactmessage model
from django.shortcuts import get_object_or_404
from .forms import PropertyForm  # Import the PropertyForm

from.import models
# Removed duplicate import
from django.http import HttpResponse

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        username = 'landhub'
        password = 'landhub'
        if email == username and pwd == password:
            request.session['email'] = 'email'
            return redirect('adminhome')  # Replace 'adminhome' with the actual admin home page URL name
        else:
            alert = "Invalid credentials. Please try again."
            return render(request, 'adminlogin.html', {'alert': alert})
    else:  # For GET requests, return the login page
        return render(request, 'adminlogin.html')

from django.shortcuts import render, redirect
from . import models  # Ensure models are correctly imported

def adminhome(request):
    if 'email'  in request.session:
        total_users = models.reg_form.objects.count() + models.Buyer.objects.count()
        print (f"Total users: {total_users}")  # Debugging line
        total_properties = models.property.objects.count()
        total_reviews = models.Reviews.objects.count()

    context = {
        'total_users': total_users,
        'total_properties': total_properties,
        'total_reviews': total_reviews
    }
    return render(request, 'adminhome.html', context)

from . import models
from django.contrib import messages 
 
def deleteusers(request, id):
    user = get_object_or_404(reg_form, id=id)  # Get user or show 404 error
    user.delete()
    messages.success(request, "User deleted successfully!")  # Flash message
    return redirect('user_management')



def delteproperty(request, id):
    Pro = get_object_or_404(property, id=id)
    Pro.delete()
    print(f"Property with ID {id} deleted.")  # Debugging line
    messages.success(request, "Property deleted successfully!")
    return redirect('propertyviewadmin')  # Redirect to property listing page

    
def listusers(request):
    users = models.reg_form.objects.all()  # General users from landhub_reg_form
    buyers = models.Buyer.objects.all()    # Buyers from Buyer model
    return render(request, 'user_management.html', {
        'users': users,
        'buyers': buyers,
    })  # Redirect back to user list
from django.shortcuts import render
from django.db.models import Q
from .models import property  # Importing only the property model

from django.shortcuts import render
from django.db.models import Q
from .models import property  # Assuming this is your model import

def propertylisting(request):
    # Start with all properties
    properties = property.objects.all()

    # Get filter parameters from the GET request
    property_type = request.GET.get('property_type', '')  # Matches HTML name="property_type"
    search_query = request.GET.get('search', '')

    # Apply property type filter if selected (case-insensitive)
    if property_type:
        properties = properties.filter(propertytype__iexact=property_type)

    # Apply search filter if provided (searches location or property name)
    if search_query:
        properties = properties.filter(
            Q(place__icontains=search_query) | 
            Q(name__icontains=search_query)
        )

    # Render the template with filtered properties
    return render(request, 'propertyviewadmin.html', {'properties': properties})

def message(request):
    if 'email' in request.session:
        email = request.session.get('email')

        # Fetch user from Reg_form based on session email
        try:
            sender = Buyer.objects.get(buyer_id=request.session['buyer_id'])
            sender = Buyer.objects.get(buyer_id=request.session['buyer_id'])
            user = reg_form.objects.get(email=email)
        except reg_form.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('some_error_page')  # Redirect to an error page or home
        
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            typing_message = request.POST.get('message', '')

            if subject and typing_message:
                # Save message to database
                contactmessage.objects.create(
                    user=user,
                    name=user.name,  # Assuming Reg_form has a name field
                    subject=subject,
                    message=typing_message
                )
                alert="<script>alert('message sent suceesfully..!');window.location.href='/home/';</script>"
                return HttpResponse(alert) # Redirect to a success page
            
            messages.error(request, "All fields are required.")

        return render(request, 'message.html', {'user': user})
    
    messages.error(request, "You must be logged in to send a message.")
    return redirect('login')  # Redirect to login if no session email
def view_messages(request):
    msg=models.contactmessage.objects.all()
    return render(request,'views_messages.html', {'msg':msg})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import contactmessage

def reply_message(request, message_id):
    msg = get_object_or_404(contactmessage, id=message_id)

    if request.method == 'POST':
        reply_text = request.POST['reply']
        if reply_text.strip():
            msg.reply = reply_text
            msg.replied_at = now()
            msg.save()
            messages.success(request, "Reply sent successfully!")
        else:
            messages.error(request, "Reply cannot be empty.")
        return redirect( 'viewmessage')  # Redirect to the messages page

    return render(request, 'reply_message.html', {'message': msg})
from django.shortcuts import render, redirect
from .models import contactmessage, reg_form
from django.contrib import messages

def user_replied_messages(request):
    """Fetch only messages with admin replies for the user in session."""
    user_email = request.session.get('email')

    if not user_email:
        messages.error(request, "Session expired. Please enter your email again.")
        return redirect('home')  # Redirect to home or an email input page

    # Get the user from the reg_form model
    try:
        user = reg_form.objects.get(email=user_email)
    except reg_form.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('home')

    # Filter messages that belong to this user and have admin replies
    replied_messages = contactmessage.objects.filter(user=user).exclude(reply__isnull=True).exclude(reply="").order_by('-replied_at')

    return render(request, 'user_replied.html', {'messages': replied_messages})

def delete_message(request, message_id):
    """Allow admin to delete a specific message."""
    message = get_object_or_404(contactmessage, id=message_id)
    
    # Delete the message
    message.delete()
    messages.success(request, "Message deleted successfully.")
    
    return redirect('viewmessage')  # Ensure 'viewmessage' is the correct name of the message listing URL


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Buyer, buyer_contactmessage
import logging

logger = logging.getLogger(__name__)

def buyer_message(request):
    if 'buyer_id' in request.session:
        buyer_id = request.session.get('buyer_id')
        logger.debug(f"Session buyer_id: {buyer_id} (type: {type(buyer_id)})")

        # Fetch buyer using the buyer_id field (CharField)
        try:
            buyer = Buyer.objects.get(buyer_id=buyer_id)  # Query buyer_id, not id
            logger.debug(f"Buyer found: {buyer.name}, {buyer.buyer_id}")
        except Buyer.DoesNotExist:
            logger.error(f"No Buyer found for buyer_id: {buyer_id}")
            messages.error(request, "Buyer not found. Please log in with a valid buyer account.")
            return redirect('404')
        
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            typing_message = request.POST.get('message', '')

            if subject and typing_message:
                buyer_contactmessage.objects.create(
                    buyer=buyer,
                    name=buyer.name,
                    subject=subject,
                    message=typing_message
                )
                alert = "<script>alert('Message sent successfully..!');window.location.href='/dashboard/';</script>"
                return HttpResponse(alert)
            
            messages.error(request, "All fields are required.")

        return render(request, 'buyer_message.html', {'buyer': buyer})
    
    messages.error(request, "You must be logged in to send a message.")
    return redirect('Login_buyer')

# View All Buyer Messages (Admin)
def view_buyer_messages(request):
    buyer_msgs = buyer_contactmessage.objects.all()
    return render(request, 'view_buyer_messages.html', {'msg': buyer_msgs})

# Reply to Buyer Message (Admin)
def reply_buyer_message(request, message_id):
    msg = get_object_or_404(buyer_contactmessage, id=message_id)

    if request.method == 'POST':
        reply_text = request.POST['reply']
        if reply_text.strip():
            msg.reply = reply_text
            msg.replied_at = now()
            msg.save()
            messages.success(request, "Reply sent successfully!")
        else:
            messages.error(request, "Reply cannot be empty.")
        return redirect('view_buyer_messages')  # Redirect to buyer messages page

    return render(request, 'reply_buyer_message.html', {'message': msg})

# View Replied Messages for Buyer
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Buyer, buyer_contactmessage
import logging

logger = logging.getLogger(__name__)

def buyer_replied_messages(request):
    """Fetch only messages with admin replies for the buyer in session."""
    buyer_id = request.session.get('buyer_id')  # Use buyer_id instead of email
    logger.debug(f"Session buyer_id: {buyer_id}")

    if not buyer_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('dashboard')

    # Get the buyer from the Buyer model using buyer_id
    try:
        buyer = Buyer.objects.get(buyer_id=buyer_id)  # Query buyer_id instead of email
        logger.debug(f"Buyer found: {buyer.name}, {buyer.buyer_id}")
    except Buyer.DoesNotExist:
        logger.error(f"No Buyer found for buyer_id: {buyer_id}")
        messages.error(request, "Buyer not found.")
        return redirect('dashboard')

    # Filter buyer messages that belong to this buyer and have admin replies
    replied_messages = buyer_contactmessage.objects.filter(buyer=buyer).exclude(reply__isnull=True).exclude(reply="").order_by('-replied_at')
    logger.debug(f"Replied messages count: {replied_messages.count()}")

    return render(request, 'buyer_replied.html', {'messages': replied_messages})

# Delete Buyer Message (Admin)
def delete_buyer_message(request, message_id):
    """Allow admin to delete a specific buyer message."""
    message = get_object_or_404(buyer_contactmessage, id=message_id)
    
    # Delete the message
    message.delete()
    messages.success(request, "Message deleted successfully.")
    
    return redirect('view_buyer_messages')  # Redirect to buyer messages page


from django.shortcuts import render
from .models import contactmessage, buyer_contactmessage

def view_all_messages(request):
    """Display all seller and buyer messages for admin."""
    seller_msgs = contactmessage.objects.all()
    buyer_msgs = buyer_contactmessage.objects.all()
    
    # Pass both sets of messages to the template
    return render(request, 'views_messages.html', {
        'seller_msgs': seller_msgs,
        'buyer_msgs': buyer_msgs
    })

   



   
# Create your views here.



from .models import Reviews  # Import the Reviews model

def index(request):
    reviews = Reviews.objects.all().order_by('-created_at')  # Fetch reviews
    context = {
        'reviews': reviews,  # Pass reviews to the template
    }
    return render(request, 'index.html', context)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import reg_form

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random

import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
  # Ensure correct import

from django.core.files.storage import default_storage
def register(request):
    if request.method == 'POST':
        name = request.POST.get('Name')  # Use .get() for safety
        email = request.POST.get('Email')
        pwd = request.POST.get('Password')
        confirmpwd = request.POST.get('confirm password')
        age = request.POST.get('age')
        phone = request.POST.get('Phone Number')
        place = request.POST.get('place')
        gend = request.POST.get('gender')
        image = request.FILES.get('image')  # Get image if uploaded

        # Ensure all fields are filled
        if not all([name, email, pwd, confirmpwd, age, phone, place, gend,image]):
            return HttpResponse("<script>alert('All fields are required'); window.location.href='/register/';</script>")

        # Check if email already exists
        if models.reg_form.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists'); window.location.href='/register/';</script>")

        if pwd != confirmpwd:
            return HttpResponse("<script>alert('Passwords do not match'); window.location.href='/register/';</script>")

        otp = str(random.randint(100000, 999999))  # Convert OTP to string
        request.session['otp'] = otp  # Store OTP in session
        if image:
            # Save the file to media folder and store the path
            image_path = default_storage.save(f'profile_images/{image.name}', image)
        else:
            image_path = None  # If no image is uploaded
        # Store user data in the session for OTP verification
        request.session['user_data'] = {
            'name': name, 'email': email, 'pwd': pwd,
            'age': age, 'phone': phone, 'place': place, 'gend': gend,'image': image_path 
            
        }

        # Store image name (for reference) in the session if image exists
        if image:
            request.session['image'] = image.name  # Store image name

        # Render HTML email
        html_content = render_to_string('email_templates/otp_email.html', {'otp': otp})
        text_content = strip_tags(html_content)

        # Send OTP email
        email_message = EmailMultiAlternatives(
            'Your OTP for PrimeLand Hub Registration',
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'register.html')



from django.contrib import messages
from django.shortcuts import redirect, render
from landhub.models import reg_form  # Make sure to import the correct model

def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        stored_otp = request.session.get('otp')  # Get OTP from session
        
        if str(otp_entered) == str(stored_otp):  # Ensure correct type
            user_data = request.session.get('user_data')

            if not user_data:  # If user_data is missing, return an error
                return HttpResponse("<script>alert('Session expired. Please register again.');window.location.href='/register/';</script>")

            # Retrieve the image from the session and files
            image = request.FILES.get('image')  # Get the image uploaded during registration

            # Check if email already exists in the database
            if reg_form.objects.filter(email=user_data['email']).exists():
                messages.error(request, 'An account with this email already exists. Please log in.')
                return redirect('/register/')  # Redirect to login page if email exists

            # Save user to database
            user = reg_form.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                pwd=user_data['pwd'],
                age=user_data['age'],
                phone=user_data['phone'],
                place=user_data['place'],
                gend=user_data['gend'],
                image=image  # Save the image if available
            )
            user.save()

            # Clear session data after successful verification
            del request.session['otp']
            del request.session['user_data']
            return HttpResponse ("""
    <html>
        <head>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="flex items-center justify-center min-h-screen bg-gradient-to-b from-gray-100 to-gray-300">
            <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm text-center">
                <h2 class="text-xl font-semibold text-green-600 mb-4">Registration Successful!</h2>
                <p class="text-gray-700 mb-6 text-sm">Your account has been successfully created! Please log in to continue.</p>
                <button 
                    onclick="window.location.href='/login/'" 
                    class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all duration-300">
                    Go to Login Page
                </button>
            </div>
        </body>
    </html>
""")


            

            # Add success message to be displayed on the login page
            
            # Redirect to the login page
            

        else:
            return HttpResponse("<script>alert('Invalid OTP');window.location.href='/verify_otp/';</script>")

    return render(request, 'verify_otp.html')






from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

def login(request):
    if request.method == 'POST':
        email = request.POST['Email']
        pwd = request.POST['Password']
        if models.reg_form.objects.filter(email=email, pwd=pwd).exists():
            request.session['email'] = email
            request.session['user_type'] = 'seller'  # Set user type
            return redirect('home')
        else:
            alert = "<script>alert('invalid credentials');window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:
        return render(request, 'login.html')
def home(request):


    return render(request,'home.html')

def profile(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = models.reg_form.objects.get(email=email)
            wishlist = models.Wishlist.objects.filter(user=user).select_related('property')
            return render(request, 'profile.html', {'user': user, 'wishlist': wishlist})
        except models.reg_form.DoesNotExist:
            alert = "<script>alert('Something went wrong');window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:
        return render(request, 'profile.html')  # No user logged in

def wishlist_action(request):
    if 'email' not in request.session:
        return JsonResponse({"status": "error", "message": "Not authenticated"})
    
    if request.method == "POST":
        email = request.session['email']
        try:
            user = models.reg_form.objects.get(email=email)
            property_id = request.POST.get("property_id")
            action = request.POST.get("action")
            message = request.POST.get("message", "")

            prop = get_object_or_404(models.property, id=property_id)

            if action == "add":
                wishlist_item, created = models.Wishlist.objects.get_or_create(
                    user=user,
                    property=prop,
                    defaults={'message': message}
                )
                if not created:
                    wishlist_item.message = message
                    wishlist_item.save()
                return JsonResponse({"status": "success", "action": "added"})
            elif action == "remove":
                models.Wishlist.objects.filter(user=user, property=prop).delete()
                return JsonResponse({"status": "success", "action": "removed"})

            return JsonResponse({"status": "error", "message": "Invalid action"})
        except models.reg_form.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
def editprofile(request):
    if 'email' in request.session:
        email=request.session['email']
        user=models.reg_form.objects.get(email=email)
        if user:
            if request.method=='POST':
                user.name=request.POST.get('Name')
                user.email=request.POST.get('Email')
                user.age=request.POST.get('age')
                user.phone=request.POST.get('Phone Number')
                user.place=request.POST.get('place')
                user.gend=request.POST.get('gend')
                user.pwd=request.POST.get('Password')
                user.confirmpwd=request.POST.get('confirm password')
                if 'image' in request.FILES:
                    

                    user.image = request.FILES['image']
               
                user.save()
                return redirect('profile')
            
        return render(request,'editprofile.html',{'user':user})

def deleteprofile(request):
    if 'email' in request.session:
        email=request.session['email']
        user=models.reg_form.objects.get(email=email)
        user.delete()
        return redirect('login')
    else:
        return redirect('login')    
def aboutus(request):
    return render(request,'aboutus.html')
def about(request):
    return render('about.html')
def view_properties(request):
    # Fetch all properties to display
    properties = models.property.objects.all()
    return render(request, 'viewproperties.html', {'properties': properties})

def view_property_detail(request, id):
    # Check if the user is logged in
    
   
    messages.info(request, "Please register to view property details.")
    return redirect('register')  # Redirect to a home or another relevant page

from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import models

def add_review(request):
    if request.method == 'POST':
        review = request.POST['review']
        rating = request.POST['rating']
        user_email = request.session.get('email')
        
        if user_email:
            # User is logged in, save the review
            user = models.reg_form.objects.get(email=user_email)
            models.Reviews.objects.create(user=user, rating=rating, review_text=review)
            
            # Return a JSON response to indicate success
            return JsonResponse({'success': True, 'message': 'Thanks for your feedback!'})
        
        else:
            # User is not logged in, redirect to main page
            return JsonResponse({'success': False, 'message': 'Please log in to submit a review.'})
    
    # If GET request or failed submission, render the review page
    return render(request, 'review.html')


from django.shortcuts import render
from django.shortcuts import get_object_or_404
from landhub.models import Buyer, BuyerReview
from django.shortcuts import reverse
def add_buyer_review(request):
    if request.method == 'POST':
        # Get the string ID from session (like "B000001")
        buyer_id = request.session.get('buyer_id')
        
        if not buyer_id:
            return JsonResponse({'success': False, 'message': 'Please login first'})

        try:
            # Match using the string buyer_id field (not numeric ID)
            buyer = Buyer.objects.get(buyer_id=buyer_id)  # Changed from .get(id=...)
            
            # Validate rating
            rating = int(request.POST.get('rating', 0))
            if not (1 <= rating <= 5):
                return JsonResponse({'success': False, 'message': 'Invalid rating'})

            # Create review
            BuyerReview.objects.create(
                buyer=buyer,
                rating=rating,
                review_text=request.POST.get('review', '')
            )
            return JsonResponse({'success': True, 'message': 'Review submitted!'})

        except Buyer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Buyer not found'})

    # GET request
    return render(request, 'buyer_review.html')

from django.http import JsonResponse
from .models import property



    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def contact(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Prepare the email details
        subject = f"Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send the email to the recipient (DEFAULT_TO_EMAIL)
            send_mail(
                subject,            # Email subject
                body,               # Email body
                settings.DEFAULT_FROM_EMAIL,  # From email
                [settings.DEFAULT_TO_EMAIL],  # To email(s)
                fail_silently=False,
            )
            
            # Send a confirmation email to the sender (email provided by the user)
            confirmation_subject = "Your message has been sent successfully"
            confirmation_body = f"Dear {name},\n\nThank you for contacting us! We have received your message and will get back to you soon.\n\nMessage:\n{message}"

            send_mail(
                confirmation_subject,  # Confirmation email subject
                confirmation_body,     # Confirmation email body
                settings.DEFAULT_FROM_EMAIL,  # From email
                [email],  # Send confirmation to the sender's email
                fail_silently=False,
            )

            # Success message to display in the frontend
            messages.success(request, "Your message has been sent successfully!")

        except Exception as e:
            # Error message in case of failure
            messages.error(request, "There was an error sending your message. Please try again.")
        
        return redirect("contact")  # Redirect back to the contact page

    return render(request, "contact.html")


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        request.session.flush()  # Clear all session data
        return redirect('login')
    else:
        return redirect('login')  

from django.shortcuts import render, redirect
from . import models

def addproperty(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            place = request.POST.get('place')
            propertytype = request.POST.get('propertytype')
            prop = request.POST.get('prop')
            price = request.POST.get('price')
            description = request.POST.get('description')
            status = request.POST.get('status')
            date = request.POST.get('date')

            # Fetch user email from session
            email = request.session.get('email')
            user = models.reg_form.objects.get(email=email)

            # Optional fields with default values
            bedrooms = request.POST.get('bedrooms', 0)
            bathrooms = request.POST.get('bathrooms', 0)
            area_sqft = request.POST.get('area_sqft', 0)
            is_furnished = request.POST.get('is_furnished', False)
            parking_space = request.POST.get('parking_space', False)
            location = request.POST.get('location', '')

            # File Uploads (Handle optional image & document)
            image = request.FILES.get('image', None)
            document = request.FILES.get('document', None)

            # Create Property
            property_obj = models.property.objects.create(
                name=name,
                email=user,
                phone=phone,
                place=place,
                image=image,
                propertytype=propertytype,
                prop=prop,
                price=price,
                description=description,
                status=status,
                date=date,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area_sqft=area_sqft,
                is_furnished=is_furnished == 'True',
                parking_space=parking_space == 'True',
                location=location,
                document=document
            )
            property_obj.save()
            return redirect('home')

        except models.reg_form.DoesNotExist:
            return render(request, 'property.html', {'error': 'User not found! Please log in again.'})
        except Exception as e:
            return render(request, 'property.html', {'error': str(e)})

    return render(request, 'property.html')

from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib import messages  # For success/error messages
def viewproperty(request):
    email=request.session['email']
    data=models.reg_form.objects.get(email=email)
    user=models.property.objects.filter(email=data)
    return render(request,'viewproperty.html',{'user':user})

def edit_property(request, property_id):
    property_obj = get_object_or_404(models.property, id=property_id)

    if request.method == "POST":
        try:
            # Update fields
            property_obj.name = request.POST.get("name", property_obj.name)
            property_obj.description = request.POST.get("description", property_obj.description)
            property_obj.price = request.POST.get("price", property_obj.price)
            property_obj.status = request.POST.get("status", property_obj.status)
            property_obj.place = request.POST.get("place", property_obj.place)
            property_obj.propertytype = request.POST.get("propertytype", property_obj.propertytype)
            property_obj.bedrooms = request.POST.get("bedrooms", property_obj.bedrooms)
            property_obj.bathrooms = request.POST.get("bathrooms", property_obj.bathrooms)
            property_obj.area_sqft = request.POST.get("area_sqft", property_obj.area_sqft)
            property_obj.location = request.POST.get("location", property_obj.location)

            # Boolean fields
            property_obj.is_furnished = request.POST.get("is_furnished") == "True"
            property_obj.parking_space = request.POST.get("parking_space") == "True"

            # Handle optional image upload
            if "image" in request.FILES:
                property_obj.image = request.FILES["image"]

            # Save the updated property
            property_obj.save()
            messages.success(request, "Property updated successfully!")
            return redirect('viewproperty')  # Redirect to property list after saving

        except Exception as e:
            messages.error(request, f"Error updating property: {str(e)}")

    return render(request, "edit_property.html", {"property": property_obj})


# Delete Property
def delete_property(request, property_id):
    property_obj = get_object_or_404(models.property, id=property_id)
    property_obj.delete()
    return redirect('viewproperty')  # Redirect after deletion





from django.shortcuts import render
from django.http import JsonResponse
from groq import Groq
from django.views.decorators.csrf import csrf_exempt
import logging

# Initialize the Groq client with the API key directly
clientt = Groq(
    api_key="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"  # Directly use the API key
)

# Set up logging to capture request details
logger = logging.getLogger(__name__)

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        # Log the incoming request data for debugging
        logger.info(f"Received POST request: {request.POST}")
        
        user_message = request.POST.get('message')

        # Check if the message is empty
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Modify the message depending on the user's input (for example, checking if it's related to real estate)
        prompt = """
        You are a chatbot crafted to tackle all real estate project inquiries. 
        Address every question about properties, buying and selling homes, 
        market trends, rental properties, and beyond with precision. 
        If a query lacks detail or exceeds real estate scope, seek clarification or explain limits briefly. 
        Give accurate, clear, and relevant answers in short, concise sentences.
        """

        # Construct the message for the API
        user_input_message = f"User: {user_message}"

        # Make a request to the Groq API using the SDK
        try:
            chat_completion = clientt.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"{prompt} {user_input_message}",
                }],
                model="llama-3.3-70b-versatile",  # Specify the model to use
            )

            # Extract the chatbot's reply from the response
            chatbot_reply = chat_completion.choices[0].message.content

            return JsonResponse({'response': chatbot_reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'chatbot.html')



from django.shortcuts import render
from django.http import JsonResponse
from groq import Groq
from django.views.decorators.csrf import csrf_exempt
import logging

print('htyr',dir(clientt.chat.completions))
# Set up logging to capture request details
logger = logging.getLogger(__name__)

@csrf_exempt
def chatbot2(request):
    if request.method == "POST":
        # Log the incoming request data for debugging
        logger.info(f"Received POST request: {request.POST}")
        
        user_message = request.POST.get('message')

        # Check if the message is empty
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Modify the message depending on the user's input (for example, checking if it's related to real estate)
        prompt = """
        You are a chatbot crafted to tackle all real estate project inquiries. 
        Address every question about properties, buying and selling homes, 
        market trends, rental properties, and beyond with precision. 
        If a query lacks detail or exceeds real estate scope, seek clarification or explain limits briefly. 
        Give accurate, clear, and relevant answers in short, concise sentences.
        """

        # Construct the message for the API
        user_input_message = f"User: {user_message}"

        # Make a request to the Groq API using the SDK
        try:
            chat_completion = clientt.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"{prompt} {user_input_message}",
                }],
                model="llama-3.3-70b-versatile",  # Specify the model to use
            )

            # Extract the chatbot's reply from the response
            chatbot_reply = chat_completion.choices[0].message.content
            print(chatbot_reply)

            return JsonResponse({'response': chatbot_reply})
            
        except Exception as e:
            print('hh',e)
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'chatbot2.html')

def deleteproperty(request,id):
    
    user=models.property.objects.get(id=id)
    user.delete()
    return redirect('viewproperty')
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings



from django.shortcuts import render, get_object_or_404, redirect
from .models import property, interested  # Import models
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from .models import property, interested, reg_form  

def property_detail(request, property_id):
    prop = get_object_or_404(property, id=property_id)
    usdata = request.session.get('email')  # Get email from session

    if not usdata:
        messages.error(request, "Please log in to express interest.")
        return redirect('login')  

    user1 = reg_form.objects.get(email=usdata)

    if request.method == 'POST':
        # Get checkbox value ('on' if checked, None if unchecked)
        interested_value = request.POST.get('interested')

        # Check if interest record exists
        interest, created = interested.objects.get_or_create(
            user=user1, propertyuser=prop
        )

        # Update interested field based on checkbox state
        interest.interested = bool(interested_value)  # True if checked, False if unchecked
        interest.save()

        messages.success(request, "Your interest has been updated.")
        return redirect('property_detail', property_id=property_id)  # Refresh page

    # Get current interest state for this user & property
    user_interest = interested.objects.filter(user=user1, propertyuser=prop).first()

    return render(request, 'properties_details.html', {
        'property': prop, 
        'user_interest': user_interest
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
import random
from landhub.models import reg_form
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = reg_form.objects.filter(email=email).first()

        if user:
            otp = random.randint(100000, 999999)  # Generate OTP
            request.session["otp"] = otp  # Store OTP in session
            request.session["email"] = email  # Store email in session

            # Send OTP via email with stylish HTML
            subject = "🔐 PrimeLand Hub - Password Reset OTP"
            from_email = "noreply@primelandhub.com"
            recipient_list = [email]

            text_content = f"Your OTP for password reset is: {otp}\nIf you didn’t request this, please ignore this email."

            html_message = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #28a745, #1d7a34);
                        padding: 20px;
                        text-align: center;
                        color: white;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: bold;
                    }}
                    .content {{
                        padding: 30px;
                        text-align: center;
                    }}
                    .otp-box {{
                        background: #e8f4ea;
                        display: inline-block;
                        padding: 15px 25px;
                        border-radius: 8px;
                        font-size: 24px;
                        font-weight: bold;
                        color: #28a745;
                        margin: 20px 0;
                        letter-spacing: 2px;
                        border: 2px dashed #28a745;
                    }}
                    .content p {{
                        font-size: 16px;
                        line-height: 1.6;
                        color: #555;
                    }}
                    .footer {{
                        background: #f8f9fa;
                        padding: 15px;
                        text-align: center;
                        font-size: 14px;
                        color: #777;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .footer a {{
                        color: #28a745;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    .footer a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>PrimeLand Hub</h1>
                    </div>
                    <div class="content">
                        <h2>Password Reset OTP</h2>
                        <p>We’ve received a request to reset your password. Please use the one-time password (OTP) below to proceed:</p>
                        <div class="otp-box">{otp}</div>
                        <p>This OTP is valid for the next 10 minutes. If you didn’t request this, please ignore this email or contact our support team.</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 PrimeLand Hub | <a href="mailto:support@primelandhub.com">Contact Support</a></p>
                    </div>
                </div>
            </body>
            </html>
            """

            send_mail(subject, text_content, from_email, recipient_list, fail_silently=False, html_message=html_message)

            messages.success(request, "✅ OTP sent! Check your inbox.")
            return redirect("password_verify")  # Redirect to OTP verification page
        else:
            messages.error(request, "❌ No account found with that email.")

    return render(request, "forgot_password.html")



from django.shortcuts import render, redirect
from django.contrib import messages

def verify_otp1(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")  # Get OTP from session
        email = request.session.get("email")  # Get stored email

        if stored_otp and str(entered_otp) == str(stored_otp):
            messages.success(request, "OTP Verified! You can now reset your password.")
            return redirect("reset_password")  # Redirect to reset password page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "password_verify.html")




from django.shortcuts import render, redirect
from django.contrib import messages
from landhub.models import reg_form  # Your user model

def reset_password(request):
    if request.method == "POST":
        email = request.session.get("email")  # Get email from session
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not email:
            messages.error(request, "Session expired. Please request OTP again.")
            return redirect("forgot_password")

        user = reg_form.objects.filter(email=email).first()

        if user:
            if new_password == confirm_password:
                user.pwd = new_password  # Save plain text password
                user.save()
                messages.success(request, "Password updated successfully! Please login.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "User not found.")

    return render(request, "reset_password.html")

from django.shortcuts import render
from .models import property  

def property_search(request):
    query = request.GET.get('query', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    properties = property.objects.all()

    if query:
        properties = properties.filter(place__icontains=query)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    return render(request, 'search_results.html', {'properties': properties, 'query': query})


import os
import sys
import django
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Django Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primelandhub.settings")
django.setup()

# Import Django Models
from landhub.models import property, interested

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define Autoencoder Model
class Autoencoder(nn.Module):
    def __init__(self, num_properties):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(num_properties, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, num_properties),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

# Define Model Path
MODEL_PATH = os.path.join(settings.BASE_DIR, "trained_models", "autoencoder.pth")

# Function to check model validity
def check_model_validity():
    properties = property.objects.all()
    interests = interested.objects.all()
    
    if not properties.exists() or not interests.exists():
        return False

    interest_df = pd.DataFrame(list(interests.values('user_id', 'propertyuser_id', 'interested')))
    user_item_matrix = interest_df.pivot_table(index='user_id', columns='propertyuser_id', values='interested', fill_value=0)
    user_item_matrix = user_item_matrix.reindex(columns=[p.id for p in properties], fill_value=0)
    num_properties = user_item_matrix.shape[1]

    if not os.path.exists(MODEL_PATH):
        return False  # No model exists, needs training

    try:
        model = Autoencoder(num_properties).to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=False))
        return True  # Model is valid
    except Exception as e:
        print(f"⚠ Model loading error: {e}")
        return False  # Model shape mismatch, needs retraining

# Function to train autoencoder
def train_autoencoder():
    interests = interested.objects.all()
    interest_df = pd.DataFrame(list(interests.values('user_id', 'propertyuser_id', 'interested')))
    
    if interest_df.empty:
        print("⚠ No user interactions found. Add data first.")
        return

    user_item_matrix = interest_df.pivot_table(index='user_id', columns='propertyuser_id', values='interested', fill_value=0).values
    num_properties = user_item_matrix.shape[1]

    print(f"🔄 Retraining Autoencoder for {num_properties} properties...")

    model = Autoencoder(num_properties).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    for epoch in range(50):
        model.train()
        train_tensor = torch.FloatTensor(user_item_matrix).to(device)
        optimizer.zero_grad()
        output = model(train_tensor)
        loss = criterion(output, train_tensor)
        loss.backward()
        optimizer.step()

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"✅ Model retrained & saved at {MODEL_PATH}")

@csrf_exempt
def hybrid_recommendation(request):
    properties = property.objects.all()
    interests = interested.objects.all()

    if not properties.exists():
        return JsonResponse({'recommendations': []})

    prop_df = pd.DataFrame(list(properties.values('id', 'name', 'description', 'propertytype', 'prop', 'price', 'place', 'image')))
    prop_df.fillna("", inplace=True)

    # Content-Based Filtering (TF-IDF)
    prop_df['features'] = prop_df['name'] + " " + prop_df['description'] + " " + prop_df['propertytype'] + " " + prop_df['prop'] + " " + prop_df['place']
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(prop_df['features'])
    cbf_sim_matrix = cosine_similarity(tfidf_matrix)

    # Collaborative Filtering (Autoencoder)
    if check_model_validity():
        interest_df = pd.DataFrame(list(interests.values('user_id', 'propertyuser_id', 'interested')))
        user_item_matrix = interest_df.pivot_table(index='user_id', columns='propertyuser_id', values='interested', fill_value=0)
        user_item_matrix = user_item_matrix.reindex(columns=prop_df['id'], fill_value=0)
        num_properties = user_item_matrix.shape[1]

        model = Autoencoder(num_properties).to(device)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=False))
        model.eval()

        with torch.no_grad():
            user_item_tensor = torch.FloatTensor(user_item_matrix.values).to(device)
            predicted_matrix = model(user_item_tensor).cpu().numpy()

        cf_sim_matrix = cosine_similarity(predicted_matrix.T)
    else:
        print("⚠ Model is outdated or missing. Retraining...")
        train_autoencoder()
        cf_sim_matrix = np.zeros_like(cbf_sim_matrix)

    # KNN Recommendation
    knn = NearestNeighbors(n_neighbors=min(len(prop_df), 5), metric='cosine', algorithm='brute')
    knn.fit(tfidf_matrix)
    distances, indices = knn.kneighbors(tfidf_matrix)
    knn_sim_matrix = np.zeros_like(cbf_sim_matrix)
    for i in range(len(prop_df)):
        for j, idx in enumerate(indices[i]):
            knn_sim_matrix[i][idx] = 1 - distances[i][j]

    # Hybrid Recommendation
    hybrid_sim_matrix = (0.4 * cbf_sim_matrix) + (0.4 * cf_sim_matrix) + (0.2 * knn_sim_matrix)

    if len(prop_df) < 6:
        return JsonResponse({'recommendations': []})

    random_index = np.random.randint(0, len(prop_df))
    similar_indices = hybrid_sim_matrix[random_index].argsort()[-6:-1]
    recommended_properties = [prop_df.iloc[i]['id'] for i in similar_indices if i < len(prop_df)]
    recommended = property.objects.filter(id__in=recommended_properties)
    
    return JsonResponse({'recommendations': [{'id': p.id, 'name': p.name, 'place': p.place, 'price': p.price, 'image': request.build_absolute_uri(f"/media/{p.image}") if p.image else None} for p in recommended]})

from django.shortcuts import render
import joblib
import pandas as pd
import numpy as np

# Load the trained model and price per sqft averages
model = joblib.load('property_price_model.joblib')
avg_price_per_sqft_by_place = joblib.load('avg_price_per_sqft_by_place.joblib')

def predict_property_price(request):
    predicted_price = None
    error = None

    if request.method == 'POST':
        try:
            # Extract form data
            bedrooms = int(request.POST.get('bedrooms', 0))
            bathrooms = int(request.POST.get('bathrooms', 0))
            area_sqft = float(request.POST.get('area_sqft', 0))
            is_furnished = request.POST.get('is_furnished') == 'on'
            parking_space = request.POST.get('parking_space') == 'on'
            propertytype = request.POST.get('propertytype')
            prop = request.POST.get('prop')
            location = request.POST.get('location')

            # Calculate missing features
            total_rooms = bedrooms + bathrooms
            # Use location-based average for price_per_sqft
            price_per_sqft = avg_price_per_sqft_by_place.get(location, 500)  # Fallback to 500 if location not found

            # Prepare data for prediction
            property_data = {
                'propertytype': propertytype,
                'prop': prop,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqft': area_sqft,
                'is_furnished': 'Yes' if is_furnished else 'No',
                'parking_space': 'Yes' if parking_space else 'No',
                'place': location,  # Map 'location' to 'place'
                'total_rooms': total_rooms,
                'price_per_sqft': price_per_sqft
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([property_data])

            # Predict and reverse log transformation
            log_predicted_price = model.predict(input_df)[0]
            predicted_price = np.expm1(log_predicted_price)  # Convert back to actual price
            print(f"Predicted Price: {predicted_price}")  # Debug

        except Exception as e:
            error = f"Error in prediction: {str(e)}"
            print(f"Error: {error}")  # Debug

    return render(request, 'predict_price.html', {
        'predicted_price': predicted_price,
        'error': error
    })


from django.shortcuts import render
import joblib
import pandas as pd
import numpy as np

# Load the trained model and price per sqft averages
model = joblib.load('property_price_model.joblib')
avg_price_per_sqft_by_place = joblib.load('avg_price_per_sqft_by_place.joblib')

def predict_property_pricebuyer(request):
    predicted_price = None
    error = None

    if request.method == 'POST':
        try:
            # Extract form data
            bedrooms = int(request.POST.get('bedrooms', 0))
            bathrooms = int(request.POST.get('bathrooms', 0))
            area_sqft = float(request.POST.get('area_sqft', 0))
            is_furnished = request.POST.get('is_furnished') == 'on'
            parking_space = request.POST.get('parking_space') == 'on'
            propertytype = request.POST.get('propertytype')
            prop = request.POST.get('prop')
            location = request.POST.get('location')

            # Calculate missing features
            total_rooms = bedrooms + bathrooms
            # Use location-based average for price_per_sqft
            price_per_sqft = avg_price_per_sqft_by_place.get(location, 500)  # Fallback to 500 if location not found

            # Prepare data for prediction
            property_data = {
                'propertytype': propertytype,
                'prop': prop,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area_sqft': area_sqft,
                'is_furnished': 'Yes' if is_furnished else 'No',
                'parking_space': 'Yes' if parking_space else 'No',
                'place': location,  # Map 'location' to 'place'
                'total_rooms': total_rooms,
                'price_per_sqft': price_per_sqft
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([property_data])

            # Predict and reverse log transformation
            log_predicted_price = model.predict(input_df)[0]
            predicted_price = np.expm1(log_predicted_price)  # Convert back to actual price
            print(f"Predicted Price: {predicted_price}")  # Debug

        except Exception as e:
            error = f"Error in prediction: {str(e)}"
            print(f"Error: {error}")  # Debug

    return render(request, 'predictprice buyers.html', {
        'predicted_price': predicted_price,
        'error': error
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Question, Answer, AnswerUpvote, ForumCategory
from landhub.models import reg_form  # Import the reg_form model

from django.shortcuts import render
from .models import Question, ForumCategory
from django.db.models import Count

from django.shortcuts import render
from django.db.models import Count
from .models import Question, ForumCategory, Answer

from django.shortcuts import render
from django.db.models import Count
from .models import Question, ForumCategory, Notification

def forum_home(request):
    """Loads the forum homepage with sorting functionality."""
    
    filter_type = request.GET.get("filter", "recent")
    
    # Fetch questions based on filters
    if filter_type == "recent":
        questions = Question.objects.all().order_by("-created_at")
    elif filter_type == "popular":
        questions = Question.objects.annotate(vote_count=Count("best_answer")).order_by("-vote_count")
    elif filter_type == "most_answered":
        questions = Question.objects.annotate(answer_count=Count("answers")).order_by("-answer_count")
    elif filter_type == "unanswered":
        questions = Question.objects.annotate(answer_count=Count("answers")).filter(answer_count=0).order_by("-created_at")
    else:
        questions = Question.objects.all().order_by("-created_at")

    categories = ForumCategory.objects.all()
    count = questions.count()  # Active discussions count

    # Get unread notifications count
    user_email = request.session.get('email')
    unread_notifications = 0  
    if user_email:
        unread_notifications = Notification.objects.filter(user__email=user_email, is_read=False).count()

    return render(request, "forum/forum.html", {
        "questions": questions,
        "categories": categories,
        "count": count,
        "filter_option": filter_type,
        "unread_notifications": unread_notifications,  # ✅ Pass unread notifications count
    })



def question_detail(request, question_id):
    """Render the question detail page with answers (returns JSON only for AJAX requests)."""
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)

    # If the request is an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response_data = {
            "title": question.title,
            "description": question.description,
            "user": question.user.name,
            "created_at": question.created_at.strftime("%B %d, %Y"),
            "answers": [
                {
                    "id": answer.id,
                    "user": answer.user.name,
                    "content": answer.content,
                    "upvotes": answer.upvotes,
                }
                for answer in answers
            ],
        }
        return JsonResponse(response_data)

    # Otherwise, return the normal HTML page
    return render(request, "forum/question_detail.html", {"question": question, "answers": answers})

def add_question(request):
    """Handles new question submission."""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        category = ForumCategory.objects.get(id=category_id) if category_id else None

        user_email = request.session.get('email')
        user = reg_form.objects.get(email=user_email)

        Question.objects.create(user=user, title=title, description=description, category=category)
        
        return redirect("forum_home")

    categories = ForumCategory.objects.all()
    return render(request, "forum/add_question.html", {"categories": categories})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from .models import Question, Answer, ForumCategory, AnswerUpvote, Notification

def add_answer(request, question_id):
    """Handles new answer submission and sends a notification to the question owner."""
    if request.method == "POST":
        content = request.POST.get("content")

        user_email = request.session.get('email')  # Get current user
        user = reg_form.objects.get(email=user_email)
        question = get_object_or_404(Question, id=question_id)

        # Save the answer
        answer = Answer.objects.create(user=user, question=question, content=content)

        # ✅ Send Notification to the question owner
        Notification.objects.create(
                user=question.user,  # Notify the question owner
                question=question,
                message=f"Your question '{question.title}' has received a new answer!"
            )

        messages.success(request, "Your answer has been posted!")

        return redirect("question_detail", question_id=question.id)

    return render(request, "forum/add_answer.html")

def upvote_answer(request, answer_id):
    """Handles AJAX upvoting of answers."""
    if request.method == "POST":
        user_email = request.session.get('email')
        user = reg_form.objects.get(email=user_email)
        answer = Answer.objects.get(id=answer_id)

        if AnswerUpvote.objects.filter(user=user, answer=answer).exists():
            return JsonResponse({"error": "You have already upvoted this answer."}, status=400)

        AnswerUpvote.objects.create(user=user, answer=answer)
        answer.upvotes += 1
        answer.save()

        return JsonResponse({"message": "Upvote successful!", "upvotes": answer.upvotes})

    return JsonResponse({"error": "Invalid request method."}, status=400)



def notifications(request):
    """Show user notifications."""
    user_email = request.session.get('email')
    user = reg_form.objects.get(email=user_email)

    notifications = Notification.objects.filter(user=user).order_by("-created_at")

    return render(request, "forum/notifications.html", {"notifications": notifications})


def mark_notifications_read(request):
    """Marks all notifications as read."""
    user_email = request.session.get('email')
    user = reg_form.objects.get(email=user_email)

    Notification.objects.filter(user=user, is_read=False).update(is_read=True)

    return JsonResponse({"message": "All notifications marked as read!"})


# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def get_notification_count(request):
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

import os
import magic
from PyPDF2 import PdfReader, generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import pytesseract
from pdf2image import convert_from_bytes
import re
import hashlib
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PropertyForm  # Adjust import
from .models import reg_form, property  # Adjust import

@csrf_exempt
def verify_document(request):
    if request.method != 'POST' or not request.FILES.get('document'):
        return JsonResponse({'status': 'error', 'message': 'POST request with a document file is required.'})

    document = request.FILES['document']
    validation_results = {'checks': {}, 'warnings': [], 'errors': []}

    VALID_EXTENSIONS = ['.pdf']
    MAX_SIZE = 5 * 1024 * 1024
    VALID_MIME_TYPES = ['application/pdf']
    MIN_PAGES = 1
    MAX_PAGES = 50

    ext = os.path.splitext(document.name)[1].lower()
    if ext not in VALID_EXTENSIONS:
        validation_results['errors'].append('Only PDF files are allowed.')
    validation_results['checks']['extension'] = ext

    if document.size > MAX_SIZE:
        validation_results['errors'].append('File size must not exceed 5MB.')
    validation_results['checks']['size'] = document.size

    mime = magic.Magic(mime=True)
    document.seek(0)
    mime_type = mime.from_buffer(document.read(1024))
    if mime_type not in VALID_MIME_TYPES:
        validation_results['errors'].append('Invalid file type. Only PDFs are allowed.')
    validation_results['checks']['mime_type'] = mime_type
    document.seek(0)

    document.seek(0)
    file_hash = hashlib.sha256(document.read()).hexdigest()
    validation_results['checks']['file_hash'] = file_hash
    document.seek(0)

    try:
        pdf = PdfReader(document)
        num_pages = len(pdf.pages)
        if num_pages < MIN_PAGES:
            validation_results['errors'].append('The PDF file is empty or invalid.')
        if num_pages > MAX_PAGES:
            validation_results['errors'].append(f'Maximum {MAX_PAGES} pages allowed.')
        validation_results['checks']['page_count'] = num_pages

        for page in pdf.pages:
            if any(key in page for key in ['/JS', '/JavaScript', '/OpenAction', '/AA']):
                validation_results['errors'].append('PDFs with scripts or auto-actions are not allowed.')
        validation_results['checks']['scripts_detected'] = False

        metadata = pdf.metadata or {}
        doc_title = metadata.get('/Title', '').lower()
        doc_date = metadata.get('/CreationDate', '')
        
        if not doc_title:
            validation_results['warnings'].append('No document title found in metadata.')
        elif not any(keyword in doc_title for keyword in ['property', 'deed', 'title', 'mortgage', 'agreement', 'contract']):
            validation_results['warnings'].append('Document title does not appear related to real estate.')
        validation_results['checks']['title'] = doc_title or 'None'

        if doc_date:
            try:
                year = int(re.search(r'D:(\d{4})', doc_date).group(1))
                if year < datetime.now().year - 5:
                    validation_results['warnings'].append('Document is older than 5 years; verify relevance.')
                validation_results['checks']['creation_year'] = year
            except (AttributeError, ValueError):
                validation_results['warnings'].append('Invalid creation date format in metadata.')
        else:
            validation_results['warnings'].append('No creation date in metadata; freshness unverified.')
        validation_results['checks']['creation_date'] = doc_date or 'None'

        document.seek(0)
        images = convert_from_bytes(document.read())
        text = ""
        for image in images[:1]:
            text += pytesseract.image_to_string(image)

        required_terms = ['property address', 'parcel number', 'legal description', 'owner']
        found_terms = [term for term in required_terms if re.search(term, text, re.IGNORECASE)]
        if len(found_terms) < len(required_terms):
            missing_terms = set(required_terms) - set(found_terms)
            validation_results['warnings'].append(f'Missing real estate terms: {", ".join(missing_terms)}.')
        validation_results['checks']['detected_terms'] = found_terms

        if not re.search(r'transfer.*ownership|deed|title', text, re.IGNORECASE):
            validation_results['warnings'].append('No clear indication of ownership transfer; verify purpose.')

        root_obj = pdf.trailer.get('/Root')
        if isinstance(root_obj, generic.IndirectObject):
            root_obj = pdf.get_object(root_obj)
        acro_form = root_obj.get('/AcroForm') if isinstance(root_obj, dict) else None
        if not acro_form:
            validation_results['warnings'].append('No digital signature detected; signed documents are preferred.')
        validation_results['checks']['has_signature'] = bool(acro_form)

    except Exception as e:
        validation_results['errors'].append(f'PDF processing failed: {str(e)}')

    if validation_results['errors']:
        return JsonResponse({
            'status': 'error',
            'message': 'Document verification failed.',
            'details': validation_results
        })
    elif not found_terms:
        return JsonResponse({
            'status': 'error',
            'message': 'Document lacks any real estate content.',
            'details': validation_results
        })

    file_path = default_storage.save(f'temp/{document.name}', document)
    return JsonResponse({
        'status': 'success' if not validation_results['warnings'] else 'success_with_warnings',
        'message': 'Document verified.' if not validation_results['warnings'] else 'Document verified with warnings.',
        'file_path': file_path,
        'file_hash': file_hash,
        'details': validation_results
    })

@login_required
def submit_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES.get('document')
            if document:
                temp_request = request.__class__(request.POST, {'document': document})
                temp_request.method = 'POST'
                verification_response = verify_document(temp_request)
                
                if verification_response.status_code != 200 or verification_response.json()['status'] == 'error':
                    messages.error(request, verification_response.json()['message'])
                    return render(request, 'property.html', {'form': form, 'verification': verification_response.json()})
                elif verification_response.json()['status'] == 'success_with_warnings':
                    messages.warning(request, 'Document verified with warnings: ' + '; '.join(verification_response.json()['details']['warnings']))

            prop = form.save(commit=False)
            try:
                reg_form_instance = reg_form.objects.get(email=request.user.email)
                prop.email = reg_form_instance
            except reg_form.DoesNotExist:
                if reg_form.objects.exists():
                    prop.email = reg_form.objects.first()
                    messages.warning(request, "Linked to first available profile as fallback.")
                else:
                    messages.error(request, "No registration profile found. Property saved without email link.")
            prop.save()
            messages.success(request, 'Property submitted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Form submission failed. Please correct the errors.')
            return render(request, 'property.html', {'form': form})
    else:
        form = PropertyForm()
    return render(request, 'property.html', {'form': form})

def home(request):
    return render(request, 'home.html')




from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import Buyer
from django.contrib import messages

def Generate_otp():
    return str(random.randint(100000, 999999))

def Register_buyer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        confirmpwd = request.POST.get('confirmpwd')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        gender = request.POST.get('gender')

        if pwd != confirmpwd:
            messages.error(request, "Passwords don't match")
            return redirect('Register_buyer')

        if Buyer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('Register_buyer')

        buyer = Buyer(
            name=name,
            email=email,
            age=age,
            phone=phone,
            place=place,
            gender=gender
        )
        buyer.set_password(pwd)

        otp = Generate_otp()
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['buyer_data'] = {
            'name': name,
            'email': email,
            'pwd': buyer.pwd,
            'age': age,
            'phone': phone,
            'place': place,
            'gender': gender
        }

        try:
            # Plain text version
            plain_message = f'Your OTP for registration at PrimeLand Hub is: {otp}. Please use this code to complete your registration.'

            # Stylish HTML version
            html_message = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #28a745, #1d7a34);
                        padding: 20px;
                        text-align: center;
                        color: white;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: bold;
                    }}
                    .content {{
                        padding: 30px;
                        text-align: center;
                    }}
                    .otp-box {{
                        background: #e8f4ea;
                        display: inline-block;
                        padding: 15px 25px;
                        border-radius: 8px;
                        font-size: 24px;
                        font-weight: bold;
                        color: #28a745;
                        margin: 20px 0;
                        letter-spacing: 2px;
                        border: 2px dashed #28a745;
                    }}
                    .content p {{
                        font-size: 16px;
                        line-height: 1.6;
                        color: #555;
                    }}
                    .footer {{
                        background: #f8f9fa;
                        padding: 15px;
                        text-align: center;
                        font-size: 14px;
                        color: #777;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .footer a {{
                        color: #28a745;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    .footer a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to PrimeLand Hub</h1>
                    </div>
                    <div class="content">
                        <h2>Your OTP for Registration</h2>
                        <p>Thank you for choosing PrimeLand Hub! Please use the one-time password (OTP) below to complete your registration:</p>
                        <div class="otp-box">{otp}</div>
                        <p>This OTP is valid for the next 10 minutes. If you didn’t request this, please ignore this email or contact our support team.</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 PrimeLand Hub | <a href="mailto:support@primelandhub.com">Contact Support</a></p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Send the email with both plain text and HTML versions
            send_mail(
                subject='Your OTP for Registration',
                message=plain_message,  # Plain text fallback
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
                html_message=html_message,  # Stylish HTML version
            )

        except Exception as e:
            messages.error(request, f"Failed to send OTP: {str(e)}")
            return redirect('Register_buyer')

        return redirect('Verify_otpbuyer')
    
    return render(request, 'Register_buyer.html')

def Verify_otp_buyer(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if user_otp == session_otp:
            buyer_data = request.session.get('buyer_data')
            if buyer_data:
                buyer = Buyer.objects.create(**buyer_data)
                buyer.buyer_id = f"B{buyer.id:06d}"
                buyer.save()
                
                request.session.pop('otp', None)
                request.session.pop('buyer_data', None)
                request.session.pop('email', None)
                
                messages.success(request, "Registration successful!")
                return redirect('Login_buyer')
            else:
                messages.error(request, "Session expired. Please register again.")
                return redirect('Register_buyer')
        else:
            messages.error(request, "Invalid OTP")
    
    return render(request, 'Verify_otpbuyer.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Buyer

def Login_buyer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        try:
            buyer = Buyer.objects.get(email=email)
            if buyer.check_password(pwd):  # Assuming pwd is hashed
                request.session['buyer_id'] = buyer.buyer_id  # Keep for your existing logic
                request.session['buyer_pk'] = str(buyer.id)  # Store Buyer.id for chat
                request.session['user_type'] = 'buyer'  # Set user type
                request.session['buyer_email'] = buyer.email  
                
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
        except Buyer.DoesNotExist:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'Login_buyer.html')

def Forgot_password_buyer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            buyer = Buyer.objects.get(email=email)
            otp = Generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            
            try:
                # Plain text version
                plain_message = f'Your OTP for password reset is: {otp}'
                
                # Stylish HTML version
                html_message = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        body {{
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            color: #333;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            background: #ffffff;
                            border-radius: 10px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                            overflow: hidden;
                        }}
                        .header {{
                            background: linear-gradient(135deg, #28a745, #1d7a34);
                            padding: 20px;
                            text-align: center;
                            color: white;
                        }}
                        .header h1 {{
                            margin: 0;
                            font-size: 28px;
                            font-weight: bold;
                        }}
                        .content {{
                            padding: 30px;
                            text-align: center;
                        }}
                        .otp-box {{
                            background: #e8f4ea;
                            display: inline-block;
                            padding: 15px 25px;
                            border-radius: 8px;
                            font-size: 24px;
                            font-weight: bold;
                            color: #28a745;
                            margin: 20px 0;
                            letter-spacing: 2px;
                            border: 2px dashed #28a745;
                        }}
                        .content p {{
                            font-size: 16px;
                            line-height: 1.6;
                            color: #555;
                        }}
                        .footer {{
                            background: #f8f9fa;
                            padding: 15px;
                            text-align: center;
                            font-size: 14px;
                            color: #777;
                            border-top: 1px solid #e0e0e0;
                        }}
                        .footer a {{
                            color: #28a745;
                            text-decoration: none;
                            font-weight: bold;
                        }}
                        .footer a:hover {{
                            text-decoration: underline;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>PrimeLand Hub</h1>
                        </div>
                        <div class="content">
                            <h2>Password Reset OTP</h2>
                            <p>We’ve received a request to reset your password. Please use the one-time password (OTP) below to proceed:</p>
                            <div class="otp-box">{otp}</div>
                            <p>This OTP is valid for the next 10 minutes. If you didn’t request this, please ignore this email or contact our support team.</p>
                        </div>
                        <div class="footer">
                            <p>© 2025 PrimeLand Hub | <a href="mailto:support@primelandhub.com">Contact Support</a></p>
                        </div>
                    </div>
                </body>
                </html>
                """

                send_mail(
                    'Password Reset OTP',
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=html_message,  # Added HTML version
                )
                return redirect('Reset_password_otpbuyer')
            except Exception as e:
                messages.error(request, f"Failed to send OTP: {str(e)}")
                return redirect('Forgot_password_buyer')
        except Buyer.DoesNotExist:
            messages.error(request, "Email not found")
    
    return render(request, 'Forgot_passwordbuyer.html')

def Reset_password_otp_buyer(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('otp'):
            return redirect('Reset_passwordbuyer')
        messages.error(request, "Invalid OTP")
    
    return render(request, 'Reset_password_otpbuyer.html')

def Reset_password_buyer(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        confirmpwd = request.POST.get('confirmpwd')
        
        if pwd == confirmpwd:
            email = request.session.get('email')
            if email:
                try:
                    buyer = Buyer.objects.get(email=email)
                    buyer.set_password(pwd)
                    buyer.save()
                    
                    request.session.pop('otp', None)
                    request.session.pop('email', None)
                    
                    messages.success(request, "Password reset successful!")
                    return redirect('Login_buyer')
                except Buyer.DoesNotExist:
                    messages.error(request, "Session expired or invalid email")
            else:
                messages.error(request, "Session expired. Please start over")
                return redirect('Forgot_password_buyer')
        else:
            messages.error(request, "Passwords don't match")
    
    return render(request, 'Reset_passwordbuyer.html')


from django.shortcuts import render, redirect
from .models import property, Buyer


# Optional: ensures only logged-in users can access
from django.core.exceptions import ObjectDoesNotExist

def dashboard(request):
    # Fetch all available properties for the comparison tool
    properties = property.objects.all()  # Adjust filter as needed (e.g., status='available')

    # Fetch recommended properties for the "Recommended For You" section
    recommended_properties = property.objects.filter(
          # Only show available properties
        prop='sale'          # Example: properties for sale
    ).order_by('-date')[:6]  # Most recent 3 properties

    # Handle buyer info from session
    buyer = None
    buyer_id = request.session.get('buyer_id')  # Retrieve buyer_id from session
    if buyer_id:
        try:
            buyer = Buyer.objects.get(buyer_id=buyer_id)  # Fetch Buyer object
        except ObjectDoesNotExist:
            buyer = None  # Handle case where buyer_id doesn't match any record

    # Alternative: Using Django's built-in authentication (uncomment if applicable)
    # if request.user.is_authenticated:
    #     buyer = request.user  # Assumes Buyer is linked to User or User has name field

    context = {
        'properties': properties,              # For the comparison tool
        'recommended_properties': recommended_properties,  # For "Recommended For You"
        'buyer': buyer,                        # For "Hello, {{ buyer.name }}"
    }

    return render(request, 'dashboard.html', context)


from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import property, Buyer, SavedProperty  # Use lowercase 'property'

def buyer_profile(request):
    """Display the Buyer's Profile with Saved Properties"""
    if 'buyer_id' not in request.session:
        return redirect('Login_buyer')

    buyer_id = request.session['buyer_id']
    try:
        buyer = Buyer.objects.get(buyer_id=buyer_id)
        # Use default reverse relation 'savedproperty_set'
        saved_properties = property.objects.filter(savedproperty__buyer=buyer).order_by('-savedproperty__saved_date')
        
        # Debug print to verify data
        print(f"Buyer: {buyer.name}, Saved properties: {[p.name for p in saved_properties]}")
        
        return render(request, 'buyerprofile.html', {
            'buyer': buyer,
            'saved_properties': saved_properties,
        })
    except Buyer.DoesNotExist:
        del request.session['buyer_id']
        return redirect('Login_buyer')
    except Exception as e:
        print(f"Error in buyer_profile: {str(e)}")
        return HttpResponse("<script>alert('An unexpected error occurred. Please try again later.');window.location.href='/';</script>")




import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import Buyer  # Assuming your model is in models.py

def editprofilebuyer(request):
    # Check if buyer_id exists in session
    if 'buyer_id' not in request.session:
        return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)

    # Get buyer_id from session
    buyer_id = request.session['buyer_id']
    try:
        buyer = Buyer.objects.get(buyer_id=buyer_id)
    except Buyer.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Buyer not found"}, status=404)

    if request.method == 'POST':
        try:
            # Update buyer fields
            buyer.name = request.POST.get('name')
            new_email = request.POST.get('email', '').strip().lower()
            if new_email and new_email != buyer.email:
                # Check if new email is already taken
                if Buyer.objects.filter(email=new_email).exclude(buyer_id=buyer_id).exists():
                    return JsonResponse({"status": "error", "message": "Email already in use"}, status=400)
                buyer.email = new_email
            
            # Handle password update
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password and confirm_password:
                if password != confirm_password:
                    return JsonResponse({"status": "error", "message": "Passwords don't match"}, status=400)
                buyer.set_password(password)  # Using model's set_password method

            buyer.age = request.POST.get('age')
            buyer.phone = request.POST.get('phone')
            buyer.place = request.POST.get('place')
            buyer.gender = request.POST.get('gender') or None  # Handle empty selection

            # Handle image upload
            if 'image' in request.FILES:
                if buyer.image and os.path.isfile(buyer.image.path):
                    os.remove(buyer.image.path)
                buyer.image = request.FILES['image']

            buyer.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"status": "success", "message": "Profile updated successfully"})
            return redirect('dashboard')

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    # For GET request, render the template
    return render(request, 'editprofilebuyer.html', {'buyer': buyer})

def deleteprofilebuyer(request):
    if 'email' in request.session:
        email=request.session['email']
        user=models.Buyer.objects.get(email=email)
        user.delete()
        return redirect('Login_user')
    else:
        return redirect('Login_user')


# from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie  # Optional, if CSRF issues persist
from .models import property, Buyer, SavedProperty  # Adjusted to capitalized model names

# Property Detail View for Buyers
def property_detail_buyer(request, property_id):
    prop = get_object_or_404(property, id=property_id)
    buyer = None
    is_saved = False

    if 'buyer_id' in request.session:
        try:
            buyer = Buyer.objects.get(buyer_id=request.session['buyer_id'])
            is_saved = SavedProperty.objects.filter(buyer=buyer, property=prop).exists()
        except Buyer.DoesNotExist:
            del request.session['buyer_id']
            return redirect('Login_buyer')  # Redirect to login if buyer not found

    print(f"Property {property_id} is_saved: {is_saved}")
    return render(request, 'property_detailbuyer.html', {
        'property': prop,
        'buyer': buyer,
        'is_saved': is_saved,
    })

# Save/Remove Property View
def save_property_buyer(request):
    if 'buyer_id' not in request.session:
        return JsonResponse({"status": "error", "message": "Not authenticated"}, status=401)
    
    if request.method == "POST":
        try:
            buyer = Buyer.objects.get(buyer_id=request.session['buyer_id'])
            property_id = request.POST.get("property_id")
            action = request.POST.get("action")

            if not property_id:
                return JsonResponse({"status": "error", "message": "Property ID is required"}, status=400)
            
            prop = get_object_or_404(property, id=property_id)

            if action == "save":
                saved_property, created = SavedProperty.objects.get_or_create(buyer=buyer, property=prop)
                if created:
                    print(f"Saved {prop.name} for {buyer.name}")
                return JsonResponse({
                    "status": "success",
                    "action": "saved" if created else "already_saved",
                    "property_name": prop.name
                })

            elif action == "remove":
                deleted, _ = SavedProperty.objects.filter(buyer=buyer, property=prop).delete()
                if deleted:
                    print(f"Removed {prop.name} from {buyer.name}'s saved properties")
                    return JsonResponse({
                        "status": "success",
                        "action": "removed",
                        "property_name": prop.name
                    })
                return JsonResponse({"status": "error", "message": "Property not in saved list"}, status=404)

            return JsonResponse({"status": "error", "message": "Invalid action"}, status=400)
        
        except Buyer.DoesNotExist:
            del request.session['buyer_id']
            return JsonResponse({"status": "error", "message": "Buyer not found"}, status=404)
        except property.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Property not found"}, status=404)
        except Exception as e:
            print(f"Error in save_property_buyer: {str(e)}")
            return JsonResponse({"status": "error", "message": "An error occurred"}, status=500)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


        

# Rest of your views remain unchanged
        
def viewpropertybuyer(request):
    properties = property.objects.all()
    return render(request, 'viewpropertiesbuyer.html', {'properties': properties})




from django.shortcuts import render, get_object_or_404
from .models import reg_form, Buyer,Chat
def chat_view(request, seller_id, buyer_id):
    user_type = request.session.get('user_type')
    if not user_type or user_type not in ['seller', 'buyer']:
        return HttpResponse("Unauthorized access", status=403)

    seller_email = request.session.get('email')
    if user_type == 'seller' and seller_email:
        seller = get_object_or_404(reg_form, email=seller_email)
        if seller.id != seller_id:
            return HttpResponse("Unauthorized access", status=403)
    else:
        seller = get_object_or_404(reg_form, id=seller_id)

    buyer = get_object_or_404(Buyer, id=buyer_id)
    messages = Chat.objects.filter(seller=seller, buyer=buyer).order_by('id')  # Use id instead of created_at

    return render(request, 'chat.html', {
        'seller': seller,
        'buyer': buyer,
        'messages': messages,
        'user_type': user_type,
    })
from django.shortcuts import render
from .models import Chat, reg_form
from django.http import HttpResponse

def chat_list(request):
    if request.session.get('user_type') != 'seller':
        return HttpResponse("Unauthorized access", status=403)
    
    seller_email = request.session.get('email')
    if not seller_email:
        return HttpResponse("Seller not logged in", status=401)
    
    try:
        seller = reg_form.objects.get(email=seller_email)
    except reg_form.DoesNotExist:
        return HttpResponse("Seller not found", status=404)
    
    # Get all unique chats involving this seller
    chats = Chat.objects.filter(seller=seller).values('buyer__id', 'buyer__name').distinct().order_by('buyer__name')
    
    return render(request, 'seller_chat_list.html', {
        'seller': seller,
        'chats': chats,
    })

from django.shortcuts import render
from django.http import HttpResponse
from .models import Chat, Buyer, reg_form
import logging

# Set up logging
logger = logging.getLogger(__name__)

def buyer_chat_list(request):
    # Check session user type
    if request.session.get('user_type') != 'buyer':
        return HttpResponse("Unauthorized access", status=403)
    
    buyer_email = request.session.get('buyer_email')
    if not buyer_email:
        return HttpResponse("Buyer not logged in", status=401)
    
    try:
        buyer = Buyer.objects.get(email__iexact=buyer_email.strip().lower())
    except Buyer.DoesNotExist:
        return HttpResponse(f"Buyer not found for email: {buyer_email}", status=404)
    
    # Get distinct sellers the buyer has chatted with
    seller_ids = Chat.objects.filter(buyer=buyer).values_list('seller__id', flat=True).distinct()
    sellers = reg_form.objects.filter(id__in=seller_ids).order_by('name')

    return render(request, 'buyer_chat_list.html', {
        'buyer': buyer,
        'sellers': sellers,  # changed from 'chats' to 'sellers'
    })

# views.py
from django.http import JsonResponse
from .models import property
from django.views.decorators.http import require_GET

@require_GET
def property_search_api(request):
    query = request.GET.get('query', '').strip()
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    properties = property.objects.all()
    if query:
        properties = properties.filter(place__icontains=query)  # Changed to place
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    results = [{
        'id': prop.id,
        'name': prop.name,
        'location': prop.place or 'N/A',  # Use place here too for consistency
        'price': prop.price,
        'image': prop.image.url if prop.image else None,
    } for prop in properties]

    return JsonResponse({'properties': results})





# import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import property as propertymodel

# paypalrestsdk.configure({
#     "mode": settings.PAYPAL_MODE,  # sandbox or live
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_SECRET,
# })
# def create_payment(request, property_id):
#     request.session['property_id'] = property_id  # Store property_id for later use
#     property = propertymodel.objects.get(id=property_id)

#     payment = paypalrestsdk.Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": request.build_absolute_uri(reverse('payment_success')),
#             "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
#         },
#         "transactions": [{
#             "item_list": {
#                 "items": [{
#                     "name": property.name,
#                     "sku": f"property_{property.id}",
#                     "price": str(property.price),
#                     "currency": "USD",
#                     "quantity": 1
#                 }]
#             },
#             "amount": {
#                 "total": str(property.price),
#                 "currency": "USD"
#             },
#             "description": f"Payment for property: {property.name}"
#         }]
#     })

#     if payment.create():
#         for link in payment.links:
#             if link.rel == "approval_url":
#                 return redirect(link.href)
#     else:
#         return render(request, "payment_error.html", {"error": payment.error})

from django.core.mail import send_mail, EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required

# @login_required
# def payment_success(request):
#     payment_id = request.GET.get('paymentId')
#     payer_id = request.GET.get('PayerID')

#     if not payment_id or not payer_id:
#         return render(request, "payment_error.html", {"error": "Payment not completed."})

#     # Retrieve the property
#     property_id = request.session.get('property_id')
#     if not property_id:
#         return render(request, "payment_error.html", {"error": "Property not found."})

#     prop = get_object_or_404(propertymodel, id=property_id)

#     # ✅ Mark property as Sold
#     prop.status = "Sold"
#     prop.save()

#     # ✅ Get Seller & Buyer details
#     seller_email = prop.email.email  # Assuming ForeignKey `reg_form` has an email field
#     buyer_email = request.session.get('buyer_email')  # Assuming the logged-in user is the buyer

#     # ✅ Prepare email content
#     context = {
#         'property': prop,
#         'buyer_name': request.user.username,
#         'seller_name': prop.email.name,  # Assuming `name` exists in `reg_form`
#         'payment_id': payment_id,
#         'payer_id': payer_id
#     }

#     # Render email HTML templates
#     seller_html_message = render_to_string("email_templates/seller_email.html", context)
#     buyer_html_message = render_to_string("email_templates/buyer_email.html", context)

#     # Convert HTML to plain text
#     seller_plain_message = strip_tags(seller_html_message)
#     buyer_plain_message = strip_tags(buyer_html_message)

#     # ✅ Send Email to Seller
#     email_seller = EmailMultiAlternatives(
#         subject="Your Property Has Been Sold!",
#         body=seller_plain_message,
#         from_email="pranavsunny999@gmail.com",
#         to=[seller_email]
#     )
#     email_seller.attach_alternative(seller_html_message, "text/html")
#     email_seller.send()

#     # ✅ Send Email to Buyer
#     email_buyer = EmailMultiAlternatives(
#         subject="Your Purchase Confirmation",
#         body=buyer_plain_message,
#         from_email="pranavsunny999@gmail.com",
#         to=[buyer_email]
#     )
#     email_buyer.attach_alternative(buyer_html_message, "text/html")
#     email_buyer.send()

#     return render(request, "payment_success.html")


# def payment_cancel(request):
#     return render(request, "payment_cancel.html")




from django.http import HttpResponse

def test_buyer_email(request):
    buyer_email = request.session.get('buyer_email')  # ✅ Fetch from session
    if not buyer_email:
        return HttpResponse("No buyer email found! Please check if the user is logged in.")

    send_mail(
        subject="Test Email",
        message="This is a test email from Django.",
        from_email="pranavsunny999@gmail.com",
        recipient_list=[buyer_email],  # ✅ Use session email
        fail_silently=False,
    )
    
    return HttpResponse(f"Test email sent to {buyer_email}!")



import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from razorpay.errors import SignatureVerificationError
from .models import property as propertymodel, Buyer, Payment

client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def create_payment(request, property_id):
    prop = get_object_or_404(propertymodel, id=property_id)
    if prop.status.lower() == "sold":
        return render(request, "already_sold.html", {"property": prop})
    buyer_id = request.session['buyer_email']
    print(buyer_id)  # Debug print to verify buyer_id
    buyer = get_object_or_404(Buyer, email=buyer_id)
    print(buyer)  # Debug print to verify buyer object

    request.session['property_id'] = prop.id
    property_id =request.session['property_id']
    print(f"Property ID from session: {property_id}")

    amount = int(prop.price) * 100  # paise
    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
        "receipt": f"receipt_{prop.id}"
    })

    context = {
        "property": prop,
        "order_id": razorpay_order['id'],
        "razorpay_key": settings.RAZOR_KEY_ID
        ,
        "amount": amount,
        "callback_url": reverse('payment_success'),
        "user": request.user,
    }
    return render(request, "razorpay_payment.html", context)



from razorpay.errors import SignatureVerificationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import property as propertymodel, Buyer, Payment

@csrf_exempt

def payment_success(request):
    if request.method != "POST":
        return redirect("home")

    params = request.POST
    razorpay_payment_id = params.get('razorpay_payment_id')
    razorpay_order_id = params.get('razorpay_order_id')
    razorpay_signature = params.get('razorpay_signature')

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except SignatureVerificationError:
        return render(request, "payment_error.html", {"error": "Signature verification failed."})

    property_id =request.session['property_id']
    print(f"Property ID from session: {property_id}")  # Debug print to verify property_id
    if not property_id:
        return render(request, "payment_error.html", {"error": "Session expired. Property info not found."})

    prop = get_object_or_404(propertymodel, id=property_id)
    buyer_id = request.session['buyer_email']
    buyer = get_object_or_404(Buyer, email=buyer_id)

    # ✅ Lock property
    prop.status = "Sold"
    prop.save()

    # ✅ Store payment
    Payment.objects.create(
        buyer=buyer,
        seller=prop.email,  # Assuming prop.email is reg_form (Seller)
        property=prop,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_order_id=razorpay_order_id,
        amount=prop.price
    )

    # ✅ Email context
    context = {
        'property': prop,
        'buyer_name': buyer.name,
        'seller_name': prop.email.name,
        'payment_id': razorpay_payment_id,
        'order_id': razorpay_order_id
    }

    # ✅ Seller Email
    seller_html = render_to_string("email_templates/seller_email.html", context)
    seller_email = EmailMultiAlternatives(
        subject="Your Property Has Been Sold!",
        body=strip_tags(seller_html),
        from_email="pranavsunny999@gmail.com",
        to=[prop.email.email]
    )
    seller_email.attach_alternative(seller_html, "text/html")
    seller_email.send()

    # ✅ Buyer Email
    buyer_html = render_to_string("email_templates/buyer_email.html", context)
    buyer_email_msg = EmailMultiAlternatives(
        subject="Purchase Confirmation",
        body=strip_tags(buyer_html),
        from_email="pranavsunny999@gmail.com",
        to=[buyer.email]
    )
    buyer_email_msg.attach_alternative(buyer_html, "text/html")
    buyer_email_msg.send()

    return render(request, "payment_success.html")





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Buyer, Payment


def purchase_history(request):
    buyer_id = request.session['buyer_email']
    buyer = get_object_or_404(Buyer, email=buyer_id)

    purchases = Payment.objects.filter(buyer=buyer).order_by('-date')  # Assuming 'date' is a field in Payment model
    
    return render(request, 'purchase_history.html', {
        'buyer': buyer,
        'purchases': purchases
    })



