from django.db import models
from django.contrib.auth.models import User
from habits.models import Action

class Notification(models.Model):
    class NotificationCategoryChoice(models.TextChoices):
        USER_MISSED_HABIT = "user_missed_habit", "User Missed Habit"
        PARTNER_MISSED_HABIT = "partner_missed_habit", "Partner Missed Habit"
        STREAK_MILESTONE = "streak_milestone", "Streak Milestone"
        ROUTINE_COMPLETED = "routine_completed", "Routine Completed"
        PARTNERSHIP_REQUEST = "partnership_request", "Partnership Request"
        PARTNERSHIP_REQUEST_ACCEPTED = "partnership_request_accepted", "Partnership Request Accepted"
        PARTNERSHIP_REQUEST_REJECTED = "partnership_request_rejected", "Partnership Request Rejected"

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_notifications"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_notifications",
        null=True,
        blank=True
    )

    message = models.TextField(
        verbose_name="Message",
        max_length=500,
    )

    category = models.CharField(
        verbose_name="Category",
        choices=NotificationCategoryChoice.choices,
        max_length=50
    )

    read_status = models.BooleanField(
        verbose_name="Read Status",
        default=False
    )

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )

    trigger_action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        related_name="action_notifications",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                name="habit_trigger_is_action_and_action_exists",
                check=
                    ~models.Q(category__in=["user_missed_habit", "partner_missed_habit", "streak_milestone"]) |
                    models.Q(trigger_action__isnull=False)
            ),
            models.CheckConstraint(
                name="partnership_request_does_not_have_trigger_action",
                check=
                    ~models.Q(category__startswith="partnership") |
                    models.Q(trigger_action__isnull=True)
            ),
            models.CheckConstraint(
                name="partnership_request_has_a_created_by_user",
                check=
                    ~models.Q(category="partnership") |
                    models.Q(created_by__isnull=False)
            )
        ]
    
    def __str__(self):
        return f"{self.category} for {self.recipient.username} at {self.created_at}"
