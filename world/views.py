from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm, ReviewForm, ReportForm
from .models import Post, Like, Review, Report, ReportReview, ReportPost
# Create your views here.


class InstagramCopyListView(ListView):
    template_name = "list.html"
    model = Post
    

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post_form = form.save(commit=False)

            post_form.user = request.user
            post_form.save()

            return redirect("world:view_posts")
    else:
        form = PostForm()

    context = {
        "form":form,
    }
    return render(request, "post/add.html", context)

def success(request):
    return HttpResponse('Successfully created')

@login_required
def view_posts(request):
   
    if request.method == 'GET':
        
        posts = Post.objects.filter(user=request.user)

        context = {
            "posts": posts,
        }

        return render(request, "post/current_user_posts.html", context)
    
@login_required
def view_other_user_posts(request, user_id):
    
    if request.method == 'GET':
        
        try:
            posts = Post.objects.filter(user=user_id)
        except Post.DoesNotExist:
            messages.error(request, "Sorry, user does not have posts yet")
            redirect("users:user_friends_posts_pgntd")

        other_user = user_id

        context = {
            "posts": posts,
            "user_id": other_user,
        }

        return render(request, "other_user_posts.html", context)   


class PostDetailView(DetailView):
    template_name = "post/post_detail.html"
    model = Post

# we are using the above DetailVeiw instead of the below post_detatil
def post_detail(request, post_id):
     if request.method == 'GET':
        # post = get_object_or_404(Post, pk=post_id)
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            messages.error(request, "Invalid request!")
            return redirect("users:profile")

        context = {
            "post": post,
        }

        return render(request, "post/post_detail.html", context)

@login_required     
def delete_post(request, post_id):
    user = request.user

    try:
        image= Post.objects.get(user=user, id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "Invalid Request")
        return redirect("world:view_posts")
   
    if image:
        Post.objects.filter(user=user, id=post_id).delete()
        messages.success(request, "Image removed from your list")
        return redirect("users:profile")

 

@login_required
def like_post(request):
    current_user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_like')
        print(post_id)
       
        post_obj = Post.objects.get(id=post_id)


        if current_user in post_obj.liked.all():
            post_obj.liked.remove(current_user)
        else:
            post_obj.liked.add(current_user)

        like, created = Like.objects.get_or_create(user=current_user, post=post_obj)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
        
        # return redirect("users:user_friends_posts")
        return redirect("world:post_detail", post_id=post_id)
    
    return redirect("users:user_friends_posts_pgntd")

# not able to click successfully on like icon without refreshing page
@login_required
def like_post_with_ajax(request):
    like_icon = 'favorite'
    unlike_icon = 'favorite_border'

    current_user = request.user
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        post_obj = get_object_or_404(Post, id=post_id)

        if current_user in post_obj.liked.all():
            post_obj.liked.remove(current_user)
        else:
            post_obj.liked.add(current_user)

        like, created = Like.objects.get_or_create(user=current_user, post=post_obj)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
                result = unlike_icon
            else:
                like.value = 'Like'
                result = like_icon

        like.save()
    return JsonResponse({'result': result, 'unlike':unlike_icon})

