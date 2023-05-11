from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.username.lower()
        if User.objects.filter(username=username):
            raise forms.ValidationError("User already exist")
        return username

    def email_clean(self):
        email = self.email.lower()
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email already exist")
        return email

    def clean_password2(self):
        password1 = self.password1
        password2 = self.password2
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Email already exist")
        return password2

    def is_valid(self):
        self.username_clean()
        self.email_clean()
        self.clean_password2()
        return True

    def save(self, commit=True):
        user = User.objects.create_user(
            self.username,
            self.email,
            self.password1
        )
        return user

    def __init__(self, request=None, *args: any, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        if request != None:
            self.username = request.POST['username']
            self.email = request.POST['email']
            self.password1 = request.POST['password1']
            self.password2 = request.POST['password2']

    def __str__(self) -> str:
        return f"{self.username} {self.email}"
    
class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
