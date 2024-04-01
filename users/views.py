from itertools import chain
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator

from .form import InstagramCopyUserCreationForm
from .models import InstagramCopyUser, FriendRequest

# Create your views here.

class SignUp(generic.CreateView):
    form_class = InstagramCopyUserCreationForm
    success_url = reverse_lazy("users:login")
    template = 'signup.html'

def login(request):
    return render(request, "login.html",{})

@login_required
def profile(request):
    friend_requests = FriendRequest.objects.all()

    current_user = request.user
    followers = FriendRequest.objects.filter(to_user = current_user, status_on_to_user="follower")
    following = FriendRequest.objects.filter(from_user = current_user, status_on_from_user="following")
 
    context = {
        "friend_requests": friend_requests,
        "followers": followers,
        "following": following,
    }

    return render(request,"profile.html", context)


@login_required
def edit_profile(request):
    user =request.user
    print(user.__dict__)
    
    if request.method == 'POST':
        print(request.POST)
        print(user.email) 
        print("old password is: "+request.POST.get('old_password'))
        print("new password is:"+user.password)
        if user.check_password(request.POST.get('old_password')):
            user.set_password(request.POST.get('new_password'))
            user.email = request.POST.get('email')
            user.save()
            messages.info(request, "profile editing is successful!")
            return redirect("users:profile") 
        else:
            messages.info(request, "Password incorrect")
            return render(request, "edit_profile.html",{})
        
    context = {
        "user" : user,
    }
    return render(request, "edit_profile.html",context)


@login_required
def get_user_profile(request, user_id):
    current_user = request.user
    try:
        other_user = InstagramCopyUser.objects.get(id=user_id)
    except InstagramCopyUser.DoesNotExist:
        messages.error(request, "User does not exist!")
        return redirect("home")
  
    friend_request, created = FriendRequest.objects.get_or_create(from_user=current_user, to_user=other_user)
    other_user_status = friend_request.status_on_from_user

    other_user_followers = FriendRequest.objects.filter(to_user=user_id, status_on_to_user="follower")
    other_user_following = FriendRequest.objects.filter(from_user=user_id, status_on_from_user="following")
  
    context = {
        "other_user": other_user,
        "posts": other_user.post_set.all(),
        "friend_request": friend_request,
        "other_user_status": other_user_status,
        "followers": other_user_followers,
        "following": other_user_following,
    }
    return render(request, "other_user_posts.html", context)


@login_required
def user_search(request):
    if request.method == 'POST':
        # name="username" in html, then username is a key in POST
        print(request.POST)
        # 1. get the search text
        input_username = request.POST.get('username')
        print(input_username)
        if input_username:
            try: 
                # 2. find the matching users list
                users = InstagramCopyUser.objects.filter(username__contains=input_username)
                # print(users.count())
    
            # this block looks redundant
            except InstagramCopyUser.ValueError():
                messages.error(request, "Invalid or Error username")
                return redirect("home")

            # 3. return matches
            if users:
                
                context ={
                    "users": users,
                }
                return render(request, "user_search.html",context)
        
        messages.error(request, "Invalid username")
        return render(request,"user_search.html", {})
    
    messages.error(request, "Invalid search")
    return render(request,"user_search.html", {})

@login_required
def send_friend_request(request, other_user_id):
    from_user = request.user

    try:
        to_user = InstagramCopyUser.objects.get(id=other_user_id)
    except InstagramCopyUser.DoesNotExist:
        messages.error(request, "User does not exist!")
        return redirect("users:user_friends_posts_pgntd")

    if from_user != to_user:
        try:
            friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        except FriendRequest.DoesNotExist:
            return redirect("users:get_user_profile", user_id=other_user_id)
        
        if friend_request.to_user==to_user and friend_request.from_user == from_user:
            friend_request.status_on_from_user = "request_sent"
            friend_request.status_on_to_user = "request_received"
            friend_request.save()
                
        if created:
            messages.info(request, "friend request sent")
            return redirect("users:get_user_profile", user_id=friend_request.to_user.id)
        else:
            messages.info(request, "friend request sent")
            return redirect("users:get_user_profile", user_id=friend_request.to_user.id)


