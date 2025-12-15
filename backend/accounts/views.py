from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login as auth_login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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

def teste(requests):
    User = get_user_model()
    users = User.objects.all()
    return render(requests, 'accounts/teste.html', {'users': users})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Desconectado com sucesso.")
    return redirect("home")

