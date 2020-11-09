from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from .forms import OrderForm, CustomerForm, ProductForm

# for creating multiple orders
from django.forms import inlineformset_factory

# ordering filters
from .filters import OrderFilter

# Create your views here.

def registerPage(request):
    context = {}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    orders = Order.objects.all().order_by('-id')
    customers = Customer.objects.all().order_by('-id')

    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    total_customers = customers.count()

    context = {
                'orders': orders,
                'customers': customers,
                'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending,
            }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'accounts/products.html', context)

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all().order_by('-id')
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
                'customer': customer,
                'orders': orders,
                'total_orders': total_orders,
                'myFilter': myFilter,
            }
    return render(request, 'accounts/customer.html', context)

def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

def createOrderById(request, pk):
    # use 'extra' for as many fields as required
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)

    customer = Customer.objects.get(id=pk)

    ## in case of using new fields and also placed orders
    # formset = OrderFormSet(instance = customer)

    ## in case of using only new fields
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)

    ## form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/customer/'+ str(pk))

    context = {'formset': formset}
    return render(request, 'accounts/order_form_by_id.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        order.delete()
        return redirect('/')

    context = { 'id': pk,
                'item': order.product,
                'customer': order.customer,
                'date_created': order.date_created,
                'status': order.status,
            }
    return render(request, 'accounts/delete.html', context)


def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)

def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer/'+str(pk))

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)

def createProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context = {'form': form}
    return render(request, 'accounts/product_form.html', context)
