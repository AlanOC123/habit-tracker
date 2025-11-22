from .models import Routine, Action, HabitCompletion
from rest_framework import serializers

class ActionSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    class Meta:
        model = Action
        fields = [
            "id", "name", "frequency",
            "routine", "start_time", "current_streak",
            "longest_streak", "deadline", "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id", "current_streak", "longest_streak", "deadline", "routine", "created_at", "updated_at"
        ]
    
    def get_deadline(self, obj):
        return obj.deadline

class RoutineSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(read_only=True, many=True)
    completion_percentage = serializers.SerializerMethodField(method_name="completion")
    is_active = serializers.SerializerMethodField()
    class Meta:
        model = Routine
        fields = [
            "id", "name", "reason",
            'status', 'owner', "actions",
            "start_date", "end_date", "completion_percentage", "target_completions"
        ]
        read_only_fields = ["id", "owner"]
    
    def completion(self, obj):
        return obj.get_completion_percentage
    
    def get_is_active(self, obj):
        return obj.is_active

class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model=HabitCompletion
        fields=[
            "id", "action", "user", 
            "completion_date", "difficulty", "confidence", "feeling"
        ]
        read_only_fields=[
            "id", "user"
        ]