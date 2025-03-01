from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    # here in attributes we can add css class or placeholders etc but we are doing it in __init__ method
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
     
    class Meta:
       model = Account
       fields = ['first_name', 'last_name', 'email', 'phone_number','password']
       
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match!")
            
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if Account.objects.filter(username=username).exists():
    #         raise forms.ValidationError("This username is already taken.")
    #     return username

    