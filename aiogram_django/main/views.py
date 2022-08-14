from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login')
def homepage(request):
    return render(request, "main/homepage.html")


@login_required(login_url='login')
def about(request):
    return render(request, "main/about.html")


def login_page(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    #     form = LoginUserForm()
    #     if request.method == 'POST':
    #         form = LoginUserForm(request.POST)
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #
    #         user = authenticate(request, username=username, password=password)
    #
    #         if user is not None:
    #             login(request, username)
    #             redirect('')
    #         else:
    #             messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, "main/login.html", context)
