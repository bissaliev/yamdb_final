from api.views.review_views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)
from api.views.user_views import (
    GetTokenViewSet,
    SendConfirmCodeViewSet,
    UserViewSet,
)
from django.urls import include, path
from rest_framework import routers

app_name = "api"

router_v1 = routers.SimpleRouter()

# users
router_v1.register("users", UserViewSet, basename="user")

# reviews
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)" r"/comments",
    CommentViewSet,
    basename="comments",
)

# authentication
auth_urls = [
    path(
        "send_confirm_code/",
        SendConfirmCodeViewSet.as_view(),
        name="send_confirm_code",
    ),
    path("token/", GetTokenViewSet.as_view(), name="get_token"),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router_v1.urls)),
]
