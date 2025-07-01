import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ..models import UserProfile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile when a new User is created.
    """
    if created:
        # Check if the UserProfile does not already exist for this User instance
        if not hasattr(instance, 'userprofile'):
            logger.info("Signal 'create_user_profile' triggered for user %s", instance.username)
            UserProfile.objects.create(user=instance)
        else:
            logger.warning("UserProfile already exists for user %s", instance.username)
