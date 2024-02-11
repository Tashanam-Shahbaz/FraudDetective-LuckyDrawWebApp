from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from fruddecApp.prize_management import select_daily_winner,credit_monthly_return,detect_fraudulent_activity
from .models import Deposits,CustomUserCreationForm,CustomUserEditForm,DailyWinner,PrizeDistributionDetails,FrudulentActivityDetail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

# function run when the program start
select_daily_winner()
credit_monthly_return()


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
        print(password)
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
    if request.user.is_authenticated:
        user = request.user
        deposits = Deposits.objects.filter(user=user).order_by('deposit_date').reverse()
        winners = DailyWinner.objects.all().order_by('winning_date').reverse()   

                # Check if there is a winner for today
        today_winner = None
        today = datetime.now().date()
        if winners[0].winning_date.date() == today:
            today_winner = winners[0]

        # Prepare winner message
        winner_msg = ""
        if today_winner:
            winner_msg = f"Today's winner: {today_winner.user.first_name} { today_winner.user.last_name}"
        else:
            winner_msg = "Today \'s winner has not been announced yet."

        return render(request, 'profile.html', {'deposits': deposits,'winners':winners,   "winner_msg":winner_msg})
    else:
        # Handle the case when the user is not authenticated
        return render(request, 'profile.html', {'deposits': None})
   
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


def update_user_2(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        # Clear existing messages before adding a new one
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, 'Sign in Again')
        return redirect('signin')

    form = CustomUserEditForm(request.POST, instance=user) if request.method == 'POST' else CustomUserEditForm(instance=user)

    if request.method == 'POST' and form.is_valid():
        password = request.POST.get('password', '').strip()
        user.set_password(password)
        form.save()
        user.save()
        update_session_auth_hash(request, user)
        
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, 'User updated successfully')
        return redirect('profile')
    elif request.method == 'POST':
        messages.error(request, 'Please correct the errors in the form.')

    return render(request, 'update_user_2.html', {'form': form, 'user': user})

def user_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
       # Retrieve all records from the table
        users = User.objects.filter(is_superuser=False)
        winners = DailyWinner.objects.all().order_by('winning_date').reverse()   
        frudDetectionDetail = FrudulentActivityDetail.objects.all()
        frud_deposit_id = frudDetectionDetail.values_list('deposit_id', flat=True)
        deposits = Deposits.objects.exclude(deposit_id__in=frud_deposit_id).order_by('deposit_date').reverse()
        pdd = PrizeDistributionDetails.objects.all()

        
        # Check if there is a winner for today
        today_winner = None
        today = datetime.now().date()
        if winners[0].winning_date.date() == today:
            today_winner = winners[0]

        # Prepare winner message
        winner_msg = ""
        if today_winner:
            winner_msg = f"Today's winner: {today_winner.user.first_name} { today_winner.user.last_name}"
        else:
            winner_msg = "Today \'s winner has not been announced yet."
       
        return render(request, 'admin.html',{
            'users': users,
            'winners':winners,
            'deposits':deposits,
            'pdd':pdd,
            "frudDetectionDetail":frudDetectionDetail,
            "winner_msg":winner_msg
            })
    else:
        return redirect('/')

def update_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = request.user
    else:
        # Clear existing messages before adding a new one
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, 'Sign in Again')
        return redirect('signin')

    form = CustomUserEditForm(request.POST, instance=user) if request.method == 'POST' else CustomUserEditForm(instance=user)

    if request.method == 'POST' and form.is_valid():
        password = request.POST.get('password', '').strip()
        user.set_password(password)
        form.save()
        user.save()
        update_session_auth_hash(request, user)
        
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, 'Admin updated successfully')
        return redirect('user_admin')
    elif request.method == 'POST':
        messages.error(request, 'Please correct the errors in the form.')

    return render(request, 'update_admin.html', {'form': form, 'user': user})

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


def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            form.save()

            # Clear existing messages before adding a new one
            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, 'User updated successfully')
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
    
def select_winner(request):
    select_daily_winner()
    return redirect("/user_admin")


def credit_monthly_return_view(request):
    credit_monthly_return()
    return redirect("/user_admin")    



def demo_frud_deposit(request):
    
    col_numbers = list(range(1, 29))
    user = request.user
    if user.is_authenticated:     
        if request.method == 'POST':
            
            v_values =  [float(request.POST.get(f'V{i}', 0 )) for i in range(1, len(col_numbers) + 1 )]
            v_values =  [float(request.POST.get('time', 0))] + v_values + [float(request.POST.get('amount', 0 ))]
            comment  =  request.POST.get('comment')

            result = detect_fraudulent_activity(user,v_values,comment)
           
            storage      = messages.get_messages(request)
            storage.used = True
            message_text = "Your deposit has been successfully submitted." if result else "Suspicious activity detected."
            messages.success(request, message_text)
            
            return redirect("/profile") 
        
        return render(request, 'demo_deposit.html', {'user': request.user,'numbers':col_numbers}) # Get Method
    else:
        form = AuthenticationForm()

        # Clear existing messages before adding a new one
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request,"Oops! We encountered errors while processing your deposit."
                         "To ensure a successful transaction, please log in again and re-submit your deposit." 
                         "Thank you for your understanding")

        return render(request, 'login.html', {'form': form})
