from django import forms
from .models import post, GenreList
from django.forms.widgets import SelectMultiple

class Select2MultipleWithPlaceholder(SelectMultiple):
    def __init__(self, placeholder=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['data-placeholder'] = placeholder

class postForm(forms.ModelForm):
    
    tags= forms.ModelMultipleChoiceField(
        queryset=GenreList.objects.all(),
        widget=Select2MultipleWithPlaceholder(placeholder='Select genre(s) for your post'),
    )

    class Meta:
        model = post
        fields = ["image","title","tags","content"]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'New post title here...'}),      
        }

