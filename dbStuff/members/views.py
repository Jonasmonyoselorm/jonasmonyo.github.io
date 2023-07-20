from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # to diplay message on pages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.

# LOGIN PAGE


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Method 1
        # if user is None:
        #     context = {"error": "Invalid Details"}
        #     return render(request, 'auth/userlogin.html', context)
        # login(request, user)
        # return redirect('/')

        # # Method 2
        if user is not None:
            login(request, user)
            # Redirect to a success page / home page.
            return redirect('/')

        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Invalid Login Credentials"))
            return render(request, 'auth/userlogin.html', {})

    else:
        return render(request, 'auth/userlogin.html', {})

# LOGOUT PAGE


def logOutPage(request):
    logout(request)
    messages.success(request, ("You are Logged Out!"))
    return redirect('/')


# USER REGISTRATION
def registerUser(request):
    # Method 1 without first_name, last_name

    # if request.method == "POST":
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password1']
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         messages.success(request, ("Registration Successful"))
    #         return redirect('/')
    # else:
    #     form = UserCreationForm()

    # return render(request, 'auth/register.html', {
    #     'userRegistrationForm': form,
    # })

    # Method 2

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful"))
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'auth/register.html', {
        'userRegistrationForm': form,
    })
