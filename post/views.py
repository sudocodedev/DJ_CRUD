from django.shortcuts import render
from .form import postForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import post

#read all posts
def postPage(request):
    try:
        posts=post.objects.all()
    except:
        raise "Objects not found, check whether anything is available..."    
    context={'posts':posts}
    return render(request,'post/index.html',context)

#create post
def createPost(request):
    if request.method=="POST":
        form=postForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['title']
            print("{} is created.".format(name))
            form.save()
            return HttpResponseRedirect(reverse('post-page'))
    else:
        form=postForm()
    context={'form':form}
    return render(request,'post/postcreateform.html',context)


#update post
def updatePost(request,postid):
    try:
        upost=post.objects.get(id=postid)
    except:
        raise "Requested post not found!!"
    form=postForm(instance=upost)
    if request.method == "POST":
        form=postForm(request.POST,instance=upost)
        if form.is_valid():
            name=form.cleaned_data["title"]
            print("{} is updated successfully".format(name))
            return HttpResponseRedirect(reverse('post-page'))
    context={'form':form}
    return render(request,'post/index.html',context)


#delete post
def deletePost(request,postid):
    try:
        dpost=post.objects.get(id=postid)
    except:
        raise "Requested post not found!!"
    if request.method=="POST":
        dpost.delete()
        print("post successfully removed!!")
        return HttpResponseRedirect(reverse('post-page'))
    context={}
    return render(request,'post/index.html',context)


#read a post
def detailedPost(request,postid):
    try:
        rpost=post.objects.get(id=postid)
    except:
        raise "Requested object not found!!"
    context={'post':rpost}
    return render(request,'post/singlepost.html',context)



    
