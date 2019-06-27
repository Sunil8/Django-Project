from django import forms
from django.contrib import messages

nepaliMonth= (
    ('Baishak','Baishak'),
    ('Jestha','Jestha'),
    ('Ashad','Ashad'),
    ('Shrawan','Shrawan'),
    ('Bhadra','Bhadra'),
    ('Ashwin','Ashwin'),
    ('Kartik','Kartik'),
    ('Mangshir','Mangshir'),
    ('Poush','Poush'),
    ('Magh','Magh'),
    ('Falgun','Falgun'),
    ('Chaitra','Chaitra'),
)

class loginForm(forms.Form):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
        }))
    password=forms.CharField(label='password',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'password'
        }))
class employForm(forms.Form):
    request = forms.IntegerField(label='Total Liter of Petrol', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'required': True}))
    reason = forms.CharField(label='Mention your reason', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3}))


# employee/bill_submit
class bill_submit(forms.Form):
    bill_image = forms.ImageField(label='Upload your Bill Image', widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': 'multiple'}))
    petrol = forms.IntegerField(label='Total Liter of Petrol', widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    nepali_month=forms.CharField(label='Nepali month of bill submit',widget=forms.Select(choices=nepaliMonth,attrs={
        'class':'form-control',
        }))
    bill_month = forms.DateField(label='Bill Month', widget=forms.SelectDateWidget())
    month=forms.IntegerField(label='For how many month the bill has been submited' ,widget=forms.NumberInput(attrs={'class':'form-control','max':3,'min':1}))
class modify_request(forms.Form):
    petrol=forms.IntegerField(required=False,label='Total Liter of Petrol',widget=forms.NumberInput(
        attrs={ 'class': 'form-control'}))

class modify_bill(forms.Form):
    bill_image = forms.ImageField(label='Upload your Bill Image', widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': 'multiple'}))
    petrol = forms.IntegerField(label='Total Liter of Petrol', widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    bill_month = forms.DateField(label='Bill Month', widget=forms.SelectDateWidget())
    month=forms.IntegerField(label='For how many month the bill has been submited' ,widget=forms.NumberInput(attrs={'class':'form-control','max':3,'min':1}))
    