@login_required
def add_review(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        
        if form.is_valid:
            print("hi")
            # actually the below review_form is a new review object
            review_form = form.save(commit=False)

            review_form.user = request.user
            review_form.post = post

            review_form.save()
            # return redirect(post.get_absolute_url())
            return redirect("world:post_detail", post_id=post_id)
        
    else: 
        form = ReviewForm()

    context = {
        "form" : form,
        "post" : post,
    }
    return render(request, "review/add.html", context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, user=request.user, pk=review_id)

    # instance!!
    form = ReviewForm(request.POST or None, instance=review)
        
    if request.method == 'POST':
        if form.is_valid:         
            form.save()
            messages.info(request, "Comment updated successfully!")
            return redirect("world:post_detail", post_id=review.post.id)
    
    context = {
        "form": form,
        "review": review,
    }
    return render(request, "review/edit.html", context)

@login_required
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return redirect("world:post_detail", post_id=review.post.id) 
    
    review.delete()
    review.save()
    messages.info(request, "review is deleted successfully!")
    return redirect("world:post_detail", post_id=review.post.id)

# only admin can add new report name
@login_required()
def add_report(request):

    form = ReportForm()
    if request.method == 'POST':
        report_form = ReportForm(request.POST or None)

        if report_form.is_valid:
            form = report_form
            form.save()
            return redirect("home")

    context= {
        "form": form
    }
    return render(request, "report/add_report.html", context)


@login_required
def report_review(request, review_id):

    # review = get_object_or_404(Review, pk=review_id)
    try: 
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
         messages.error(request, "Review does not exist anymore!")
         return redirect("users:user_friends_posts_pgntd")
   
    if request.method == 'POST':
        report = Report.objects.get(category=request.POST.get("report"))
        
        report_text = report.text
        report_category = report.category
        try:
            report_review = ReportReview.objects.get(user= request.user, review=review)
            
        except ReportReview.DoesNotExist:
            report_review = ReportReview.objects.create(user= request.user, review=review, report = report, report_text = report_text, category=report_category)
            report_review.save()
            messages.info(request,"Your report is saved, thank you!")
            return redirect("world:post_detail", post_id=review.post.id)
        
        
    messages.info(request, "You have already reported this review")
    return redirect("world:post_detail", post_id=review.post.id)

@login_required
def report_post(request, post_id):
    try:
       post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.info(request, "This post does not exist yet anymore!")
        return redirect("users:user_friends_posts_pgntd")
    
    if request.method == 'POST':
        report_category = request.POST.get("report")
        report = Report.objects.get(category=report_category)
        try:
            report_post = ReportPost.objects.get(user=request.user, post=post)
        except ReportPost.DoesNotExist:
            report_post = ReportPost.objects.create(
                post=post,
                report = report,
                user = request.user,
                report_text = report.text,
                category = report_category
            )
            report_post.save()
            messages.info(request, "You reported the current post successfully, thank you!")
            return redirect("world:post_detail", post_id=post_id)
        
    messages.info(request, "You already have a report about the current post, thank you!")
    return redirect("world:post_detail", post_id=post_id)
 

@login_required
def post_report_list(request):
    
    post_reports = ReportPost.objects.all()
    context = {
        'post_reports': post_reports,
    }
    return render(request, "report/post_report_list.html", context)

def review_report_list(request): 
    review_reports = ReportReview.objects.all()

    context = {
        'review_reports': review_reports,
    }
    return render(request, "report/review_report_list.html", context)


@login_required
def post_report_detail(request, report_id):
    print("post url ")
    print(request.build_absolute_uri())
    try:
        report = ReportPost.objects.get(pk=report_id)
    except ReportPost.DoesNotExist:
        messages.error(request, "Invalid request!")
        return redirect("world:post_report_list")
    print(report)

    context = {
        "type": "Post",
        "report": report,
    }
    return render(request, "report/view_report.html", context)



@login_required
def review_report_detail(request, report_id):
    try:
        report = ReportReview.objects.get(pk=report_id)
    except ReportReview.DoesNotExist:
        messages.error(request, "Invalid request!")
        return redirect("world:review_report_list")
    print("report is ")
    print(report)
    
    context = {
        "type": "Review",
        "report": report,
    }

    return render(request, "report/view_report.html", context)

@login_required
def report_approval(request):
    if request.method == 'POST':
        if  'post_id' in request.POST:
            print("it is a post")
            post_id_text = request.POST.get('post_id')
            post_id = post_id_text[12:]
            try:
                image= Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                messages.error(request, "Invalid Request")
                return redirect("world:post_report_list")
        
            if image:
                Post.objects.filter(id=post_id).delete()
                messages.success(request, f"Image {post_id} removed successfully!")

            return redirect("world:post_report_list")
        

        elif 'review_id' in request.POST:
            print("it is a review.")   
            review_id_text = request.POST.get('review_id')
            review_id = review_id_text[12:]

            try:
                review = Review.objects.get(id=review_id)
            except Review.DoesNotExist:
                return redirect("world:review_report_list", post_id=review.post.id) 

            if review:
                Review.objects.get(id=review_id).delete()
                messages.info(request, f"review {review_id} is deleted successfully!")   
                return redirect("world:review_report_list")
        
    messages.info(request, "Invalid request!")
    return redirect("home")
    




    


# below code is failing at line 316 => user_friend_requests = user.friendrequest_set.all()
# @login_required
# def user_friends_posts(request):

#     user = request.user
#     front_page_posts = user.post_set.order_by('-post_date')
    
#     user_friend_requests = user.friendrequest_set.all()

#     for friend_request in user_friend_requests:
#         if friend_request.from_user == user and friend_request.status_on_from_user=="following":
#             friend_posts = friend_request.to_user.post_set.order_by('-post_date')[:10]
#             # print(friend_posts.count())
#             front_page_posts = front_page_posts|friend_posts
#         context = {
#                 "friends_posts": front_page_posts,
#             }
#         return render(request, "friend/user_friends_posts.html", context)
    
#     context = {
#             "friends_posts": front_page_posts,
#         }
   
#     return render(request, "friend/user_friends_posts.html", context)










    
