from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .forms import userRegisterForm

def registerUser(request):
    if request.method == "POST":
        # form=UserCreationForm(request.POST)
        form=userRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            print("New account for {} has been created!".format(user.username))
            user.save()
            login(request,user)
            return redirect('post-page')
    else:
        # form=UserCreationForm()
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
        messages.success(request,"User doesn't exist")
    
    #Authenticating user credentials
    user=authenticate(request, username=username, password=password)
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