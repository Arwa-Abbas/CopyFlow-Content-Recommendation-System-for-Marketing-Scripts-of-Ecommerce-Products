import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Get the correct base directory (backend folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_products():
    try:
        # Correct file path - go up one level from src to backend, then to data folder
        products_path = os.path.join(DATA_DIR, 'products.csv')
        print(f"📁 Looking for products at: {products_path}")
        
        df = pd.read_csv(products_path, encoding="utf-8")
        print(f"✅ Loaded {len(df)} products from CSV")
        
        # Convert price to float and handle missing values
        if "price" in df.columns:
            df["price"] = pd.to_numeric(df["price"], errors='coerce')
            df["price"] = df["price"].fillna(0.0)
        
        # Extract features from description if features column doesn't exist
        if "features" not in df.columns:
            print("⚠️  No 'features' column found. Features will be extracted later...")
        
        # Insert into MongoDB
        db.products.insert_many(df.to_dict("records"))
        print(f"✅ Successfully inserted {len(df)} products into MongoDB")
        
    except FileNotFoundError:
        print(f"❌ Products CSV file not found at: {products_path}")
        print("💡 Please make sure the file exists in the data folder")
        raise
    except Exception as e:
        print(f"❌ Error loading products: {e}")
        raise

def load_marketing_copy():
    try:
        # Correct file path
        marketing_path = os.path.join(DATA_DIR, 'marketing_copy.csv')
        print(f"📁 Looking for marketing data at: {marketing_path}")
        
        df = pd.read_csv(marketing_path, encoding="utf-8")
        print(f"✅ Loaded {len(df)} marketing scripts from CSV")
        
        # Convert performance_score and review_score to numeric
        if "performance_score" in df.columns:
            df["performance_score"] = pd.to_numeric(df["performance_score"], errors='coerce')
            df["performance_score"] = df["performance_score"].fillna(5.0)
        
        if "review_score" in df.columns:
            df["review_score"] = pd.to_numeric(df["review_score"], errors='coerce')
            df["review_score"] = df["review_score"].fillna(1000)
        
        # Convert keywords from string to list if they're comma-separated
        if "keywords" in df.columns:
            df["keywords"] = df["keywords"].apply(
                lambda x: x.split(",") if isinstance(x, str) else []
            )
        
        # **NEW: Handle the 'content' column from our generated dataset**
        if "content" not in df.columns:
            print("⚠️  No 'content' column found in marketing data")
        
        # Insert into MongoDB
        db.scripts.insert_many(df.to_dict("records"))
        print(f"✅ Successfully inserted {len(df)} marketing scripts into MongoDB")
        
    except FileNotFoundError:
        print(f"❌ Marketing CSV file not found at: {marketing_path}")
        print("💡 Please make sure the file exists in the data folder")
        raise
    except Exception as e:
        print(f"❌ Error loading marketing copy: {e}")
        raise

def check_data_quality():
    """Check if data was loaded correctly"""
    try:
        product_count = db.products.count_documents({})
        script_count = db.scripts.count_documents({})
        
        print(f"\n📊 DATA QUALITY CHECK:")
        print(f"   Products in database: {product_count}")
        print(f"   Marketing scripts in database: {script_count}")
        
        # Check category distribution
        categories = db.products.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ])
        
        print(f"\n📦 Category Distribution:")
        for cat in categories:
            print(f"   {cat['_id']}: {cat['count']} products")
        
        # Check platform distribution
        platforms = db.scripts.aggregate([
            {"$group": {"_id": "$platform", "count": {"$sum": 1}}}
        ])
        
        print(f"\n📱 Platform Distribution:")
        for platform in platforms:
            print(f"   {platform['_id']}: {platform['count']} scripts")
        
        if product_count > 0 and script_count > 0:
            print("✅ Data loading successful!")
            
            # Show sample data
            sample_product = db.products.find_one()
            sample_script = db.scripts.find_one()
            
            print(f"\n📦 Sample Product:")
            print(f"   Name: {sample_product.get('name', 'N/A')}")
            print(f"   Category: {sample_product.get('category', 'N/A')}")
            print(f"   Price: ${sample_product.get('price', 'N/A')}")
            
            print(f"\n📝 Sample Marketing Script:")
            print(f"   Platform: {sample_script.get('platform', 'N/A')}")
            print(f"   Tone: {sample_script.get('tone', 'N/A')}")
            print(f"   Performance Score: {sample_script.get('performance_score', 'N/A')}")
            
        else:
            print("❌ Data loading may have issues")
            
    except Exception as e:
        print(f"❌ Error checking data quality: {e}")

def create_indexes():
    """Create indexes for better performance"""
    try:
        db.products.create_index("product_id")
        db.products.create_index("category")
        db.products.create_index("brand")
        db.products.create_index("target_audience")
        
        db.scripts.create_index("product_id")
        db.scripts.create_index("platform")
        db.scripts.create_index("tone")
        db.scripts.create_index("content_structure")
        db.scripts.create_index("performance_score")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")

def verify_data_relationships():
    """Verify that marketing scripts link to existing products"""
    try:
        # Get all unique product_ids from marketing scripts
        marketing_product_ids = db.scripts.distinct("product_id")
        
        # Get all product_ids from products
        product_ids = db.products.distinct("product_id")
        
        # Find orphaned marketing scripts (pointing to non-existent products)
        orphaned_scripts = set(marketing_product_ids) - set(product_ids)
        
        print(f"\n🔗 DATA RELATIONSHIP CHECK:")
        print(f"   Unique products in marketing data: {len(marketing_product_ids)}")
        print(f"   Total products: {len(product_ids)}")
        print(f"   Orphaned marketing scripts: {len(orphaned_scripts)}")
        
        if len(orphaned_scripts) == 0:
            print("✅ All marketing scripts have valid product references!")
        else:
            print(f"⚠️  {len(orphaned_scripts)} marketing scripts point to non-existent products")
            
    except Exception as e:
        print(f"❌ Error verifying data relationships: {e}")

def check_file_locations():
    """Check if CSV files are in the correct locations"""
    print("🔍 Checking file locations...")
    
    products_path = os.path.join(DATA_DIR, 'products.csv')
    marketing_path = os.path.join(DATA_DIR, 'marketing_copy.csv')
    
    print(f"📁 Expected products.csv at: {products_path}")
    print(f"📁 Expected marketing_copy.csv at: {marketing_path}")
    
    products_exists = os.path.exists(products_path)
    marketing_exists = os.path.exists(marketing_path)
    
    print(f"   products.csv exists: {products_exists}")
    print(f"   marketing_copy.csv exists: {marketing_exists}")
    
    if not products_exists or not marketing_exists:
        print("\n❌ Missing CSV files! Please ensure:")
        print("   - Both CSV files are in the 'data' folder")
        print("   - The 'data' folder is in the same directory as 'src'")
        print("   - File names are exactly: 'products.csv' and 'marketing_copy.csv'")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting MongoDB Data Loader...")
    
    # First check if files exist
    if not check_file_locations():
        print("❌ Cannot proceed - CSV files not found in correct locations")
        exit(1)
    
    # Clear existing collections
    db.products.drop()
    db.scripts.drop()
    print("🗑️  Cleared existing collections")
    
    # Load new data
    load_products()
    load_marketing_copy()
    
    # Create indexes
    create_indexes()
    
    # Check data quality
    check_data_quality()
    
    # Verify data relationships
    verify_data_relationships()
    
    print("\n🎉 CSV data loaded into MongoDB successfully!")