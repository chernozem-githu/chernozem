from django import forms
from accounts.models import CustomUser
from django import forms
from .models import Perfume

class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = ['name', 'description', 'category', 'price', 'image']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'avatar', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
