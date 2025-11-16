import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import spacy
import joblib
from config import Config
from typing import List, Dict, Any, Tuple
import re
from collections import Counter
import json
from datetime import datetime

class AdvancedMarketingRecommender:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        
        # Initialize ML models
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=2000, 
            stop_words='english',
            ngram_range=(1, 3)
        )
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  SpaCy model not found. Using basic preprocessing...")
            self.nlp = None
        
        # Model state
        self.models_trained = False
        self.product_vectors = None
        self.script_vectors = None
        self.product_ids = []
        self.script_data = []
        
        # Pattern learning storage
        self.category_patterns = {}
        self.tone_effectiveness = {}
        self.platform_preferences = {}
        
    def load_training_data(self):
        """Load and prepare data for model training"""
        print("📥 Loading training data...")
        
        # Load products with extracted features
        products = list(self.db.products.find({}))
        
        # Load marketing scripts with performance data
        scripts = list(self.db.scripts.find({}))
        
        if not products:
            raise Exception("No products found in database. Please add products first.")
        
        print(f"✅ Loaded {len(products)} products and {len(scripts)} scripts")
        return products, scripts
    
    def train_product_similarity_model(self):
        """Train model to find similar products"""
        print("🔄 Training product similarity model...")
        
        products, _ = self.load_training_data()
        
        if len(products) < 2:
            print("⚠️  Not enough products for similarity model. Need at least 2 products.")
            # Create dummy data for testing
            self._create_fallback_models()
            return
        
        # Create product feature vectors
        product_texts = []
        self.product_ids = []
        
        for product in products:
            # Combine all product information
            features = " ".join(product.get('extracted_features', []))
            combined_text = f"{product.get('name', '')} {product.get('category', '')} {product.get('description', '')} {features}"
            processed_text = self.preprocess_text(combined_text)
            
            product_texts.append(processed_text)
            self.product_ids.append(str(product['_id']))
        
        # Train TF-IDF and create vectors
        try:
            tfidf_vectors = self.tfidf_vectorizer.fit_transform(product_texts)
            
            # Add sentence embeddings for semantic similarity
            sentence_vectors = self.sentence_model.encode(product_texts)
            
            # Combine features
            tfidf_dense = tfidf_vectors.toarray()
            combined_vectors = np.concatenate([tfidf_dense, sentence_vectors], axis=1)
            
            # Dimensionality reduction
            self.svd = TruncatedSVD(n_components=min(150, len(products)-1), random_state=42)
            self.product_vectors = self.svd.fit_transform(combined_vectors)
            
            print(f"✅ Product similarity model trained on {len(products)} products")
        except Exception as e:
            print(f"❌ Error training similarity model: {e}")
            self._create_fallback_models()
    
    def _create_fallback_models(self):
        """Create fallback models when there's insufficient data"""
        print("🔄 Creating fallback models...")
        
        # Create dummy product vectors for basic functionality
        self.product_vectors = np.random.rand(2, 10)
        self.product_ids = ['dummy_1', 'dummy_2']
        self.svd = TruncatedSVD(n_components=10, random_state=42)
        self.svd.fit(self.product_vectors)
        
        # Create basic TF-IDF vectorizer
        dummy_texts = ["product electronics tech", "fashion clothing style"]
        self.tfidf_vectorizer.fit(dummy_texts)
        
        print("✅ Fallback models created")
    
    def train_marketing_pattern_model(self):
        """Train model to learn successful marketing patterns"""
        print("🎯 Training marketing pattern model...")
        
        products, scripts = self.load_training_data()
        
        # Analyze successful patterns by category
        self.category_patterns = {}
        
        categories = set(p.get('category', 'General') for p in products)
        
        for category in categories:
            # Get scripts for this category
            category_scripts = []
            for script in scripts:
                product_id = script.get('product_id')
                if not product_id:
                    continue
                    
                product = next((p for p in products if str(p['_id']) == str(product_id)), None)
                if product and product.get('category') == category:
                    category_scripts.append(script)
            
            if category_scripts:
                self.analyze_category_patterns(category, category_scripts)
        
        # If no category patterns found, create general patterns
        if not self.category_patterns:
            self.category_patterns = self.get_general_successful_patterns()
        
        print(f"✅ Marketing pattern model trained for {len(self.category_patterns)} categories")
    
    def analyze_category_patterns(self, category: str, scripts: List[Dict]):
        """Analyze successful marketing patterns for a specific category"""
        
        # Tone effectiveness
        tone_scores = {}
        for script in scripts:
            tone = script.get('tone', 'professional')
            score = script.get('performance_score', 6.0)  # Default score
            if tone not in tone_scores:
                tone_scores[tone] = []
            tone_scores[tone].append(score)
        
        # Calculate average performance per tone
        tone_effectiveness = {}
        for tone, scores in tone_scores.items():
            tone_effectiveness[tone] = np.mean(scores)
        
        # Platform preferences
        platform_scores = {}
        for script in scripts:
            platform = script.get('platform', 'Instagram')
            score = script.get('performance_score', 6.0)
            if platform not in platform_scores:
                platform_scores[platform] = []
            platform_scores[platform].append(score)
        
        platform_preferences = {}
        for platform, scores in platform_scores.items():
            platform_preferences[platform] = np.mean(scores)
        
        # Content structure effectiveness
        structure_scores = {}
        for script in scripts:
            structure = script.get('content_structure', 'feature-benefit')
            score = script.get('performance_score', 6.0)
            if structure not in structure_scores:
                structure_scores[structure] = []
            structure_scores[structure].append(score)
        
        structure_effectiveness = {}
        for structure, scores in structure_scores.items():
            structure_effectiveness[structure] = np.mean(scores)
        
        # Successful keywords
        all_keywords = []
        for script in scripts:
            if script.get('performance_score', 0) >= 6.0:  # Medium-performing scripts
                keywords = script.get('keywords', [])
                if isinstance(keywords, list):
                    all_keywords.extend(keywords)
        
        keyword_counts = Counter(all_keywords)
        top_keywords = [kw for kw, count in keyword_counts.most_common(10)]
        
        # Store patterns
        self.category_patterns[category] = {
            'top_keywords': top_keywords,
            'structure_effectiveness': structure_effectiveness,
            'best_tones': dict(sorted(tone_effectiveness.items(), key=lambda x: x[1], reverse=True)[:3]),
            'best_platforms': dict(sorted(platform_preferences.items(), key=lambda x: x[1], reverse=True)[:3])
        }
    
    def train_models(self):
        """Train all ML models"""
        print("🚀 Training complete recommendation system...")
        
        try:
            self.train_product_similarity_model()
            self.train_marketing_pattern_model()
            self.models_trained = True
            print("✅ All models trained successfully!")
            return True
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            # Even if training fails, mark as trained with fallback models
            self.models_trained = True
            return False
    
    def find_similar_products(self, input_product: Dict[str, Any], top_n: int = 5) -> List[Dict]:
        """Find similar products using advanced ML similarity"""
        if not self.models_trained:
            success = self.train_models()
            if not success:
                return self._get_fallback_similar_products(input_product, top_n)
        
        # Prepare input product vector
        input_features = " ".join(input_product.get('extracted_features', []))
        input_text = f"{input_product['name']} {input_product['category']} {input_product['description']} {input_features}"
        processed_input = self.preprocess_text(input_text)
        
        try:
            # Transform input
            tfidf_vector = self.tfidf_vectorizer.transform([processed_input])
            sentence_vector = self.sentence_model.encode([processed_input])
            
            # Combine and reduce dimensions
            tfidf_dense = tfidf_vector.toarray()
            combined_input = np.concatenate([tfidf_dense, sentence_vector], axis=1)
            input_reduced = self.svd.transform(combined_input)
            
            # Calculate similarities
            similarities = cosine_similarity(input_reduced, self.product_vectors).flatten()
            
            # Get top similar products
            top_indices = similarities.argsort()[-top_n:][::-1]
            
            similar_products = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Lower similarity threshold
                    product_id = self.product_ids[idx]
                    
                    # Skip dummy products
                    if product_id.startswith('dummy_'):
                        continue
                        
                    # Get original product data
                    original_product = self.db.products.find_one({"_id": product_id})
                    if original_product:
                        # Get marketing performance for this product
                        marketing_stats = self.get_product_marketing_stats(product_id)
                        
                        similar_products.append({
                            'product': original_product,
                            'similarity': float(similarities[idx]),
                            'marketing_stats': marketing_stats,
                            'shared_features': self.find_shared_features(input_product, original_product)
                        })
            
            return similar_products[:top_n]
        except Exception as e:
            print(f"❌ Error finding similar products: {e}")
            return self._get_fallback_similar_products(input_product, top_n)
    
    def _get_fallback_similar_products(self, input_product: Dict, top_n: int) -> List[Dict]:
        """Fallback method when ML models fail"""
        print("🔄 Using fallback similar products method...")
        
        # Get some random products from the database as fallback
        products = list(self.db.products.find({
            "category": input_product['category']
        }).limit(top_n))
        
        similar_products = []
        for product in products:
            if str(product['_id']) != str(input_product.get('_id', '')):
                similar_products.append({
                    'product': product,
                    'similarity': 0.7,  # Default similarity
                    'marketing_stats': self.get_product_marketing_stats(str(product['_id'])),
                    'shared_features': [input_product['category']]
                })
        
        return similar_products[:top_n]
    
    def get_product_marketing_stats(self, product_id: str) -> Dict:
        """Get marketing performance statistics for a product"""
        scripts = list(self.db.scripts.find({"product_id": product_id}))
        
        if not scripts:
            return {
                "avg_performance": 6.0, 
                "best_platform": "Instagram", 
                "script_count": 0,
                "top_performing_script": None
            }
        
        performances = [s.get('performance_score', 6.0) for s in scripts]
        platforms = [s.get('platform', 'Instagram') for s in scripts]
        
        # Find best performing platform
        platform_scores = {}
        for script in scripts:
            platform = script.get('platform', 'Instagram')
            score = script.get('performance_score', 6.0)
            if platform not in platform_scores:
                platform_scores[platform] = []
            platform_scores[platform].append(score)
        
        best_platform = max(platform_scores.items(), key=lambda x: np.mean(x[1]))[0] if platform_scores else "Instagram"
        
        return {
            "avg_performance": float(np.mean(performances)),
            "best_platform": best_platform,
            "script_count": len(scripts),
            "top_performing_script": max(scripts, key=lambda x: x.get('performance_score', 0)) if scripts else None
        }

    def find_shared_features(self, product1: Dict, product2: Dict) -> List[str]:
        """Find shared features between two products"""
        features1 = set(product1.get('extracted_features', []))
        features2 = set(product2.get('extracted_features', []))
        
        shared = list(features1.intersection(features2))
        return shared[:5]  # Return top 5 shared features

    def get_recommended_marketing_strategy(self, input_product: Dict, similar_products: List[Dict]) -> Dict:
        """Generate data-driven marketing recommendations based on learned patterns"""
        
        category = input_product['category']
        
        # Get category-specific patterns
        category_pattern = self.category_patterns.get(category, {})
        
        # If no specific patterns for this category, use general successful patterns
        if not category_pattern:
            category_pattern = self.get_general_successful_patterns()
        
        # Analyze similar products' successful marketing
        similar_strategies = self.analyze_similar_products_strategies(similar_products)
        
        # Combine category patterns with similar product insights
        recommendations = {
            'recommended_tones': self.get_recommended_tones(category_pattern, similar_strategies),
            'recommended_platforms': self.get_recommended_platforms(category_pattern, similar_strategies),
            'recommended_structures': self.get_recommended_structures(category_pattern, similar_strategies),
            'successful_keywords': self.get_recommended_keywords(input_product, category_pattern, similar_strategies),
            'cta_recommendations': self.get_cta_recommendations(category),
            'content_guidelines': self.get_content_guidelines(category, input_product)
        }
        
        return recommendations

    def analyze_similar_products_strategies(self, similar_products: List[Dict]) -> Dict:
        """Analyze what worked for similar products"""
        
        strategies = {
            'successful_tones': [],
            'successful_platforms': [],
            'successful_structures': [],
            'high_performing_keywords': []
        }
        
        for sp in similar_products:
            stats = sp.get('marketing_stats', {})
            if stats.get('avg_performance', 0) >= 7.0:  # Only consider successful ones
                top_script = stats.get('top_performing_script')
                if top_script:
                    strategies['successful_tones'].append(top_script.get('tone'))
                    strategies['successful_platforms'].append(top_script.get('platform'))
                    strategies['successful_structures'].append(top_script.get('content_structure'))
                    
                    keywords = top_script.get('keywords', [])
                    if isinstance(keywords, list):
                        strategies['high_performing_keywords'].extend(keywords)
        
        # Get most common successful elements
        strategies['best_tones'] = [tone for tone, count in Counter(strategies['successful_tones']).most_common(3) if tone]
        strategies['best_platforms'] = [platform for platform, count in Counter(strategies['successful_platforms']).most_common(3) if platform]
        strategies['best_structures'] = [struct for struct, count in Counter(strategies['successful_structures']).most_common(2) if struct]
        strategies['top_keywords'] = [kw for kw, count in Counter(strategies['high_performing_keywords']).most_common(15) if kw]
        
        return strategies

    def get_recommended_tones(self, category_pattern: Dict, similar_strategies: Dict) -> List[str]:
        """Get recommended tones based on learned patterns"""
        tones = []
        
        # Add tones from category patterns
        tones.extend(list(category_pattern.get('best_tones', {}).keys()))
        
        # Add tones from similar successful products
        tones.extend(similar_strategies.get('best_tones', []))
        
        # Remove duplicates and return top 3
        unique_tones = list(dict.fromkeys(tones))
        return unique_tones[:3] if unique_tones else ['professional', 'friendly', 'energetic']

    def get_recommended_platforms(self, category_pattern: Dict, similar_strategies: Dict) -> List[str]:
        """Get recommended platforms based on learned patterns"""
        platforms = []
        
        # Add platforms from category patterns
        platforms.extend(list(category_pattern.get('best_platforms', {}).keys()))
        
        # Add platforms from similar successful products
        platforms.extend(similar_strategies.get('best_platforms', []))
        
        # Remove duplicates and return top 3
        unique_platforms = list(dict.fromkeys(platforms))
        return unique_platforms[:3] if unique_platforms else ['Instagram', 'YouTube', 'Facebook']

    def get_recommended_structures(self, category_pattern: Dict, similar_strategies: Dict) -> List[str]:
        """Get recommended content structures"""
        structures = []
        
        # Add structures from category patterns
        structures.extend(list(category_pattern.get('structure_effectiveness', {}).keys()))
        
        # Add structures from similar successful products
        structures.extend(similar_strategies.get('best_structures', []))
        
        # Remove duplicates and return top 2
        unique_structures = list(dict.fromkeys(structures))
        return unique_structures[:2] if unique_structures else ['feature-benefit', 'problem-solution']

    def get_recommended_keywords(self, input_product: Dict, category_pattern: Dict, similar_strategies: Dict) -> List[str]:
        """Get recommended keywords combining product features and successful patterns"""
        keywords = []
        
        # Add product-specific features
        keywords.extend(input_product.get('extracted_features', [])[:10])
        
        # Add category-specific successful keywords
        keywords.extend(category_pattern.get('top_keywords', [])[:10])
        
        # Add keywords from similar successful products
        keywords.extend(similar_strategies.get('top_keywords', [])[:10])
        
        # Remove duplicates and return most relevant
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:15] if unique_keywords else ['quality', 'premium', 'innovative']

    def get_cta_recommendations(self, category: str) -> List[str]:
        """Get call-to-action recommendations based on category"""
        cta_library = {
            'Electronics': [
                "Upgrade your tech today!",
                "Experience cutting-edge technology!",
                "Shop the latest innovation!",
                "Get yours before it's gone!"
            ],
            'Home & Kitchen': [
                "Transform your home today!",
                "Shop now for limited time offer!",
                "Create your dream space!",
                "Limited stock available!"
            ],
            'Fashion': [
                "Elevate your style!",
                "Shop the new collection!",
                "Limited edition - get yours!",
                "Express your unique style!"
            ],
            'Beauty & Personal Care': [
                "Discover your glow!",
                "Shop self-care essentials!",
                "Limited time beauty offer!",
                "Transform your routine!"
            ],
            'Sports & Outdoors': [
                "Elevate your performance!",
                "Gear up for adventure!",
                "Limited edition gear!",
                "Train like a pro!"
            ]
        }
        
        return cta_library.get(category, [
            "Shop now!",
            "Limited time offer!",
            "Get yours today!",
            "Don't miss out!"
        ])

    def get_content_guidelines(self, category: str, product: Dict) -> Dict:
        """Get content creation guidelines based on category and product type"""
        
        guidelines = {
            'focus_points': [],
            'emotional_appeals': [],
            'technical_depth': 'medium',
            'storytelling_elements': []
        }
        
        if category == 'Electronics':
            guidelines['focus_points'] = ['specifications', 'innovation', 'performance', 'compatibility']
            guidelines['emotional_appeals'] = ['excitement', 'curiosity', 'fear of missing out']
            guidelines['technical_depth'] = 'high'
            guidelines['storytelling_elements'] = ['problem-solution', 'tech evolution', 'user experience']
        
        elif category == 'Fashion':
            guidelines['focus_points'] = ['style', 'comfort', 'versatility', 'trends']
            guidelines['emotional_appeals'] = ['confidence', 'self-expression', 'belonging']
            guidelines['technical_depth'] = 'low'
            guidelines['storytelling_elements'] = ['lifestyle', 'personal transformation', 'occasion-based']
        
        elif category == 'Beauty & Personal Care':
            guidelines['focus_points'] = ['ingredients', 'results', 'safety', 'routine integration']
            guidelines['emotional_appeals'] = ['self-care', 'confidence', 'transformation']
            guidelines['technical_depth'] = 'medium'
            guidelines['storytelling_elements'] = ['before-after', 'scientific backing', 'user testimonials']
        
        # Add product-specific focus points
        price = product.get('price', 0)
        if price > 200:
            guidelines['focus_points'].append('premium quality')
            guidelines['emotional_appeals'].append('exclusivity')
        else:
            guidelines['focus_points'].append('value for money')
            guidelines['emotional_appeals'].append('smart choice')
        
        return guidelines

    def get_general_successful_patterns(self) -> Dict:
        """Get general successful patterns when category-specific data is insufficient"""
        return {
            'top_keywords': ['quality', 'premium', 'innovative', 'reliable', 'exclusive', 'best', 'new', 'popular'],
            'structure_effectiveness': {'problem-solution': 7.5, 'feature-benefit': 7.2, 'story-based': 6.8},
            'best_tones': {'professional': 7.8, 'friendly': 7.5, 'energetic': 7.3},
            'best_platforms': {'Instagram': 7.6, 'YouTube': 7.4, 'Facebook': 7.1}
        }

    def preprocess_text(self, text: str) -> str:
        """Advanced text preprocessing"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep words and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text


class IntelligentScriptGenerator:
    def __init__(self, recommender: AdvancedMarketingRecommender):
        self.recommender = recommender
    
    def generate_comprehensive_marketing_package(self, input_product: Dict, similar_products: List[Dict]) -> Dict:
        """Generate complete marketing package using learned patterns"""
        
        # Get data-driven recommendations
        recommendations = self.recommender.get_recommended_marketing_strategy(input_product, similar_products)
        
        # Generate scripts for each recommended platform
        marketing_package = {
            'strategy_overview': self.generate_strategy_overview(recommendations),
            'platform_specific_content': {},
            'performance_predictions': self.predict_performance(input_product, recommendations),
            'implementation_guidelines': self.generate_implementation_guidelines(recommendations)
        }
        
        # Generate content for each recommended platform
        for platform in recommendations['recommended_platforms'][:2]:  # Top 2 platforms
            marketing_package['platform_specific_content'][platform] = self.generate_platform_content(
                platform, input_product, recommendations
            )
        
        return marketing_package
    
    def generate_strategy_overview(self, recommendations: Dict) -> Dict:
        """Generate overall marketing strategy"""
        return {
            'core_message': f"Focus on {', '.join(recommendations['content_guidelines']['focus_points'][:2])}",
            'target_tones': recommendations['recommended_tones'],
            'key_value_propositions': self.generate_value_propositions(recommendations),
            'success_metrics': ['engagement_rate', 'conversion_rate', 'brand_recall']
        }
    
    def generate_value_propositions(self, recommendations: Dict) -> List[str]:
        """Generate compelling value propositions"""
        value_props = []
        
        guidelines = recommendations['content_guidelines']
        
        for appeal in guidelines['emotional_appeals'][:2]:
            if appeal == 'confidence':
                value_props.append("Boost your confidence with premium quality")
            elif appeal == 'innovation':
                value_props.append("Experience cutting-edge innovation")
            elif appeal == 'value':
                value_props.append("Exceptional quality at an unbeatable value")
            else:
                value_props.append(f"Transform your experience with {appeal}")
        
        return value_props
    
    def generate_platform_content(self, platform: str, product: Dict, recommendations: Dict) -> Dict:
        """Generate platform-specific marketing content"""
        
        if platform == 'YouTube':
            return self.generate_youtube_script(product, recommendations)
        elif platform == 'Instagram':
            return self.generate_instagram_content(product, recommendations)
        elif platform == 'Facebook':
            return self.generate_facebook_content(product, recommendations)
        elif platform == 'TikTok':
            return self.generate_tiktok_content(product, recommendations)
        else:  # Email
            return self.generate_email_content(product, recommendations)
    
    def generate_youtube_script(self, product: Dict, recommendations: Dict) -> Dict:
        """Generate YouTube video script"""
        
        tone = recommendations['recommended_tones'][0]
        structure = recommendations['recommended_structures'][0]
        
        script = {
            'video_title': f"Review: {product['name']} - Is It Worth It?",
            'thumbnail_ideas': [
                f"Before/After using {product['name']}",
                f"Shocking results with {product['name']}",
                f"{product['name']} - Honest Review"
            ],
            'script_structure': self.get_video_structure(structure, product, recommendations),
            'cta': recommendations['cta_recommendations'][0],
            'hashtags': self.generate_hashtags(product, recommendations)
        }
        
        return script
    
    def generate_instagram_content(self, product: Dict, recommendations: Dict) -> Dict:
        """Generate Instagram marketing content"""
        
        return {
            'caption_templates': [
                self.generate_instagram_caption(product, recommendations, 'carousel'),
                self.generate_instagram_caption(product, recommendations, 'single_post'),
                self.generate_instagram_caption(product, recommendations, 'story')
            ],
            'visual_elements': [
                "Lifestyle product shots",
                "Feature close-ups", 
                "User testimonials",
                "Before/after comparisons"
            ],
            'hashtag_strategy': {
                'primary': [f"#{product['name'].replace(' ', '')}", f"#{product['category'].replace(' ', '')}"],
                'secondary': ['#innovation', '#quality', '#musthave'],
                'trending': ['#tech', '#lifestyle', '#premium']
            },
            'engagement_ideas': [
                "Ask followers about their experience",
                "Run a giveaway with product features",
                "Create a poll about favorite features"
            ]
        }
    
    def generate_instagram_caption(self, product: Dict, recommendations: Dict, post_type: str) -> str:
        """Generate Instagram caption based on post type"""
        
        if post_type == 'carousel':
            return f"""✨ Meet your new favorite {product['category']}! 

