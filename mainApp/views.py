from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')


def privacy(request):
    return render(request, 'privacy_policy.html')

def terms(request):
    return render(request, 'terms.html')
