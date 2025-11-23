from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'routines', views.RoutineViewSet, basename='routine')
router.register(r'actions', views.ActionViewSet, basename='action')
router.register(r'completions', views.HabitCompletionViewSet, basename='completion')

urlpatterns = [
    path('', include(router.urls))
]