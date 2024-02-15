import csv
import os
from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# User = settings.AUTH_USER_MODEL

from reviews.models import Genre, Category, Title, Review, GenreTitle, Comment

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    help = "Load data from csv file to model"

    def load_genres(self):
        file = os.path.join(BASE_DIR, "static", "data", "genre.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            Genre.objects.all().delete()
            for row in reader:
                Genre.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Жанр {row['name']} добавлен в модель Genre."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_categories(self):
        file = os.path.join(BASE_DIR, "static", "data", "category.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            Category.objects.all().delete()
            for row in reader:
                Category.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Категория {row['name']} добавлен в модель Category."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_users(self):
        file = os.path.join(BASE_DIR, "static", "data", "users.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            # Genre.objects.all().delete()
            for row in reader:
                User.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"user {row['username']} добавлен в модель User."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_titles(self):
        file = os.path.join(BASE_DIR, "static", "data", "titles.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            Title.objects.all().delete()
            for row in reader:
                Title.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Произведение {row['name']} добавлен в модель Title."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_genre_title(self):
        file = os.path.join(BASE_DIR, "static", "data", "genre_title.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            GenreTitle.objects.all().delete()
            for row in reader:
                GenreTitle.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(f"Связь добавлена в модель GenreTitle.")
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_reviews(self):
        file = os.path.join(BASE_DIR, "static", "data", "review.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            Review.objects.all().delete()
            for row in reader:
                Review.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(f"Отзыв добавлен в модель Review.")
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def load_comments(self):
        file = os.path.join(BASE_DIR, "static", "data", "comments.csv")
        with open(file, encoding="utf-8") as r_file:
            reader = csv.DictReader(r_file, delimiter=",")
            Comment.objects.all().delete()
            for row in reader:
                Comment.objects.get_or_create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Комментарий добавлен в модель Comment."
                    )
                )
            self.stdout.write(self.style.SUCCESS("Записи добавлены."))

    def handle(self, *args: Any, **options: Any):
        self.load_users()
        self.load_genres()
        self.load_categories()
        self.load_titles()
        self.load_reviews()
        self.load_genre_title()
        self.load_comments()
