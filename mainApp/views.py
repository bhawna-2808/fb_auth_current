from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
import requests
from .serializer import LeadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')


def privacy(request):
    return render(request, 'privacy_policy.html')

def terms(request):
    return render(request, 'terms.html')


def custom_logout(request):
    logout(request)
    # Redirect to a specific page after logout, such as the homepage
    return redirect('home')  # Replace 'home' with the name of your desired URL pattern


class FacebookLeadsView(APIView):
    def get(self, request):
        lead_id = '6585987406069'  # Replace with your lead ID
        FACEBOOK_ACCESS_TOKEN = "EAAIpbOmtZBUUBOZCJTDewdDSSUbNcSiCUO9u38CJcNZCYG5VVUuCo4ZAIsZBj07FQs0VdXoIHXnk7xSZA6bZBmkFL06lpsmwvsVHwGNKAc0pvVZABIEA7h6IyWuGLuPYNSRcxdPWJpE1TBTDFZAZBjDS2UAxtdDovsFd8ZAGZANNi7Uv0JYm5HZAcfTr6jmbNQUYo4Iuu6vT2ilUnKuL8WfzUCUHZCCUZBTCxfWToAQVDBs1EedzKqyKsdE2GFcBwZCghAnd" 
        url = f'https://graph.facebook.com/v12.0/{lead_id}?fields=name,leads&access_token={FACEBOOK_ACCESS_TOKEN}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-200 status codes
            
            leads_data = response.json()
            leads = leads_data.get('leads', {}).get('data', [])
            
            return Response(leads, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error fetching data from Facebook Graph API: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)