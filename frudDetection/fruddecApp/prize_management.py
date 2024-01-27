import random 
from django.utils import timezone
from fruddecApp.models import Deposits, DailyWinner, PrizeDistributionDetails  
from django.db.models import Sum,F
from decimal import Decimal
from datetime import timedelta

def select_daily_winner():
    print("select_daily_winner")
    current_date = timezone.now().date()
    last_with_draw_datetime = DailyWinner.objects.latest("winning_date").winning_date

    # Ensure last_with_draw_datetime is not None
    last_with_draw_date = last_with_draw_datetime.date() if last_with_draw_datetime else current_date
    date_range_list = [last_with_draw_date + timedelta(days=x) for x in range((current_date - last_with_draw_date).days + 1)]


    for lucky_drawer_date in date_range_list:
        depositors = Deposits.objects.filter(deposit_date__date=lucky_drawer_date)
        
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
            
            # Create and save Prize Distribution Details instance linked to DailyWinner
            PrizeDistributionDetails.objects.create(
                winner=database_winner,
                deduction_amount=deduction_amount,
                welfare_fund_amount=welfare_fund_amount,
                service_charges=service_charges,
            )
            
            print("Daily winner selected and saved successfully.")
        else:
            print(f"No deposits found for {lucky_drawer_date}. No winner selected.")
    

def credit_monthly_return():
    # Get the current date in the timezone used by Django
    current_date = timezone.now().date()
    
    # Calculate the start and end dates for the current month
    start_of_month = current_date.replace(day=1)
    end_of_month = start_of_month.replace(year=start_of_month.year + 1,month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1)
    
    print("Start Date:", start_of_month)
    print("End Date:", end_of_month)

    # Update winners who should receive the monthly return within the date range
    test = DailyWinner.objects.filter(
        monthly_return=0.00,
        winning_date__range=(start_of_month, end_of_month)
    ).update(monthly_return=F('monthly_return') + 1000)

    print("TEST:", test)
    
def detect_fraudulent_activity(user_id):
    return False