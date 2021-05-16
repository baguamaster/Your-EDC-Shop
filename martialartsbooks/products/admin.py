from django.contrib import admin

# Register your models here.
from .models import Book, Publisher, Genre, Tag, Author

admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Author)
