from django.shortcuts import render,redirect,get_object_or_404,session
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import hashlib

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = login.query.filter_by(email=email).first()
        if not user:
            return "Email address not found"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.password != hashed_password:
            return "Incorrect password"

        session['user_id'] = user.id
        return render(request,'index.html')

    return render(request,'login.html')

@login_required
def index(request):
    users = Expense.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'index.html',context)

@login_required
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        created_by = request.user
        expense = Expense(
            name=name,
            date=date,
            category=category,
            description=description,
            amount=amount,
            created_by=created_by,
        )
        expense.save()
        messages.success(request, 'Expense created successfully!')
        return redirect('home')
    else:
        expense = Expense()
        context = {'expense': expense}
        return render(request, 'index.html',context)
    
login_required
def edit(request):
    users = Expense.objects.all()
    context = {
        'users':users,
    }
    return redirect(request, 'upate',context)
    
@login_required
def update(request, id):
    expense = get_object_or_404(Expense, pk=id, created_by=request.user)
    if request.method == 'POST':
        expense.name = request.POST['name']
        expense.date = request.POST['date']
        expense.category = request.POST['category']
        expense.description = request.POST['description']
        expense.amount = request.POST['amount']
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('index')
    return render(request, 'index.html', {'expense': expense})

@login_required
def delete(request, id):
    expense = get_object_or_404(Expense, pk=id, created_by=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('index')

@login_required
def view_expenses(request):
    if request.user.is_staff:
        expenses = Expense.objects.all()
    else:
        expenses = Expense.objects.filter(created_by=request.user)
    return render(request, 'index', {'expenses': expenses})

def logout():
    session.pop('user_id', None)
    return redirect('/')
