from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from purchase.models import Client
from .models import *
from inventory.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.contrib import messages
from django.utils import translation
from django.utils.dateformat import DateFormat

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.utils.timezone import now, timedelta

from django.db.models import Sum, F

from django.db import transaction

@login_required
@permission_required('pos.view_sales', raise_exception=True)
def pos(request):
    
    clients = Client.objects.all()
    products = Products.objects.filter(status=1).order_by('name')
    product_json = []
    client_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price) , 'taxpercentage': product.taxpercentage})
    for client in clients:
        client_json.append({'id': client.id, 'name': client.name})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'clients': clients,
        'client_json': json.dumps(client_json),
    }
    print(product_json)
    return render(request, 'pos/pos.html', context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
    }
    return render(request, 'pos/checkout.html', context)

@login_required
@permission_required('pos.add_sales', raise_exception=True)
@csrf_exempt
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST

    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += 1
        check = Sales.objects.filter(code=str(pref) + str(code)).exists()
        if not check:
            break
    code = str(pref) + str(code)

    try:
        # Fetch the client name from the form data
        client_id = data.get('client_id')  # Ensure this matches the key sent from the frontend
        if not client_id:
            raise ValueError("Client ID is required.")

        # Fetch the client instance
        client = get_object_or_404(Client, id=client_id)

        # Create the Sales instance with the client's name
        sales = Sales(
            code=code,
            sub_total=data['sub_total'],
            tax=data['tax'],
            tax_amount=data['tax_amount'],
            grand_total=data['grand_total'],
            tendered_amount=data['tendered_amount'],
            amount_change= "{:.3f}".format(float(data['amount_change'])),
            discount_amount = "{:.3f}".format(float(data['total_discount'])),
            cliente=client.name,  # Store the client's name as a string
        )
        sales.save()

        sale_id = sales.pk
        i = 0
        for prod_id in data.getlist('product[]'):
            product = get_object_or_404(Products, id=prod_id)
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            discount = data.getlist('discount[]')[i]
            total = float(qty) * float(price)
            totalDescounted = total - (total * (float(discount) / 100))

            totalTax = "{:.3f}".format(totalDescounted * (1+(float(product.taxpercentage) / 100)))
            sales_item = salesItems(
                sale=sales,
                product=product,
                qty=qty,
                price=price,
                discount=discount,
                total=totalTax
            )
            sales_item.save()
            i += 1

        resp['status'] = 'success'
        resp['sale'] = sale_id
        messages.success(request, "La vente à été enregistrée.")
    except Exception as e:
        resp['msg'] = "An error occurred: " + str(e)

    return JsonResponse(resp)

@login_required
@permission_required('pos.view_sales', raise_exception=True)
def salesList(request):
    sales = Sales.objects.order_by('-date_added').all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        items = salesItems.objects.filter(sale_id=sale).all()
        products_list = {}
        for item in items:
            product_name = item.product.name
            if product_name in products_list:
                products_list[product_name] += item.qty
            else:
                products_list[product_name] = item.qty
        data['products_list'] = products_list
        data['total_items_sold'] = sum(products_list.values())
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        sale_data.append(data)
    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
    }
    return render(request, 'pos/sales.html', context)

@login_required
@permission_required('pos.add_sales', raise_exception=True)
def create_sales_item(request, product_id, qty, sale_instance):
    product = get_object_or_404(Products, id=product_id)
    try:
        qty = int(qty)
        if product.cantidad < qty:
            return JsonResponse({"error": "No hay suficiente cantidad de producto para vender."}, status=400)
        sales_item = salesItems.objects.create(
            product=product,
            qty=qty,
            price=product.price,
            total=product.price * qty,
            sale=sale_instance
        )
        product.update_quantity_on_sale(qty)
        return JsonResponse({"success": "Item de venta creado exitosamente."})
    except ValueError:
        return JsonResponse({"error": "Cantidad inválida."}, status=400)

@login_required
@permission_required('pos.add_sales', raise_exception=True)
@csrf_exempt
def create_sale(request):
    if request.method == "POST":
        sale_code = request.POST.get('code')
        items = json.loads(request.POST.get('items'))

        sale = Sales.objects.create(
            code=sale_code,
            sub_total=0,
            grand_total=0,
            tax_amount=0,
            tax=0,
            tendered_amount=0,
            amount_change=0,
            discount_amount=0
        )

        for item in items:
            product_id = item['product_id']
            qty = item['qty']
            response = create_sales_item(request, product_id, qty, sale)
            if response.status_code == 400:
                sale.delete()
                return response

        sale.sub_total = sum([item.total for item in sale.salesitems_set.all()])
        sale.tax_amount = sale.sub_total * (sale.tax / 100)
        sale.grand_total = sale.sub_total + sale.tax_amount
        print("---------------")
        print(sum([item.price * (item.discount / 100) for item in sale.salesitems_set.all()]))
        sale.discount_amount = sum([item.price * (item.discount / 100) for item in sale.salesitems_set.all()])
        sale.save()

        return JsonResponse({"success": "Venta creada exitosamente."})

    return JsonResponse({"error": "Método no permitido."}, status=405)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None: 
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale=sales).all()
    
        # Cambiar el idioma a español para la fecha
    with translation.override('fr-FR'):
        formatted_date = DateFormat(sales.date_added).format(r'd-m-Y')
    context = {
        "transaction": transaction,
        "salesItems": ItemList,
        
        "formatted_date": formatted_date,
    }
    return render(request, 'pos/receipt.html', context)

@login_required
@permission_required('pos.delete_sales', raise_exception=True)
def delete_sale(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        sale = Sales.objects.get(id=id)
        with transaction.atomic():
            for item in sale.salesitems_set.all():
                item.delete()
            sale.delete()
        resp['status'] = 'success'
        messages.success(request, 'El registro de Venta fue eliminado y las cantidades de productos fueron restauradas.')
    except Sales.DoesNotExist:
        resp['msg'] = "La venta no existe"
    except Exception as e:
        resp['msg'] = f"Ocurrió un error: {str(e)}"
    return HttpResponse(json.dumps(resp), content_type='application/json')

@login_required
@permission_required('pos.inventorybyqty', raise_exception=True)
def products_to_purchase(request):
    # Define the threshold for low stock quantity (you can customize this)
    low_stock_threshold = 10

    # Define the time period for sales (e.g., last 30 days)
    start_date = now() - timedelta(days=30)

    # Calculate the total quantity sold for each product in the last period
    sales_data = (
        salesItems.objects.filter(sale__date_added__gte=start_date)
        .values('product__id', 'product__name', 'product__quantity')
        .annotate(total_sold=Sum('qty'))
        .order_by('-total_sold')  # Sort by sales rate (most sold first)
    )

    # Filter products that are low in stock and add sales data
    products_to_purchase = []
    for data in sales_data:
        product = Products.objects.filter(id=data['product__id']).first()
        if product and product.quantity <= low_stock_threshold:
            products_to_purchase.append({
                'id': product.id,
                'name': product.name,
                'quantity_in_stock': product.quantity,
                'total_sold': data['total_sold'],
            })

    # Render the data or return as JSON
    return render(request, 'pos/products_to_purchase.html', {
        'products_to_purchase': products_to_purchase,
    })

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)
