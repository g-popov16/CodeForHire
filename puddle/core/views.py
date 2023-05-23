from django.shortcuts import render

from item.models import Item, Category


def index(request):
     items = Item.objects.all()[0:6]
     categories = Category.objects.all()
     return render(request, 'core/index.html', {
          'categories': categories,
          'items': items, 
          })


def contact(request):
     return render(request, 'core/contact.html')