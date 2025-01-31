from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from jobsync.app.api.views import UserViewSet, RecommendationViewSet, AuthViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register(r'recommendations', RecommendationViewSet, basename='recommendations')

router.register("auth", AuthViewSet, basename="auth")

app_name = "api"
urlpatterns = router.urls
