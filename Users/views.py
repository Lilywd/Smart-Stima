from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from Users.forms import RegistrationForm, UserAuthenticationForm, UserUpdateForm,ContactForm,NewsletterForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from Users.models import User, SubscribedUsers
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from Users.decorators import user_is_superuser




# Create your views here.

def register(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            messages.error(request,  "Password did not match")
            return redirect ("Users:register")
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exist")
            return redirect ("Users:register")
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exist")
            return redirect ("Users:register")
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
        email=email, password=password1)
        user.save()
        activateEmail(request, user, email)
        return redirect ("Users:signin")
    else: # GET request
        form = RegistrationForm()
        context={'registration_form':form}

    return render(request, 'Users/register.html', context)


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('Users/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user} please go to you email {to_email}inbox and click on \
            received activation link to confirm and complete the registration. Note:Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
   
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/signin')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')


def signin(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.info(request, f"You are now logged in as {user}.")
            return redirect("/")
        else:
            messages.error(request, user, "incorrect credentials")
            return redirect( "Users:signin")
    else:
        return render(request, "Users/signin.html", context)


def signout(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect('/')


@login_required(login_url='/signin')
def profile(request):

	if not request.user.is_authenticated:
			return redirect("signin")

	context = {}
	if request.POST:
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			messages.success(request, 'Your profile has been updated successfully')
			

		else:
			messages.error(request,  "Error")
	else:
		form = UserUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['profile_form'] = form





	return render(request, "Users/profile.html", context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        message = request.POST["message"]
        subject = "Website Inquiry"
        body = {
			'first_name': first_name,
			'last_name': last_name,
			'email': email,
			'message':message
			}
        try:
            from_email = settings.EMAIL_HOST_USER 
            send_mail(subject, message, from_email, ['ndungulilianwanjiku@gmail.com'], fail_silently=True)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        messages.success(request, "Message sent")
        return redirect ('/')    
    form = ContactForm()
    return render(request, 'Users/contact.html', {'form':form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_Users = User.objects.filter(Q(email=data))
			if associated_Users.exists():
				for user in associated_Users:
					subject = "Password Reset Requested"
					email_template_name = "Users/passwords/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':get_current_site(request).domain,
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="Users/passwords/password_reset.html", context={"password_reset_form":password_reset_form})



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must type legit name and email to subscribe to a Newsletter")
            return redirect("/")
        
        if User.objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/")) 

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))

@user_is_superuser
def newsletter(request):
	if request.method == 'POST':
		form = NewsletterForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data.get('subject')
			receivers = form.cleaned_data.get('receivers').split(',')
			email_message = form.cleaned_data.get('message')

			mail = EmailMessage(subject, email_message, f"PyLessons <{request.user.email}>", bcc=receivers)
			mail.content_subtype = 'html'

			if mail.send():
				messages.success(request, "Email sent succesfully")
			else:
				messages.error(request, "There was an error sending email")

		else:
			for error in list(form.errors.values()):
				messages.error(request, error)

		return redirect('/')

  
	form = NewsletterForm()
	form.fields["receivers"].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
	return render(request=request, template_name='Users/newsletter.html', context={"form": form})


def social_login(request):
    
    return render(request,'social_login.html')