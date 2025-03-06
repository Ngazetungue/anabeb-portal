from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from users.models import CustomUser
from dashboard.models import Profile

@receiver(post_save, sender=CustomUser)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance)
    else:
        profile = instance.profile
    
    profile.email = instance.email
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.identification_document = instance.identification_document
    profile.date_of_birth = instance.date_of_birth
    profile.cellphone_number = instance.cellphone_number
    profile.user_type = instance.user_type
    profile.save()
    
    if created:
        group_mapping = {
            'admin': 'Admin',
            'staff': 'Staff',
        }
        group_name = group_mapping.get(instance.user_type)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
    
        if instance.is_superuser:
            instance.user_type = 'admin'
            instance.save()

@receiver(post_delete, sender=CustomUser)
def delete_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.delete()

@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    pass
