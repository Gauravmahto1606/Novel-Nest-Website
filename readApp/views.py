from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from .forms import FileUploadForm
# from .models import UploadedFile
# from .forms import PDFFileForm

# Create your views here.
def home(request):
    zipped_data = Book.objects.select_related('author', 'genre').all()[:4]
    newReleases_data = Book.objects.all().order_by('-publication_year')[:4]
    romance_data = Book.objects.select_related('author', 'genre').filter(genre_id=1)[:4]
    sciFi_fantasy_data = Book.objects.select_related('author', 'genre').filter(genre_id=2)[:4]
    mystery_thriller_data = Book.objects.select_related('author', 'genre').filter(genre_id=3)[:4]
    comics_data = Book.objects.select_related('author', 'genre').filter(genre_id=4)[:4]

    zipped_data1 = Book.objects.select_related('author', 'genre').all()[4:8]
    newReleases_data1 = Book.objects.all().order_by('-publication_year')[4:8]
    romance_data1 = Book.objects.select_related('author', 'genre').filter(genre_id=1)[4:8]
    sciFi_fantasy_data1 = Book.objects.select_related('author', 'genre').filter(genre_id=2)[4:8]
    mystery_thriller_data1 = Book.objects.select_related('author', 'genre').filter(genre_id=3)[4:8]
    comics_data1 = Book.objects.select_related('author', 'genre').filter(genre_id=4)[4:8]


    if request.GET.get('search'):
        
        book_title = Book.objects.select_related('author', 'genre').filter(title__icontains = request.GET.get('search'))
        # for i in product :
        #     print(i.title)
        print(book_title)
        return render(request,"HOME/viewAll.html",context={'genre_data': book_title,'name':'Searched Book'})

    context = {'zipped_data': zipped_data,"newReleases_data":newReleases_data,"romance_data":romance_data,"sciFi_fantasy_data":sciFi_fantasy_data,"mystery_thriller_data":mystery_thriller_data,"comics_data":comics_data,'zipped_data1': zipped_data1,"newReleases_data1":newReleases_data1,"romance_data1":romance_data1,"sciFi_fantasy_data1":sciFi_fantasy_data1,"mystery_thriller_data1":mystery_thriller_data1,"comics_data1":comics_data1}

    return render(request,"HOME/index.html",context=context)

# def login(request):
#     return render(request,"HOME/login.html")

def Login_page(request):

    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Username does not exist.")
            return redirect("/login/")
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request, "Incorrect Password.")
            return redirect("/login/")
        else:
            login(request,user)
            return redirect("/")



    return render(request,"HOME/login.html",context={'page':'Login'})


def logout_page(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login/")
def bookDetails(request):

    try :
        author_data = Author.objects.all()
        genre_data = Genre.objects.all()
        book_id = Book.objects.last().book_id
        book_id+=1
        if request.method == "POST" :
            data = request.POST
            # book_id = (Book.objects.last().book_id + 1)
            title = data.get("title")
            author = data.get("selected_author")
            genre = data.get('selected_genre')
            publication_year = data.get("publication_year")
            isbn = data.get("isbn")
            availability_status = True
            cover_page = request.FILES.get("cover_page")
            pdf_info = request.FILES.get("pdf_info")
            description = data.get("description")
            
            print(title,author,genre,publication_year,isbn,availability_status,cover_page,pdf_info)
            bookDetails = Book.objects.create(book_id=book_id,title=title,author_id=author,genre_id=genre,publication_year=publication_year,isbn=isbn,availability_status=availability_status,description=description,cover_page=cover_page,pdf=pdf_info)
            bookDetails.save()
    except(Exception) as e :
        print(e)

    return render(request,"HOME/addBook.html",context={"author_data":author_data,"genre_data":genre_data})

def viewBook(request,id):
    
    # book_data = Book.objects.all()
    # author_data = Author.objects.all()
    # genre_data = Genre.objects.all()
    book_data = Book.objects.get(book_id=id)
    # print(book_data)
    # return render(request,"HOME/viewBook.html",context={"book_data":book_data,"author_data":author_data,"genre_data":genre_data})
    # zipped_data = zip(book_data, author_data, genre_data)
    # context = {'zipped_data': zipped_data}
    # book_data = Book.objects.select_related('author', 'genre')
    context = {'book_data': book_data}
    # print(context)
    return render(request, 'HOME/viewBook.html', context=context)

# def getCarouselId(request) :
#     if request.method


def viewAll(request,id=None):
    
    if(id=="bestSeller"):
        book_data = Book.objects.select_related('author', 'genre').all()
        name = "BEST SELLER"
    
    elif(id == "newReleases") :
        book_data = Book.objects.all().order_by('-publication_year')
        name = "NEW RELEASES"
    
    else  :
        # book_data = Book.objects.get(book_id=id)
        book_data = Book.objects.select_related('author', 'genre').filter(genre_id=id)
        name = book_data[0].genre.genre_name

    context = {"genre_data":book_data,"name":name}
    return render(request,"HOME/viewAll.html",context=context)


def register(request):
    if request.method == "POST":
       
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.error(request, "Username already taken")
            return redirect('/register/')
        
        user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
        )
        
        user.set_password(password)
        user.save()
        messages.info(request , "Account created successfully")
        return redirect('/register/')
    
    return render(request,"HOME/register.html",context={'page':'register'})
