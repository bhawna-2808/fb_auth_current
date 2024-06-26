import requests
import json

def send_data_to_monday_com():
    # Define your Monday.com board ID and group ID
    board_id = '6878904065'
    group_id = 'topics'
    item_name = 'New Contact - John Doe'  # Replace with dynamic item names if needed

    # Replace 'YOUR_API_KEY_HERE' with your actual Monday.com API key
    monday_api_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzNjMyNDI0MiwiYWFpIjoxMSwidWlkIjoxMTExNTk0OSwiaWFkIjoiMjAyNC0wMy0yMVQyMDozMDoyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTAxODY4MCwicmduIjoidXNlMSJ9.0zLMH1Qt_xzxBh845x7HakVo7kblwzob3BvPsl--1DA"

    # Define column values for Monday.com item (example values)
    column_values = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'phone': '+1234567890',
        'status': 'Need Follow up'  # Adjust based on your board's column names and types
    }

    # Serialize column values to JSON string
    column_values_json = json.dumps(column_values)

    # Define your GraphQL mutation query
    mutation_query = '''
    mutation CreateNewItem($boardId: Int!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
      create_item(board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) {
        id
      }
    }
    '''

    # Prepare variables for the GraphQL query
    variables = {
        'boardId': int(board_id),
        'groupId': group_id,
        'itemName': item_name,
        'columnValues': column_values_json
    }

    # Data with variables for the GraphQL query
    data = {
        'query': mutation_query,
        'variables': variables
    }

    # GraphQL endpoint URL for Monday.com API v2
    graphql_endpoint = 'https://api.monday.com/v2'

    # Headers for the HTTP request
    headers = {
        'Authorization': f'Bearer {monday_api_token}',
        'Content-Type': 'application/json'
    }

    try:
        # Make the HTTP POST request to the GraphQL endpoint
        response = requests.post(graphql_endpoint, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status codes

        # Print response for debugging
        print("Response:", response.json())

    except requests.exceptions.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)

# # Call the function to send data to Monday.com
# send_data_to_monday_com()
