import csv
import os
from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

from reviews.models import Genre, Category, Title, Review, GenreTitle, Comment

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    help = "Load data from csv file to model"
    PATH_FILE = os.path.join(BASE_DIR, "data")
    models = {
        "genre.csv": Genre,
        "category.csv": Category,
        "users.csv": User,
        "titles.csv": Title,
        "genre_title.csv": GenreTitle,
        "review.csv": Review,
        "comments.csv": Comment,
    }

    def load_file(self, file, model):
        with open(
            f'{os.path.join(BASE_DIR, "data", file)}', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter=',')
            model.objects.all().delete()
            for row in reader:
                model.objects.get_or_create(**row)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Данные для модель '{model}' загружена в БД.")
            )

    def main(self):
        for csv_file, model in self.models.items():
            self.load_file(csv_file, model)
        self.stdout.write(
            self.style.SUCCESS("Данные полностью загружены в БД.")
        )

    def handle(self, *args: Any, **options: Any):
        self.main()
