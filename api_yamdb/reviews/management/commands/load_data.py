import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

BASE_DIR = settings.BASE_DIR


MODEL = {
    "user": (User, "users.csv"),
    "category": (Category, "category.csv"),
    "genre": (Genre, "genre.csv"),
    "title": (Title, "titles.csv"),
    "review": (Review, "review.csv"),
    "comment": (Comment, "comments.csv"),
    "genre_title": (GenreTitle, "genre_title.csv"),
}


class Command(BaseCommand):
    help = "Загрузка данных из csv-файла в БД."

    def get_csv_file(self, filename) -> str:
        return os.path.join(BASE_DIR, "static", "data", filename)

    def load_data(self, key: str):
        model, filename = MODEL.get(key)
        file_path = self.get_csv_file(filename)
        with open(file_path, encoding="utf-8") as file:
            csv_file = csv.DictReader(file)
            model.objects.all().delete()
            for row in csv_file:
                model.objects.create(**row)

    def handle(self, *args, **options):
        for key in MODEL:
            self.load_data(key)
