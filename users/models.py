from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class InstagramCopyUser(AbstractUser):
    friends = models.ManyToManyField("InstagramCopyUser", blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(InstagramCopyUser, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(InstagramCopyUser, related_name="to_user", on_delete=models.CASCADE)
    status_on_from_user = models.CharField(default="follow")
    status_on_to_user = models.CharField(default="follow")

    class Meta:
        unique_together = ["from_user", "to_user"]
        constraints = [
            models.CheckConstraint(check=models.Q(status_on_from_user__in =["follow", "request_sent", "request_received", "following", "follower"]), name="friendship_status_on_from_user_check"),
            models.CheckConstraint(check=models.Q(status_on_to_user__in =["follow", "request_sent", "request_received", "following", "follower"]), name="friendship_status_on_to_user_check"),
        ]
