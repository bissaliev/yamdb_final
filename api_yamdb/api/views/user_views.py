from api.permissions import IsAdminOrSuperuser
from api.serializers.user_serializers import (
    CertainUserSerializer,
    CustomGetTokenSerializer,
    GetInfoAboutMeSerializer,
    GetOrCreateUsersSerializer,
    SendConfirmCodeSerializer,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

CACHE_TIMEOUT = settings.CACHE_TIMEOUT


class SendConfirmCodeViewSet(APIView):
    """Отправка кода верификации на указанный email-адрес."""

    permission_classes = [AllowAny]
    serializer_class = SendConfirmCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        timeout_in_min = CACHE_TIMEOUT // 60
        return Response(
            {
                "message": (
                    "Код верификации отправлен на ваш email. "
                    f"Он будет действовать в течение {timeout_in_min} минут"
                )
            },
            status=status.HTTP_200_OK,
        )


class GetTokenViewSet(APIView):
    """Получаем токен после подтверждения кода верификации."""

    permission_classes = [AllowAny]
    serializer_class = CustomGetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = user.get_token()
        return Response(token, status=status.HTTP_200_OK)


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
