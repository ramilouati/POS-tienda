from django import forms
from .models import Supplier, PurchaseProduct,Client
from inventory.models import *

from django.core.exceptions import ValidationError
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']
        labels = {
            'name': 'Noms et noms de famille (personne / entreprise) ',
            'contact_info': 'Informations sur les fournisseurs',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres y Apellido / Empresa S.A.    ',
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese información:\n Dirección\n Teléfono\n Rubro\n Etc',
                'rows': 6,  
            }),
        }
        error_messages = {
            'name': {
                'required': 'El nombre del proveedor es obligatorio.',
                'max_length': 'El nombre no puede exceder los 100 caracteres.',
            },
            'contact_info': {
                'required': 'La información de contacto es obligatoria.',
                'max_length': 'La información de contacto no puede exceder los 200 caracteres.',
            },
        }
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'client_type', 'contact_info']  # Removed 'contact_info'
        labels = {
            'name': 'Nom du client',
            'email': 'Adresse e-mail',
            'phone': 'Numéro de téléphone',
            'address': 'Adresse',
            'client_type': 'Type de client',
            'contact_info': 'Information Client',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom et prénom ou entreprise',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de téléphone',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète',
            }),
            'client_type': forms.Select(attrs={
                'class': 'form-control',
            }, choices=Client.TYPE_CHOICES),
            
            'contact_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Infomations de client',
            }),
        }
        error_messages = {
            'name': {
                'required': 'Le nom du client est obligatoire.',
                'max_length': 'Le nom ne peut pas dépasser 100 caractères.',
            },
            'email': {
                'invalid': 'Veuillez entrer une adresse e-mail valide.',
                'unique': 'Cette adresse e-mail est déjà utilisée.',
            },
            'phone': {
                'required': 'Le numéro de téléphone est obligatoire.',
                'max_length': 'Le numéro de téléphone ne peut pas dépasser 15 caractères.',
            },
            'address': {
                'required': 'L\'adresse est obligatoire.',
                'max_length': 'L\'adresse ne peut pas dépasser 200 caractères.',
            },
            'client_type': {
                'required': 'Veuillez choisir un type de client.',
            },
            'contact_info': {
                'required': 'L\'informations est obligatoire.',
                'max_length': 'L\'Informations Client ne peut pas dépasser 500 caractères.',
            },
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['supplier', 'product','cost','qty']
        labels = {
            'supplier': 'Proveedor',
            'product': 'Productos',
            'cost': 'Costo',
            'qty':'Cantidad',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el monto total',
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el monto total',
            }),
        }
        error_messages = {
            'qty': {
                'required': 'El cantidad es obligatorio.',
                'invalid': 'Ingrese un cantidad válida.',
            },
            'cost':{
                'required': 'El costo debe tener 8 decimales.',
                'invalid': 'Ingrese un monto válido.',
            }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar el queryset de category alfabéticamente
        self.fields['supplier'].queryset = Supplier.objects.all().order_by('name')
        self.fields['product'].queryset = Products.objects.all().order_by('name')
    
