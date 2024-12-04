import random

from api.permissions import IsAdminOrSuperuser
from api.serializers.user_serializers import (
    CertainUserSerializer,
    CustomGetTokenSerializer,
    GetInfoAboutMeSerializer,
    GetOrCreateUsersSerializer,
    RegisterAndSendConfirmCodeSerializer,
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from api_yamdb.settings import EMAIL_HOST_USER


class RegisterAndSendConfirmCodeViewSet(APIView):
    """Регистрируем пользователя совместно с выдачей кода."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterAndSendConfirmCodeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        confirmation_code = ""
        # TODO: Улучшить генерацию кода подтверждения
        for i in range(7):
            confirmation_code += str(random.randint(0, 9))

        try:
            user = User.objects.get(
                username=serializer.validated_data.get("username")
            )
            user.confirmation_code = confirmation_code
            user.save()
        except User.DoesNotExist:
            serializer.save(confirmation_code=confirmation_code)

        # Отправляем письмо с кодом
        send_mail(
            "Подтверждение почты",
            (
                f"Ваш код подтверждения: {confirmation_code}\n"
                f"Никнейм: {serializer.validated_data.get('username')}\n"
            ),
            EMAIL_HOST_USER,
            [serializer.validated_data.get("email")],
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCustomTokenViewSet(APIView):
    """Получаум кастомный токен."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomGetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data["username"],
        )

        if (
            user.confirmation_code
            == serializer.validated_data["confirmation_code"]
        ):
            refresh = RefreshToken.for_user(user)

            return Response(
                {"token": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        return Response(
            "Неверный ключ доступа!", status=status.HTTP_400_BAD_REQUEST
        )


class GetOrCreateUsers(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Получаем список пользователей или создаём пользователя."""

    queryset = User.objects.all()
    serializer_class = GetOrCreateUsersSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["=username"]
    permission_classes = [IsAdminOrSuperuser]

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Методы get и patch к пользователю отправившему запрос."""
        user = get_object_or_404(User, pk=request.user.id)

        if request.method == "GET":
            serializer = GetInfoAboutMeSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = GetInfoAboutMeSerializer(
            user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertainUser(viewsets.ViewSet):
    """Методы get patch и delete к конкретному юзеру."""

    lookup_field = "username"
    permission_classes = [IsAdminOrSuperuser]

    def retrieve(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = CertainUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, username=None):
        user = get_object_or_404(User, username=username)
        serializer = CertainUserSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, username=None):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
