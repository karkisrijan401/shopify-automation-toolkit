import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'X-Shopify-Access-Token': os.getenv('SHOPIFY_ACCESS_TOKEN'),
    'Content-Type': 'application/json'
}
BASE_URL = f"{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2024-01"


def pivot_price(variant_id, new_price, compare_at_price=None):
    """
    Update the price of a product variant in real-time.
    Optionally set a compare_at_price to trigger Shopify's 'Sale' badge.

    Args:
        variant_id (int): Shopify variant ID
        new_price (str): New selling price e.g. "49.99"
        compare_at_price (str): Optional strikethrough price e.g. "99.99"
    """
    payload = {
        "variant": {
            "id": variant_id,
            "price": new_price
        }
    }

    if compare_at_price:
        payload["variant"]["compare_at_price"] = compare_at_price

    response = requests.put(f"{BASE_URL}/variants/{variant_id}.json", headers=HEADERS, json=payload)

    if response.status_code == 200:
        variant = response.json()['variant']
        print(f"✅ Price updated: ${variant['price']} (was ${variant.get('compare_at_price', 'N/A')})")
        return variant
    else:
        print(f"❌ Price update failed: {response.status_code}")
        print(response.text)
        return None


def get_all_variants():
    """Fetch all products and their variant IDs and current prices."""
    response = requests.get(f"{BASE_URL}/products.json?limit=250", headers=HEADERS)
    products = response.json().get('products', [])

    print(f"\n{'Variant ID':<20} {'Price':<10} {'Compare At':<15} Product Title")
    print("-" * 70)
    for p in products:
        for v in p['variants']:
            compare = v.get('compare_at_price') or 'None'
            print(f"{v['id']:<20} ${v['price']:<9} ${compare:<14} {p['title']}")


if __name__ == "__main__":
    print("Fetching all current variant prices:")
    get_all_variants()
