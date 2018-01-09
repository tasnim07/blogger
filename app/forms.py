from django import forms


class RegisterUser(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(max_length=50)
    is_superuser = forms.BooleanField()


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class CreatePost(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    description = forms.CharField(widget=forms.Textarea)
