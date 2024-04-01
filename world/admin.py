from django.contrib import admin
from .models import Post, Like, Review, Report, ReportReview, ReportPost

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(ReportReview)
admin.site.register(ReportPost)
