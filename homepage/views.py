from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect

from homepage.forms import LoginUserForm


@login_required(login_url='login')
def homepage(request):
    return render(request, "homepage/homepage.html")


@login_required(login_url='login')
def about(request):
    return render(request, "homepage/about.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = AuthenticationForm(request, data=request.POST)
        if request.method == 'POST':
            if form.is_valid():
                login(request, form.get_user())
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

    return render(request, "homepage/login.html", {'form': form})


class MyLogOut(LogoutView):
    redirect_authenticated_user = True
    template_name = 'home'
