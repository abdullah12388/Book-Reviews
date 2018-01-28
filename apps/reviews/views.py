from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

import bcrypt
from models import *

def index(request):
    if request=='POST':
        return redirect('/')
    else:
        return render(request, 'log_and_reg/index.html')

def success(request):
    # Check if the user logged in
    if request.session['user_id']:
        return render(request, 'log_and_reg/success.html',
                {"user": User.objects.get(id=request.session['user_id'])})
    else:
        return redirect('/')

def processRegistration(request):
    # Check if entered info is valid
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    else:
        email = request.POST['email']
        # Check if a user with this email already exists
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists")
            return redirect('/')
        except:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = bcrypt.hashpw(request.POST['password'].encode(),
                    bcrypt.gensalt())
            # Create a new user
            this_user = User.objects.create(first_name = first_name,
                    last_name = last_name, email = email, password = password)
            request.session['user_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/success')

def processLogin(request):
    email = request.POST['email']
    # Check if the user is registered
    try:
        this_user = User.objects.get(email=email)
        if bcrypt.checkpw(
                request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            messages.error(request, "Successfully registered (or logged in)!")
            return redirect('/success')
        else:
            messages.error(request, "Wrong password")
            return redirect('/')
    except:
        messages.error(request, "Email not found")
        return redirect('/')

def logout(request):
    request.session['user_id'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/')
