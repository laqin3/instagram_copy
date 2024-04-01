from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.


# posts
class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.TextField(null=True)
    description = models.TextField()
    image = models.ImageField(null=False)
    liked = models.ManyToManyField(get_user_model(), related_name='liked', default=None, blank=True)

    post_date = models.DateTimeField(editable=False, auto_now_add=True)
    last_modified_date = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.user.email} - {self.title}"

    def get_post_date(self):
        time = datetime.now()
        if self.post_date.year == time.year and self.post_date.month == time.month and self.post_date.day == time.day and self.post_date.hour == time.hour:
            return str(abs(time.minute - self.post_date.minute)) +"m"
        elif self.post_date.year == time.year and self.post_date.month == time.month and self.post_date.day == time.day and self.post_date.hour != time.hour:
            return str(abs(time.hour - self.post_date.hour)) +"h " + str(abs(time.minute - self.post_date.minute)) +"m"
        elif self.post_date.year == time.year and self.post_date.month == time.month and self.post_date.day != time.day:
            return str(abs(time.day - self.post_date.day)) +"d"
        elif self.post_date.year == time.year and self.post_date.month != time.month:
            if (time.day - self.post_date.day) > 30:
                return str(abs(time.month - self.post_date.month))+"m "+str(abs(time.day - self.post_date.day)) +"d"
            else:
                return str(abs(time.day - self.post_date.day)) +"d"
        else:
            if (time.month - self.post_date.month) > 12:
                return str(abs(time.year - self.post_date.year)) +"year"
            else:
                return str(abs(time.year - self.post_date.year)) +"year"+ str(abs(time.month - self.post_date.month))+"m"
            
        
    
    @property    
    def num_likes(self):
        return self.liked.all().count()
        
LIKE_CHOICE = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)        

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICE, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)

# review
class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),null=True, on_delete=models.CASCADE)
    
    title = models.CharField(blank=True)
    content = models.TextField(blank=True)

    original_date = models.DateTimeField(editable=False, auto_now_add=True)
    last_modified_date = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"{self.post.id} - {self.content}"
    
class Report(models.Model):
    text = models.CharField(max_length=300)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category}"
    
class ReportReview(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report_text = models.CharField(max_length=300)
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.report.category} - to {self.review.id} - by {self.user.username}"
    
    class Meta:
        unique_together = ["review", "user"]

class ReportPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    report_text = models.CharField(max_length=300)
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.report.category} - to {self.post.id} - by {self.user.username}"
    
    class Meta:
        unique_together = ["post", "user"]
