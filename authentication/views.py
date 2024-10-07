from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .forms import userRegisterForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .tokens import account_activation_token
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models.query_utils import Q


def confirmResetPassword(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(id=uid)
    except (ValueError, User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user,token):
        if request.method=='POST':
            form=SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                user.refresh_from_db()
                user.save()
                messages.success(request,"Your password reset process completed successfully🎉. You can go ahead & login now.")
                return redirect('post-page')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
        form=SetPasswordForm(user)
        return render(request, 'post/reset-password.html',{'form':form})
    else:
        messages.error(request,"Link got expired, try again...")

    messages.error(request,"Something went wrong, redirecting to home page!")
    return redirect('post-page')


def resetPassword(request):
    if request.method=='POST':
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            print('im inside validation block')
            user_email=form.cleaned_data.get('email')
            print(user_email)
            get_user=User.objects.filter(Q(email=user_email)).first()
            if get_user:
                print("about to send mail 1")
                mail_subject="Request for Password"
                context = {
                    'user': get_user,
                    'domain': get_current_site(request).domain,
                    'protocol': 'https' if request.is_secure() else 'http',
                    'uid': urlsafe_base64_encode(force_bytes(get_user.id)),
                    'token': account_activation_token.make_token(get_user),
                }
                message=render_to_string('authentication/template_reset_password.html',context)

                reset_email=EmailMessage(mail_subject,message,to=[get_user.email])
                print("about to send mail 2")
                if reset_email.send():
                    print("sent mail")
                    messages.success(request,
                    """
                        Password Reset Mail send:
                            We have mailed you the instructions for password reset 📮, kindly check your inbox or spam folder.
                            If you have not received, pls make sure the credentials which you have entered are correct.
                    """
                    )
                else:
                    messages.error(request,"Sorry😞, we are unable to send password reset mail due to <b>SERVER ISSUE</b>")
        return redirect('post-page')
    form=PasswordResetForm()

    return render(request,'authentication/reset-password.html',{'form':form})



def activate(request, uidb64, token):
    User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError,  ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request,"Awesome!!, your account has been registered successfully 👍🏻")
        return redirect('login-page')
    else:
        messages.error(request,"Activation link was invalid, try again!!")

    return redirect('post-page')

def activateEmail(request, user, to_email):
    mail_subject="Activate your user account"

    context={
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }

    #rendering with custom email template
    message=get_template('authentication/template_activate_account.html').render(context)

    email=EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request,'Dear {user.username}, an email has been sent to {to_email} ✅, kindly click to confirm your account registration')
    else:
        messages.error(request,f"problem in sending mail to {to_email}")

def registerUser(request):
    if request.method == "POST":
        form=userRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.is_active=False
            user.save()
            activateEmail(request,user,form.cleaned_data.get('email'))
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:
        form=userRegisterForm()
    context={'form':form}
    return render(request,'authentication/authentication.html',context)

def loginUser(request):
    #getting user's credentials from the request
    username,password='',''
    if request.method=="POST":
        username=request.POST.get('username','').lower()
        password=request.POST.get('password','').lower()

        #checking whether the user object exists in the DB
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User doesn't exist")

        #Authenticating user credentials
        user=authenticate(request, username=username, password=password)
        print(user)
        print(request)
        if user is not None:
            login(request,user)
            print("{} has been logged in successfully".format(username))
            return redirect('post-page')
        else:
            messages.error(request,"User credentials are invalid!")
    context={'page':'login'}
    return render(request,'authentication/authentication.html',context)

def logoutUser(request):
    logout(request)
    return redirect('post-page')