Introducing {product['name']} - designed to revolutionize your routine! 

Swipe through to see:
👉 Premium {recommendations['successful_keywords'][0]} features
👉 Real user transformations  
👉 Exclusive limited-time offer

{recommendations['cta_recommendations'][0]}

{' '.join(self.generate_hashtags(product, recommendations))}"""
        
        elif post_type == 'single_post':
            return f"""🚀 JUST LAUNCHED: {product['name']}

This isn't just another {product['category']} - it's a game-changer! 

What makes it special?
⭐ {recommendations['successful_keywords'][0].title()}
⭐ {recommendations['successful_keywords'][1].title()} 
⭐ {recommendations['successful_keywords'][2].title()}

{recommendations['cta_recommendations'][1]}

{' '.join(self.generate_hashtags(product, recommendations))}"""
        
        else:  # story
            return f"""Swipe up! 👆 

{product['name']} is changing everything! 

{recommendations['cta_recommendations'][2]}"""
    
    def get_video_structure(self, structure: str, product: Dict, recommendations: Dict) -> List[str]:
        """Get video script structure based on content structure"""
        
        if structure == 'problem-solution':
            return [
                "Hook: Present common problem",
                "Agitate: Show pain points", 
                "Solution: Introduce product",
                "Demo: Show product solving problem",
                "Results: Display benefits",
                "CTA: Call to action"
            ]
        elif structure == 'feature-benefit':
            return [
                "Hook: Attention-grabbing feature",
                "Feature 1: Showcase + benefit",
                "Feature 2: Showcase + benefit", 
                "Feature 3: Showcase + benefit",
                "Lifestyle integration",
                "CTA: Limited offer"
            ]
        else:  # story-based
            return [
                "Character introduction", 
                "Challenge faced",
                "Discovery moment",
                "Transformation journey",
                "Results and benefits",
                "CTA: Join the story"
            ]
    
    def generate_hashtags(self, product: Dict, recommendations: Dict) -> List[str]:
        """Generate relevant hashtags"""
        hashtags = [
            f"#{product['name'].replace(' ', '')}",
            f"#{product['category'].replace(' ', '')}",
            f"#{product['brand'].replace(' ', '')}" if product.get('brand') else "#premium"
        ]
        
        # Add successful keywords as hashtags
        for keyword in recommendations['successful_keywords'][:3]:
            hashtags.append(f"#{keyword.replace(' ', '')}")
        
        return hashtags[:10]
    
    def predict_performance(self, product: Dict, recommendations: Dict) -> Dict:
        """Predict marketing performance based on patterns"""
        
        # Simple prediction based on category patterns and product features
        base_score = 6.0
        
        # Adjust based on category performance
        category = product['category']
        category_pattern = self.recommender.category_patterns.get(category, {})
        if category_pattern:
            avg_tone_score = np.mean(list(category_pattern.get('best_tones', {}).values()))
            base_score += (avg_tone_score - 7.0) * 0.1
        
        # Adjust based on product features
        feature_count = len(product.get('extracted_features', []))
        if feature_count > 10:
            base_score += 0.5
        
        price = product.get('price', 0)
        if 50 <= price <= 200:  # Sweet spot for impulse purchases
            base_score += 0.3
        
        return {
            'predicted_engagement': round(base_score, 1),
            'confidence_level': 'medium',
            'key_success_factors': [
                f"Strong {recommendations['recommended_tones'][0]} tone",
                f"Focus on {recommendations['successful_keywords'][0]}",
                f"{recommendations['recommended_platforms'][0]} optimization"
            ]
        }
    
    def generate_implementation_guidelines(self, recommendations: Dict) -> Dict:
        """Generate practical implementation guidelines"""
        return {
            'content_calendar': {
                'week_1': ['Platform setup', 'Content creation', 'Community engagement'],
                'week_2': ['Performance analysis', 'Content optimization', 'Audience building'],
                'week_3': ['Scale successful content', 'Explore new platforms', 'Partnership outreach']
            },
            'performance_tracking': [
                'Engagement rate per platform',
                'Conversion rate from CTAs', 
                'Audience growth rate',
                'Content shareability'
            ],
            'optimization_tips': [
                'A/B test different tones weekly',
                'Monitor competitor strategies',
                'Engage with user comments promptly',
                'Update content based on performance data'
            ]
        }


# Backward compatibility wrapper
class MarketingScriptRecommender:
    """Legacy wrapper for backward compatibility"""
    
    def __init__(self):
        self.advanced_recommender = AdvancedMarketingRecommender()
        self.script_generator = IntelligentScriptGenerator(self.advanced_recommender)
    
    def find_similar_products(self, input_product, top_n=5):
        return self.advanced_recommender.find_similar_products(input_product, top_n)
    
    def generate_marketing_script(self, input_product, similar_products):
        package = self.script_generator.generate_comprehensive_marketing_package(input_product, similar_products)
        return self.format_legacy_output(package)
    
    def generate_social_media_post(self, input_product):
        # Simple fallback for legacy compatibility
        return "📱 Social media content will be generated based on platform-specific recommendations."
    
    def format_legacy_output(self, marketing_package):
        """Format the advanced output for legacy compatibility"""
        
        strategy = marketing_package['strategy_overview']
        platform_content = marketing_package['platform_specific_content']
        
        output = []
        output.append("🎯 **AI-GENERATED MARKETING STRATEGY**")
        output.append("=" * 50)
        output.append(f"Core Message: {strategy['core_message']}")
        output.append(f"Recommended Tones: {', '.join(strategy['target_tones'])}")
        output.append("")
        
        for platform, content in platform_content.items():
            output.append(f"📱 **{platform.upper()} CONTENT**")
            output.append("-" * 30)
            
            if platform == 'Instagram':
                for template in content['caption_templates']:
                    output.append(f"Caption: {template}")
            elif platform == 'YouTube':
                output.append(f"Video Title: {content['video_title']}")
                output.append("Script Structure:")
                for i, step in enumerate(content['script_structure'], 1):
                    output.append(f"  {i}. {step}")
            
            output.append("")
        
        return "\n".join(output)