from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from .models import *
from django.views import View
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            request.session['id'] = user.id
            return redirect('home')
        else:
            context = "Invalid username or password"
            return render(request, 'login.html', {'context': context})
    return render(request, 'login.html')

def profile(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    try:
        user_profile = Profile.objects.get(user=user_id)
    except Profile.DoesNotExist:
        user_profile = None

    return render(request, 'profile.html', {'profile': user_profile})

def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})

def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect('login')


class CreateProducts(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_id = self.request.session.get('id')
        if user_id is None:
            return self.form_invalid(form)
        form.instance.owner_id = user_id  
        return super().form_valid(form)
class ProductsViews(ListView):
    model = Products
    template_name = 'home.html'
    context_object_name = 'products'
class UpdateProducts(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        user_id = self.request.session.get('id')
        return Products.objects.filter(owner_id=user_id)

class DeleteProducts(DeleteView):
    model = Products
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('id')
        obj = self.get_object()
        if obj.owner_id != user_id:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class DetailProducts(DetailView):
    model = Products
    template_name = 'detail_product.html'
    context_object_name = 'product'




class CartView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



class AddToCartView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        product = get_object_or_404(Products, pk=pk)
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        
        if quantity < 1:
            quantity = 1

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')

    
class RemoveFromCartView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk)
        cart_item.delete()
        return redirect('cart')

class CreateOrderView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')  

        total = sum(item.product.product_price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='pending'
        ) 

        cart_items.delete()
 
        return redirect('orders')  
    

class OrderView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'