from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'preferences', views.PreferencesViewSet, basename="preference")
router.register(r'partnerships', views.AccountabilityPartnershipViewSet, basename="partnership")

urlpatterns = [
    path('', include(router.urls))
]