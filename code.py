import pandas as pd
import requests
import json
import logging

# Set up logging
logging.basicConfig(filename='product_upload.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def read_product_data(file_path):
    """
    Reads product data from a CSV/Excel file and returns it as a pandas DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        logging.info(f"Successfully loaded product data from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error reading product file: {str(e)}")
        return None

def upload_product(api_url, api_key, product_data):
    """
    Uploads a single product to the eCommerce platform via API.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(product_data))
        
        if response.status_code == 201:
            logging.info(f"Successfully uploaded product: {product_data['name']}")
            return True
        else:
            logging.error(f"Failed to upload product: {product_data['name']}, Error: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error uploading product: {product_data['name']}, Exception: {str(e)}")
        return False

def bulk_upload(file_path, api_url, api_key):
    """
    Reads the product data from the given file and uploads each product to the platform.
    """
    data = read_product_data(file_path)
    if data is None:
        logging.error("No product data to upload.")
        return

    for _, row in data.iterrows():
        product_data = {
            "name": row['Product Name'],
            "description": row['Description'],
            "price": row['Price'],
            "sku": row['SKU'],
            "inventory": row['Stock Quantity'],
            "images": [{"src": row['Image URL']}],  # Adjust according to API structure
        }
        # Upload product via API
        success = upload_product(api_url, api_key, product_data)
        if not success:
            logging.error(f"Failed to upload product {row['Product Name']}")

# Usage example:
if __name__ == "__main__":
    api_url = "https://your-ecommerce-platform.com/api/products"
    api_key = "your-api-key"
    file_path = "path/to/your/product_data.xlsx"  # Or CSV file
    
    bulk_upload(file_path, api_url, api_key)
