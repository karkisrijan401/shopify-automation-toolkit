# 🛒 Shopify Automation Toolkit

A production-grade Python toolkit for automating Shopify store operations via the REST Admin API. Built and battle-tested on a live dropshipping store generating real traffic.

## 🚀 What This Does

Eliminates manual store management. Every script in this toolkit talks directly to the Shopify Admin REST API to perform operations that would otherwise require 10-20 minutes of dashboard clicking — in under 5 seconds.

## 📦 Scripts

### `product_injector.py`
Programmatically create and publish products with full metadata, variants, pricing, and images — without touching the Shopify dashboard.

```python
# Example: Inject a new product with a single command
python product_injector.py --title "Sciatic Relief Hip Belt" --price 49.99 --compare-at 99.99
```

### `image_manager.py`
Bulk-replace all product images via URL injection. Useful for A/B testing product photography without manual uploads.

### `price_pivot.py`
Execute a price change across any product variant in real-time. Supports `compare_at_price` for automatic "Sale" badge generation.

```python
# Slash price and trigger a Sale badge in one command
python price_pivot.py --variant-id 47941931630836 --price 49.99 --compare-at 99.99
```

### `shipping_auditor.py`
Query and display all active shipping zones, rates, and thresholds. Instantly surfaces mismatches between storefront promises and backend settings.

### `store_diagnostics.py`
Full health check: validates frontend domain (HTTP status), backend API connectivity, shop plan status, and payment configuration.

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/shopify-automation-toolkit
cd shopify-automation-toolkit
pip install -r requirements.txt
```

Create a `.env` file:
```
SHOPIFY_ACCESS_TOKEN=your_private_app_token
SHOPIFY_STORE_URL=https://your-store.myshopify.com
```

## 🔧 Requirements

```
requests>=2.28.0
python-dotenv>=1.0.0
```

## 💼 Use Cases

- **Dropshipping operators** managing 10+ products who need to update prices in response to supplier changes
- **Shopify agencies** building client store management dashboards
- **E-commerce developers** automating product catalog migrations

## 📊 Real-World Performance

This toolkit was used to manage a live Shopify store running a $50/day Meta Ads campaign. Key operations automated:
- Product injection (saved ~20 min per product)
- Image gallery updates (saved ~15 min per update cycle)  
- Price pivots (executed in under 3 seconds vs. manual dashboard navigation)
- Shipping zone auditing (diagnosed and fixed a live revenue-killing $12 shipping fee mismatch)

## 📄 License

MIT License — free to use and modify.
