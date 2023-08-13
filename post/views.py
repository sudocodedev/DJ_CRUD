from django.shortcuts import render
from .form import postForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import post

def postPage(request):
    try:
        posts=post.objects.all()
    except:
        raise "Objects not found, check whether anything is available..."    
    context={'posts':posts}
    return render(request,'post/index.html',context)

def createPost(request):
    if request.method=="POST":
        form=postForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['title']
            print("{} is created.".format(name))
            return HttpResponseRedirect(reverse('home-page'))
    else:
        form=postForm()
    context={'form':form}
    return render(request,'post/postcreateform.html',context)
