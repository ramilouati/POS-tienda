import json
import logging
from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import Category, Products
from purchase.models import PurchaseProduct
from .forms import ProductsForm, CategoryForm

logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class CategoryProductsList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):

    model = Category
    template_name = "inventory/category_list_link.html"
    context_object_name = "products"
    permission_required = 'inventory.view_category'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Products.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
class CategoryList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):

    model = Category
    template_name = "inventory/category_list.html"
    context_object_name = "categories"
    permission_required = 'inventory.view_category'
    
    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('products'))
    
class CategoryCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Category
    template_name = "inventory/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    permission_required = 'inventory.add_category'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        category_name = form.instance.name
        messages.success(self.request, f"Catégorie '{category_name}' créée avec succès.")
        return response

    def form_invalid(self, form):
        logger.error("Erreur lors de la création de la catégorie : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la création de la catégorie. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))
    
class CategoryUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Category
    template_name = "inventory/category_update.html"
    form_class = CategoryForm
    success_url = reverse_lazy('inventory:category_list')
    permission_required = 'inventory.change_category'

    def form_valid(self, form):
        category_name = self.get_object().name
        response = super().form_valid(form)
        messages.success(self.request, f"Catégorie '{category_name}' mise à jour avec succès.")
        return response

    def form_invalid(self, form):
        category_name = self.get_object().name
        messages.error(self.request, f"Impossible de mettre à jour la catégorie '{category_name}'. Veuillez corriger les erreurs.")
        return super().form_invalid(form)
    
class CategoryDelete(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMixin, generic.DeleteView):
    model = Category
    template_name = "inventory/category_delete.html"
    success_url = reverse_lazy('inventory:category_list')
    permission_required = 'inventory.delete_category'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_name = self.object.name
        success_message = f"Catégorie '{category_name}' supprimée avec succès."
        messages.success(self.request, success_message)
        return self.delete(request, *args, **kwargs)



class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Products
    template_name = "inventory/product_details.html"
    context_object_name = "product"
    permission_required = 'inventory.view_products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        purchase_products = PurchaseProduct.objects.filter(product=product)
        logger.debug(f"Nombre d'achats liés au produit : {purchase_products.count()}")

        cantidad_historica = sum([pp.qty for pp in purchase_products])
        logger.debug(f"Quantité historique calculée : {cantidad_historica}")

        context['cantidad_historica'] = cantidad_historica
        return context
    
class ProductList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Products
    template_name = "inventory/product_list.html"
    context_object_name = "products"
    permission_required = 'inventory.view_products'
    
class ProductCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Products
    template_name = "inventory/product_create.html"
    form_class = ProductsForm
    success_url = reverse_lazy('inventory:product_list')
    permission_required = 'inventory.add_products'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        product_name = form.instance.name
        messages.success(self.request, f"Produit '{product_name}' créé avec succès.")
        return response

    def form_invalid(self, form):
        logger.error("Erreur lors de la création du produit : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la création du produit. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))
    
class ProductUpdate(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Products
    template_name = "inventory/product_update.html"
    form_class = ProductsForm
    success_url = reverse_lazy('inventory:product_list')
    permission_required = 'inventory.change_products'
    
    def form_valid(self, form):
        product_name = self.get_object().name
        response = super().form_valid(form)
        messages.success(self.request, f"Produit '{product_name}' mis à jour avec succès.")
        return response
    
    def form_invalid(self, form):
        logger.error("Erreur lors de la mise à jour du produit : %s", form.errors)
        messages.error(self.request, "Une erreur s'est produite lors de la mise à jour du produit. Veuillez réessayer.")
        return self.render_to_response(self.get_context_data(form=form))

class ProductDelete(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMixin,  generic.DeleteView):
    model = Products
    template_name = "inventory/product_delete.html"
    success_url = reverse_lazy('inventory:product_list')
    permission_required = 'inventory.delete_products'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_name = self.object.name
        success_message = f"Produit '{product_name}' supprimé avec succès."
        messages.success(self.request, success_message)
        return self.delete(request, *args, **kwargs)
