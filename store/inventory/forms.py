from django import forms
from .models import  Products, Category
import unicodedata
from django.utils.text import slugify
import re
import unicodedata
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Nombre',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez des informations générales, etc..',
                'rows': 3,  
            }),
            
        }
        error_messages = {
            # Puedes agregar mensajes de error personalizados aquí si es necesario
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Normalizar el nombre: eliminar acentos, espacios extra y convertir a minúsculas
            normalized_name = ''.join(c for c in unicodedata.normalize('NFD', name)
                                    if unicodedata.category(c) != 'Mn')
            normalized_name = re.sub(r'\s+', '', normalized_name.lower())
            
            instance = self.instance
            # Buscar categorías existentes con nombres similares
            existing_categories = Category.objects.exclude(id=instance.id)
            for category in existing_categories:
                category_normalized = ''.join(c for c in unicodedata.normalize('NFD', category.name)
                                            if unicodedata.category(c) != 'Mn')
                category_normalized = re.sub(r'\s+', '', category_normalized.lower())
                if category_normalized == normalized_name:
                    raise ValidationError(f"Il y a déjà une catégorie similaire: '{category.name}'")
        return name

        
class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['code', 'category', 'name', 'description', 'price', 'status','taxpercentage']
        labels = {
            'code': 'Code',
            'category': 'Catégorie',
            'name': 'Nom de produit',
            'description': 'Description',
            'price': 'Prix',
            'status': 'État',
            'cost': 'Coût',
            'quantity': 'Quantité',
            'taxpercentage': 'Pourcentage de TVA'
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vino001',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vino Dulce',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese información general Etc.',
                'rows': 3,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio del producto',
                'step': '0.01',
            }),
                    'taxpercentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'TVA',
                'step': '1.00',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[
                (1, 'Activo'),
                (0, 'Inactivo')
            ]),
            
            'cost': forms.NumberInput(attrs={
                'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'}),
        }
        error_messages = {
            'code': {
                'required': 'Ce champ est obligatoire.',
                'max_length': 'Ce champ ne peut pas dépasser 100 caractères.',
            },
            'category': {
                'required': 'Ce champ est obligatoire.',
            },
            'name': {
                'required': 'Ce champ est obligatoire.',
            },
            'description': {
                'required': 'Ce champ est obligatoire.',
            },
            'price': {
                'required': 'Ce champ est obligatoire.',
                'invalid': 'Entrez un prix valide.',
            },
                     'taxpercentage': {
                'required': 'Ce champ est obligatoire.',
                'invalid': 'Entrez un prix valide.',
            },
            'status': {
                'required': 'Ce champ est obligatoire.',
                'invalid': 'Entrez un prix valide.',
            }
        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.errors:
                field.widget.attrs['class'] += ' is-invalid'
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar el queryset de category alfabéticamente
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        # Establecer el campo como no editable
        self.fields['status'].disabled = True
    
    
    @staticmethod
    def normalize_text(text):
        if text:
            # Eliminar acentos y convertir a minúsculas
            text = ''.join(c for c in unicodedata.normalize('NFD', text)
                        if unicodedata.category(c) != 'Mn')
            # Eliminar caracteres especiales y espacios
            text = re.sub(r'[^\w]', '', text.lower())
        return text
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        code = cleaned_data.get('code')

        if name and code:
            normalized_name = self.normalize_text(name)
            normalized_code = self.normalize_text(code)

            # Obtener la instancia actual si estamos editando
            instance_id = self.instance.pk if self.instance.pk else None

            # Verificar duplicados de nombre
            name_duplicates = Products.objects.all()
            if instance_id:
                name_duplicates = name_duplicates.exclude(pk=instance_id)
            
            for product in name_duplicates:
                if self.normalize_text(product.name) == normalized_name:
                    self.add_error('name', "Il y a déjà un produit avec un nom similaire.")
                    raise ValidationError("Il y a déjà un produit avec un nom similaire.")

            # Verificar duplicados de código
            code_duplicates = Products.objects.filter(code__iexact=normalized_code)
            if instance_id:
                code_duplicates = code_duplicates.exclude(pk=instance_id)
            if code_duplicates.exists():
                self.add_error('code', "Il y a déjà un produit avec ce code.")
                raise ValidationError("Il y a déjà un produit avec ce code.")

        return cleaned_data
    