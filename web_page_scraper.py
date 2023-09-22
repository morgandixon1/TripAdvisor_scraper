import requests
import os
import pyperclip
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the webpage to scrape
url = "https://dashboard.findyourbluezone.com/reviews"

# Set headers for the requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Referer": url,
}

# Send a GET request to the webpage with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    css_links = soup.select('link[rel="stylesheet"]')
    output_folder = "/Users/morgandixon/Desktop/webpage_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    css_folder = os.path.join(output_folder, "css")
    if not os.path.exists(css_folder):
        os.makedirs(css_folder)
    for css_link in css_links:
        css_url = urljoin(url, css_link["href"])
        css_response = requests.get(css_url, headers=headers)
        if css_response.status_code == 200:
            css_content = css_response.text
            css_filename = os.path.basename(css_url)
            css_file_path = os.path.join(css_folder, css_filename)
            with open(css_file_path, "w") as css_file:
                css_file.write(css_content)
            css_link["href"] = os.path.join("css", css_filename)

    # Find all image tags in the HTML
    image_tags = soup.select("img")
    images_folder = os.path.join(output_folder, "images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Retrieve images and save to folder
    for image_tag in image_tags:
        if image_tag.has_attr("src"):
            image_url = urljoin(url, image_tag["src"])
            if image_url.startswith("data:image"):
                continue
            image_response = requests.get(image_url, stream=True, headers=headers)
            if image_response.status_code == 200:
                image_filename = os.path.basename(image_url)
                image_file_path = os.path.join(images_folder, image_filename)
                with open(image_file_path, "wb") as image_file:
                    for chunk in image_response.iter_content(chunk_size=128):
                        image_file.write(chunk)
                image_tag["src"] = os.path.join("images", image_filename)

    # Find all script tags in the HTML
    script_tags = soup.select("script")
    js_folder = os.path.join(output_folder, "js")
    if not os.path.exists(js_folder):
        os.makedirs(js_folder)

    # Retrieve JavaScript content and save to file
    for script_tag in script_tags:
        if script_tag.has_attr("src"):
            js_url = urljoin(url, script_tag["src"])
            js_response = requests.get(js_url, headers=headers)
            if js_response.status_code == 200:
                js_content = js_response.text
                js_filename = os.path.basename(js_url)
                js_file_path = os.path.join(js_folder, js_filename)
                with open(js_file_path, "w") as js_file:
                    js_file.write(js_content)
                script_tag["src"] = os.path.join("js", js_filename)

    # Save the updated HTML to a file
    html_filename = os.path.join(output_folder, "index.html")
    with open(html_filename, "w") as html_file:
        html_file.write(str(soup))

    # Print success message
    print("Webpage files saved successfully!")
else:
    # Print error message if the request was not successful
    print(f"Failed to retrieve HTML content. Status code: {response.status_code}")
