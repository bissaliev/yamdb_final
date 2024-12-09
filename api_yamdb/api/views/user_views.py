from api.permissions import IsAdminOrSuperuser
from api.serializers.user_serializers import (
    CustomGetTokenSerializer,
    SendConfirmCodeSerializer,
    UserSerializer,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
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
        serializer.save()  # Отправка кода верификации
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


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=username", "email"]
    permission_classes = [IsAdminOrSuperuser]

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Профиль пользователя."""
        user = get_object_or_404(User, pk=request.user.id)
        if self.request.method == "GET":
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        serializer = self.serializer_class(
            user, request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
