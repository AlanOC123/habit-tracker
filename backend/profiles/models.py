from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    bio = models.TextField(
        verbose_name="Biography", 
        max_length=200, 
        null=True, 
        blank=True
    )

    date_of_birth = models.DateField(
        verbose_name="Date of Birth", 
        null=True, 
        blank=True
    )

    profile_picture = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to="profile_pictures/",
        null=True,
        blank=True
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )

    created_at = models.DateTimeField(
        verbose_name="Created At", 
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Updated At", 
        auto_now=True
    )

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-avatar.png'
    
    def __str__(self) -> str:
        return f"Profile for {self.user.username}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Preferences(models.Model):
    class ThemeMode(models.TextChoices):
        LIGHT= "light", 'Light'
        DARK= "dark", 'Dark'
        SYSTEM= "system", 'System'
    
    theme_mode = models.CharField(
        verbose_name="Theme Mode",
        choices=ThemeMode.choices,
        max_length=15,
        default=ThemeMode.SYSTEM
    )

    color_scheme_name = models.CharField(
        verbose_name="Theme Name",
        default="Default",
        max_length=30
    )

    timezone = models.CharField(
        verbose_name="Timezone",
        max_length=50,
        default='UTC',
        help_text='IANA timezone identifier'
    )

    user_profile = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name="preferences"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Preference"
        verbose_name_plural = "User Preferences"

    def __str__(self) -> str:
        return f"Profile for {self.user_profile.user.username}"
    
class AccountabilityPartnership(models.Model):
    class AccountabilityStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CLOSED = "closed", "Closed"
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="as_accountable_user",
        null=True
    )

    partner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="as_accountability_partner",
        null=True
    )

    status = models.CharField(
        verbose_name="Status",
        choices=AccountabilityStatus.choices,
        default=AccountabilityStatus.PENDING,
        max_length=15
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # notifications = models.OneToOneField(
    #     Notification,
    #     on_delete=models.SET_NULL,
    #     related_name="notification"
    # )

    def __str__(self) -> str:
        return f"Partnership request for {self.user.username if self.user else "User"} to {self.partner.username if self.partner else "Partner"}"

    class Meta:
        verbose_name = "Accountability Partnership"
        verbose_name_plural = "Accountability Partnerships"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'partner'],
                condition=models.Q(status__in=["pending", 'accepted']),
                name="unique_active_partnership"
            )
        ]