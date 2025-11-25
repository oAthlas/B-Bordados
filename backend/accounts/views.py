from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User


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

        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to a success page.
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def profile(request):
    return render(request, 'accounts/profile.html')

