from api.views.review_views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)
from api.views.user_views import (
    CertainUser,
    GetCustomTokenViewSet,
    GetOrCreateUsers,
    RegisterAndSendConfirmCodeViewSet,
)
from django.urls import include, path
from rest_framework import routers

app_name = "api"

router_v1 = routers.SimpleRouter()
router_v1.register(r"users", GetOrCreateUsers, basename="users")
router_v1.register(r"users", CertainUser, basename="users_certain")
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

auth_urls = [
    path("token/", GetCustomTokenViewSet.as_view(), name="get_token"),
    path(
        "signup/",
        RegisterAndSendConfirmCodeViewSet.as_view(),
        name="get_conf_code",
    ),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router_v1.urls)),
]
