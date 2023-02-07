import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the URL to scrape

url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"


# Define the headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36","Referer": "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
}

# Make the request to the URL
response = requests.get(url, headers=headers)


# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the product containers on the page
    product_containers = soup.find_all("div", class_="s-result-item")

    # Open a CSV file to write the data to
    with open("amazon_products.csv", "w", newline="") as file:
        # Define the fieldnames for the CSV file
        fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of reviews", "Description", "ASIN", "Product Description", "Manufacturer"]

        # Create a CSV writer
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Loop through each product container
        for product_container in product_containers:
            # Initialize an empty dictionary to store the product data
            product_data = {}

            # Get the product URL
            product_url = product_container.find("a", class_="a-link-normal")
            product_url = product_url.get("href") if product_url else ""
            product_data["Product URL"] = product_url
            if product_url:
                 if not product_url.startswith("http"):
                        product_url = "http://" + product_url
                 product_response = requests.get(product_url, headers=headers)

            # Get the product name
            product_name = product_container.find("span", class_="a-size-medium")
            product_name = product_name.text if product_name else ""
            product_data["Product Name"] = product_name

            # Get the product price
            product_price = product_container.find("span", class_="a-offscreen")
            product_price = product_price.text if product_price else ""
            product_data["Product Price"] = product_price

            # Get the rating
            product_rating = product_container.find("span", class_="a-icon-alt")
            product_rating = product_rating.text if product_rating else ""
            product_data["Rating"] = product_rating

            # Get the number of reviews
            product_reviews = product_container.find("span", class_="a-size-base")
            product_reviews = product_reviews.text if product_reviews else ""
            product_data["Number of reviews"] = product_reviews

            # Get the product description
            product_description = product_container.find("div", id="productDescription")
            product_description = product_description.text.strip() if product_description else ""
            product_data["Description"] = product_description

            # Get the ASIN
            product_ASIN = product_container.find("th", string="ASIN:")
            if product_ASIN:
                product_ASIN = product_ASIN.find_next_sibling("td").text.strip()
            else:
                product_ASIN = ""
            product_data["ASIN"] = product_ASIN

            # Get the Product Description
            product_product_description = product_container.find("div", id="feature-bullets")
            if product_product_description:
                product_product_description = product_product_description.text.strip()
            else:
                product_product_description = ""
            product_data["Product Description"] = product_product_description

            # Get the Manufacturer
            product_manufacturer = product_container.find("th", string="Manufacturer:")
            if product_manufacturer:
                product_manufacturer = product_manufacturer.find_next_sibling("td").text.strip()
            else:
                product_manufacturer = ""
            product_data["Manufacturer"] = product_manufacturer


            # Make a request to the product URL to get additional information
            product_response = requests.get(product_url, headers=headers)

            # Check if the request was successful
            if product_response.status_code == 200:
                # Parse the HTML content
                product_soup = BeautifulSoup(product_response.text, 'html.parser')
        products = []
        for i in range(1, 21):
           url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
           products.extend(scrape_products(url))

        df = pd.DataFrame(products)
        df.to_csv('products.csv', index=False)

