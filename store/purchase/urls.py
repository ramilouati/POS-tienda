from django.urls import path
from .views import *
app_name = 'purchase'

urlpatterns = [
    path('suppliers/', SupplierList.as_view(), name='supplier_list'),
    path('suppliers/new/', SupplierCreate.as_view(), name='supplier_create'),
    path('suppliers/edit/<int:pk>/', SupplierUpdate.as_view(), name='supplier_update'),
    path('suppliers/delete/<int:pk>/', SupplierDelete.as_view(), name='supplier_delete'),
    
    path('clients/', ClientList.as_view(), name='client_list'),
    path('clients/new/', ClientCreate.as_view(), name='client_create'),
    path('clients/edit/<int:pk>/', ClientUpdate.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDelete.as_view(), name='client_delete'),
    
    path('purchase/', PurchaseList.as_view(), name='purchase_list'),
    path('purchase/new/', PurchaseCreate.as_view(), name='purchase_create'),
    path('purchase/edit/<int:pk>/', PurchaseUpdate.as_view(), name='purchase_update'),
    path('purchase/delete/<int:pk>/', PurchaseDelete.as_view(), name='purchase_delete'),
]