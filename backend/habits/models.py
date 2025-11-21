from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Routine(models.Model):
    class RoutineStatusChoice(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    name = models.CharField(
        verbose_name="Routine Name",
        max_length=50
    )

    reason = models.TextField(
        verbose_name="Reason",
        max_length=500,
        help_text="Why is this routine important to you?"
    )

    status = models.CharField(
        verbose_name="Status",
        choices=RoutineStatusChoice.choices,
        default=RoutineStatusChoice.PENDING,
        max_length=20
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="routines"
    )

    start_date = models.DateField(
        verbose_name="Start Date",
        default=date.today
    )

    end_date = models.DateField(
        verbose_name="End Date",
        null=True,
        blank=True
    )

    target_completions = models.PositiveIntegerField(
        verbose_name="Target Completions",
        help_text="Number of Completions before check in starts",
        default=30
    )

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True
    )

    class Meta:
        verbose_name = "Routine"
        verbose_name_plural = "Routines"
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True) | models.Q(end_date__gte=models.F('start_date')),
                name="end_date_after_start_date"
            )
        ]

    @property
    def get_completion_percentage(self):
        pass

    @property
    def is_active(self):
        return self.status == self.RoutineStatusChoice.ACTIVE
    
    def mark_complete(self):
        now = timezone.now().date()
        self.end_date = now
        self.status = self.RoutineStatusChoice.COMPLETED
        self.save()
    
    def __str__(self):
        return f"{self.name} ({self.owner.username})"

class Action(models.Model):
    class ActionFrequencyChoice(models.TextChoices):
        DAILY = "daily", "Daily"

    name = models.CharField(
        verbose_name="Action Name",
        max_length=50
    )

    frequency = models.CharField(
        verbose_name="Frequency",
        choices=ActionFrequencyChoice.choices,
        default=ActionFrequencyChoice.DAILY,
        max_length=20
    )

    routine= models.ForeignKey(
        Routine,
        on_delete=models.PROTECT,
        related_name="actions"
    )

    start_time = models.TimeField(
        verbose_name="Start Time",
        help_text="What time do you plan to do this habit?"
    )

    current_streak = models.PositiveIntegerField(
        verbose_name="Current Streak",
        default=0
    )

    longest_streak = models.PositiveIntegerField(
        verbose_name="Longest Streak",
        default=0
    )

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True
    )

    def increase_streak(self):
        self.current_streak = self.current_streak + 1
        self.longest_streak = max(self.current_streak, self.longest_streak)
        self.save()
    
    def reset_streak(self):
        self.current_streak = 0
        self.save()
    
    @property
    def deadline(self):
        if not self.start_time:
            return None

        from datetime import datetime, timedelta

        start_dt = datetime.combine(datetime.today(), self.start_time)
        deadline_dt = start_dt + timedelta(minutes=30)

        return deadline_dt.time()


    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return f"{self.name} ({self.routine.name})"


class HabitCompletion(models.Model):
    class FeelingChoice(models.TextChoices):
        GREAT = "great", "Great"
        GOOD = "good", "Good"
        OKAY = "okay", "Okay"
        STRUGGLED = "struggled", "Struggled"
        FORCED = "forced", "Forced"

    action = models.ForeignKey(
        Action,
        on_delete=models.PROTECT,
        related_name="completion_records"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="habit_completions"
    )

    completion_date = models.DateField(
        verbose_name="Completed At",
        default=date.today
    )

    difficulty = models.PositiveSmallIntegerField(
        verbose_name="Difficulty",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="How difficulty was this?"
    )

    confidence = models.PositiveSmallIntegerField(
        verbose_name="Confidence",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="How confident are you that you will keep it up?"
    )

    feeling = models.CharField(
        verbose_name="Feeling",
        default=FeelingChoice.OKAY,
        choices=FeelingChoice.choices,
        max_length=20
    )

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True
    )

    def __str__(self):
        return f"{self.action.name} on {self.completion_date} by {self.user.username}"

    class Meta:
        verbose_name = "Habit Completion"
        verbose_name_plural = "Habit Completions"
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['action', 'completion_date'],
                name='one_completion_per_action_per_day'
            )
        ]