from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from .models import Question

def index(req):
    questions = Question.objects.order_by("-pub_date")
    return render(req, 'quora/index.html', { "questions": questions, "username": req.user.username })

def login(req):
    if(req.method=="POST"):
        username = req.POST['username']
        password = req.POST['password']
        
        user = authenticate(req, username=username, password=password)
        if user is not None:
            auth_login(req, user)
            return redirect(index)

    print(req.user)

    return render(req, 'quora/login.html')

def signup(req):
    if(req.method=="POST"):
        username = req.POST['username']
        firstName = req.POST['firstName']
        lastName = req.POST['lastName']
        email = req.POST['email']
        password = req.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstName
        user.last_name = lastName
        user.save()

        return render(req, 'quora/login.html')
    
    return render(req, 'quora/signup.html')