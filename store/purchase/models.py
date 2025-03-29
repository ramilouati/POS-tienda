from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
from inventory.models import Products
from django.db import transaction
from django.db import models, transaction
from decimal import Decimal
from django.core.exceptions import ValidationError

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    TYPE_CHOICES = [
        ('individual', 'Particulier'),
        ('company', 'Entreprise'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    client_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='individual')
    contact_info = models.TextField(blank=True, null=True)  # Add this line
    date_added = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} ({self.get_client_type_display()})"

    def get_orders(self):
        """ Retourne les commandes associées au client """
        return self.orders.all()

    def get_total_purchases(self):
        """ Calcule le total des achats réalisés par le client """
        from models import PurchaseProduct
        return PurchaseProduct.objects.filter(client=self).aggregate(total=models.Sum('total'))['total'] or 0

class PurchaseProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 Nouveau
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    qty = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=8, editable=False, default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.qty <= 0:
            raise ValidationError("The quantity must be greater than zero.")
        if self.cost <= 0:
            raise ValidationError("The cost must be greater than zero.")

    def save(self, *args, **kwargs):
        self.clean()
        self.total = self.cost * self.qty
        
        with transaction.atomic():
            if self.pk:
                previous_instance = PurchaseProduct.objects.get(pk=self.pk)
                quantity_difference = self.qty - previous_instance.qty
            else:
                quantity_difference = self.qty
            super().save(*args, **kwargs)

            # Mettre à jour le stock du produit
            if self.product:
                self.product.update_quantity_on_purchase(quantity_difference)
                self.product.update_cost(self.cost)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.product:
                self.product.decrease_quantity(self.qty)
                self.product.update_cost_after_deletion(self.cost)
            super().delete(*args, **kwargs)

    def __str__(self):
        client_info = f" pour {self.client}" if self.client else ""
        return f"{self.product} de {self.supplier}{client_info} - {self.qty} @ {self.cost} chaque"
    