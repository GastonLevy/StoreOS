import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ..models import UserProfile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically saves the user profile when the user is saved,
    if the profile already exists.
    """
    # Check if the UserProfile exists for this User instance
    if hasattr(instance, 'userprofile'):
        logger.info("Signal 'save_user_profile' triggered for user %s", instance.username)
        instance.userprofile.save()
    else:
        logger.warning("UserProfile does not exist for user %s", instance.username)
