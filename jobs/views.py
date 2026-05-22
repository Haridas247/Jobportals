from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from .models import Job
from .forms import JobForm
from .tasks import send_job_notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        query = self.request.GET.get('q')  
        # get search text from URL
        
        if query:
            return Job.objects.filter(title__icontains=query)  # filter by title
        return Job.objects.all() 
class AddJobView(LoginRequiredMixin, View):

    def get(self, request):
        form = JobForm()
        return render(request, 'jobs/add_job.html', {'form': form})

    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            job = Job.objects.create(
                title=form.cleaned_data['title'],
                company=form.cleaned_data['company'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description'],
            )
            send_job_notification.delay(job.title, job.company)
            return redirect('/jobs/')
        return render(request, 'jobs/add_job.html', {'form': form})

# Django automatically feteches ajob.objects.all()and send to template
# you don't need to write a get() and post() - listView does it for you autommatically.
class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'jobs/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/jobs/')
        return render(request, 'jobs/register.html', {'form': form})

class JobApiView(APIView):
    def get_permission(self):
          if self.request.method == 'GET':
            return [AllowAny()]        
          return [IsAuthenticated()]

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailApiView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]       
        return [IsAuthenticated()]    

    def get_object(self, pk):
        return get_object_or_404(Job, id=pk)

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        job.delete()
        return Response({'message': 'Job deleted!'}, status=status.HTTP_204_NO_CONTENT)