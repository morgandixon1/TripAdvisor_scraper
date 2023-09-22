import requests
from lxml import html
import csv

def find_urls(url):
  # Initialize a list to store the URLs
  urls = []

  # Make a request to the given URL
  response = requests.get(url)

  # Parse the response HTML
  doc = html.fromstring(response.text)

  # Find all the div nodes with the specified class
  div_nodes = doc.find_class("css-w8rns border-color--default__09f24__NPAKY")

  # Loop through each div node
  for div_node in div_nodes:
    # Find all the anchor nodes within the div node
    anchor_nodes = div_node.findall(".//a")

    # Find the span node with the specified class using doc.cssselect
    span_node = doc.cssselect("span.comment__09f24__ZU8MN.truncated__09f24__lSBbT.css-qgunke")

    # Check if the span node was found
    if span_node:
      # Extract the text from the span node
      text = span_node[0].text_content()
    else:
      # Set the text to an empty string if the span node was not found
      text = ""

    # Extract the href attributes from the anchor nodes and add them to the list
    urls.extend([(text, "https://www.yelp.com" + anchor.attrib['href']) for anchor in anchor_nodes])

  return urls

# Set the base URL
base_url = "https://www.yelp.com/search?find_desc=&find_loc=Rancho%20Cucamonga"

# Open the CSV file for writing
with open('/Users/morgandixon/Desktop/reviewsoutput.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the column titles
    writer.writerow(["Review", "Span Node Text"])

    # Loop [insert loops] times
    for i in range(23):

        # Construct the URL by adding 10 to the base URL for each iteration of the loop
        url = base_url + "&start=" + str(10 * i)

        # Find the URLs and span node text for the current URL
        urls = find_urls(url)

        # Loop through each URL and span node text
        for url in urls:

            # Print the website link to the terminal
            print(url[1])
            # Make the request to the website and store the response
            response = requests.get(url[1])

            # Parse the HTML content of the page
            tree = html.fromstring(response.content)

            # Find all elements with the class "raw__09f24__T4Ezm"
            elements = tree.find_class("raw__09f24__T4Ezm")

            # Write the text from each element and the span node text to a new line in the CSV file
            for element in elements:
                writer.writerow([element.text_content(), url[0]])
