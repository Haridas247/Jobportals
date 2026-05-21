from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Job 

# Create your tests here.
 
class JobModelTest(TestCase):
    def setUp(self):
        self.job = Job.objects.create(
            title = 'Software Engineer',
            company ='OpenAi',
            location = 'San Francisco',
            description = 'Develop AI models'
        )

    def test_job_created_successfully(self):
        self.assertEqual(self.job.title, 'Software Engineer')
        print("test_job_created_successfully passed")
    def test_job_str(self):
        self.assertEqual(str(self.job) , 'Software Engineer')
        print("test_job_str passed")
    def test_job_company(self):
        self.assertEqual(self.job.company, 'OpenAi')
        print("test_job_company passed")
class jobManagerTest(TestCase):
    def setUp(self):

        Job.objects.create(title='Frontend Dev', company='Zoho', location='Chennai', description='React developer needed')
        Job.objects.create(title='Backend Dev', company='Google', location='Bangalore', description='Django developer needed')
     
    def test_by_location(self):
        jobs = Job.objects.by_location('Chennai')
        self.assertEqual(jobs.count(), 1)
        self.assertEqual(jobs.first().title, 'Frontend Dev')
        print("test_by_location passed")

    def test_by_company(self):
        
        jobs = Job.objects.by_company('Google')
        self.assertEqual(jobs.count(), 1)
        self.assertEqual(jobs.first().location, 'Bangalore')
        print("test_by_company passed")

    def test_todays_jobs(self):
        
        jobs = Job.objects.todays_jobs()
        self.assertEqual(jobs.count(), 2)
        print("test_todays_jobs passed")



class JobViewTest(TestCase):

    def setUp(self):
       
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.job = Job.objects.create(
            title='Test Job',
            company='Test Company',
            location='Chennai',
            description='Test description'
        )

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        print("test_job_list_view passed")

    def test_add_job_view_requires_login(self):
        response = self.client.get(reverse('add_job'))
        self.assertEqual(response.status_code, 302)  # 302 = redirect
        print("test_add_job_view_requires_login passed")

    def test_add_job_view_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_job'))
        self.assertEqual(response.status_code, 200)
        print("test_add_job_view_logged_in passed")

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        print("test_register_view passed")

class JobAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.job = Job.objects.create(
            title='API Test Job',
            company='API Company',
            location='Chennai',
            description='API test description'
        )

    def test_get_all_jobs_api(self):
        response = self.client.get(reverse('job_api'))
        self.assertEqual(response.status_code, 200)
        print("test_get_all_jobs_api passed")

    def test_get_single_job_api(self):
        response = self.client.get(reverse('job_detail_api', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        print("test_get_single_job_api passed")

    def test_delete_job_api(self):
        response = self.client.delete(reverse('job_detail_api', args=[self.job.id]))
        self.assertEqual(response.status_code, 204)  # 204 = deleted successfully
        print("test_delete_job_api passed")