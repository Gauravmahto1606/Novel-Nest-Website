from django.contrib import admin
from readApp.models import *
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Review)