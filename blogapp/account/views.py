from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request,"account/login.html",{
                "error" : "kullanıcı veya parola yanlış!!!"
            })    
            
    return render(request, "account/login.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,"account/register.html",
                    {
                        "error": username + " kullanılıyor."
                    })
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                return redirect("login")
        else:
            return render(request, "account/register.html",
                {
                    "error":"parola eşleşmiyor."
                })


        
    return render(request, "account/register.html")
 
 
def logout_request(request):
    logout(request)
    return redirect("home")

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout(request):
# 	del request.session["uid"]
# 	return redirect('login')