from django.db import models


class JobQuerySet(models.QuerySet):

    def by_location(self, location):
        return self.filter(location=location)

    def by_company(self, company):
        return self.filter(company__icontains=company)

    def todays_jobs(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.filter(created_at__date=today)
    
class JobManager(models.Manager):

    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def by_location(self, location):
        return self.get_queryset().by_location(location)

    def by_company(self, company):
        return self.get_queryset().by_company(company)

    def todays_jobs(self):
        return self.get_queryset().todays_jobs()

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = JobManager()    

    def __str__(self):
        return self.title