import requests

def get_facebook_data(object_id, access_token):
    base_url = f"https://graph.facebook.com/{object_id}"
    params = {
        'fields': 'name,leads',
        'access_token': access_token
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage:
object_id = '6585987406069'
access_token = 'your_access_token_here'  # Replace with your actual access token
facebook_data = get_facebook_data(object_id, access_token)
if facebook_data:
    print(facebook_data)
