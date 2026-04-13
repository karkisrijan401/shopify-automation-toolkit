import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'X-Shopify-Access-Token': os.getenv('SHOPIFY_ACCESS_TOKEN'),
    'Content-Type': 'application/json'
}
BASE_URL = f"{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2024-01"


def inject_product(title, price, compare_at_price, description, image_url=None):
    """
    Inject a new product into Shopify with full metadata.

    Args:
        title (str): Product title
        price (str): Selling price e.g. "49.99"
        compare_at_price (str): Original price for Sale badge e.g. "99.99"
        description (str): HTML product description
        image_url (str): URL of the product image (optional)

    Returns:
        dict: Created product data
    """
    payload = {
        "product": {
            "title": title,
            "body_html": description,
            "status": "active",
            "variants": [
                {
                    "price": price,
                    "compare_at_price": compare_at_price,
                    "inventory_management": "shopify",
                    "fulfillment_service": "manual"
                }
            ]
        }
    }

    if image_url:
        payload["product"]["images"] = [{"src": image_url}]

    response = requests.post(f"{BASE_URL}/products.json", headers=HEADERS, json=payload)

    if response.status_code == 201:
        product = response.json()['product']
        print(f"✅ Product created: {product['title']} (ID: {product['id']})")
        return product
    else:
        print(f"❌ Failed to create product: {response.status_code}")
        print(response.text)
        return None


def set_product_status(product_id, status="draft"):
    """
    Set a product to active or draft.

    Args:
        product_id (int): Shopify product ID
        status (str): 'active' or 'draft'
    """
    payload = {"product": {"id": product_id, "status": status}}
    response = requests.put(f"{BASE_URL}/products/{product_id}.json", headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"✅ Product {product_id} set to {status}")
    else:
        print(f"❌ Failed to update status: {response.text}")


def list_products():
    """List all products and their current prices and statuses."""
    response = requests.get(f"{BASE_URL}/products.json?limit=250", headers=HEADERS)
    products = response.json().get('products', [])

    print(f"\n{'ID':<15} {'Status':<10} {'Price':<10} Title")
    print("-" * 60)
    for p in products:
        price = p['variants'][0]['price'] if p['variants'] else 'N/A'
        print(f"{p['id']:<15} {p['status']:<10} ${price:<9} {p['title']}")

    return products


if __name__ == "__main__":
    print("Shopify Product Injector — listing current products:")
    list_products()
