from django.urls import path


from .views import InstagramCopyListView, add_post, view_posts, success, post_detail, delete_post, like_post, add_review, edit_review, delete_review, report_review, add_report, report_post, post_report_list, review_report_list, post_report_detail, review_report_detail, report_approval

app_name = "world"
urlpatterns = [
    path("list", InstagramCopyListView.as_view(), name="list"),
    path("post/add", add_post, name="add_post"),
    path("post/user_all_posts", view_posts, name="view_posts"),
    path("success", success, name="success"),
    # path("post/post_detail/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:post_id>", post_detail, name="post_detail"),
    path("post/delete/<int:post_id>", delete_post, name="delete_post"),
    path("post/view_posts/like", like_post, name="like_post"),
    path("post/add_review/<int:post_id>", add_review, name="add_review"),
    path("post/edit_review/<int:review_id>", edit_review, name="edit_review"),
    path("post/delete_review/<int:review_id>", delete_review, name="delete_review"),
    
    path("report/add_report", add_report, name="add_report"),
    path("report_review/<int:review_id>", report_review, name="report_review"),
    path("report_post/<int:post_id>", report_post, name="report_post"),
    path('reports/posts/list',  post_report_list, name="post_report_list"),
    path('reports/reviews/list',  review_report_list, name="review_report_list"),

    path('reports/post/<int:report_id>', post_report_detail, name="post_report_detail"),
    path('reports/review/<int:report_id>', review_report_detail, name="review_report_detail"),
    path('reports/approval', report_approval, name="report_approval")
    # path("view_posts",user_friends_posts, name="user_friends_posts"),
]

