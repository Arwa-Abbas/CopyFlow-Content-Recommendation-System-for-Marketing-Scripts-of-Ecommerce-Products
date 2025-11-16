import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Dict

# Load SpaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ SpaCy model loaded successfully")
except OSError:
    print("❌ SpaCy model not found. Please install with: python -m spacy download en_core_web_sm")
    nlp = None

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def extract_features_from_text(text):
    """Extract key features from product description using NLP"""
    if not text or not nlp:
        return []
    
    doc = nlp(text)
    
    # Extract nouns and adjectives as key features
    features = []
    for token in doc:
        if (token.pos_ in ["NOUN", "ADJ", "PROPN"] and 
            not token.is_stop and 
            len(token.text) > 2 and
            token.is_alpha):
            features.append(token.lemma_.lower())
    
    return list(set(features))  # Remove duplicates

def extract_key_phrases(text):
    """Extract meaningful phrases and key specifications"""
    if not text:
        return []
    
    # Extract specifications like "108MP camera", "120Hz display", etc.
    specifications = re.findall(r'(\d+(?:\.\d+)?\s*(?:GB|MP|GHz|Hz|W|mAh|inch|hours?))', text, re.IGNORECASE)
    
    # Extract material descriptions
    materials = re.findall(r'(stainless steel|aluminum|leather|cotton|plastic|glass|wood|fabric)', text, re.IGNORECASE)
    
    # Extract key benefits
    benefits = re.findall(r'(waterproof|shockproof|energy efficient|eco.friendly|wireless|bluetooth|smart|premium|professional)', text, re.IGNORECASE)
    
    return specifications + materials + benefits

def update_products_features():
    """Extract and update features for all products"""
    print("🔄 Extracting features from product descriptions...")
    
    products_updated = 0
    for product in db.products.find():
        description = product.get("description", "")
        name = product.get("name", "")
        category = product.get("category", "")
        
        # Combine text for feature extraction
        combined_text = f"{name} {category} {description}"
        
        # Extract features using NLP
        nlp_features = extract_features_from_text(combined_text)
        
        # Extract key phrases and specifications
        key_phrases = extract_key_phrases(combined_text)
        
        # Combine all features
        all_features = nlp_features + key_phrases
        
        # Limit to top 15 most relevant features
        relevant_features = all_features[:15]
        
        # Update product in database
        db.products.update_one(
            {"_id": product["_id"]}, 
            {"$set": {
                "extracted_features": relevant_features,
                "feature_count": len(relevant_features)
            }}
        )
        
        products_updated += 1
        
        if products_updated % 500 == 0:
            print(f"   Processed {products_updated} products...")
    
    print(f"✅ Features extracted for {products_updated} products")

def analyze_marketing_patterns():
    """Analyze patterns in marketing data for feature extraction"""
    print("📊 Analyzing marketing patterns...")
    
    # Extract common keywords from high-performing marketing scripts
    high_performing_scripts = db.scripts.find({
        "performance_score": {"$gte": 8.0}
    })
    
    successful_keywords = []
    for script in high_performing_scripts:
        keywords = script.get("keywords", [])
        if isinstance(keywords, list):
            successful_keywords.extend(keywords)
    
    # Get most common successful keywords
    from collections import Counter
    keyword_counts = Counter(successful_keywords)
    top_keywords = [keyword for keyword, count in keyword_counts.most_common(50)]
    
    print(f"✅ Found {len(top_keywords)} top-performing keywords")
    return top_keywords

def create_feature_mappings():
    """Create category-specific feature mappings"""
    print("🗺️ Creating feature mappings...")
    
    categories = db.products.distinct("category")
    category_features = {}
    
    for category in categories:
        # Get all products in this category
        category_products = db.products.find({"category": category})
        
        all_features = []
        for product in category_products:
            features = product.get("extracted_features", [])
            all_features.extend(features)
        
        # Get most common features for this category
        from collections import Counter
        feature_counts = Counter(all_features)
        top_features = [feature for feature, count in feature_counts.most_common(20)]
        
        category_features[category] = top_features
        print(f"   {category}: {len(top_features)} common features")
    
    # Store category features in database
    db.category_features.delete_many({})
    for category, features in category_features.items():
        db.category_features.insert_one({
            "category": category,
            "common_features": features
        })
    
    print(f"✅ Feature mappings created for {len(categories)} categories")

def extract_marketing_insights():
    """Extract insights from marketing performance data"""
    print("💡 Extracting marketing insights...")
    
    # Analyze which tones work best for which categories
    pipeline = [
        {
            "$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "product_id",
                "as": "product_info"
            }
        },
        {"$unwind": "$product_info"},
        {
            "$group": {
                "_id": {
                    "category": "$product_info.category",
                    "tone": "$tone"
                },
                "avg_performance": {"$avg": "$performance_score"},
                "count": {"$sum": 1}
            }
        },
        {"$match": {"count": {"$gte": 10}}},  # Only consider tones with sufficient data
        {"$sort": {"avg_performance": -1}}
    ]
    
    tone_effectiveness = list(db.scripts.aggregate(pipeline))
    
    # Store insights in database
    db.marketing_insights.delete_many({})
    for insight in tone_effectiveness:
        db.marketing_insights.insert_one(insight)
    
    print(f"✅ Extracted {len(tone_effectiveness)} marketing insights")

def main():
    """Main function to run all feature extraction processes"""
    print("🚀 Starting Feature Extraction Pipeline...")
    
    # Step 1: Extract features from product descriptions
    update_products_features()
    
    # Step 2: Analyze marketing patterns
    successful_keywords = analyze_marketing_patterns()
    
    # Step 3: Create category feature mappings
    create_feature_mappings()
    
    # Step 4: Extract marketing insights
    extract_marketing_insights()
    
    # Final summary
    product_count = db.products.count_documents({})
    products_with_features = db.products.count_documents({"extracted_features": {"$exists": True}})
    
    print(f"\n🎉 FEATURE EXTRACTION COMPLETED!")
    print(f"   Products processed: {products_with_features}/{product_count}")
    print(f"   Top performing keywords: {len(successful_keywords)}")
    print(f"   Marketing insights extracted: {db.marketing_insights.count_documents({})}")

if __name__ == "__main__":
    main()