from django.shortcuts import redirect, render
from .form import postForm
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import post
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#read all posts
def postPage(request):
    try:
        #copy get request in a placeholder
        cache=request.GET
        
        #getting the query parameters
        sort=cache.get('sort') if cache.get('sort') != None else ''
        search=cache.get('search') if cache.get('search') != None else ''
        genre=cache.get('genre') if cache.get('genre') != None else ''
        print(search,genre)
        #query the db model
        posts=post.objects.filter(
            Q(genre__icontains=genre) |
            Q(author__username__icontains=search) |
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )
        
        #sorting posts based on sort param based in get request
        if sort=="1": posts=posts.order_by("ratings")
        if sort=="-1": posts=posts.order_by("-ratings")

        posts_count=posts.count() if genre != '' else False
        print(posts_count)
    except:
        raise "Objects not found, check whether anything is available..."    
    context={'posts':posts,'post_count':posts_count}
    return render(request,'post/index.html',context)

#create post
@login_required(login_url='login-page')
def createPost(request):
    if request.method=="POST":
        form=postForm(request.POST,request.FILES)
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
@login_required(login_url='login-page')
def updatePost(request,postid):
    try:
        upost=post.objects.get(id=postid)
    except:
        raise "Requested post not found!!"
    form=''
    if request.user == upost.author:
        form=postForm(instance=upost)
        if request.method=="POST":
            form=postForm(request.POST,instance=upost)
            if form.is_valid():
                form.save() #saving it to DB
                name=form.cleaned_data["title"]
                print("{} has been updated successfully!!".format(name))
                return HttpResponseRedirect(reverse('post-page'))
    else:
        return redirect("You are not allowed here!")
    context={'form':form}
    return render(request,'post/postcreateform.html',context)

#delete post
@login_required(login_url='login-page')
def deletePost(request,postid):
    try:
        dpost=post.objects.get(id=postid)
    except:
        raise "Requested post not found!!"
    print("{} is deleted...".format(dpost.title))
    dpost.delete()
    return HttpResponseRedirect(reverse('post-page'))

#detailed post
def detailedPost(request,postid):
    try:    
        detailed_post=post.objects.get(id=postid)
    except:
        raise "Requested post not found!!"
    context={'post':detailed_post}
    return render(request,'post/singlepost.html',context)


          


    