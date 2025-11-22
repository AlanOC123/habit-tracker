from rest_framework import serializers
from .models import UserProfile, Preferences, AccountabilityPartnership
from django.contrib.auth.models import User

class PartnerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email",
        ]
        read_only_fields = ["id", "username", "email"]

class AccountabilityPartnershipSerializer(serializers.ModelSerializer):
    user = PartnerUserSerializer(read_only=True)
    partner = PartnerUserSerializer(read_only=True)

    class Meta:
        model = AccountabilityPartnership
        fields = [
            "id", "user", "partner",
            "status", "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "user", "partner",
            "created_at", "updated_at"
        ]

class UserSerializer(serializers.ModelSerializer):
    as_accountable_user = AccountabilityPartnershipSerializer(read_only=True, many=True)
    as_accountability_partner = AccountabilityPartnershipSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name",
            "username", "email", "as_accountable_user",
            "as_accountability_partner"
        ]
        read_only_fields = [
            "id", 
            "as_accountable_user",
            "as_accountability_partner"
        ]

class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = [
            "theme_mode", "color_scheme_name", "timezone"
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    preferences = PreferencesSerializer(read_only=True)
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id", "user", "bio",
            "profile_picture", "preferences", "date_of_birth"
        ]
        read_only_fields = ["id", "user", "preferences"]

    def get_profile_picture(self, obj):
        return obj.get_profile_picture()
