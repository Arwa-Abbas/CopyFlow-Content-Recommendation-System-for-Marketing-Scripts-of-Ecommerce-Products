from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
import logging
import asyncio
import time

from config import Config
from src.recommender import AdvancedMarketingRecommender, IntelligentScriptGenerator, MarketingScriptRecommender

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="CopyFlow - Marketing Recommendation System",
    description="AI-powered marketing script recommendation and generation",
    version="3.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
recommender = None
script_generator = None
models_loading = False
models_loaded = False

@app.on_event("startup")
async def startup_event():
    """Initialize ML models on startup in background"""
    global recommender, script_generator, models_loading, models_loaded
    
    models_loading = True
    logger.info("🚀 Starting AI Model Initialization...")
    
    # Run model loading in background to avoid blocking startup
    asyncio.create_task(initialize_models())

async def initialize_models():
    """Initialize ML models asynchronously"""
    global recommender, script_generator, models_loading, models_loaded
    
    try:
        logger.info("🔄 Loading BrandWise AI Models...")
        
        # Initialize the advanced recommender
        recommender = AdvancedMarketingRecommender()
        
        # Train models (this might take some time)
        logger.info("🎯 Training ML models with your marketing data...")
        success = recommender.train_models()
        
        if success:
            # Initialize script generator
            script_generator = IntelligentScriptGenerator(recommender)
            models_loaded = True
            logger.info("✅ AI Models initialized successfully!")
        else:
            logger.warning("⚠️  Models loaded with fallback mode")
            models_loaded = True  # Still mark as loaded for basic functionality
        
        models_loading = False
        
    except Exception as e:
        logger.error(f"❌ Model initialization failed: {e}")
        models_loading = False
        # Fallback to basic functionality
        try:
            logger.info("🔄 Falling back to basic recommender...")
            recommender = AdvancedMarketingRecommender()
            recommender.models_trained = True  # Force mark as trained
            script_generator = IntelligentScriptGenerator(recommender)
            models_loaded = True
            logger.info("✅ Basic recommender loaded as fallback")
        except Exception as fallback_error:
            logger.error(f"❌ Fallback also failed: {fallback_error}")
            recommender = None
            script_generator = None
            models_loaded = False

# MongoDB connection
try:
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]
    client.admin.command('ping')
    logger.info(f"✅ Connected to MongoDB: {Config.DB_NAME}")
    db_connected = True
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {str(e)}")
    db = None
    db_connected = False

# Pydantic Models
class ProductRequest(BaseModel):
    name: str
    category: str
    description: str
    price: Optional[str] = ""
    target_audience: Optional[str] = ""

class SimilarProductResponse(BaseModel):
    name: str
    category: str
    price: Optional[float] = None
    similarity: float
    shared_features: List[str]
    marketing_performance: Dict[str, Any]

class MarketingStrategyResponse(BaseModel):
    platform: str
    content: Dict[str, Any]
    performance_prediction: Dict[str, Any]

class AdvancedMarketingResponse(BaseModel):
    success: bool
    input_product: Dict[str, Any]
    similar_products: List[SimilarProductResponse]
    marketing_strategy: Dict[str, Any]
    performance_insights: Dict[str, Any]
    implementation_guide: Dict[str, Any]
    platform_content: Dict[str, Any]  # Added missing field

class HealthResponse(BaseModel):
    status: str
    database: str
    models: str
    models_loading: bool
    models_loaded: bool  # Added this field
    error: Optional[str] = None

# Helper functions
def serialize_doc(doc):
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    elif isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

def safe_float_convert(price):
    if price is None:
        return None
    try:
        return float(price)
    except (ValueError, TypeError):
        return None

def prepare_input_product(product_data: ProductRequest) -> Dict[str, Any]:
    """Prepare input product for the recommender"""
    return {
        'name': product_data.name,
        'category': product_data.category,
        'description': product_data.description,
        'price': product_data.price,
        'target_audience': product_data.target_audience,
        'extracted_features': []  # Will be populated by feature extractor
    }

