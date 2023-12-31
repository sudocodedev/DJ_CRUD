from django import forms
from .models import post

class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ["title","tags","image","content"]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'New post title here...'}),      
        }

