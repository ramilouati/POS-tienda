import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Supplier, PurchaseProduct, Client
from .forms import SupplierForm, PurchaseForm, ClientForm
from inventory.models import Products
<<<<<<< HEAD
=======

>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)  # 🔍 Correct import de logger

# 📌 Gestion des fournisseurs
class SupplierList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Supplier
    template_name = 'purchases/supplier_list.html'
    context_object_name = 'suppliers'
    permission_required = 'purchase.view_supplier'

class SupplierCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Supplier
    form_class = SupplierForm  
    template_name = 'purchases/supplier_create.html'
    success_url = reverse_lazy('purchase:supplier_list')
    permission_required = 'purchase.add_supplier'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        supplier_name = form.instance.name
        messages.success(self.request, f"Fournisseur '{supplier_name}' créé avec succès.")
        return response

    def form_invalid(self, form):
        logger.error("Erreur lors de la création du fournisseur : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la création du fournisseur. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))

class SupplierUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Supplier
    form_class = SupplierForm  
    template_name = 'purchases/supplier_update.html'
    success_url = reverse_lazy('purchase:supplier_list')
    permission_required = 'purchase.change_supplier'
    
    def form_valid(self, form):
        supplier_name = self.get_object().name
        response = super().form_valid(form)
        messages.success(self.request, f"Fournisseur '{supplier_name}' mis à jour avec succès.")
        return response

class SupplierDelete(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Supplier
    template_name = 'purchases/supplier_delete.html'
    success_url = reverse_lazy('purchase:supplier_list')
    permission_required = 'purchase.delete_supplier'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        supplier_name = self.object.name
<<<<<<< HEAD
        messages.success(self.request, f"Fournisseur '{supplier_name}' supprimé avec succès.")
=======
        success_message = f"Fournisseur '{supplier_name}' supprimé avec succès."
        messages.success(self.request, success_message)
>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262
        return self.delete(request, *args, **kwargs)

# 📌 Gestion des clients
class ClientList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Client
    template_name = 'purchases/client_list.html'
    context_object_name = 'clients'
    permission_required = 'purchase.view_client'

class ClientCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientForm  
    template_name = 'purchases/client_create.html'
    success_url = reverse_lazy('purchase:client_list')
    permission_required = 'purchase.add_client'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        client_name = form.instance.name
        messages.success(self.request, f"Client '{client_name}' créé avec succès.")
        return response

    def form_invalid(self, form):
        logger.error("Erreur lors de la création du client : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la création du client. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))

class ClientUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm  
    template_name = 'purchases/client_update.html'
    success_url = reverse_lazy('purchase:client_list')
    permission_required = 'purchase.change_client'
    
    def form_valid(self, form):
        client_name = self.get_object().name
        response = super().form_valid(form)
        messages.success(self.request, f"Client '{client_name}' mis à jour avec succès.")
        return response

class ClientDelete(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Client
    template_name = 'purchases/client_delete.html'
    success_url = reverse_lazy('purchase:client_list')
    permission_required = 'purchase.delete_client'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        client_name = self.object.name
<<<<<<< HEAD
        messages.success(self.request, f"Client '{client_name}' supprimé avec succès.")
        return self.delete(request, *args, **kwargs)

# 📌 Gestion des achats
=======
        success_message = f"Client '{client_name}' supprimé avec succès."
        messages.success(self.request, success_message)
        return self.delete(request, *args, **kwargs)


>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262
class PurchaseList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = PurchaseProduct
    template_name = 'purchases/purchase_list.html'
    context_object_name = 'purchases'
    ordering = ['-date_updated']
    permission_required = 'purchase.view_purchaseproduct'
<<<<<<< HEAD

=======
    
>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262
class PurchaseCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = PurchaseProduct
    form_class = PurchaseForm  
    template_name = 'purchases/purchase_create.html'
    success_url = reverse_lazy('purchase:purchase_list')
    permission_required = 'purchase.add_purchaseproduct'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        purchase_name = form.instance.product.name
        messages.success(self.request, f"Achat de '{purchase_name}' enregistré avec succès.")
        return response

    def form_invalid(self, form):
        logger.error("Erreur lors de la création de l'achat : %s", form.errors)
<<<<<<< HEAD
        messages.error(self.request, "Une erreur s'est produite lors de l'enregistrement de l'achat. Veuillez réessayer.")
=======
        messages.error(self.request, "Une erreur s'est produite lors de la création de l'achat. Veuillez réessayer.")
>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262
        return self.render_to_response(self.get_context_data(form=form))

class PurchaseUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = PurchaseProduct
    form_class = PurchaseForm  
    template_name = 'purchases/purchase_update.html'
    success_url = reverse_lazy('purchase:purchase_list')
    permission_required = 'purchase.change_purchaseproduct'
    
    def form_valid(self, form):
        purchase_name = self.get_object().product.name
        response = super().form_valid(form)
        messages.success(self.request, f"Achat de '{purchase_name}' mis à jour avec succès.")
        return response
<<<<<<< HEAD
=======
    
    def form_invalid(self, form):
        logger.error("Erreur lors de la mise à jour du produit : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la mise à jour du produit. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))

>>>>>>> 21780e68a24e5620e75abf8378fc682ef58a9262

class PurchaseDelete(SuccessMessageMixin, PermissionRequiredMixin, generic.DeleteView):
    model = PurchaseProduct
    template_name = 'purchases/purchase_delete.html'
    success_url = reverse_lazy('purchase:purchase_list')
    success_message = "Achat supprimé avec succès."
    permission_required = 'purchase.delete_purchaseproduct'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase'] = self.get_object()
        return context
