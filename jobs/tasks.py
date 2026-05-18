from celery import shared_task 

@shared_task
def send_job_notification(job_title, company):
    print(f"Sending notification for job: {job_title} at  {company}")
    return f"Notification sent for {job_title}"