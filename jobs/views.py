from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from .tasks import send_job_notification

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = Job.objects.create(
                title=form.cleaned_data['title'],
                company=form.cleaned_data['company'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description'],
            )
            #Run in background!
            send_job_notification.delay(job.title, job.company)
            return redirect('/jobs/')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/jobs/')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/register.html', {'form': form})

@api_view(['GET', 'POST'])
def job_api(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def job_detail_api(request, pk):
    job = get_object_or_404(Job, id=pk)
    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        job.delete()
        return Response('Job deleted!')