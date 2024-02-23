from django import forms
from .models import post, GenreList, UserProfile
from django.forms.widgets import SelectMultiple
from tinymce.widgets import TinyMCE

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
            'image': forms.ClearableFileInput(attrs={'id': "post-pic-input", 'accept': "image/*"}),
        }

class profileForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instagram'].label=""
        self.fields['x'].label=""
        self.fields['telegram'].label=""
        self.fields['github'].label=""
    class Meta:
        model = UserProfile
        exclude = ["user","followers","doj"]
        widgets = {
            'firstName': forms.TextInput(attrs={'placeholder': 'eg. Naruto'}),
            'lastName': forms.TextInput(attrs={'placeholder': 'eg. Uzumaki'}),
            'instagram': forms.TextInput(attrs={'placeholder': 'your instagram URL'}),
            'x': forms.TextInput(attrs={'placeholder': 'your x URL'}),
            'github': forms.TextInput(attrs={'placeholder': 'your github URL'}),
            'telegram': forms.TextInput(attrs={'placeholder': 'your telegram URL'}),
            'pronoun': forms.TextInput(attrs={'placeholder': 'eg. He/Him, She/Her...'}),
            'location': forms.TextInput(attrs={'placeholder': 'eg. State/ Country'}),
            'bio': TinyMCE(
                mce_attrs={
                    'toolbar': 'bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent',
                }
            ),
            'profileImg': forms.ClearableFileInput(attrs={'id': "profile-pic-input", 'accept': "image/*"}),
            'profileBackground': forms.ClearableFileInput(attrs={'id': "bg-pic-input", 'accept': "image/*"}),
        }
