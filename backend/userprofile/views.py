from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def pessoal(request):
    user = request.user
    customer = user.customer
    return render(request, 'userprofile/pessoal.html', {'user': user, 'customer': customer})