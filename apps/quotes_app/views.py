from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

# Create your views here.

def index(request):
	return(render(request, "quotes_app/index.html"))

def register(request):
    print(request.POST)
    results = User.objects.register(request.POST)

    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["alias"] = results[1].alias
        return redirect("/quotes")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def login(request):
    print(request.POST)
    results = User.objects.login(request.POST)

    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["alias"] = results[1].alias
        return redirect("/quotes")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def quotes(request):
    registered_users = User.objects.all()
    current_user = User.objects.get(id = request.session['user_id']) 
    favorites = Quote.objects.filter(favoriting_users=current_user)
    allquotes = Quote.objects.all().order_by('-id').exclude(id__in=[f.id for f in favorites])
    context = {
        "registered_users": registered_users,
        "current_user": current_user,
        "quotes": allquotes,
        "favorites" : favorites
    }

    return render(request, "quotes_app/quotes.html", context)

def addquote(request):
    if request.method == "GET":
        return redirect ('/')
    if request.method == "POST":
        quote_text = request.POST['quote_text']
        user_id = request.session['user_id']
        author = request.POST['author']
        result = Quote.objects.validate_quote(quote_text, user_id, author)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect ('/quotes')
        else:
            return redirect('/quotes')

def users(request, user_id):
    created_by = User.objects.get(id=user_id)
    context = {
        'quotes': Quote.objects.filter(created_by = created_by),
        'created_by': created_by 
    }
    return render(request, "quotes_app/users.html", context)

def favorite(request, quote_id):
    user_id = request.session['user_id']
    Quote.objects.add_favorite(user_id, quote_id)
    return redirect('/quotes')

def remove(request, quote_id):
    user_id = request.session['user_id']
    Quote.objects.remove_favorite(user_id, quote_id)
    return redirect('/quotes')