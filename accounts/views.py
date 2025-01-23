from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            # create user to the database by using above fields
            user = Account.objects.create_user(first_name= first_name, last_name= last_name, email= email, username=username, password=password)
            # In model we are not giving phone number to create user so we did not pass in the user but we are adding below after creating the user
            user.phone_number = phone_number  # so that it will update the user object in DB.
            user.save()
            
            # USER ACTIVATION
            # TODO: Send email verification link to the user
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            # here we provide template/content of the message body
            message = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to = [to_email])
            send_email.send()
              
            # TODO: Redirect to a verification page
            
            # messages.success(request, 'Thank you for registering, We have sent you a verification link. Please Verify.')
            return redirect('/accounts/login/?command=verification&email='+email)  # Redirect to the login page or success page
            
            # messages.success(request, 'Registration successful.')
            # return redirect('register') 
        # If form is invalid, errors will be displayed in the template      
    else:
        form = RegistrationForm() # Here it is GET request in else case, so registration form should render
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context) 

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f'this is my email:{email} and {password}')

        # Authenticate using email (since email is used as the username here)
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in
             # Clear any existing messages before adding the success message
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')  # Redirect to the home page or dashboard
        
        else:  # If authentication fails
            messages.error(request, 'Invalid login credentials')
            return redirect('login')  # Stay on the login page
    return render(request, 'accounts/login.html')  # Render the login page for GET requests

@login_required(login_url='login')
def logout_view(request):
    # Explicitly clear all messages before logging out
    storage = messages.get_messages(request)
    storage.used = True  # Mark messages as processed to avoid duplication
    
    logout(request) # Log out the user
    messages.success(request, 'You are now logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congradulation! Your account has been activated.')
        return redirect('login')  # Redirect to the login page or success page
    else:
        messages.error(request, 'The activation link is invalid.')
        return redirect('login')  # Stay on the login page

@login_required(login_url='login')  # this means when we logged in then only it should show dashboard   
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user =Account.objects.get(email__exact=email)   # __iexact is 
            
            # Reset forgot password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'We have sent you a password reset link. Please check your email.')
            return redirect('login')
        else:
            messages.error(request, 'Email does not exist in our records.')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
         request.session['uid'] = uid  # from here i can access the session whlie i am resetting the password
         messages.success(request, 'Please reset your password')
         return redirect('resetPassword')
    else:
        messages.error(request, 'The password reset link is invalid or expired.')
        return redirect('login')
        

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            uid = request.session.get('uid')  # Retrieve `uid` from session
            if uid:
                try:
                    user = Account.objects.get(pk=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('login')  # Redirect to login after reset
                except Account.DoesNotExist:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Session expired. Please try again.')
        else:
            messages.error(request, 'Passwords do not match.')

        return redirect('resetPassword')  # Redirect back to the same page for corrections
    else:
        return render(request, 'accounts/resetPassword.html')  # Render the template on GET
        