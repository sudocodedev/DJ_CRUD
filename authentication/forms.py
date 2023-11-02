from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class userRegisterForm(UserCreationForm):
    email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'placeholder': 'enter your email...','class': 'signup_field'}))
    fullname=forms.CharField(max_length=30,label="Full Name",widget=forms.TextInput(attrs={'placeholder': 'enter your full name...','class': 'signup-field'}))
    class Meta:
        model=User
        fields=("username","fullname","email","password1","password2")
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
        first_name,last_name=self.cleaned_data['fullname'].split()
        user.first_name,user.last_name=first_name,last_name
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
        return user
