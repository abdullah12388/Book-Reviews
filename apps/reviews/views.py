from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

import bcrypt
from models import *


def index(request):
    if request=='POST':
        return redirect('/')
    else:
        return render(request, 'reviews/index.html')


def processRegistration(request):
    # Check if entered info is valid
    errors = User.objects.user_validator(request.POST)
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
            alias = request.POST['alias']
            password = bcrypt.hashpw(request.POST['password'].encode(),
                    bcrypt.gensalt())
            # Create a new user
            this_user = User.objects.create(first_name = first_name,
                    last_name = last_name, alias=alias, email = email,
                    password = password)
            request.session['user_id'] = this_user.id
            errors["success"] = "Successfully registered (or logged in)!"
            return redirect('/books')


def processLogin(request):
    email = request.POST['email']
    # Check if the user is registered
    try:
        this_user = User.objects.get(email=email)
        if bcrypt.checkpw(
                request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            messages.error(request, "Successfully registered (or logged in)!")
            return redirect('/books')
        else:
            messages.error(request, "Wrong password")
            return redirect('/')
    except:
        messages.error(request, "Email not found")
        return redirect('/')


def showBooks(request):
    if request.session['user_id']:
        recent_reviews = Review.objects.all().order_by('-created_at')[:3]
        this_user = User.objects.get(id=request.session['user_id'])
        return render(request, 'reviews/books.html',
                {"recent_reviews": recent_reviews, "user": this_user,
                 "books": Book.objects.all()})
    else:
        return redirect('/')


def showAddForm(request):
    if request.session['user_id']:
        return render(request, 'reviews/add.html',
            {"authors": Book.objects.order_by().values('author').distinct()} )
    else:
        return redirect('/')


def addBook(request):
    errors = User.objects.book_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/books/add')
    else:
        # Check if entered data is valid
        title = request.POST['title']
        if request.POST['author']:
            author = request.POST['author']
        else:
            author = request.POST['author-from-list']
        uploader = request.session['user_id']
        review = request.POST['review']
        rating = request.POST['rating']
        this_user = User.objects.get(id=request.session['user_id'])
        this_book = Book.objects.create(title=title, author=author,
            uploader=this_user)
        #this_book.reviewed_users.add(this_user)
        #this_user.reviewed_books.add(this_book)
        Review.objects.create(review=review, rating=rating, book=this_book,
            user=this_user)
        return redirect('/books/'+str(this_book.id))


def showOneBook(request, number):
    if request.session['user_id']:
        this_book = Book.objects.get(id=number)
        print this_book
        return render(request, 'reviews/book.html',
            {"reviews": Review.objects.filter(book=this_book),
             "book": this_book})
    else:
        return redirect('/')


def addReview(request, number):
    # Check if entered data is valid
    errors = User.objects.review_validator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/books/'+number)
    else:
        uploader = request.session['user_id']
        review = request.POST['review']
        rating = request.POST['rating']
        this_user = User.objects.get(id=request.session['user_id'])
        this_book = Book.objects.get(id=number)
        #this_book.reviewed_users.add(this_user)
        #this_user.reviewed_books.add(this_book)
        Review.objects.create(review=review, rating=rating,
            book=this_book, user=this_user)
        return redirect('/books/'+str(this_book.id))


def deleteReview(request, number):
    this_review = Review.objects.get(id=number)
    this_book = this_review.book
    if request.session['user_id'] == this_review.user.id:
        this_review.delete()
    return redirect('/books/'+str(this_book.id))



def showUser(request, number):
    if request.session['user_id']:
        this_user = User.objects.get(id=number)
        count = Review.objects.filter(user=this_user).count()
        return render(request, 'reviews/user.html', {"user": this_user,
            "reviews": Review.objects.filter(user=this_user), "count": count})
    else:
        return redirect('/')


def logout(request):
    request.session['user_id'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/')
