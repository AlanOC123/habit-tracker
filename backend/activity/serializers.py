from django.contrib.auth.models import User
from .models import Notification
from rest_framework import serializers
from habits.models import Action

class UserAsNotifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email"
        ]
        read_only_fields = [
            "id", "username", "email"
        ]

class TriggerActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "name"]

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserAsNotifierSerializer(read_only=True)
    created_by = UserAsNotifierSerializer(read_only=True)
    trigger_action = TriggerActionSerializer(read_only=True, many=True)
    class Meta:
        model=Notification
        fields = [
            "id", "recipient", "created_by",
            "category", "message", "read_status",
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "recipient", "created_by",
            "category", "message", "created_at", "updated_at"
        ]