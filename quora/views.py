import copy

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from .models import Question, Comment, Like

def index(req):
    loggedIn = req.user.is_authenticated
    questions = Question.objects.order_by("-pub_date")
    comments = []
    for question in questions:
        questionComments = Comment.objects.filter(question_id=question.id).order_by("-pub_date").order_by("-likes")
        for comment in questionComments:
            this_comment = copy.deepcopy(comment)
            if loggedIn:
                if Like.objects.filter(comment=comment, user=req.user).__len__():
                    this_comment.liked = 1
                else:
                    this_comment.liked = 0
            comments.append(this_comment)
    
    user = req.user
    print(comments)
    return render(req, 'quora/index.html', 
    {   "questions": questions, 
        "comments": comments,
        "loggedIn": loggedIn,
        "user": user
    })

def login(req):
    if(req.method=="POST"):
        username = req.POST['username']
        password = req.POST['password']
        
        user = authenticate(req, username=username, password=password)
        if user is not None:
            auth_login(req, user)
            return redirect(index)

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

        return redirect(index)
    
    return render(req, 'quora/signup.html')

def logout(req):
    auth_logout(req)
    return redirect(index)

def post_question(req):
    if req.user.is_authenticated and req.method=="POST":
        question = req.POST['question']
        Question.objects.create(question_text=question, pub_date=timezone.now(), pub_by=req.user)
        return redirect(index)
    
    return render(req, 'quora/post-question.html')

def post_comment(req, question_id):
    if req.user.is_authenticated and req.method=="POST":
        comment = req.POST['comment']
        question = Question.objects.filter(id=question_id)[0]
        Comment.objects.create(question=question, comment_text=comment, likes=0, pub_date=timezone.now(), pub_by=req.user)
        return redirect(index)
    
    return render(req, 'quora/post-comment.html')

def post_upvote(req):
    if req.user.is_authenticated and req.method=="POST":
        comment_id = req.POST['comment_id']
        comment = Comment.objects.filter(id=comment_id)[0]
        likes = Like.objects.filter(comment_id=comment_id, user_id=req.user.id)
        
        if not likes.__len__():
            comment.likes+=1
            Like.objects.create(user=req.user, comment=comment)
        else:
            comment.likes-=1
            like = likes[0]
            like.delete()

        comment.save()
    return redirect(index)

def delete_comment(req):
    if req.user.is_authenticated and req.method=="POST":
        comment_id = req.POST['comment_id']
        comment = Comment.objects.filter(id=comment_id)
        comment.delete()

    return redirect(index)