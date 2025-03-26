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
                'required': 'le nom est obligatoire.',
                'max_length': 'le nom ne peut pas depasser 100 caracteres.',
            },
            'contact_info': {
                'required': 'les informations des contact sont obligatoires.',
                'max_length': 'les informations des contact ne peuvent pas depasser 200 caracteres.',
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
            'supplier': 'Fournisseur',
            'product': 'Produit',
            'cost': 'Cout',
            'qty':'Quantité',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le montant total',
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la quanttié total',
            }),
        }
        error_messages = {
            'qty': {
                'required': 'La quantité est obligatoire.',
                'invalid': 'Entrez une quantité valide.',
            },
            'cost':{
                'required': 'Le montant est obligatoire.',
                'invalid': 'Entrez un montant valide.',
            }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar el queryset de category alfabéticamente
        self.fields['supplier'].queryset = Supplier.objects.all().order_by('name')
        self.fields['product'].queryset = Products.objects.all().order_by('name')
    
