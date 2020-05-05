from django.shortcuts import render, redirect
from .models import Pizza
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

#when a URL request matched the pattern we just defined, Django looks for a function called index() in the views.py file.
def index(request):
    #The home page for pizzeria.
    return render(request, 'pizzas/index.html')

@login_required
def pizzas(request):
    pizzas = Pizza.objects.filter(owner=request.user).all()
    context = {'pizzas':pizzas}
    return render(request, 'pizzas/pizzas.html', context)

@login_required
def pizza(request,pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    #make suer the pizza belongs to the current user
    if pizza.owner != request.user:
        raise Http404
    # foreign key can be accessed using '_set'
    toppings = pizza.topping_set.all()
    comments = pizza.comment_set.all()
    context = {'pizza':pizza, 'toppings':toppings, 'comments':comments}
    return render(request, 'pizzas/pizza.html', context)

@login_required
def new_comment(request,pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.pizza = pizza
            new_comment.save()
            form.save()
            return redirect('pizzas:pizza',pizza_id=pizza_id)
    
    context = {'form': form, 'pizza': pizza}
    return render(request, 'pizzas/new_comment.html', context)
