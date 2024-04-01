from django.contrib.auth.forms import UserCreationForm

from .models import InstagramCopyUser

class InstagramCopyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = InstagramCopyUser
        fields = ["username","first_name", "last_name", "email"]