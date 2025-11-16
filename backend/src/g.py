import pandas as pd
import numpy as np
import random
from faker import Faker
import csv
from typing import List, Dict

# Initialize faker for realistic data
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ==================== PRODUCTS DATASET ====================

def generate_products_dataset():
    print("Generating Products Dataset (5000 rows)...")
    
    # Category distribution
    categories = {
        'Electronics': 1500,
        'Home & Kitchen': 1250, 
        'Fashion': 1000,
        'Beauty & Personal Care': 750,
        'Sports & Outdoors': 500
    }
    
    # Brands by category
    brands = {
        'Electronics': ['TechPro', 'Quantum', 'SonicWave', 'VisionTech', 'PowerMax', 'SmartLife', 'AudioElite', 'GigaTech'],
        'Home & Kitchen': ['HomeEssentials', 'KitchenMaster', 'ComfortLiving', 'ChefPro', 'UrbanHome', 'EcoLiving', 'PremiumKitchen'],
        'Fashion': ['StyleCraft', 'UrbanWear', 'EliteFashion', 'ComfortFit', 'TrendStyle', 'LuxeApparel', 'ModernWear'],
        'Beauty & Personal Care': ['GlowBeauty', 'PureSkin', 'NatureCare', 'LuxeBeauty', 'FreshGlow', 'RadiantYou'],
        'Sports & Outdoors': ['ActiveLife', 'ProFit', 'OutdoorGear', 'SportElite', 'AdventurePro', 'FitTech']
    }
    
    # Target audiences
    target_audiences = ['B2C Consumers', 'Professionals', 'Students', 'Families', 'Luxury Buyers', 'Budget Conscious']
    
    products = []
    
    product_id = 1
    for category, count in categories.items():
        print(f"Generating {count} {category} products...")
        
        for _ in range(count):
            # Generate product name
            if category == 'Electronics':
                names = [f"{brand} {fake.word().title()} {random.choice(['Pro', 'Max', 'Plus', 'Elite', 'Premium', 'X', 'Ultra'])} {random.choice(['Smartphone', 'Laptop', 'Headphones', 'Smartwatch', 'Tablet', 'Camera', 'Speaker'])}" 
                        for brand in brands[category]]
            elif category == 'Home & Kitchen':
                names = [f"{brand} {fake.word().title()} {random.choice(['Professional', 'Deluxe', 'Premium', 'Smart', 'Ultra', 'Pro'])} {random.choice(['Blender', 'Coffee Maker', 'Vacuum', 'Air Fryer', 'Cookware Set', 'Mattress'])}" 
                        for brand in brands[category]]
            elif category == 'Fashion':
                names = [f"{brand} {fake.word().title()} {random.choice(['Designer', 'Premium', 'Comfort', 'Style', 'Luxe'])} {random.choice(['Sneakers', 'Jacket', 'Watch', 'Handbag', 'Jeans', 'Dress'])}" 
                        for brand in brands[category]]
            elif category == 'Beauty & Personal Care':
                names = [f"{brand} {fake.word().title()} {random.choice(['Advanced', 'Natural', 'Professional', 'Luxury', 'Organic'])} {random.choice(['Face Cream', 'Serum', 'Makeup Kit', 'Perfume', 'Hair Care'])}" 
                        for brand in brands[category]]
            else:  # Sports
                names = [f"{brand} {fake.word().title()} {random.choice(['Pro', 'Elite', 'Training', 'Performance', 'Advanced'])} {random.choice(['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Tent', 'Bicycle'])}" 
                        for brand in brands[category]]
            
            name = random.choice(names)
            brand = random.choice(brands[category])
            
            # Generate realistic price based on category
            if category == 'Electronics':
                price = round(random.uniform(80, 1200), 2)
            elif category == 'Home & Kitchen':
                price = round(random.uniform(25, 800), 2)
            elif category == 'Fashion':
                price = round(random.uniform(20, 500), 2)
            elif category == 'Beauty & Personal Care':
                price = round(random.uniform(15, 300), 2)
            else:  # Sports
                price = round(random.uniform(30, 600), 2)
            
            # Generate detailed description
            description = generate_product_description(category, name, brand)
            
            # Select target audience with weighted distribution
            audience_weights = [0.25, 0.20, 0.15, 0.20, 0.10, 0.10]
            target_audience = random.choices(target_audiences, weights=audience_weights)[0]
            
            products.append({
                'product_id': product_id,
                'name': name,
                'category': category,
                'description': description,
                'price': price,
                'brand': brand,
                'target_audience': target_audience
            })
            
            product_id += 1
    
    # Shuffle products to mix categories
    random.shuffle(products)
    
    return pd.DataFrame(products)

