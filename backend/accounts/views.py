from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from products.models import Product
from checkout.models import OrderItem
from django.db.models import Exists, OuterRef


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return render(request, 'accounts/register.html')
        
        if username == "" or password == "":
            messages.error(request, "Nome de usuário e senha não podem ser vazios.")
            return render(request, 'accounts/register.html')
        
        if len(password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username, 
            password=password)
        user.save()
        messages.success(request, "Conta criada com sucesso. Faça login.")
        return redirect("login")
    
    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if username == "" or password == "":
            messages.error(request, "Por favor, forneça um nome de usuário e uma senha.")
            return render(request, 'accounts/login.html')

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Usuário ou senha incorretos ou inexistentes.')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Desconectado com sucesso.")
    return redirect("home")

@login_required
def profile(request):
    customer = request.user.customer
    user = request.user

    if request.method == 'POST' and customer.confirmed_data:
        messages.warning(
            request, 
            "Você já confirmou seus dados."
        )
        return render(request, 'accounts/profile.html',
            {'customer': customer,
            'locked': customer.confirmed_data}              
        )
    
    if request.method == 'POST' and not customer.confirmed_data:
        user.email = request.POST.get('email')

        customer.cpf = request.POST.get('cpf')
        customer.phone = request.POST.get('phone')
        customer.complete_name = request.POST.get('complete_name')
        customer.gender = request.POST.get('gender')
        
        day = request.POST.get('birth_day')
        month = request.POST.get('birth_month')
        year = request.POST.get('birth_year')

        if day and month and year:
            customer.birth_date = date(
                int(year), 
                int(month), 
                int(day)
            )

            try:
                customer.birth_date = date(int(year), int(month), int(day))
            except ValueError:
                messages.error(request, "Data de nascimento inválida.")
                return redirect('profile')

        if not all([customer.complete_name, customer.cpf, customer.phone]):
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('profile')

        customer.confirmed_data = True
        customer.save()
        user.save()

        messages.success(
            request, 
            "Dados confirmados com sucesso! Por favor, recarregue a página."
        )
        return render(request, 'accounts/profile.html',)
    
    return render(request, 'accounts/profile.html',
        {'customer': customer,
         'user': user,
         'locked': customer.confirmed_data}
    )

def my_products(request):
    user = request.user

    paid_items = OrderItem.objects.filter(
        order__user=request.user,
        order__status='paid',
        product=OuterRef('pk')
    )

    products = (
        Product.objects
        .filter(orderitem__order__user=request.user)
        .annotate(is_paid=Exists(paid_items))
        .distinct()
    )

    return render(
        request,
        'accounts/myproducts.html',
        {'products': products}
    )

def perguntas(request):
    return render(request, 'accounts/Perguntas.html')