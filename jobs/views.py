from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from.models import Job
from.forms import JobForm

# Create your views here.

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html',{'jobs' : jobs}) 
def add_job(request):
    if request.method =='POST':
        form = JobForm(request.POST)
        if form.is_valid():
            Job.objects.create(
        title = form.Cleaned_data ['title'],
        company=form.Cleaned_data['comapny'],
        location=form.Cleaned_data['location'],
        description =form.cleaned_data['description'],
        )
        return redirect('/jobs/')
    else:
        form = JobForm()
        return render(request, 'jobs/add_job.html',{'form':form})
    
def register (request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/jobs/')
    else:
        form = UserCreationForm()
    return render(request, 'jobs/register.html', {'form': form})
