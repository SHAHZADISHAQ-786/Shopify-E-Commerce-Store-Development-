import re

import streamlit as st


st.set_page_config(
    page_title="Softkind | Skincare, made simple",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRODUCTS = [
    {
        "id": "cloud-cleanser",
        "name": "Cloud Cleanser",
        "category": "Cleanser",
        "price": 18.00,
        "description": "A gentle, creamy daily cleanser that rinses away the day.",
        "ingredients": ["oat", "aloe", "glycerin"],
        "concerns": ["dry-feeling", "sensitive-feeling"],
        "step": "Cleanse",
        "emoji": "☁️",
        "stock": 24,
        "rating": 4.8,
        "reviews": 32,
    },
    {
        "id": "green-tea-gel",
        "name": "Green Tea Gel Cleanser",
        "category": "Cleanser",
        "price": 20.00,
        "description": "A fresh gel cleanser with green tea and a light finish.",
        "ingredients": ["green tea", "aloe"],
        "concerns": ["combination-feeling", "oily-feeling"],
        "step": "Cleanse",
        "emoji": "🍃",
        "stock": 11,
        "rating": 4.7,
        "reviews": 21,
    },
    {
        "id": "dew-serum",
        "name": "Dew Drop Serum",
        "category": "Serum",
        "price": 26.00,
        "description": "A lightweight hydration step with hyaluronic acid.",
        "ingredients": ["hyaluronic acid", "glycerin"],
        "concerns": ["dry-feeling", "dull-looking"],
        "step": "Treat",
        "emoji": "💧",
        "stock": 8,
        "rating": 4.9,
        "reviews": 46,
    },
    {
        "id": "calm-serum",
        "name": "Calm & Clear Serum",
        "category": "Serum",
        "price": 24.00,
        "description": "A simple niacinamide serum for an easy everyday routine.",
        "ingredients": ["niacinamide", "green tea"],
        "concerns": ["combination-feeling", "dull-looking"],
        "step": "Treat",
        "emoji": "🌱",
        "stock": 3,
        "rating": 4.6,
        "reviews": 18,
    },
    {
        "id": "daily-cloud-cream",
        "name": "Daily Cloud Cream",
        "category": "Moisturizer",
        "price": 22.00,
        "description": "A cushiony moisturizer with ceramides and oat.",
        "ingredients": ["ceramides", "oat", "squalane"],
        "concerns": ["dry-feeling", "sensitive-feeling"],
        "step": "Moisturize",
        "emoji": "🫧",
        "stock": 16,
        "rating": 4.9,
        "reviews": 54,
    },
    {
        "id": "lightweight-lotion",
        "name": "Lightweight Daily Lotion",
        "category": "Moisturizer",
        "price": 21.00,
        "description": "A light daily lotion with squalane and aloe.",
        "ingredients": ["squalane", "aloe", "glycerin"],
        "concerns": ["oily-feeling", "combination-feeling"],
        "step": "Moisturize",
        "emoji": "🌿",
        "stock": 19,
        "rating": 4.7,
        "reviews": 29,
    },
    {
        "id": "soft-shield-spf",
        "name": "Soft Shield SPF 30",
        "category": "Sun care",
        "price": 25.00,
        "description": "A comfortable broad-spectrum SPF 30 for daytime.",
        "ingredients": ["zinc oxide", "aloe"],
        "concerns": ["daily-protection"],
        "step": "Protect",
        "emoji": "☀️",
        "stock": 0,
        "rating": 4.8,
        "reviews": 37,
    },
    {
        "id": "overnight-mask",
        "name": "Overnight Comfort Mask",
        "category": "Treatment",
        "price": 28.00,
        "description": "A rich final step for a slower evening routine.",
        "ingredients": ["shea butter", "ceramides", "oat"],
        "concerns": ["dry-feeling", "sensitive-feeling"],
        "step": "Treat",
        "emoji": "🌙",
        "stock": 6,
        "rating": 4.8,
        "reviews": 25,
    },
]

CONCERN_LABELS = {
    "dry-feeling": "Feels dry",
    "oily-feeling": "Feels oily",
    "combination-feeling": "Feels combination",
    "sensitive-feeling": "Feels sensitive",
    "dull-looking": "Looks dull",
    "daily-protection": "Daily sun protection",
}

MEDICAL_TERMS = re.compile(
    r"\b(diagnos\w*|prescription|rash|eczema|acne treatment|infection|allerg\w*)\b",
    re.IGNORECASE,
)


def money(amount: float) -> str:
    return f"${amount:,.2f}"


def filtered_catalog(
    query: str, categories: list[str], budget: float, available_only: bool
) -> list[dict]:
    words = [word for word in re.findall(r"[a-z0-9]+", query.lower()) if len(word) > 2]
    matches = []
    for product in PRODUCTS:
        if categories and product["category"] not in categories:
            continue
        if product["price"] > budget:
            continue
        if available_only and product["stock"] < 1:
            continue
        search_text = " ".join(
            [
                product["name"],
                product["category"],
                product["description"],
                *product["ingredients"],
                *product["concerns"],
                product["step"],
            ]
        ).lower()
        score = sum(word in search_text for word in words)
        if not words or score:
            matches.append((score, product))
    return [
        product
        for _, product in sorted(
            matches,
            key=lambda match: (-match[0], match[1]["name"]),
        )
    ]


def show_product_card(product: dict, key_suffix: str) -> None:
    with st.container(border=True):
        st.markdown(f"## {product['emoji']}")
        st.markdown(f"### {product['name']}")
        st.caption(f"{product['category']} · {product['step']}")
        st.write(product["description"])
        st.markdown(
            f"**{money(product['price'])}**　·　⭐ {product['rating']} "
            f"({product['reviews']} reviews)"
        )
        st.caption(f"Key ingredients: {', '.join(product['ingredients'])}")
        if product["stock"] < 1:
            st.caption("Demo inventory: currently out of stock")
        else:
            st.caption(f"Demo inventory: {product['stock']} in stock")
        if st.button(
            "Save to my shortlist",
            key=f"save-{key_suffix}-{product['id']}",
            width="stretch",
        ):
            saved_ids = st.session_state["shortlist"]
            if product["id"] not in saved_ids:
                saved_ids.append(product["id"])
            st.toast(f"{product['name']} saved to your shortlist.")


def recommend_products(query: str, concerns: list[str], limit: int = 3) -> list[dict]:
    words = [word for word in re.findall(r"[a-z0-9]+", query.lower()) if len(word) > 2]
    scored = []
    for product in PRODUCTS:
        if product["stock"] < 1:
            continue
        search_text = " ".join(
            [
                product["name"],
                product["description"],
                *product["ingredients"],
                *product["concerns"],
                product["step"],
            ]
        ).lower()
        score = sum(word in search_text for word in words)
        score += 2 * len(set(concerns).intersection(product["concerns"]))
        if score:
            scored.append((score, product))
    return [
        product
        for _, product in sorted(
            scored, key=lambda match: (-match[0], match[1]["name"])
        )[:limit]
    ]


if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []

with st.sidebar:
    st.markdown("# softkind")
    st.caption("Thoughtful skincare, made simple.")
    page = st.segmented_control(
        "Explore",
        ["Discover", "Routine finder", "My shortlist", "Store overview"],
        default="Discover",
        selection_mode="single",
        width="stretch",
    )
    st.divider()
    st.caption("Student project demo · sample catalog and sample store metrics")

if page == "Discover":
    st.markdown("## YOUR DAILY ESSENTIALS")
    st.title("A little more care. A lot more you.")
    st.write(
        "Explore a thoughtfully curated demo catalog. Use the filters to find "
        "products by category, ingredient, or price."
    )
    query_col, budget_col = st.columns([3, 1])
    with query_col:
        query = st.text_input(
            "Search products",
            placeholder="Try oat, cleanser, moisturizer...",
        )
    with budget_col:
        budget = st.slider("Maximum price", 10, 40, 40)
    categories = st.multiselect(
        "Categories",
        sorted({product["category"] for product in PRODUCTS}),
    )
    available_only = st.checkbox("Only show in-stock items", value=True)

    results = filtered_catalog(query, categories, budget, available_only)
    st.caption(f"{len(results)} products")
    if results:
        for start in range(0, len(results), 3):
            columns = st.columns(3)
            for column, product in zip(columns, results[start : start + 3]):
                with column:
                    show_product_card(product, "discover")
    else:
        st.info("No products match those filters. Try a broader search.")

elif page == "Routine finder":
    st.markdown("## A ROUTINE THAT FEELS LIKE YOU")
    st.title("Find your everyday favorites")
    st.write(
        "Share your preferences to find matching products in our sample catalog. "
        "This demo uses simple catalog matching, not medical or AI advice."
    )
    with st.form("routine-finder"):
        concerns = st.multiselect(
            "What would you like your routine to focus on?",
            options=list(CONCERN_LABELS),
            format_func=lambda value: CONCERN_LABELS[value],
        )
        preference = st.text_input(
            "Ingredients or products you are interested in",
            placeholder="For example: oat, cleanser, SPF",
        )
        submitted = st.form_submit_button("Find products", type="primary")
    if submitted:
        st.session_state.pop("recommendation_ids", None)
        if MEDICAL_TERMS.search(preference):
            st.warning(
                "This tool can help browse products, but it cannot diagnose "
                "conditions or recommend treatment. For medical advice, speak "
                "with a qualified healthcare professional."
            )
        else:
            st.session_state["recommendation_ids"] = [
                product["id"]
                for product in recommend_products(preference, concerns)
            ]

    if "recommendation_ids" in st.session_state:
        recommendations = [
            product
            for product in PRODUCTS
            if product["id"] in st.session_state["recommendation_ids"]
        ]
        if recommendations:
            st.success(
                "Here are catalog matches based on the preferences you selected. "
                "Check each product page for full ingredient and usage details."
            )
            columns = st.columns(len(recommendations))
            for column, product in zip(columns, recommendations):
                with column:
                    show_product_card(product, "routine")
        else:
            st.info(
                "No close matches found in this demo catalog. Try a product "
                "type or ingredient."
            )

elif page == "My shortlist":
    st.markdown("## YOUR SAVED PICKS")
    st.title("My shortlist")
    selected_products = [
        product
        for product in PRODUCTS
        if product["id"] in st.session_state["shortlist"]
    ]
    if selected_products:
        columns = st.columns(min(len(selected_products), 3))
        for index, product in enumerate(selected_products):
            with columns[index % len(columns)]:
                show_product_card(product, "shortlist")
                if st.button(
                    "Remove from shortlist",
                    key=f"remove-{product['id']}",
                    width="stretch",
                ):
                    st.session_state["shortlist"].remove(product["id"])
                    st.rerun()
    else:
        st.info("Your shortlist is empty. Save products while you explore.")

elif page == "Store overview":
    st.markdown("## SHOP OWNER PREVIEW")
    st.title("Store overview")
    st.warning(
        "Preview only: all inventory and order numbers below are sample data, "
        "not connected to Shopify."
    )
    demo_orders = [
        {"order": "SK-1048", "status": "Fulfilled", "total": 46.00},
        {"order": "SK-1047", "status": "Processing", "total": 72.00},
        {"order": "SK-1046", "status": "Processing", "total": 24.00},
        {"order": "SK-1045", "status": "Fulfilled", "total": 43.00},
        {"order": "SK-1044", "status": "Pending COD", "total": 40.00},
    ]
    total_sales = sum(order["total"] for order in demo_orders)
    low_stock = sum(1 for product in PRODUCTS if 0 < product["stock"] < 5)
    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Demo orders", len(demo_orders))
    metric_b.metric("Demo sales", money(total_sales))
    metric_c.metric("Low-stock products", low_stock)

    st.subheader("Sample recent orders")
    for order in demo_orders:
        order_id, status, total = st.columns([2, 2, 1])
        order_id.markdown(f"**{order['order']}**")
        status.caption(order["status"])
        total.markdown(f"**{money(order['total'])}**")

    st.subheader("Sample inventory")
    inventory = sorted(PRODUCTS, key=lambda product: product["stock"])
    for product in inventory:
        name, stock, price = st.columns([3, 1, 1])
        name.write(product["name"])
        stock.caption(f"{product['stock']} units")
        price.caption(money(product["price"]))

st.divider()
st.caption(
    "Softkind is a learning demo with sample data. Product matches are informational, "
    "not medical recommendations. Shopify remains responsible for real products, "
    "accounts, orders, payments, and Cash on Delivery."
)

streamlit>=1.57,<2.0
