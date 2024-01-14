from django.db import models
from django.contrib.auth.models import User  # Import Users model if it's in the same app
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CustomUserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['username','first_name','last_name','password','email']  # Include the fields you want to display/edit


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].required = True
        self.fields['email'].required = True


class Deposits(models.Model):
    STATUS_CHOICES = [
        ('Successful', '1'),
        ('Failed', '3'),
        ('Pending', '2')
    ]

    deposit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default=STATUS_CHOICES[0][1])
    comment = models.CharField(max_length=500,default="")

    def __str__(self):
        return f"Deposit ID: {self.deposit_id}, User: {self.user}, Amount: {self.amount}, Status: {self.status},Comment: {self.comment}"


class DailyWinner(models.Model):

    winner_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winning_date = models.DateTimeField()
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    monthly_return = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Winner ID: {self.winner_id}, User: {self.user}, Amount: {self.winning_amount}, Monthly Return: {self.monthly_return},Date Time: {self.winning_date}"


class PrizeDistributionDetails(models.Model):
    prize_distribution_detail_id = models.AutoField(primary_key=True)
    winner = models.OneToOneField(DailyWinner, on_delete=models.CASCADE, related_name='details')
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    service_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    welfare_fund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Winner: {self.winner.user}, Deduction: {self.deduction_amount}, Welfare Fund: {self.welfare_fund_amount},Services Charges: {self.service_charges}"


class FrudulentActivityDetail(models.Model):
    frudulent_activity_detail_id = models.AutoField(primary_key=True)
    date_of_occurance = models.DateTimeField()
    log = models.CharField(max_length=500,default="")
    deposit = models.OneToOneField(Deposits, on_delete=models.CASCADE, related_name='frudulentactivity')