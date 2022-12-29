from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=7, min_length=7)
    password = forms.CharField(max_length=4, min_length=4)
    password2 = forms.CharField(max_length=4, min_length=4)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        
        if password.isalpha() and password == password2:
            return password
        raise ValidationError("Password error")


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user