@login_required
def unsend_request(request, user_id):
    try:
        user_friend = InstagramCopyUser.objects.get(id=user_id)
    except InstagramCopyUser.DoesNotExist:
        messages.error(request, "User does not exist, please visit other friends' posts!")
        return redirect("users:user_friends_posts_pgntd")
    print("hello")

    try:
       friend_request = FriendRequest.objects.get(from_user=request.user, to_user=user_friend)
    except FriendRequest.DoesNotExist or friend_request.status_on_from_user != 'following':
        messages.info(request, f"You are not following {user_friend}")
        return redirect("users:get_user_profile", user_id=friend_request.to_user.id)

    if friend_request:
        print("hi")
        if friend_request.status_on_from_user == 'request_sent' and friend_request.status_on_to_user == 'request_received':
            friend_request.status_on_from_user = 'follow'
            friend_request.status_on_to_user = 'follow'
            # if friend_request.from_user.friends.get(friend_request.to_user): 
            #     friend_request.from_user.friends.remove(friend_request.to_user) 
            #     messages.info(request, f"you removed {user_friend} from your friend list!")
            friend_request.save()
            friend_request.delete()
            friend_request= None
            messages.info(request, f"Your friend Request for {user_friend} is cancelled!")
            return redirect("users:get_user_profile", user_id=user_friend.id)
        
    return redirect("users:get_user_profile", user_id=user_friend.id)

@login_required
def accept_friend_request(request, other_user_id):
    try: 
        friend_request = FriendRequest.objects.get(from_user=other_user_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        messages.info(request, "Sorry, friend request does not exist!")
        return redirect("users:profile")

    if friend_request.to_user == request.user:
        print(friend_request.from_user.username)
        # friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        # friend_request.delete()  # we are not deleting to get the relationship
        friend_request.status_on_from_user = "following"
        friend_request.status_on_to_user = "follower"
        friend_request.save()
        messages.info(request, "friend request accepted")
        return render(request,"profile.html", {})
    else:
        messages.info(request, "friend request not accepted") 
        return render(request,"profile.html", {})
    
def unfollow(request, user_id):

    try:
        user_friend = InstagramCopyUser.objects.get(id=user_id)
    except InstagramCopyUser.DoesNotExist:
        messages.info(request, "Sorry, user does not exist!")
        return redirect("users:profile")

    try:
       friend_request = FriendRequest.objects.get(from_user=request.user, to_user=user_friend)
    except FriendRequest.DoesNotExist or friend_request.status_on_from_user != 'following':
        messages.info(request, f"You are not following {user_friend}")
        return redirect("users:profile")

    if friend_request:
        if friend_request.status_on_from_user == 'following' and friend_request.status_on_to_user == 'follower':
            friend_request.status_on_from_user = 'follow'
            friend_request.status_on_to_user = 'follow'
            friend_request.from_user.friends.remove(friend_request.to_user) 
            friend_request.save()
            messages.info(request, f"you removed {user_friend} from your friend list!")
            return redirect("users:get_user_profile", user_id=friend_request.to_user.id)
        
    return redirect("users:get_user_profile", user_id=user_id)

    
# without pagination
@login_required
def user_friends_posts(request):
    try:
        friend_requests = FriendRequest.objects.filter(from_user=request.user, status_on_from_user="following")
    except FriendRequest.DoesNotExist:
        messages.info(request, "No posts are available for now, please add more friends")
        return redirect("home")
     
    current_user = request.user 
    front_page_posts = current_user.post_set.order_by('-post_date')
    if friend_requests:
        for friend_request in friend_requests:
            friend_posts = friend_request.to_user.post_set.order_by('-post_date')[:10]
            # print(friend_posts.count())
            front_page_posts = front_page_posts|friend_posts

        context = {
            "friends_posts": front_page_posts,
        }
        return render(request, "friend/user_friends_posts.html", context)
    
    context = {
            "friends_posts": front_page_posts,
        }
   
    return render(request, "friend/user_friends_posts.html", context)

# with pagination
@login_required
def user_friends_posts_pgntd(request):
    try:
        friend_requests = FriendRequest.objects.filter(from_user=request.user, status_on_from_user="following")
    except FriendRequest.DoesNotExist:
        messages.info(request, "No posts are available for now, please add more friends")
        return redirect("home")
     
    current_user = request.user 
    front_page_posts = current_user.post_set.order_by('-post_date')
    
    if friend_requests:
        for friend_request in friend_requests:
            friend_posts = friend_request.to_user.post_set.order_by('-post_date')[:100]
            # print(friend_posts.count())
            front_page_posts = front_page_posts|friend_posts
    

    paginator = Paginator(front_page_posts, per_page =4)

    page_number = request.GET.get("review_page", 1)
    front_page_posts_pgntd = paginator.get_page(page_number)
    context = {
            "friends_posts": front_page_posts_pgntd,
        }  
    return render(request, "friend/user_friends_posts_pgntd.html", context)

