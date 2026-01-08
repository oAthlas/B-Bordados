from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from products.models import Product
from checkout.models import OrderItem
from django.db.models import Exists, OuterRef, Subquery


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

    avatars = [
        'avatar_1', 'avatar_2', 'avatar_3',
        'avatar_4', 'avatar_5', 'avatar_6', 'avatar_none'
    ]

    if request.method == 'POST' and customer.confirmed_data:
        messages.warning(
            request, 
            "Você já confirmou seus dados."
        )
        return render(request, 'accounts/profile.html',
            {'customer': customer, 'avatars': avatars,
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

@login_required
def my_products(request):
    user = request.user

    paid_items = OrderItem.objects.filter(
        order__user=request.user,
        order__status='paid',
        product=OuterRef('pk')
    )

    pending_payment_url = OrderItem.objects.filter(
        order__user=user,
        order__status='pending',
        product=OuterRef('pk'),
        order__payment_url__isnull=False
    ).values_list('order__payment_url', flat=True)[:1]

    products = (
        Product.objects
        .filter(orderitem__order__user=request.user)
        .annotate(is_paid=Exists(paid_items), pending_payment_url=Subquery(pending_payment_url))
        .distinct()
    )

    return render(
        request,
        'accounts/myproducts.html',
        {'products': products, 'pending_payment_url': Subquery(pending_payment_url)}
    )

@login_required
def perguntas(request):
    return render(request, 'accounts/Perguntas.html')

@login_required
def settings(request):
    return render(request, 'accounts/settings.html')

@login_required
def change_username(request):
    if request.method == 'GET':
        return render(request, 'accounts/settings.html')
    elif request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Nome de usuário atualizado com sucesso.")
        return redirect('settings')

@login_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirmation = request.POST.get('confirm_new_password')
        actual_password = user.check_password(request.POST.get('actual_password'))
        
        if not actual_password:
            messages.error(request, "Senha atual incorreta.")
            return redirect('settings')
        
        if new_password != confirmation:
            messages.error(request, "As senhas não coincidem.")
            return redirect('settings')
        
        if len(new_password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return redirect('settings')
        
        if new_password == confirmation:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Senha atualizada com sucesso.")
        return redirect('settings')
    
    else:
        return render(request, 'accounts/settings.html')

@login_required
def delete_account(request):
    messages.warning(request, "Para excluir sua conta, entre em contato com o suporte.")
    return redirect('settings')

def forgot_password(request):
    messages.info(request, "Funcionalidade de recuperação de senha em desenvolvimento. Para fazer uma nova senha entre em contato com o suporte.")
    return redirect('settings')

@login_required
def change_avatar(request):
    if request.method == 'POST':
        avatar = request.POST.get('avatar')

        allowed = [
            'avatar_1', 'avatar_2', 'avatar_3',
            'avatar_4', 'avatar_5', 'avatar_6', 'avatar_none'
        ]

        if avatar in allowed:
            request.user.customer.avatar = avatar
            request.user.customer.save()
            messages.success(request, "Avatar atualizado com sucesso.")

    return redirect('profile')
