from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
import requests
from .serializer import LeadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from .helper import *
from datetime import datetime

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
     
     
class FacebookLeadMondayView(APIView):
    def get(self, request):
        try:
            # Replace with your actual lead ID and Facebook access token
            lead_id = '6585987406069'
            facebook_access_token = "EAAIpbOmtZBUUBOZCJTDewdDSSUbNcSiCUO9u38CJcNZCYG5VVUuCo4ZAIsZBj07FQs0VdXoIHXnk7xSZA6bZBmkFL06lpsmwvsVHwGNKAc0pvVZABIEA7h6IyWuGLuPYNSRcxdPWJpE1TBTDFZAZBjDS2UAxtdDovsFd8ZAGZANNi7Uv0JYm5HZAcfTr6jmbNQUYo4Iuu6vT2ilUnKuL8WfzUCUHZCCUZBTCxfWToAQVDBs1EedzKqyKsdE2GFcBwZCghAnd"

            # Facebook Graph API URL
            facebook_api_url = f'https://graph.facebook.com/v12.0/{lead_id}?fields=name,leads&access_token={facebook_access_token}'

            # Fetch leads data from Facebook
            response = requests.get(facebook_api_url)
            response.raise_for_status()  # Raise exception for non-200 status codes

            # Extract leads data from the response
            facebook_data = response.json()
            leads_data = facebook_data.get('leads', {}).get('data', [])
            print(leads_data)
            # Prepare data to send to Monday.com
            monday_items = []
            for lead in leads_data:
                full_name = next((field['values'][0] for field in lead.get('field_data', []) if field['name'] == 'full_name'), '')
                email = next((field['values'][0] for field in lead.get('field_data', []) if field['name'] == 'email'), '')
                phone_number = next((field['values'][0] for field in lead.get('field_data', []) if field['name'] == 'phone_number'), '')
                created_time = lead.get('created_time', '')
                # Parse the ISO 8601 datetime string
                parsed_date = datetime.fromisoformat(created_time.split('T')[0]).date()

                # Convert to YYYY-MM-DD format
               
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                monday_items.append({
                    'name': full_name,
                    'email__1': email,
                    'phone__1': phone_number,
                    'status': 'Need Follow up',
                    'date4': formatted_date     # Adjust based on your Monday.com board structure
                })
                print(monday_items)
            # Send data to Monday.com using GraphQL (v2)
            monday_api_url = "https://api.monday.com/v2"
            monday_api_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzNjMyNDI0MiwiYWFpIjoxMSwidWlkIjoxMTExNTk0OSwiaWFkIjoiMjAyNC0wMy0yMVQyMDozMDoyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTAxODY4MCwicmduIjoidXNlMSJ9.0zLMH1Qt_xzxBh845x7HakVo7kblwzob3BvPsl--1DA"
             
            # boardId = str(6878904065)
            # groupId = "topics"
            headers = {
                "Authorization": f"Bearer {monday_api_token}",
                "Content-Type": "application/json"
            }
            
            # Define the GraphQL mutation query
            mutation_query = """
            mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
              create_item (board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) {
                id
              }
            }
            """

            # Send each lead to Monday.com
            for item in monday_items:
                variables = {
                    "boardId": str(6878904065),  # Replace with your actual board ID (make sure it's an integer)
                    "groupId": "topics",    #
                    "itemName": item['name'],  # Use the full name as the item name
                    "columnValues": json.dumps({
                        "email__1": {"email": item['email__1'], "text": item['email__1']},
                        "phone__1": item['phone__1'],
                        "status": {"label": item['status']},
                        "date4": item['date4']
                    })
                }

                response = requests.post(monday_api_url, json={"query": mutation_query, "variables": variables}, headers=headers)
                response.raise_for_status()  # Raise exception for non-200 status codes

            return Response({"message": "Data sent to Monday.com successfully."}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
""" Monday get data """        
class MondayDataView(APIView):
    def get(self, request):
        # Replace with your Monday.com API token
        MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzNjMyNDI0MiwiYWFpIjoxMSwidWlkIjoxMTExNTk0OSwiaWFkIjoiMjAyNC0wMy0yMVQyMDozMDoyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTAxODY4MCwicmduIjoidXNlMSJ9.0zLMH1Qt_xzxBh845x7HakVo7kblwzob3BvPsl--1DA"

        # Example request to fetch board items
        url = "https://api.monday.com/v2"
        query = '''
        {
            boards(ids: [6878904065]) {
                id
                name
                items_page {
                    items{
                        id
                        name
                    column_values {
                        id
                        value
                        text
                    }
                    }
                    
                }
            }
        }
        '''
        headers = {
            "Authorization": f"Bearer {MONDAY_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json={"query": query}, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 status codes
            
            data = response.json()
            return JsonResponse(data)
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