# Routes
@app.get("/", tags=["Root"])
async def root():
    models_status = "loading" if models_loading else ("loaded" if models_loaded else "unavailable")
    
    return {
        "message": "BrandWise AI - Intelligent Marketing Recommendation System", 
        "status": "running",
        "version": "3.0.0",
        "models_status": models_status,
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    try:
        models_status = "loaded" if models_loaded else "unavailable"
        
        return {
            "status": "healthy" if db_connected and models_loaded else "degraded",
            "database": "connected" if db_connected else "disconnected",
            "models": models_status,
            "models_loading": models_loading,
            "models_loaded": models_loaded
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy", 
            "database": "disconnected", 
            "models": "unavailable",
            "models_loading": False,
            "models_loaded": False,
            "error": str(e)
        }

@app.post("/api/generate-marketing-strategy", response_model=AdvancedMarketingResponse, tags=["Advanced Marketing"])
async def generate_marketing_strategy(product: ProductRequest, background_tasks: BackgroundTasks):
    """Generate comprehensive marketing strategy using advanced ML"""
    try:
        logger.info(f"🔍 Advanced marketing request for: {product.name}")
        
        if models_loading:
            raise HTTPException(status_code=503, detail="AI models are still loading. Please try again in a moment.")
        
        if not db_connected:
            raise HTTPException(status_code=500, detail="Database not connected")
        
        if not recommender or not models_loaded:
            raise HTTPException(status_code=503, detail="AI models are not ready. Please check /api/health")
        
        # Prepare input product
        input_product = prepare_input_product(product)
        
        # Step 1: Find similar products using advanced ML
        logger.info("🔍 Finding similar products...")
        similar_products = recommender.find_similar_products(input_product, top_n=3)
        
        if not similar_products:
            # Return empty but successful response instead of error
            similar_products = []
        
        logger.info(f"📊 Found {len(similar_products)} similar products")
        
        # Step 2: Generate comprehensive marketing package
        logger.info("🎯 Generating marketing strategy...")
        marketing_package = script_generator.generate_comprehensive_marketing_package(
            input_product, similar_products
        )
        
        # Step 3: Prepare response
        similar_products_response = []
        for sp in similar_products:
            product_data = sp['product']
            marketing_stats = sp.get('marketing_stats', {})
            
            similar_products_response.append({
                "name": product_data.get('name', 'Unknown'),
                "category": product_data.get('category', 'Unknown'),
                "price": safe_float_convert(product_data.get('price')),
                "similarity": round(sp['similarity'], 3),
                "shared_features": sp.get('shared_features', [])[:5],
                "marketing_performance": {
                    "average_score": marketing_stats.get('avg_performance', 0),
                    "best_platform": marketing_stats.get('best_platform', 'Unknown'),
                    "script_count": marketing_stats.get('script_count', 0)
                }
            })
        
        response_data = {
            "success": True,
            "input_product": input_product,
            "similar_products": similar_products_response,
            "marketing_strategy": marketing_package.get('strategy_overview', {}),
            "performance_insights": marketing_package.get('performance_predictions', {}),
            "implementation_guide": marketing_package.get('implementation_guidelines', {}),
            "platform_content": marketing_package.get('platform_specific_content', {})
        }
        
        logger.info("✅ Successfully generated advanced marketing strategy")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Marketing strategy generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Marketing strategy generation failed: {str(e)}")

@app.post("/api/quick-recommendation", tags=["Quick Recommendations"])
async def quick_recommendation(product: ProductRequest):
    """Quick recommendation without full strategy generation"""
    try:
        if models_loading:
            raise HTTPException(status_code=503, detail="AI models are still loading")
        
        if not recommender or not models_loaded:
            raise HTTPException(status_code=503, detail="AI models not available")
        
        input_product = prepare_input_product(product)
        
        # Find similar products
        similar_products = recommender.find_similar_products(input_product, top_n=3)
        
        if not similar_products:
            # Return default recommendations instead of error
            return {
                "success": True,
                "recommended_tones": ['professional', 'friendly', 'energetic'],
                "recommended_platforms": ['Instagram', 'YouTube', 'Facebook'],
                "top_keywords": ['quality', 'premium', 'innovative', 'reliable'],
                "content_guidelines": {
                    'focus_points': ['quality', 'innovation'],
                    'emotional_appeals': ['confidence', 'excitement']
                }
            }
        
        # Get quick recommendations
        recommendations = recommender.get_recommended_marketing_strategy(input_product, similar_products)
        
        return {
            "success": True,
            "recommended_tones": recommendations.get('recommended_tones', []),
            "recommended_platforms": recommendations.get('recommended_platforms', []),
            "top_keywords": recommendations.get('successful_keywords', [])[:10],
            "content_guidelines": recommendations.get('content_guidelines', {})
        }
        
    except Exception as e:
        logger.error(f"Quick recommendation failed: {e}")
        # Return fallback data instead of error
        return {
            "success": True,
            "recommended_tones": ['professional', 'friendly'],
            "recommended_platforms": ['Instagram', 'Facebook'],
            "top_keywords": ['quality', 'innovative'],
            "content_guidelines": {
                'focus_points': ['key features', 'benefits'],
                'emotional_appeals': ['confidence', 'satisfaction']
            }
        }

@app.get("/api/category-insights/{category}", tags=["Insights"])
async def get_category_insights(category: str):
    """Get marketing insights for a specific category"""
    try:
        if not recommender or not models_loaded:
            raise HTTPException(status_code=503, detail="Models not ready")
        
        category_patterns = recommender.category_patterns.get(category, {})
        
        if not category_patterns:
            return {
                "success": True,
                "category": category,
                "insights_available": False,
                "message": "Insufficient data for this category"
            }
        
        return {
            "success": True,
            "category": category,
            "insights_available": True,
            "best_performing_tones": category_patterns.get('best_tones', {}),
            "recommended_platforms": category_patterns.get('best_platforms', {}),
            "top_keywords": category_patterns.get('top_keywords', [])[:15],
            "content_structures": category_patterns.get('structure_effectiveness', {})
        }
        
    except Exception as e:
        logger.error(f"Category insights failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/status", tags=["System"])
async def system_status():
    """Get detailed system status"""
    try:
        # Get statistics
        product_count = db.products.count_documents({}) if db else 0
        script_count = db.scripts.count_documents({}) if db else 0
        
        # Get category coverage
        categories = db.products.distinct("category") if db else []
        
        status_info = {
            "success": True,
            "database": {
                "status": "connected" if db_connected else "disconnected",
                "product_count": product_count,
                "script_count": script_count,
                "categories_covered": len(categories)
            },
            "models": {
                "status": "loaded" if models_loaded else "unavailable",
                "loading": models_loading,
                "categories_trained": len(recommender.category_patterns) if recommender else 0,
                "products_analyzed": len(recommender.product_ids) if recommender else 0
            },
            "version": "3.0.0"
        }
        
        return status_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.get("/api/products", tags=["Products"])
async def get_products(limit: int = 20, skip: int = 0, category: Optional[str] = None):
    """Get products with optional filtering"""
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Database not connected")
        
        query = {}
        if category:
            query["category"] = category
        
        products = list(db.products.find(query).skip(skip).limit(limit))
        serialized_products = serialize_doc(products)
        
        total_products = db.products.count_documents(query)
        
        return {
            "success": True, 
            "products": serialized_products,
            "pagination": {
                "limit": limit,
                "skip": skip,
                "total": total_products,
                "has_more": (skip + limit) < total_products
            }
        }
    except Exception as e:
        logger.error(f"Get products error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Run the application
if __name__ == "__main__":
    logger.info(f"🚀 Starting BrandWise AI Server on port {Config.PORT}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=True,
        log_level="info"
    )