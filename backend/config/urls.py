from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/auth/login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # API Routes
    path('api/profiles/', include('profiles.urls')),
    path('api/habits/', include('habits.urls')),
    path('api/activity/', include('activity.urls'))
]
