from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.id

class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=255)

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publication_year = models.PositiveIntegerField()
    
    availability_status = models.BooleanField()
    description = models.TextField(max_length=300,null=True, blank=True)
    isbn = models.CharField(max_length=100)
    # pdf_info= models.FileField(upload_to='pdfs/', null=True, blank=True)
    pdf = models.FileField(upload_to='pdfs/')
    cover_page = models.ImageField(upload_to="coverPage/")

class User(models.Model):
    # user_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    membership_status = models.CharField(max_length=20)  # e.g., regular, premium

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_date = models.DateField()