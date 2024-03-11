from django.shortcuts import redirect, render, get_object_or_404
from .form import postForm, profileForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from .models import post,comments,UserProfile
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.serializers.json import Serializer
from django.contrib.auth.models import User

def UserProfileView(request, profileid):
    uprofile=UserProfile.objects.get(id=profileid)
    l_user=User.objects.get(id=uprofile.user.id)
    following=l_user.following.count()

    #User Stats
    post_liked=l_user.liked_post.count()
    post_commented=l_user.comments.count()
    post_bookmarked=l_user.bookmarked_post.count()
    likes_received=l_user.post_set.aggregate(tot_likes=Count('likes'))
    comments_received=l_user.post_set.aggregate(tot_comments=Count('comments'))
    followers=uprofile.followers.count()
    post_published=l_user.post_set.count()

    stats = {
        'post_liked': post_liked,
        'post_commented': post_commented,
        'post_bookmarked': post_bookmarked,
        'likes_received': likes_received['tot_likes'],
        'comments_received': comments_received['tot_comments'],
        'followers': followers,
        'post_published': post_published,
    }

    context={'user': uprofile, 'following': following, 'stats': stats}
    return render(request,'post/profileview.html',context)

def top3Posts(request):
    queryset=post.objects.annotate(nums_likes=Count('likes')).order_by('-nums_likes')[:3].values('id','title','nums_likes')
    return JsonResponse({'picks': list(queryset)},safe=False)

#like post
@login_required(login_url='login-page')
def likePost(request, postid):
    post_likes=get_object_or_404(post,id=postid)
    if request.user in post_likes.likes.all():
        liked=False
        post_likes.likes.remove(request.user)
    else:
        liked=True
        post_likes.likes.add(request.user)
    return JsonResponse({'liked':liked, 'like_count':post_likes.likes.count()})

#bookmark a post for future reference
@login_required(login_url='login-page')
def bookMarkPost(request, postid):
    post_bookmark=get_object_or_404(post,id=postid)
    if request.user in post_bookmark.bookmark.all():
        bookmarked=False
        post_bookmark.bookmark.remove(request.user)
    else:
        bookmarked=True
        post_bookmark.bookmark.add(request.user)
    return JsonResponse({'bookmarked':bookmarked,'bookmark_counts': post_bookmark.bookmark.count()})


#create profile for the user
@login_required(login_url='login-page')
def CreateUserProfile(request):
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

#edit user profile
# @login_required(login_url='login-page')
def EditUserProfile(request,profileid):
    uprofile=UserProfile.objects.get(id=profileid)
    form=profileForm(instance=uprofile)
    if request.method=="POST":
        form=profileForm(request.POST,request.FILES,instance=uprofile)
        if form.is_valid():
            form.save() #saving it to DB
            return HttpResponseRedirect(reverse('post-page'))
    context={'form':form,'profile':uprofile, 'action': 'edit'}
    return render(request,'post/profileform.html',context)

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
    cache=request.GET #copy get request in a placeholder
    #getting the query parameters
    search=cache.get('search') if cache.get('search') != None else ''
    genre=cache.get('genre') if cache.get('genre') != None else ''
    #query the db model
    posts=post.objects.filter(
        Q(genre__icontains=genre) |
        Q(author__username__icontains=search) |
        Q(title__icontains=search) |
        Q(content__icontains=search)
    )
    l_user=User.objects.get(id=request.user.id)
    uprofile=UserProfile.objects.get(user=l_user)
    following=User.objects.get(id=uprofile.user.id).following.count()
    context={'posts':posts, 'profile':uprofile, 'following':following}
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
    context={'form':form,'post':upost, 'action': 'edit'}
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
        queryset=detailed_post.comments.count()
        user_info=request.user.id    
    except:
        raise "Requested post not found!!"
    context={
        'post':detailed_post,
        'user_info':user_info,
        'comments_count':queryset,
        }
    return render(request,'post/singlepost.html',context)

def statusCheck(request,postid):
    try:
        detailed_post=post.objects.get(id=postid)
        like_check= True if request.user in detailed_post.likes.all() else False;
        bookmark_check= True if request.user in detailed_post.bookmark.all() else False;
    except:
        raise "post not found!!"
    return JsonResponse({'like_check':like_check, 'bookmark_check': bookmark_check})


    
