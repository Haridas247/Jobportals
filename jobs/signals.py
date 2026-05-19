# jobs/signals.py

from django.db.models.signals import post_save  
# post_save fires after a model is saved
from django.dispatch import receiver           
 # receiver connects signal to your function
from .models import Job
from .tasks import send_job_notification

@receiver(post_save, sender=Job)
def job_created_notification(sender, instance, created, **kwargs):
   

    if created:   
        send_job_notification.delay(instance.title, instance.company)