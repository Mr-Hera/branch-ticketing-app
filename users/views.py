from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterCustomerForm

# Create your views here.

# customer registration
def register_customer(req):
    if req.method == 'POST':
        form = RegisterCustomerForm(req.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save(commit=False)
            messages.info(req, 'Account registration successful! Proceed to login...')
            return redirect('login')
        else:
            messages.warning(req, 'Oops! Something went wrong. Please check form inputs')
            return redirect('register-customer')
    else:
        form = RegisterCustomerForm()
        context = { 'form': form }
        return render(req, 'users/register_customer.html', context)

# user login
def login_user(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)
        if user is not None and user.is_active:
            login(req, user)
            messages.info(req, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.warning(req, 'Oops! Something went wrong. Please check form inputs')
            return redirect('login')
    else:
        return render(req, 'users/login.html')

# user logout
def logout_user(req):
    logout(req)
    messages.info(req, 'Logout successful.')
    return redirect('login')