def generate_product_description(category, name, brand):
    """Generate detailed product descriptions with specific features"""
    
    if category == 'Electronics':
        features = [
            f"The {name} features a {random.choice(['6.7-inch', '15.6-inch', '5.8-inch'])} {random.choice(['OLED', 'IPS LCD', 'AMOLED'])} display with {random.choice(['4K', 'Full HD', 'Retina'])} resolution. ",
            f"Powered by {random.choice(['Snapdragon 8 Gen 2', 'Apple M2', 'Intel Core i7', 'AMD Ryzen 7'])} processor with {random.choice(['8GB', '16GB', '12GB'])} RAM. ",
            f"Features {random.choice(['triple camera system', 'advanced AI camera', 'professional-grade lens'])} with {random.choice(['108MP', '48MP', '12MP'])} main sensor. ",
            f"Battery life of {random.choice(['all-day', 'up to 20 hours', 'fast-charging'])} with {random.choice(['5G', 'WiFi 6', 'Bluetooth 5.2'])} connectivity. ",
            f"Perfect for {random.choice(['professionals', 'content creators', 'gaming enthusiasts', 'everyday users'])} seeking {random.choice(['premium performance', 'reliable technology', 'cutting-edge features'])}."
        ]
    
    elif category == 'Home & Kitchen':
        features = [
            f"The {name} boasts {random.choice(['commercial-grade', 'premium', 'energy-efficient'])} {random.choice(['1500W motor', 'stainless steel construction', 'non-stick coating'])}. ",
            f"Features {random.choice(['multiple speed settings', 'digital controls', 'smart technology'])} for {random.choice(['precise cooking', 'easy operation', 'automated functions'])}. ",
            f"Designed with {random.choice(['BPA-free materials', 'easy-clean surfaces', 'safety features'])} making it {random.choice(['family-friendly', 'durable', 'user-safe'])}. ",
            f"Perfect for {random.choice(['home cooks', 'busy families', 'culinary enthusiasts'])} who value {random.choice(['convenience', 'quality', 'innovation'])} in their kitchen. ",
            f"Includes {random.choice(['accessory set', 'recipe book', 'warranty'])} and is {random.choice(['dishwasher safe', 'space-saving', 'versatile'])} for various uses."
        ]
    
    elif category == 'Fashion':
        features = [
            f"Crafted from {random.choice(['premium cotton', 'Italian leather', 'technical fabric', 'organic materials'])} for {random.choice(['exceptional comfort', 'durable wear', 'stylish appearance'])}. ",
            f"Features {random.choice(['ergonomic design', 'water-resistant coating', 'adjustable elements', 'signature detailing'])} that enhances {random.choice(['fit', 'functionality', 'style'])}. ",
            f"Available in {random.choice(['multiple sizes', 'various colors', 'different finishes'])} to suit {random.choice(['personal style', 'specific occasions', 'individual preferences'])}. ",
            f"Perfect for {random.choice(['everyday wear', 'professional settings', 'special occasions', 'active lifestyles'])} with {random.choice(['timeless design', 'modern aesthetics', 'practical features'])}. ",
            f"From {brand}'s {random.choice(['latest collection', 'signature line', 'premium range'])} offering {random.choice(['excellent value', 'luxury quality', 'innovative design'])}."
        ]
    
    elif category == 'Beauty & Personal Care':
        features = [
            f"Formulated with {random.choice(['natural ingredients', 'advanced compounds', 'clinical-strength actives'])} like {random.choice(['hyaluronic acid', 'vitamin C', 'retinol', 'plant extracts'])}. ",
            f"Provides {random.choice(['24-hour hydration', 'visible results', 'gentle care', 'professional-grade performance'])} for {random.choice(['all skin types', 'specific concerns', 'daily use'])}. ",
            f"Features {random.choice(['non-comedogenic', 'cruelty-free', 'vegan', 'dermatologist-tested'])} formula that's {random.choice(['safe', 'effective', 'luxurious'])}. ",
            f"Delivers {random.choice(['radiant glow', 'reduced appearance', 'enhanced natural beauty', 'professional results'])} with {random.choice(['regular use', 'immediate effect', 'long-term benefits'])}. ",
            f"Packaged in {random.choice(['elegant', 'sustainable', 'functional'])} container with {random.choice(['airless pump', 'glass bottle', 'travel-friendly design'])}."
        ]
    
    else:  # Sports & Outdoors
        features = [
            f"Constructed with {random.choice(['high-density foam', 'weather-resistant fabric', 'aircraft-grade aluminum', 'premium rubber'])} for {random.choice(['maximum durability', 'optimal performance', 'superior comfort'])}. ",
            f"Features {random.choice(['ergonomic design', 'advanced technology', 'safety enhancements', 'performance optimization'])} that improves {random.choice(['workout efficiency', 'outdoor experience', 'athletic performance'])}. ",
            f"Designed for {random.choice(['intense training', 'outdoor adventures', 'casual exercise', 'professional use'])} with {random.choice(['portable design', 'easy storage', 'quick setup'])}. ",
            f"Perfect for {random.choice(['fitness enthusiasts', 'outdoor adventurers', 'sports professionals', 'recreational users'])} seeking {random.choice(['reliable equipment', 'premium quality', 'innovative features'])}. ",
            f"Includes {random.choice(['carrying case', 'accessories', 'warranty', 'instruction guide'])} and is {random.choice(['easy to maintain', 'space-efficient', 'multi-functional'])}."
        ]
    
    # Combine 3-4 random features for unique description
    description = ''.join(random.sample(features, random.randint(3, 4)))
    return description

