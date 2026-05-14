from django import forms

class JobForm(forms.Form):
    title = forms.CharField(max_length=200)
    company = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)