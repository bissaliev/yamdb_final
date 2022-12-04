from django.contrib import admin

from .models import Comment, Review, Title, Category, Genre, GenreTitle


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