# ==================== MARKETING COPY DATASET ====================

def generate_marketing_copy_dataset(products_df):
    print("Generating Marketing Copy Dataset (10,000 rows)...")
    
    platforms = ['YouTube', 'Instagram', 'Facebook', 'Email', 'TikTok']
    platform_weights = [0.30, 0.25, 0.20, 0.15, 0.10]
    
    script_types = {
        'YouTube': 'video_script',
        'Instagram': 'social_post', 
        'Facebook': 'ad_copy',
        'Email': 'email_copy',
        'TikTok': 'story_post'
    }
    
    tones = ['Professional', 'Energetic', 'Friendly', 'Inspiring', 'Humorous', 'Minimalist']
    tone_weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
    
    content_structures = ['problem-solution', 'feature-benefit', 'story-based', 'testimonial', 'comparison', 'lifestyle']
    structure_weights = [0.30, 0.25, 0.20, 0.15, 0.05, 0.05]
    
    ctas = [
        "Buy now and save 20%!", "Shop today with free shipping!", "Get yours while supplies last!",
        "Learn more on our website!", "Limited time offer - order now!", "Start your journey today!",
        "Experience the difference!", "Join thousands of satisfied customers!", "Upgrade your life today!",
        "Don't miss this exclusive deal!"
    ]
    
    marketing_data = []
    
    for script_id in range(1, 10001):
        if script_id % 1000 == 0:
            print(f"Generated {script_id} marketing scripts...")
        
        # Randomly select a product
        product = products_df.iloc[random.randint(0, len(products_df)-1)]
        product_id = product['product_id']
        category = product['category']
        product_name = product['name']
        brand = product['brand']
        
        # Select platform with weighted distribution
        platform = random.choices(platforms, weights=platform_weights)[0]
        script_type = script_types[platform]
        
        # Select tone and structure with weighted distribution
        tone = random.choices(tones, weights=tone_weights)[0]
        content_structure = random.choices(content_structures, weights=structure_weights)[0]
        
        # Generate keywords based on product
        keywords = generate_keywords(category, product_name, brand)
        
        # Select CTA
        cta = random.choice(ctas)
        
        # Generate performance score (bell curve distribution)
        performance_score = generate_performance_score()
        
        # Generate review score correlated with performance
        review_score = generate_review_score(performance_score)
        
        # Generate marketing content
        content = generate_marketing_content(
            platform, tone, content_structure, product, keywords, cta
        )
        
        marketing_data.append({
            'script_id': script_id,
            'product_id': product_id,
            'platform': platform,
            'script_type': script_type,
            'tone': tone,
            'content_structure': content_structure,
            'keywords': ','.join(keywords),
            'cta': cta,
            'performance_score': performance_score,
            'review_score': review_score,
            'content': content
        })
    
    return pd.DataFrame(marketing_data)

