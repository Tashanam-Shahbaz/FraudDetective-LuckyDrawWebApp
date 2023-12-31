from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from .models import Deposits,CustomUserCreationForm,CustomUserEditForm
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib import messages


def your_view(request):
    # Your view logic...
    messages.success(request, 'Your success message here.')
    messages.warning(request, 'Your warning message here.')
    messages.error(request, 'Your error message here.')
    messages.info(request, 'Your info message here.')
    messages.debug(request, 'Your debug message here.')
    # Redirect or render the response

def home(request): 
    return render(request, 'landing.html')

def signin(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/user_admin') #profile

    elif request.user.is_authenticated and (not request.user.is_superuser):
        return redirect('/profile') #profile

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Clear existing messages before adding a new one
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, 'Login successfully!')

            if user.is_superuser:
                return redirect("/user_admin") 
            else :
                return redirect("/profile")    
        else:

            # Clear existing messages before adding a new one
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, "Unable to log in. Please re-enter all your credentials.")


            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form})
    else:

        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def signup(request):
   
    if request.user.is_authenticated:

        # Clear existing messages before adding a new one
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, 'Already Registered.')

        return redirect('/profile')

    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # print("Inside valid")
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # Clear existing messages before adding a new one
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, 'Register successfully.')

            return redirect('/profile')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})
   

  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')



def deposit(request):

    if request.user.is_authenticated:
        
        if request.method == 'POST':
            # Assuming the form field name for amount is 'amount'
            amount = request.POST.get('amount')
            comment = request.POST.get('comment')
 
            # Assuming the user is authenticated and you have the user object
            user = request.user  # Retrieve the authenticated user

            # Create a new deposit object
            deposit = Deposits(user=user,deposit_date=datetime.now(), amount=amount, status='1',comment = comment)
            deposit.save()  # Save the deposit object to the database

             # Clear existing messages before adding a new one
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request,"Your deposit has been successfully submitted.")
            

            # Optionally, perform additional actions or redirect to a success page
            # return redirect('success_page')  # Replace 'success_page' with your desired URL name
            return redirect("/profile")
        return render(request, 'deposit.html', {'user': request.user})
    else:
        form = AuthenticationForm()

        # Clear existing messages before adding a new one
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request,"Oops! We encountered errors while processing your deposit. To ensure a successful transaction, please log in again and re-submit your deposit. Thank you for your understanding")

        return render(request, 'login.html', {'form': form})


def user_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
       # Retrieve all records from the table
        users = User.objects.filter(is_superuser='False')
        return render(request, 'admin.html',{'users': users})
    else:
        return redirect('/')

def update_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'update_admin.html')
    else:
        return redirect('/')


def add_user(request):
   
    # if request.user.is_authenticated:
    #     return redirect('/')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_admin')
        else:
            return render(request, 'add_user.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'add_user.html', {'form': form})

# def update_user(request,user_id):
#     print(user_id)
#     if request.method == "PUT":
#         pass
#     elif request.method == "GET":
#         print("Inside get")
#         user = User.objects.get(id=user_id)
#         return render(request,'edit_user.html',{"users" : user })


def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('/user_admin')
    else:
        form = CustomUserEditForm()
    
    return render(request, 'edit_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    # Clear existing messages before adding a new one
    storage = messages.get_messages(request)
    storage.used = True
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('/user_admin')
    