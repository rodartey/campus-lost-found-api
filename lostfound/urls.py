from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClaimViewSet, CommentViewSet, ItemViewSet

router = DefaultRouter()
router.register("items", ItemViewSet)
router.register("claims", ClaimViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [path("", include(router.urls))]