def generate_keywords(category, product_name, brand):
    """Generate relevant keywords based on product"""
    base_keywords = []
    
    if category == 'Electronics':
        base_keywords = ['technology', 'innovation', 'smart', 'premium', 'performance', 'quality', 'reliable']
    elif category == 'Home & Kitchen':
        base_keywords = ['home', 'kitchen', 'quality', 'durable', 'efficient', 'convenient', 'family']
    elif category == 'Fashion':
        base_keywords = ['style', 'fashion', 'trendy', 'comfort', 'quality', 'design', 'premium']
    elif category == 'Beauty & Personal Care':
        base_keywords = ['beauty', 'skincare', 'natural', 'effective', 'luxury', 'selfcare', 'glow']
    else:  # Sports
        base_keywords = ['fitness', 'sports', 'performance', 'durable', 'active', 'health', 'outdoor']
    
    # Add brand and product-specific keywords
    product_words = product_name.lower().split()
    specific_keywords = [word for word in product_words if len(word) > 3][:3]
    
    all_keywords = base_keywords + specific_keywords + [brand.lower()]
    return random.sample(list(set(all_keywords)), min(8, len(set(all_keywords))))

def generate_performance_score():
    """Generate performance score with bell curve distribution"""
    score = np.random.normal(6.5, 2.0)
    score = max(1.0, min(10.0, score))
    return round(score, 1)

def generate_review_score(performance_score):
    """Generate review score correlated with performance"""
    base_reviews = performance_score * 800  # Base multiplier
    variation = random.randint(-2000, 2000)  # Some variation
    review_score = int(max(50, base_reviews + variation))
    return min(50000, review_score)

def generate_marketing_content(platform, tone, structure, product, keywords, cta):
    """Generate platform-specific marketing content"""
    
    product_name = product['name']
    category = product['category']
    brand = product['brand']
    description = product['description']
    
    if platform == 'YouTube':
        return generate_youtube_script(product_name, category, brand, tone, structure, cta)
    elif platform == 'Instagram':
        return generate_instagram_post(product_name, category, brand, tone, structure, cta)
    elif platform == 'Facebook':
        return generate_facebook_post(product_name, category, brand, tone, structure, cta)
    elif platform == 'Email':
        return generate_email_copy(product_name, category, brand, tone, structure, cta)
    else:  # TikTok
        return generate_tiktok_script(product_name, category, brand, tone, structure, cta)

