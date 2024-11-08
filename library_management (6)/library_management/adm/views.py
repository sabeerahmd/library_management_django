from django.shortcuts import render


from django.shortcuts import render,redirect
from adm.form import CustomUserForm
from adm.models import *
from django.contrib.auth.models import User
# from app.models import Book_Login
from django.contrib.auth import authenticate,login
from datetime import datetime
from django.db import transaction


# Create your

# @views here.




def adminsignup(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        # query_dict = request.POST
        # username = query_dict.get('username')
        # print(username)
        # email =  query_dict.get('email')
        # print(email)
        if form.is_valid():
            form.save()
            # admin_user = User.objects.filter(email=email).first()
            # user_id = admin_user
            # user_details = StudentDetails(username = username,email = email,user = user_id)
            # user_details.save()
            return redirect('/admin_login')
        else:
            print("error")
    return render(request,'adminsignup.html')



def adminlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        print(3)
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        print("admin.two")
        try:
            print("admin3")
            user=authenticate(request,username=name,password=pwd)
            print(user)
            print("admin4")
            if user is not None:
                print("admin5")
                login(request,user)
                print("admin6")
                return redirect('/book_details')
            else:
                print("admin7")
                return redirect ('/admin_login')

        except:
            pass
    return render(request,'adminlogin.html')

# Create your views here.
def welcome (request):
    return render(request,'welcome.html')




def bookdetails(request):
    obj=BookDetails.objects.all()
    return render(request,'bookdetails.html',{'obj':obj})

def book_page(request):
    if request.method=='POST':
        if request.user.is_authenticated: #check login or not
            user_id = request.user.id
            date = datetime.now().date()
            BookDetails.objects.create(name=request.POST.get('Name'),book_code=request.POST.get('Code'),author_name=request.POST.get('Author'),
                                            date=request.POST.get('Date'),status=request.POST.get('Status'),amount=request.POST.get('Amount'),
                                            created_date=date,created_by=user_id,available_books = request.POST.get('available_books'),
                                            book_img = request.FILES['updatebook'])

            # a = BookDetails(name = request.POST.get('Name'))
            # a.save()
            return redirect("/book_details")
        else:
            return redirect("/add_book")
    return render(request, 'bookpage.html')

def updatebook(request,pk):
    obj=BookDetails.objects.get(id=pk)
    if request.method=='POST':
        library = BookDetails.objects.filter(id=pk).first()
        library.name = request.POST.get('Name')
        library.book_code = request.POST.get('Code')
        library.author_name = request.POST.get('Author')
        library.date = request.POST.get('Date')
        library.amount = request.POST.get('Amount')
        library.available_books = request.POST.get('available_books')
        library.book_img = request.FILES['updatebook']
        date = datetime.now().date()
        library.updated_date = date
        library.updated_by = request.user.id
        library.save()
        return redirect('/book_details')
    return render(request,'updatebook.html',{'obj':obj})

def deletebook(request,pk):
    # BookDetails.objects.filter(id=pk).delete()
    a = BookDetails.objects.filter(id=pk).first()
    a.delete()
    return redirect('/book_details')

def student_signup(request):
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        username = request.POST.get('username')
        print(username)
        print(1)
        email =  request.POST.get('email')
        print(email)
        print(2)
        if form.is_valid():
            print(3)
            form.save()
            admin_user = User.objects.filter(email=email).first()
            user_id = admin_user.id
            print(user_id)
            user_details = StudentDetails(username = request.POST.get('username'),
            email = request.POST.get('email'),user_id = user_id)
            user_details.save()
            return redirect('/student_login')
    return render(request,'studentsignup.html')

def student_login(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(3)
        try:
            user=authenticate(request,username=request.POST.get('Name'),password=pwd)
            print(4)
            if user is not None:
                print(5)
                print(user)
                login(request,user)
                print(6.5)
                user_id = request.user.id
                print(user_id)
                student=StudentDetails.objects.filter(user_id = user_id).first()
                print(student,5)
                print(7)
                if student.status==1:
                    print(8)
                    return redirect('/take_book')
                else:
                    return redirect ('/student_login')
                #return redirect ('/adm/student_login')
            else:
                print("user is not found")
            

        except:
            pass
    return render(request,'studentlogin.html')

def take_book(request):
    obj = BookDetails.objects.all()
    if request.method=='POST':
        book_name=request.POST.get('search')
        book_code=request.POST.get('searchcode')
        if book_code =='':
            obj  = BookDetails.objects.filter(name=book_name)
        if book_name == '':
            obj = BookDetails.objects.filter(book_code=book_code)
        
    return render(request,'take_book.html',{'obj':obj})

@transaction.atomic()
def takebook(request,pk):
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            #Reduce amount in Useraccount
            book_id = pk
            book_details = BookDetails.objects.filter(id = book_id).first()
            if book_details.available_books != 0:
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books
                user_details = StudentDetails.objects.filter(user_id = request.user.id).first()
                student_id = user_details.id
                #Amount Reduction
                user_amount = user_details.wallet_balance
                current_amount = user_amount - book_price
                user_details.wallet_balance = current_amount
                user_details.save()
                
                #Book History Registeration
                # student = StudentDetails.objects.filter(user_id = user_id).first()
                # student_id = student.id
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Take")
                book_history.save()
                    
                #UserBookstatus Registeration
                status = UserBookStatus(student_id=student_id,book_id = book_id)
                status.save()

                #UserBookDetails Registeration
                user = UserBookDetails.objects.filter(student_id = student_id).first()
                if user is  None:
                    user_book_details = UserBookDetails(student_id = student_id,
                                                books_quantity = 1,created_at = date)
                    user_book_details.save()
                else:
                    user_update = UserBookDetails.objects.filter(student_id = student_id).first()
                    books_quantity = user_update.books_quantity 
                    quantity = int(books_quantity) +1
                    user_update.books_quantity = quantity
                    user_update.save()

                #Books reduction in BookDetails
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity-=1

                book_details.available_books = quantity
                if quantity == 0:
                    book_details.status = 'Unavailable'
                book_details.save()
            else:
                print("No stocks")
            return redirect('/take_book')

@transaction.atomic()
def retainbook(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.id
        book_id = pk
        student = StudentDetails.objects.filter(user_id = user_id).first()
        student_id = student.id
        user_book = UserBookStatus.objects.filter(student_id=student_id,book_id=book_id).first()
        if user_book is not None:
            if user_book.status == 1:
                date = datetime.now().date()
                    
                #Details
                book_details = BookDetails.objects.filter(id = book_id).first()
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books

                #Book History Registeration
               
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Return")
                book_history.save()

                # books reduction
                books_reduction = UserBookDetails.objects.filter(student_id = student_id).first()
                book_quantity = books_reduction.books_quantity
                quantity = book_quantity-1
                books_reduction.books_quantity = quantity
                books_reduction.save()

                #books updation
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity+=1
                book_details.available_books = quantity
                if quantity !=0:
                    book_details.status = 'Available'
                book_details.save()
                # user_book.status = 0
                # user_book.save()
                user_book.delete()
            else:
                print("you dont have book so you are not able to return")

        else:
            print("please purchase book")


                
    return redirect('/take_book')


#overview
### admin work
# admin_signup
# admin_login
# book_page
# add_book
# update_book
# delete book


### student work
#student signup
#student_login
#book_details_page
#take book
#retain book
#search

#home page
                   #Wecome to Library Management

                        #admin login
                        #student login