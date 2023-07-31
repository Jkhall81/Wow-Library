import requests


def get_book_data(query):
    # Replace 'YOUR_API_KEY' with your actual Google Books API key
    api_key = 'AIzaSyDd7MoNSm_LrRzR9keXv_nQcNC4XYXHvPI'
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query,
        'key': api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


# Example usage:
search_query = 'Dune'  # Replace this with the book title or ISBN you want to search
result_data = get_book_data(search_query)
print(result_data)
