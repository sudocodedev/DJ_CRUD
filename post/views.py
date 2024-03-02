from django.core import serializers
from django.shortcuts import redirect, render
from .form import postForm, profileForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from .models import post,comments
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.serializers.json import Serializer


#create profile for the user
def UserProfile(request):
    if request.method == "POST":
        form=profileForm(request.POST, request.FILES)
        if form.is_valid():
            holder=form.save(commit=False)
            holder.user=request.user
            holder.save()
            return redirect('post-page')
    else:
        form=profileForm()
    context={'form':form}
    return render(request,"post/profileform.html",context)

#custom serializer for comment section
class CommentSerializer(Serializer):
    """custom serializer for comment section"""
    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk': continue
            elif field in self._current.keys(): continue
            else:
                try:
                    self._current[field]=getattr(obj,field)() #for model method
                    continue
                except TypeError: pass

                try:
                    self._current[field].getattr(obj,field) #for property method
                    continue
                except AttributeError: pass

        super(CommentSerializer, self).end_object(obj)

#Loads all the comments for a requested post
def LoadComments(request,postid):
    targetPost=post.objects.get(id=postid)
    queryset=targetPost.comments.all()
    serializers=CommentSerializer()
    serialized_data=serializers.serialize(queryset,use_natural_foreign_keys=True,fields=['post','user','body','comment_posted','str_comment_posted'])
    return JsonResponse(serialized_data,safe=False,status=200)

#post the comment for the corresponding post
@login_required(login_url='login-page')
def PostComment(request,postid):
    if request.method=='POST':
        targetPost=post.objects.get(id=postid)
        text=request.POST.get('text')
        comment=comments.objects.create(post=targetPost,body=text,user=request.user)
        comment.save()
        return JsonResponse({'status':'success'})
    return JsonResponse({'status':'error'})

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
            holder=form.save(commit=False)
            holder.author=request.user
            name=form.cleaned_data['title']
            print("{} is created.".format(name))
            holder.save()
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
            form=postForm(request.POST,request.FILES,instance=upost)
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
        user_info=request.user.id
    except:
        raise "Requested post not found!!"
    context={'post':detailed_post,'user_info':user_info}
    return render(request,'post/singlepost.html',context)


          


    
