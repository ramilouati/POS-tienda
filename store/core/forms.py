from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from core.models import Bussiness

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data
    
from django import forms


class CreateBusinessForm(forms.ModelForm):  # <= ici, remplace Form par ModelForm
    class Meta:
        model = Bussiness
        fields = ['matricule_fiscale', 'name', 'address', 'city', 'country', 'phone', 'email','type']
        labels = {
            'matricule_fiscale': 'Matricule Fiscale',
            'name': 'Nom',
            'address': 'Adresse',
            'city': 'Ville',
            'country': 'Pays',
            'phone': 'Numéro de téléphone',
            'email': 'Adresse e-mail',
            'type': 'Type',
        }
        widgets = {
            'matricule_fiscale': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricule Fiscale'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Pays'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            
            }
        error_messages = {
            'matricule_fiscale': {
                'required': 'Le matricule fiscale est obligatoire.',
                'invalid': 'Entrez un matricule fiscale valide.',
            },
            'name': {
                'required': 'Le nom est obligatoire.',
                'invalid': 'Entrez un nom valide.',
            },
            'address': {
                'required': 'L\'adresse est obligatoire.',
                'invalid': 'Entrez une adresse valide.',
            },
            'city': {
                'required': 'La ville est obligatoire.',
                'invalid': 'Entrez une ville valide.',
            },
            'country': {
                'required': 'Le pays est obligatoire.',
            },
            'phone': {
                'required': 'Le numéro de téléphone est obligatoire.',
                'invalid': 'Entrez un numéro de téléphone valide.',
            },
            'email': {
                'required': 'L\'adresse e-mail est obligatoire.',
                'invalid': 'Entrez une adresse e-mail valide.', 
            },
            'type': {
                'required': 'Le type est obligatoire.',
                'invalid': 'Entrez un type valide.',
            },
        }
            
        
class PasswordResetEmailForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
