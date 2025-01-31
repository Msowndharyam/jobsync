from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobListing, User,JobApplication

@receiver(post_save, sender=JobListing)
def notify_users_of_new_job(sender, instance, created, **kwargs):
    if created:
        # Only filter by role, remove skills reference
        job_seekers = User.objects.filter(role='job_seeker')
        for seeker in job_seekers:
            print(f"Notification sent to {seeker.email} about new job: {instance.title}")

@receiver(post_save, sender=JobApplication)
def notify_employer_of_application(sender, instance, created, **kwargs):
    if created:
        employer = instance.job.employer
        print(f"Notification sent to {employer.email} about new application by {instance.user.email}")
