from django import forms

from .models import Post, Review, Report

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "description", "image"]

class ReviewForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'place-holder': 'comment here !',
            'rows': 4,
            'cols': 50,
        }
    ))
    class Meta:
        model = Review
        fields = ['content']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['category', 'text']