import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

MODEL = {
    "user": (User, "users.csv"),
    "category": (Category, "category.csv"),
    "genre": (Genre, "genre.csv"),
    "title": (Title, "titles.csv"),
    "review": (Review, "review.csv"),
    "comment": (Comment, "comments.csv"),
}


class Command(BaseCommand):
    help = "Load data from csv file to model"

    @staticmethod
    def get_csv_file(filename):
        return os.path.join(settings.BASE_DIR, "static", "data", filename)

    @staticmethod
    def clear_model(model):
        model.objects.all().delete()

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def load_model(self, model_name, field_names):
        model, file_path = MODEL.get(model_name)
        with open(self.get_csv_file(file_path)) as file:
            reader = csv.reader(file, delimiter=",")
            self.clear_model(model)
            line = 0
            for row in reader:
                if row != "" and line > 0:
                    params = dict(zip(field_names, row))
                    _, created = model.objects.get_or_create(**params)
                line += 1
        self.print_to_terminal(f"{line - 1} objects added to {model_name}")

    def load_user(self):
        self.load_model(
            "user",
            ["id", "username", "email", "role", "bio",
             "first_name", "last_name"]
        )

    def load_category(self):
        self.load_model("category", ["id", "name", "slug"])

    def load_genre(self):
        self.load_model("genre", ["id", "name", "slug"])

    def adding_genre_to_title(self):
        with open(self.get_csv_file("genre_title.csv")) as file:
            reader = csv.reader(file, delimiter=",")
            line = 0
            for row in reader:
                if row != "" and line > 0:
                    title = get_object_or_404(Title, pk=row[1])
                    genre = get_object_or_404(Genre, pk=row[2])
                    title.genre.add(genre)
                line += 1
        self.print_to_terminal(f"{line - 1} objects added to genre_title")

    def load_title(self):
        self.load_model("title", ["id", "name", "year", "category_id"])
        self.adding_genre_to_title()

    def load_reviews(self):
        self.load_model(
            "review",
            ["id", "title_id", "text", "author_id", "score", "pub_date"]
        )

    def load_comments(self):
        self.load_model(
            "comment", ["id", "review_id", "text", "author_id", "pub_date"]
        )

    def handle(self, *args, **kwargs):
        self.load_user()
        self.load_category()
        self.load_genre()
        self.load_title()
        self.load_reviews()
        self.load_comments()
