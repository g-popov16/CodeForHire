from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item, Category
from .forms import SignupForm
from django.contrib.auth import logout


def index(request):
    items = Item.objects.all()[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login')

    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form,
    })

@login_required
def log_out(request):
    logout(request)
    return redirect('/login')
