from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import ShippingAddress

class UserCreateFrm(forms.Form):
    '''User creat form for storing user data to user moedl'''
    username = forms.CharField(label="User-Name", max_length=100, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),max_length=20)

    def clean_confirm_password(self):
        pasd = self.cleaned_data["password"]
        if len(pasd) < 8:
            raise ValidationError("Password should be at least 8 char long")
        return pasd

    def clean_username(self):
        usname = self.cleaned_data["username"]
        if len(usname) < 6:
            raise ValidationError("User name should be at least 6 char long")
        return usname
        
    def clean_confirm_password(self):
        pasd = self.cleaned_data["password"]
        cnf_pasd = self.cleaned_data["confirm_password"]
        
        if pasd != cnf_pasd:
            raise ValidationError("Password does not match!")
        
        return cnf_pasd

    def save(self):
        new_user  =  User(username = self.cleaned_data["username"])
        new_user.set_password(self.cleaned_data["password"])
        new_user.save()
        return new_user

class ShippingAddressForm(forms.ModelForm):
    '''Shipping address form for customer'''
    def __init__(self, *args, **kwargs):
        self.user = None
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ShippingAddress
        fields = ["city", "state", "country","address"]
    
    def save(self, comit=True):
        obj = ShippingAddress(user=self.user,address = self.cleaned_data["address"],
        city=self.cleaned_data["city"],state=self.cleaned_data["state"],
        country=self.cleaned_data["country"])

        if comit:
            obj.save()
        return obj