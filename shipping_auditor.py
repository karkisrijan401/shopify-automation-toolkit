import os
import requests
import sys
import io
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

HEADERS = {
    'X-Shopify-Access-Token': os.getenv('SHOPIFY_ACCESS_TOKEN'),
    'Content-Type': 'application/json'
}
BASE_URL = f"{os.getenv('SHOPIFY_STORE_URL')}/admin/api/2024-01"


def audit_shipping():
    """
    Query all active shipping zones and surface potential mismatches
    between storefront promises and backend shipping rate settings.
    """
    response = requests.get(f"{BASE_URL}/shipping_zones.json", headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        return

    zones = response.json().get('shipping_zones', [])

    if not zones:
        print("⚠️  No shipping zones configured. Checkout may error.")
        return

    print(f"\n{'='*60}")
    print(f"SHIPPING ZONE AUDIT REPORT")
    print(f"{'='*60}")

    for zone in zones:
        print(f"\n📍 Zone: {zone['name']} (ID: {zone['id']})")

        price_rates = zone.get('price_based_shipping_rates', [])
        weight_rates = zone.get('weight_based_shipping_rates', [])

        if not price_rates and not weight_rates:
            print("  ⚠️  No rates configured for this zone.")
            continue

        for rate in price_rates:
            min_order = rate.get('min_order_subtotal') or '0'
            max_order = rate.get('max_order_subtotal') or '∞'
            price = float(rate.get('price', 0))
            flag = "✅ FREE" if price == 0 else f"⚠️  ${price:.2f}"
            print(f"  {flag} — {rate['name']} | Orders ${min_order} to ${max_order}")

        for rate in weight_rates:
            print(f"  💰 ${rate.get('price')} — {rate['name']} (weight-based)")

    print(f"\n{'='*60}")
    print("Audit complete. Check ⚠️ flags for potential conversion killers.")
    print(f"{'='*60}\n")


def check_store_health():
    """Full store health diagnostic."""
    print("\n🔍 Running store health check...")

    # Frontend
    try:
        store_url = os.getenv('SHOPIFY_STORE_URL', '').replace('.myshopify.com', '.shop').replace('https://yohoho-2', 'https://yohoho')
        frontend_res = requests.get(store_url, timeout=10)
        status = "✅ Online" if frontend_res.status_code == 200 else f"❌ HTTP {frontend_res.status_code}"
        print(f"Frontend: {status}")
    except Exception as e:
        print(f"Frontend: ❌ Unreachable ({e})")

    # Backend API
    api_res = requests.get(f"{BASE_URL}/shop.json", headers=HEADERS)
    if api_res.status_code == 200:
        shop = api_res.json()['shop']
        print(f"Backend API: ✅ Connected")
        print(f"Shop Name: {shop['name']}")
        print(f"Plan: {shop['plan_name']}")
    else:
        print(f"Backend API: ❌ Error {api_res.status_code}")


if __name__ == "__main__":
    check_store_health()
    audit_shipping()
