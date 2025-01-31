from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import user_detail_view, user_redirect_view, user_update_view
from .api.views import JobListingViewSet, RecommendationViewSet

urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]

app_name = "app"

# Create a router to register the ViewSets
router = DefaultRouter()
router.register(r"listings", JobListingViewSet, basename="job-listings")
router.register(r"recommendations", RecommendationViewSet, basename="recommendations")

urlpatterns += [
    # Router includes all registered ViewSets
    path("", include(router.urls)),
]
