import datetime
import random 
from django.db import models
from django.utils import timezone
from fruddecApp.models import Deposits,DailyWinner
 
def select_daily_winner():
    current_date = timezone.now().date()
    print(current_date)
    depositors = Deposits.objects.filter(deposit_date__date=current_date)
    
    if depositors.exists():
        total_amount = depositors.aggregate(total_amount=models.Sum('amount'))['total_amount']
        total_amount = total_amount if total_amount else 0  # Handle case when there are no deposits
        winner = random.choice(depositors)
        database_winner = DailyWinner(user=winner.user, winning_date=current_date, amount=total_amount)
        database_winner.save()
        print("Daily winner selected and saved successfully.")
    else:
        print("No deposits found for today. No winner selected.")

    

def calculate_monthly_return(user_id):
    return 1000 

def detect_fraudulent_activity(user_id):
    return False