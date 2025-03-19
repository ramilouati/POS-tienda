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
        fields = ['name', 'contact_info']
        labels = {
            'name': 'Noms et noms de famille (personne / entreprise) ',
            'contact_info': 'Informations sur les clients',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Noms et nom de famille / Empresa S.A.   ',
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez des informations:  Adresse  and Téléphone   item  etc',
                'rows': 6,  
            }),
        }
        error_messages = {
            'name': {
                'required': 'Le nom du client est obligatoire.',
                'max_length': 'Le nom ne peut pas dépasser 100 caractères.',
            },
            'contact_info': {
                'required': 'Les coordonnées sont obligatoires.',
                'max_length': 'Les coordonnées ne peuvent pas dépasser 200 caracteres.',
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
    
