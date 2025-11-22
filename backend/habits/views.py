from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Routine, Action, HabitCompletion
from .serializers import (
    RoutineSerializer, ActionSerializer, HabitCompletionSerializer
)

class RoutineViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Routine.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_set = Action.objects.filter(routine__owner=self.request.user)

        routine_id = self.request.query_params.get('routine')

        if routine_id:
            query_set = query_set.filter(routine_id=routine_id)

        return query_set
    
    def perform_create(self, serializer):
        serializer.save()

class HabitCompletionsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HabitCompletion.objects.filter(
            user=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
