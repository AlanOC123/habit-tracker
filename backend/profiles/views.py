from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Preferences, AccountabilityPartnership
from .serializers import (
    UserProfileSerializer, PreferencesSerializer, AccountabilityPartnershipSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=["get"])
    def search(self, request):
        email_query = request.query_params.get('email', '')

        if len(email_query) < 3:
            return Response({
                "error": "Please enter at least 3 characters"
            }, status=400)

        users = User.objects.filter(
            email__icontains=email_query
        ).exclude(
            id=request.user.id
        )[:10]

        profiles = UserProfile.objects.filter(user__in=users)
        serializer = UserProfileSerializer(profiles, many=True)

        return Response(serializer.data)

class PreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = PreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Preferences.objects.filter(user_profile__user=self.request.user)
    
    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)

class AccountabilityPartnershipViewSet(viewsets.ModelViewSet):
    serializer_class = AccountabilityPartnershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccountabilityPartnership.objects.filter(
            Q(user=self.request.user) | Q(partner=self.request.user)
        )

    def perform_create(self, serializer):
        partner = serializer.validated_data['partner']
        existing = AccountabilityPartnership.objects.filter(
            user=self.request.user,
            partner=partner,
            status__in=['pending', 'accepted']
        ).exists()

        if existing:
            raise ValidationError("Partnership already exists")
        
        serializer.save(
            user = self.request.user,
            created_by=self.request.user,
            status='pending'
        )



