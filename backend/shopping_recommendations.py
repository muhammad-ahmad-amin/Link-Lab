import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
UPSTREAM_API = "https://dummyjson.com/products?limit=0" 
# Note: limit=0 gets ALL products in DummyJSON so we have a better pool to search from

# --- DATA & MAPPINGS ---
PRODUCTS_DB = []
CATEGORIES_DB = []

# Define related categories so the AI knows "Makeup" relates to "Skincare" but not "Furniture"
CATEGORY_GROUPS = {
    'tech': ['smartphones', 'laptops', 'tablets', 'mobile-accessories'],
    'home': ['furniture', 'home-decoration', 'kitchen-accessories', 'groceries'],
    'beauty': ['beauty', 'fragrances', 'skin-care', 'makeup'],
    'fashion': ['tops', 'womens-dresses', 'womens-shoes', 'mens-shirts', 'mens-shoes', 'womens-bags', 'womens-jewellery', 'sunglasses'],
    'vehicles': ['vehicle', 'motorcycle']
}

def load_data():
    global PRODUCTS_DB, CATEGORIES_DB
    try:
        print("⏳ Loading product catalog...")
        # Fetch all products (limit=0 usually fetches all in dummyjson, or we set a high number)
        response = requests.get("https://dummyjson.com/products?limit=194") 
        data = response.json()
        PRODUCTS_DB = data.get('products', [])
        CATEGORIES_DB = list(set(p['category'] for p in PRODUCTS_DB))
        print(f"✅ Loaded {len(PRODUCTS_DB)} products.")
    except Exception as e:
        print(f"❌ Error loading data: {e}")

def get_related_categories(target_category):
    """Finds siblings in the same group (e.g., 'makeup' -> ['skincare', 'fragrances'])"""
    for group, cats in CATEGORY_GROUPS.items():
        if target_category in cats:
            return cats
    return []

# --- RECOMMENDATION ENGINE ---
def get_recommendations(cart_items, strategy='hybrid'):
    # 1. COLD START: If cart is empty, show top rated diverse items
    if not cart_items:
        return sorted(PRODUCTS_DB, key=lambda x: x.get('rating', 0), reverse=True)[:12]

    # 2. ANALYZE CART
    cart_ids = {item.get('id') for item in cart_items}
    cart_categories = [item.get('category') for item in cart_items]
    
    # Count frequency of categories in cart
    category_counts = defaultdict(int)
    for c in cart_categories:
        category_counts[c] += 1

    scored_products = []

    # 3. SCORE PRODUCTS
    for product in PRODUCTS_DB:
        # Skip items already in cart
        if product['id'] in cart_ids:
            continue

        score = 0
        p_cat = product['category']
        
        # --- SCORING RULES ---
        
        # Rule A: EXACT Category Match (The most important factor)
        # We give this a HUGE score (100) so it beats everything else
        if p_cat in category_counts:
            score += 100 * category_counts[p_cat]
        
        # Rule B: RELATED Category Match (Cluster logic)
        # If user bought 'makeup', suggest 'skincare' (Score: 20)
        else:
            for cart_cat in category_counts:
                related = get_related_categories(cart_cat)
                if p_cat in related:
                    score += 20
                    break
        
        # Rule C: Rating Boost (Collaborative Simulation)
        # ONLY apply rating boost if the item is at least somewhat relevant (score > 0)
        # This prevents 5-star Furniture from showing up for Makeup users
        if score > 0:
            score += product.get('rating', 0)
            
            # Tiny price similarity boost
            cart_avg_price = sum(i['price'] for i in cart_items) / len(cart_items)
            if abs(product['price'] - cart_avg_price) < 50:
                score += 5

        # If score is still 0, it means it's completely unrelated (e.g., Furniture vs Makeup)
        # We filter it out by not adding it to the list, or giving it a negative score.
        if score > 0:
            scored_products.append((product, score))

    # 4. SORT & RETURN
    scored_products.sort(key=lambda x: x[1], reverse=True)
    
    # Return top results
    return [p[0] for p in scored_products[:15]]


# --- API ENDPOINTS ---
@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')
    results = PRODUCTS_DB
    
    if category and category != 'all':
        results = [p for p in results if p['category'] == category]
    if search:
        term = search.lower()
        results = [p for p in results if term in p['title'].lower()]
        
    return jsonify({"products": results})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES_DB)

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    product = next((p for p in PRODUCTS_DB if p['id'] == product_id), None)
    if product: return jsonify(product)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        payload = request.get_json()
        cart = payload.get('cart', [])
        strategy = payload.get('strategy', 'hybrid')
        
        # Pass the combined cart + wishlist data to the engine
        recs = get_recommendations(cart, strategy)
        return jsonify(recs)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([]), 500

if __name__ == '__main__':
    load_data()
    app.run(host='0.0.0.0', port=8000, debug=True)