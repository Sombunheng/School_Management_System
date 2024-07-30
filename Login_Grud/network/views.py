from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import User, Role , Trail , Program

def index(request):
    roles = Role.objects.all()
    users = User.objects.all()
    
    return render(request, "network/index.html",{
        "role" : roles,
        'user' : users
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        print("first login right ?")
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user(request):
    print("this is page user")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]
        role_instane = Role.objects.get(pk=role)
        print("awdadwad" , username , email , role)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/user.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User(username=username, email=email, password=password , role=role_instane)
            user.save()
        except IntegrityError:
            return render(request, "network/user.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/user.html")

def create_trail(request):
    print("hello")
    list_trails = Trail.objects.all()
    client_name = Trail.objects.get(pk=19)
    print("------------------------------------")
    print("client name" , client_name.programs)
    for program in client_name.programs.all():
        print("list_trail" , program)
    for program in client_name.handle_by.all():
        print("list_trail" , program)
    # for list_trail in list_trails:
        
    if request.method == "POST":
        client = request.POST.get("client")
        phone = request.POST.get("phone")
        number_student = request.POST.get("number_student")
        status = request.POST.get("status")
        checkbox_program = request.POST.getlist("program")        
        assigned_by = request.POST.get("assign_by")
        # provided_by = request.POST.get("handle_by")
        checkbox_handleBy = request.POST.getlist('handle_by')
        users = User.objects.filter(role_id=1)
        obj_program = Program.objects.all()
        user_handles = User.objects.filter(id__in=checkbox_handleBy)
        programs = Program.objects.filter(id__in=checkbox_program)
        print("this it program " , programs)
        print("this it waht " , user_handles)
        for user_handle in user_handles:
            print("what is it loop?" , user_handle)
        # user_handle = User.objects.get(username=provided_by)
        
        print("Received data:", client, phone, number_student, status, checkbox_program , assigned_by  ,checkbox_handleBy)
        for user in users:
            print("Existing users:", user.username)
        
        try:
            trail = Trail(client=client , phone=phone , number_student=number_student , status=status ,assign_by=request.user )
            trail.save()
            
            trail.handle_by.set(user_handles)
            trail.programs.set(programs)
            
            trail.save()
            return render(request, "network/trail.html", {
                "users": users,
                "obj_program": obj_program,
            })
        except IntegrityError:
            return render(request, "network/trail.html", {
                "message": "Username already taken."
            })
        except Exception as e:
            print("Error occurred:", e)
            return render(request, "network/trail.html", {
                "message": "An unexpected error occurred."
            })
        
        
    else:
        users = User.objects.filter(role_id=1)
        obj_program = Program.objects.all()

        return render(request, "network/trail.html", {
                "users": users,
                "obj_program": obj_program
            })
    
    
