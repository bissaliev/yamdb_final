from django.urls import include, path

from rest_framework import routers

from . import views

app_name = "api"

router_v1 = routers.SimpleRouter()
router_v1.register(r"users", views.GetOrCreateUsers, basename="users")
router_v1.register(
    r"users",
    views.CertainUser,
    basename="users_certain",
)
router_v1.register("titles", views.TitleViewSet, basename="titles")
router_v1.register("categories", views.CategoryViewSet, basename="categories")
router_v1.register("genres", views.GenreViewSet, basename="genres")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet, basename="reviews",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)"
    r"/comments", views.CommentViewSet, basename="comments"
)

auth_urls = [
    path("token/", views.GetCustomTokenViewSet.as_view(), name="get_token"),
    path(
        "signup/",
        views.RegisterAndSendConfirmCodeViewSet.as_view(),
        name="get_conf_code",
    ),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router_v1.urls)),
]
