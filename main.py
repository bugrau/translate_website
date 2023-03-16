import requests, uuid, json
from bs4 import BeautifulSoup

def func(text):

   

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource.
    # It can be found in the Azure portal on the Keys and Endpoint page.
    location = "westeurope"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'tr'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translation = response[0]['translations'][0]
    text = translation['text']

    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

    return text

base_url = 'https://realpython.com/beautiful-soup-web-scraper-python/'
visited_urls = set()

# Define a function to recursively traverse the links on the website
def traverse_links(url):
    # Check if the URL has already been visited
    if url in visited_urls:
        return
    else:
        visited_urls.add(url)

    # Send a GET request to the website and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Translate all the strings of text on the page
    for string in soup.stripped_strings:
        translated_text = func(string)
        print(translated_text)

    # Traverse the links on the page
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url is not None and link_url.startswith(base_url):
            traverse_links(link_url)

# Start traversing links from the base URL
traverse_links(base_url)