def generate_youtube_script(product_name, category, brand, tone, structure, cta):
    """Generate YouTube video script"""
    
    openings = {
        'Professional': f"Welcome to our comprehensive review of the {product_name}. Today we'll explore its innovative features and performance.",
        'Energetic': f"Get ready to be amazed by the incredible {product_name}! This is hands-down the most exciting {category} we've tested!",
        'Friendly': f"Hey everyone! Today we're checking out the amazing {product_name} from {brand}. Let me show you why I'm so impressed!",
        'Inspiring': f"Imagine transforming your daily routine with the revolutionary {product_name}. This isn't just a product - it's a lifestyle upgrade.",
        'Humorous': f"Okay, I have to admit - the {product_name} made me do a double take! This thing is seriously impressive, and here's why...",
        'Minimalist': f"The {product_name}. Clean design. Exceptional performance. Everything you need, nothing you don't."
    }
    
    content = f"{openings[tone]}\n\n"
    
    if structure == 'problem-solution':
        content += f"[SCENE: Person struggling with outdated equipment]\n"
        content += f"VOICEOVER: Tired of dealing with {random.choice(['inefficient', 'outdated', 'complicated'])} {category}? The {product_name} solves this with its {random.choice(['innovative', 'smart', 'efficient'])} design.\n\n"
    elif structure == 'feature-benefit':
        content += f"[SCENE: Close-up shots of product features]\n"
        content += f"VOICEOVER: Notice the premium materials and thoughtful design. Each feature of the {product_name} delivers tangible benefits for your daily life.\n\n"
    
    content += f"[SCENE: Demonstration of product in use]\n"
    content += f"VOICEOVER: Watch how seamlessly the {product_name} integrates into your routine. The attention to detail from {brand} is exceptional.\n\n"
    
    content += f"[SCENE: Final summary shot]\n"
    content += f"VOICEOVER: After extensive testing, we can confidently recommend the {product_name}. {cta}\n\n"
    content += f"Like this video if you found it helpful, and subscribe for more {category} reviews!"
    
    return content

def generate_instagram_post(product_name, category, brand, tone, structure, cta):
    """Generate Instagram post"""
    
    captions = {
        'Professional': f"Introducing the {product_name} from {brand} - a game-changer in {category} technology. ✨",
        'Energetic': f"OMG you guys! The {product_name} is absolutely incredible! 🤯 Life-changing {category} alert!",
        'Friendly': f"Hey friends! Just had to share my new favorite find - the {product_name}! So impressed with {brand}! 💫",
        'Inspiring': f"Elevate your everyday with the stunning {product_name}. Because you deserve the best from {brand}. 🌟",
        'Humorous': f"Me before {product_name}: 😴 Me after: 😎 No but seriously, this {category} is a game-changer!",
        'Minimalist': f"{product_name}. Perfected. {brand}"
    }
    
    content = f"{captions[tone]}\n\n"
    
    if structure == 'problem-solution':
        content += f"Say goodbye to {random.choice(['frustrating', 'inefficient', 'complicated'])} {category} problems! The {product_name} delivers the solution you've been waiting for.\n\n"
    elif structure == 'feature-benefit':
        content += f"Every detail matters. From premium materials to innovative design, the {product_name} combines style and functionality perfectly.\n\n"
    
    content += f"Available now from {brand} - the trusted name in quality {category}.\n\n"
    content += f"{cta}\n\n"
    content += f"#{brand.replace(' ', '')} #{category.replace(' ', '')} #{product_name.replace(' ', '')} #Quality #Innovation"
    
    return content

def generate_facebook_post(product_name, category, brand, tone, structure, cta):
    """Generate Facebook post"""
    
    content = f"🌟 NEW from {brand}: The {product_name} is here! 🌟\n\n"
    
    if structure == 'problem-solution':
        content += f"Are you tired of dealing with ordinary {category} that doesn't meet your expectations? We were too, which is why we created the {product_name} with innovative features that actually make a difference in your daily life.\n\n"
    elif structure == 'feature-benefit':
        content += f"Every aspect of the {product_name} has been carefully designed to provide maximum value. From its premium construction to its user-friendly features, this {category} represents the perfect balance of form and function.\n\n"
    
    content += f"What sets the {product_name} apart is our commitment to quality and customer satisfaction. {brand} has been delivering exceptional products for years, and this latest addition continues that tradition of excellence.\n\n"
    content += f"{cta}\n\n"
    content += f"Tag a friend who needs to see this! 👇"
    
    return content

