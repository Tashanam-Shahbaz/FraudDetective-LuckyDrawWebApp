import datetime
import random 
from django.db import models
from django.utils import timezone
from fruddecApp.models import Deposits, DailyWinner, WinnerDetails  
from django.db.models import Sum
from decimal import Decimal

def select_daily_winner():
    current_date = timezone.now().date()
    print(current_date)
    depositors = Deposits.objects.filter(deposit_date__date=current_date)
    
    if depositors.exists():
        daily_collected_amount = depositors.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        
        # Calculate deduction and prize amount
        prize_amount = daily_collected_amount * Decimal('0.8')
        deduction_amount = daily_collected_amount * Decimal('0.20')
        welfare_fund_amount = daily_collected_amount * Decimal('0.15')
        service_charges = daily_collected_amount * Decimal('0.05')
       
        # Randomly select a winner
        winner = random.choice(depositors)
        
        # Create and save DailyWinner instance
        database_winner = DailyWinner.objects.create(
            user=winner.user,
            winning_date=current_date,
            winning_amount=prize_amount,
        )
        
        # Create and save WinnerDetails instance linked to DailyWinner
        winner_details = WinnerDetails.objects.create(
            winner=database_winner,
            deduction_amount=deduction_amount,
            welfare_fund_amount=welfare_fund_amount,
            service_charges = service_charges,
        )
        
        print("Daily winner selected and saved successfully.")
    else:
        print("No deposits found for today. No winner selected.")
    

def calculate_monthly_return(user_id):
    return 1000 

def detect_fraudulent_activity(user_id):
    return False