from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class userRegisterForm(UserCreationForm):
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'placeholder': 'enter your email...','class': 'signup_field'}))

    class Meta:
        model=User
        fields=("username","email","password1","password2")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'enter username...','class':'signup_field'}),
        }
    
    def __init__(self,*args,**kwargs):
        super(userRegisterForm,self).__init__(*args,**kwargs)
        self.fields['password1'].widget.attrs['placeholder']='type your password...'
        self.fields['password1'].widget.attrs['class']='signup_field'
        self.fields['password2'].widget.attrs['placeholder']='retype your password...'
        self.fields['password2'].widget.attrs['class']='signup_field'
    
    def save(self,commit=True):
        user=super(userRegisterForm,self).save(commit=False)
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
        return user
