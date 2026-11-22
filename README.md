[README.md](https://github.com/user-attachments/files/35231584/README.md)
# Softkind — Shopify skincare storefront

A responsive Shopify Online Store 2.0 theme starter for a skincare shop. It uses Liquid sections and JSON templates, Shopify's native product/customer/order data, and Shopify checkout. Add store products and images in Shopify Admin to replace the empty-catalog prompts.

This repository also contains a separate **Streamlit companion demo** in `streamlit_app.py`. It is a standalone, sample-data app for skincare discovery and store-owner dashboard concepts; it is not a Shopify storefront and does not connect to live Shopify data or checkout.

## Features

- Responsive homepage, collection, product, search, cart, content page, and customer login templates.
- Product catalog cards, variant/quantity selection, quick add, cart quantity updates, and Shopify-hosted checkout.
- Newsletter signup, customer accounts, and links to Shopify account/order history.
- Cash on Delivery is handled by Shopify checkout when enabled as a manual payment method in the store.
- A catalog-grounded shopping assistant demo that matches customer terms to published products, explains its limits, and requires confirmation before adding a product to the cart.
- Product-page app-block support so a Shopify product reviews and ratings app can be added from the theme editor.
- Shopify Admin remains the source of truth for products, inventory, customer accounts, orders, and order fulfillment/tracking.

## Install with Shopify CLI

1. Install Node.js and Shopify CLI, then sign in with `shopify auth login`.
2. From this theme folder, run `shopify theme dev --store your-store.myshopify.com`.
3. Use the preview URL from the CLI. To publish after review, run `shopify theme push --store your-store.myshopify.com` and select the intended theme in Shopify Admin.
4. In Shopify Admin, add products, images, descriptions, variants, and collections. Create a main navigation menu and footer menu under **Content → Menus**.
5. In **Online Store → Themes → Customize**, select the collection for the homepage featured collection and add suitable hero/story imagery.
6. To add customer reviews and ratings, install a compatible Shopify reviews app and add its app block to the product section in the theme editor.
7. To offer COD, go to **Settings → Payments → Manual payment methods**, add Cash on Delivery, and configure its instructions and availability. Shopify controls the actual payment and checkout flow.
8. Enable customer accounts in **Settings → Customer accounts**. Shopify handles registration, login, order history, and order status.

## Run the Streamlit companion demo

From the project root, create and activate a Python environment, then install the app dependency and run it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

For Streamlit Community Cloud, push this repository to GitHub, create a new app in the Community Cloud dashboard, select this repository and branch, set the main file path to `streamlit_app.py`, and deploy. The app requires no secrets. It uses illustrative sample products, stock, and orders; replace them with authorized data integrations before using it as a real store dashboard. Streamlit does not host or replace the Shopify theme.

## AI assistant scope and production setup

`assets/assistant.js` is an intentionally small, browser-only project demo. It searches only the public products rendered into the storefront and does not send customer input or personal data to an AI provider. Product matching is keyword-based; it is not a medical advisor or a production language-model agent.

For a real AI service, build a Shopify app with a server-side app proxy. Keep model credentials on the server, validate proxy requests, minimize and redact customer data, and use Shopify's authenticated customer context for private order lookups. Do not put API keys in theme assets. Require explicit customer confirmation for cart changes, and use Shopify checkout for all payments and COD.

## Notes

- No private app credentials, API keys, or store-specific IDs are included.
- Shopify's admin and checkout provide the secured operational workflows; this theme does not implement a separate admin dashboard or a custom payment system.
- Theme typography loads Google Fonts when online; the CSS includes system-serif and sans-serif fallbacks.
