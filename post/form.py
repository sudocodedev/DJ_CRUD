from django import forms
from .models import post

class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ["title","genre","ratings","image","content"]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'enter title for your post...'}),
            # 'author': forms.Select(attrs={'placeholder': 'Select Author'}),
            'genre': forms.TextInput(attrs={'placeholder':'enter genre eg. romance,action,comedy,...'}),            
            'ratings': forms.TextInput(attrs={'placeholder':'provide your ratings...'}),            
            # 'content': forms.TextInput(attrs={'placeholder':'start typing...'}),            
        }

