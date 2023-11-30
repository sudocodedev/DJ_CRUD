from django import forms
from .models import post


class postForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ["title", "genre", "ratings", "image", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "enter title for your post..."}
            ),
            # 'author': forms.Select(attrs={'placeholder': 'Select Author'}),
            "genre": forms.TextInput(
                attrs={"placeholder": "enter genre eg. romance,action,comedy,..."}
            ),
            "ratings": forms.TextInput(
                attrs={"placeholder": "provide your ratings..."}
            ),
            # 'content': forms.TextInput(attrs={'placeholder':'start typing...'}),
        }


class SurveyForm(forms.Form):
    firstname = forms.CharField(
        max_length=20,
        label="First Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your first name...", "class": "form-input"}
        ),
    )
    lastname = forms.CharField(
        max_length=20,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your last name...", "class": "form-input"}
        ),
    )
    email = forms.EmailField(
        max_length=100,
        label="E-Mail",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your email...", "class": "form-input"}
        ),
    )
    hostname = forms.CharField(
        max_length=30,
        label="Host Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Provide a valid hostname connection...",
                "class": "form-input",
            }
        ),
        required=True,
    )
    title = forms.CharField(
        max_length=30,
        label="Title",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Title...", "class": "form-input"}
        ),
        required=True,
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title.startswith("INC:"):
            return title
        else:
            raise forms.ValidationError(
                "Title should start with INC: | eg. INC: <title>"
            )

    def clean_hostname(self):
        hostname = self.cleaned_data.get("hostname")
        if hostname.endswith(".com"):
            return hostname
        else:
            raise forms.ValidationError("provide valid hostname | eg. <hostname>.com")

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        firstname = cleaned_data.get("firstname")
        lastname = cleaned_data.get("lastname")
        if firstname == lastname:
            self.add_error("firstname", "firstname is same as lastname")
            self.add_error("lastname", "lastname can't be same as firstname")
            raise forms.ValidationError("lastname can't be same as firstname...")
