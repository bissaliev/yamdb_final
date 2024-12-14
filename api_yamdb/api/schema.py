from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view


class TitleViewExtension(OpenApiViewExtension):
    target_class = "api.views.review_views.TitleViewSet"

    def view_replacement(self):
        from reviews.models import Title

        @extend_schema(tags=["TITLES"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка произведений",
                description="Возвращает список всех произведений с информацией о рейтинге.",
            ),
            retrieve=extend_schema(
                summary="Получение информации о конкретном произведении",
                description="Возвращает полную информацию о выбранном произведении.",
            ),
            create=extend_schema(
                summary="Создание произведения",
                description="Добавляет новое произведение в базу данных.",
            ),
            update=extend_schema(
                summary="Обновление информации о произведении",
                description="Обновляет данные существующего произведения.",
            ),
            partial_update=extend_schema(
                summary="Частичное обновление информации о произведении",
                description="Обновляет данные существующего произведения.",
            ),
            destroy=extend_schema(
                summary="Удаление произведения",
                description="Удаляет выбранное произведение из базы данных.",
            ),
        )
        class Fixed(self.target_class):
            queryset = Title.objects.none()

        return Fixed


class CategoryViewExtension(OpenApiViewExtension):
    target_class = "api.views.review_views.CategoryViewSet"

    def view_replacement(self):
        from reviews.models import Category

        @extend_schema(tags=["CATEGORIES"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка всех категорий",
                description="Получение списка всех категорий.",
            ),
            create=extend_schema(
                summary="Добавление новой категории",
                description="Создать категорию.",
            ),
            destroy=extend_schema(
                summary="Удаление категории",
                description="Удалить категорию.",
            ),
        )
        class Fixed(self.target_class):
            queryset = Category.objects.none()

        return Fixed


class GenreViewExtension(OpenApiViewExtension):
    target_class = "api.views.review_views.GenreViewSet"

    def view_replacement(self):
        from reviews.models import Genre

        @extend_schema(tags=["GENRES"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка всех жанров",
                description="Получение списка всех жанров.",
            ),
            create=extend_schema(
                summary="Добавление нового жанра",
                description="Создать жанр.",
            ),
            destroy=extend_schema(
                summary="Удаление жанра",
                description="Удалить жанр.",
            ),
        )
        class Fixed(self.target_class):
            queryset = Genre.objects.none()

        return Fixed


class ReviewViewExtension(OpenApiViewExtension):
    target_class = "api.views.review_views.ReviewViewSet"

    def view_replacement(self):
        from reviews.models import Review

        @extend_schema(tags=["REVIEWS"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка всех отзывов",
                description="Получить список всех отзывов.",
            ),
            retrieve=extend_schema(
                summary="Получение отзыва по id",
                description="Получить отзыв по id для указанного произведения.",
            ),
            create=extend_schema(
                summary="Добавление нового отзыва",
                description="Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.",
            ),
            update=extend_schema(
                summary="Обновление отзыва по id",
                description="Обновить отзыв по id.",
            ),
            partial_update=extend_schema(
                summary="Частичное обновление отзыва по id",
                description="Частично обновить отзыв по id.",
            ),
            destroy=extend_schema(
                summary="Удаление отзыва по id",
                description="Удалить отзыв по id",
            ),
        )
        class Fixed(self.target_class):
            queryset = Review.objects.none()

        return Fixed


class CommentViewExtension(OpenApiViewExtension):
    target_class = "api.views.review_views.CommentViewSet"

    def view_replacement(self):
        from reviews.models import Comment

        @extend_schema(tags=["COMMENTS"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка всех комментариев к отзыву",
                description="Получить список всех комментариев к отзыву по id.",
            ),
            retrieve=extend_schema(
                summary="Получение комментария к отзыву",
                description="Получить комментарий для отзыва по id.",
            ),
            create=extend_schema(
                summary="Добавление комментария к отзыву",
                description="Добавить новый комментарий для отзыва.",
            ),
            update=extend_schema(
                summary="Обновление комментария к отзыву",
                description="Обновить комментарий к отзыву по id.",
            ),
            partial_update=extend_schema(
                summary="Частичное обновление комментария к отзыву",
                description="Частично обновить комментарий к отзыву по id.",
            ),
            destroy=extend_schema(
                summary="Удаление комментария к отзыву",
                description="Удалить комментарий к отзыву по id",
            ),
        )
        class Fixed(self.target_class):
            queryset = Comment.objects.none()

        return Fixed


class UserViewExtension(OpenApiViewExtension):
    target_class = "api.views.user_views.UserViewSet"

    def view_replacement(self):
        from users.models import User

        @extend_schema(tags=["USERS"])
        @extend_schema_view(
            list=extend_schema(
                summary="Получение списка всех пользователей",
                description="Получить список всех пользователей.",
            ),
            create=extend_schema(
                summary="Добавление пользователя",
                description="Добавить нового пользователя.",
            ),
            retrieve=extend_schema(
                summary="Получение пользователя по id",
                description="Получить пользователя по id.",
            ),
            update=extend_schema(
                summary="Изменение данных пользователя по id",
                description="Изменить данные пользователя по id.",
            ),
            partial_update=extend_schema(
                summary="Частичное изменение данных пользователя по id",
                description="Частично изменить данные пользователя по id.",
            ),
            destroy=extend_schema(
                summary="Удаление пользователя по id",
                description="Удалить пользователя по id",
            ),
            me=extend_schema(
                methods=["GET", "PATCH"],
                summary="Получение и обновление профиля текущего пользователя",
                description="Получить или обновить данные текущего пользователя.",
                operation_id="user_profile_retrieve",
            ),
        )
        class Fixed(self.target_class):
            queryset = User.objects.none()

        return Fixed


class SendConfirmCodeViewExtension(OpenApiViewExtension):
    target_class = "api.views.user_views.SendConfirmCodeViewSet"

    def view_replacement(self):
        @extend_schema(
            tags=["AUTH"],
            summary="Регистрация и аутентификация пользователя",
            description=(
                "Получить код подтверждения на переданный `email`.\n\n"
                "Права доступа: **Доступно без токена**.\n\n"
                "Поле `email` должно быть уникальным."
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed


class GetTokenViewExtension(OpenApiViewExtension):
    target_class = "api.views.user_views.GetTokenViewSet"

    def view_replacement(self):
        @extend_schema(
            tags=["AUTH"],
            summary="Получение JWT-токена",
            description=(
                "Получение JWT-токена в обмен на `email` и `confirmation_code`.\n\n"
                "Права доступа: **Доступно без токена**."
            ),
        )
        class Fixed(self.target_class):
            pass

        return Fixed