def generate_email_copy(product_name, category, brand, tone, structure, cta):
    """Generate email marketing copy"""
    
    subject = f"Introducing The {product_name} - Revolutionizing {category}"
    
    content = f"Subject: {subject}\n\n"
    content += f"Dear Valued Customer,\n\n"
    
    if structure == 'problem-solution':
        content += f"We understand the challenges of finding high-quality {category} that truly delivers on its promises. That's why we're thrilled to introduce the {product_name} from {brand} - designed specifically to address your needs with innovative solutions.\n\n"
    elif structure == 'feature-benefit':
        content += f"We're excited to present the {product_name}, where every feature has been meticulously crafted to enhance your experience. From its premium materials to its advanced functionality, this {category} represents the pinnacle of {brand}'s commitment to excellence.\n\n"
    
    content += f"Here's what makes the {product_name} special:\n"
    content += f"• Premium quality construction for lasting durability\n"
    content += f"• Innovative features that simplify your daily routine\n"
    content += f"• Backed by {brand}'s reputation for excellence\n"
    content += f"• Designed with your needs in mind\n\n"
    
    content += f"{cta}\n\n"
    content += f"Best regards,\nThe {brand} Team"
    
    return content

def generate_tiktok_script(product_name, category, brand, tone, structure, cta):
    """Generate TikTok script"""
    
    hooks = {
        'Professional': f"Professional review: {product_name} - worth the hype?",
        'Energetic': f"NO WAY! The {product_name} actually does this?! 🤯",
        'Friendly': f"Guys, I found the perfect {category} and you NEED to see this!",
        'Inspiring': f"Upgrade your life with the {product_name} ✨ Life-changing!",
        'Humorous': f"POV: You try the {product_name} for the first time 😂",
        'Minimalist': f"{product_name}. That's it. That's the tweet."
    }
    
    content = f"{hooks[tone]}\n\n"
    content += f"Wait until you see what the {product_name} can do!\n\n"
    
    if structure == 'problem-solution':
        content += f"Problem: Ordinary {category} that doesn't work\n"
        content += f"Solution: {product_name} with amazing features\n\n"
    elif structure == 'feature-benefit':
        content += f"Feature 1: Premium quality ✅\n"
        content += f"Feature 2: Amazing performance ✅\n"
        content += f"Feature 3: Great value ✅\n\n"
    
    content += f"{cta}\n\n"
    content += f"#{brand} #{category} #{product_name.replace(' ', '')} #MustHave"
    
    return content

# ==================== MAIN EXECUTION ====================

def main():
    print("🚀 Starting Dataset Generation...")
    
    # Generate products dataset
    products_df = generate_products_dataset()
    
    # Generate marketing copy dataset
    marketing_df = generate_marketing_copy_dataset(products_df)
    
    # Save to CSV files
    print("Saving datasets to CSV files...")
    
    products_df.to_csv('products.csv', index=False, quoting=csv.QUOTE_ALL)
    marketing_df.to_csv('marketing_copy.csv', index=False, quoting=csv.QUOTE_ALL)
    
    print("✅ Dataset generation completed!")
    print(f"📊 Products dataset: {len(products_df)} rows")
    print(f"📝 Marketing copy dataset: {len(marketing_df)} rows")
    print(f"💾 Files saved: 'products.csv' and 'marketing_copy.csv'")
    
    # Display sample data
    print("\n📦 Sample Product:")
    print(products_df.iloc[0])
    print("\n📝 Sample Marketing Copy:")
    print(marketing_df.iloc[0])

if __name__ == "__main__":
    main()