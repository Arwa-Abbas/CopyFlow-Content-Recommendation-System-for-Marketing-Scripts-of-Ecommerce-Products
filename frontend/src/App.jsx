import React, { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, Zap, Target, Share2, MessageCircle, BarChart3, ArrowRight, Check, X, Loader2, Box, ShoppingBag, Smartphone, Coffee, Laptop, Watch, Headphones, Camera, Heart, Star, Award, Rocket } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

// Floating 3D Product Icons Component
const FloatingIcons = () => {
  const icons = [
    { Icon: Box, delay: 0, x: '10%', y: '20%', color: 'text-pink-400' },
    { Icon: ShoppingBag, delay: 0.5, x: '80%', y: '15%', color: 'text-purple-400' },
    { Icon: Smartphone, delay: 1, x: '15%', y: '70%', color: 'text-pink-500' },
    { Icon: Coffee, delay: 1.5, x: '85%', y: '65%', color: 'text-purple-500' },
    { Icon: Laptop, delay: 2, x: '50%', y: '10%', color: 'text-pink-300' },
    { Icon: Watch, delay: 2.5, x: '90%', y: '40%', color: 'text-purple-300' },
    { Icon: Headphones, delay: 3, x: '5%', y: '45%', color: 'text-pink-600' },
    { Icon: Camera, delay: 3.5, x: '70%', y: '85%', color: 'text-purple-600' }
  ];

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {icons.map(({ Icon, delay, x, y, color }, idx) => (
        <div
          key={idx}
          className={`absolute ${color}`}
          style={{
            left: x,
            top: y,
            animation: `float 6s ease-in-out infinite`,
            animationDelay: `${delay}s`,
            opacity: 0.05
          }}
        >
          <Icon className="w-16 h-16" />
        </div>
      ))}
    </div>
  );
};

// Animated Stars Background
const AnimatedStars = () => {
  return (
    <div className="fixed inset-0 pointer-events-none">
      {[...Array(50)].map((_, i) => (
        <div
          key={i}
          className="absolute w-1 h-1 bg-pink-400 rounded-full"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animation: `twinkle ${2 + Math.random() * 3}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 2}s`,
            opacity: 0.3
          }}
        />
      ))}
    </div>
  );
};

// Loading Screen Component
const LoadingScreen = ({ progress }) => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-purple-900 to-black flex items-center justify-center z-50">
      <div className="text-center">
        <div className="relative mb-8">
          <div className="w-32 h-32 bg-gradient-to-br from-pink-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto relative overflow-hidden">
            <Sparkles className="w-16 h-16 text-white relative z-10" style={{ animation: 'spin 3s linear infinite' }} />
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30" style={{ animation: 'shimmer 2s linear infinite' }}></div>
          </div>
          <div className="absolute -inset-4 bg-pink-500/20 rounded-3xl blur-xl" style={{ animation: 'pulse 2s ease-in-out infinite' }}></div>
        </div>
        
        <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
          Initializing CopyFlow AI
        </h2>
        
        <div className="w-64 h-2 bg-gray-800 rounded-full overflow-hidden mx-auto">
          <div 
            className="h-full bg-gradient-to-r from-pink-500 to-purple-600 transition-all duration-500 rounded-full"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        <p className="text-gray-400 mt-4">{progress}% Complete</p>
      </div>
    </div>
  );
};

// Animated Metric Card
const MetricCard = ({ icon: Icon, label, value, color, delay }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setTimeout(() => setIsVisible(true), delay);
  }, [delay]);

  return (
    <div 
      className={`transform transition-all duration-700 ${
        isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'
      }`}
    >
      <div className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-6 border border-pink-500/20 hover:border-pink-500/40 transition-all group hover:scale-105 hover:shadow-2xl hover:shadow-pink-500/20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-pink-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div className={`w-12 h-12 bg-gradient-to-br from-${color}-500/20 to-purple-500/20 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform relative z-10`}>
          <Icon className={`w-6 h-6 text-${color}-400`} style={{ animation: 'float 3s ease-in-out infinite' }} />
        </div>
        <p className="text-gray-400 text-sm mb-1 relative z-10">{label}</p>
        <p className="text-2xl font-bold relative z-10">{value}</p>
      </div>
    </div>
  );
};

// 3D Product Card Component
const ProductCard = ({ product, index }) => {
  return (
    <div 
      className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-6 border border-pink-500/20 hover:border-pink-500/40 transition-all group transform hover:-translate-y-2 hover:shadow-2xl hover:shadow-pink-500/20 relative overflow-hidden"
      style={{
        animation: `slideUp 0.5s ease-out ${index * 0.1}s both`
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-pink-500/0 to-purple-500/0 group-hover:from-pink-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
      
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="w-12 h-12 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
            <Target className="w-6 h-6 text-pink-400" style={{ animation: 'spin 10s linear infinite' }} />
          </div>
          <div className="px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-full" style={{ animation: 'pulse 2s ease-in-out infinite' }}>
            <span className="text-xs font-semibold text-green-400">
              {Math.round(product.similarity * 100)}% Match
            </span>
          </div>
        </div>
        
        <h4 className="font-semibold text-lg mb-2 group-hover:text-pink-400 transition-colors">
          {product.name}
        </h4>
        <p className="text-gray-400 text-sm mb-4">{product.category}</p>
        
        {product.price && (
          <p className="text-xl font-bold mb-4 text-pink-400">${product.price}</p>
        )}
        
        <div className="space-y-3">
          <div>
            <p className="text-xs text-gray-500 mb-2">Shared Features</p>
            <div className="flex flex-wrap gap-1">
              {product.shared_features?.slice(0, 4).map((feature, idx) => (
                <span 
                  key={idx} 
                  className="px-2 py-1 bg-gray-700/50 rounded text-xs text-gray-300 hover:bg-pink-500/20 transition-colors"
                  style={{ animation: `fadeIn 0.3s ease-out ${idx * 0.1}s both` }}
                >
                  {feature}
                </span>
              ))}
            </div>
          </div>
          
          <div className="pt-3 border-t border-gray-700">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">Performance</span>
              <span className="font-semibold text-pink-400 flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                {product.marketing_performance?.average_score?.toFixed(1) || '8.5'}/10
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function CopyFlowApp() {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    description: '',
    price: '',
    target_audience: ''
  });
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [backendStatus, setBackendStatus] = useState('checking');
  const [activeTab, setActiveTab] = useState('overview');
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    // Simulate initial loading
    const interval = setInterval(() => {
      setLoadingProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => setInitialLoading(false), 500);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    checkBackendConnection();
    return () => clearInterval(interval);
  }, []);

  const checkBackendConnection = async () => {
    try {
      const response = await fetch(`${API_BASE}/health`);
      if (response.ok) {
        setBackendStatus('connected');
      } else {
        setBackendStatus('error');
      }
    } catch (err) {
      setBackendStatus('disconnected');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    setShowResults(false);

    try {
      const response = await fetch(`${API_BASE}/generate-marketing-strategy`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setTimeout(() => setShowResults(true), 300);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (initialLoading) {
    return <LoadingScreen progress={loadingProgress} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl" style={{ animation: 'pulse 4s ease-in-out infinite' }}></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" style={{ animation: 'pulse 4s ease-in-out infinite 1s' }}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" style={{ animation: 'pulse 4s ease-in-out infinite 2s' }}></div>
      </div>

      {/* Floating 3D Icons */}
      <FloatingIcons />
      
      {/* Animated Stars */}
      <AnimatedStars />

      {/* Animated Grid */}
      <div className="fixed inset-0 pointer-events-none opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(rgba(236, 72, 153, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(236, 72, 153, 0.3) 1px, transparent 1px)',
          backgroundSize: '50px 50px',
          animation: 'moveGrid 20s linear infinite'
        }}></div>
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-pink-500/20 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3" style={{ animation: 'slideInLeft 0.6s ease-out' }}>
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-purple-600 rounded-xl flex items-center justify-center relative overflow-hidden">
                  <Sparkles className="w-6 h-6 relative z-10" style={{ animation: 'spin 3s linear infinite' }} />
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30" style={{ animation: 'shimmer 2s linear infinite' }}></div>
                </div>
                <div className="absolute -inset-1 bg-pink-500/50 rounded-xl blur" style={{ animation: 'pulse 2s ease-in-out infinite' }}></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
                  CopyFlow AI
                </h1>
                <p className="text-xs text-gray-400">Intelligent Marketing Recommendations</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-800/50 rounded-full border border-pink-500/20 backdrop-blur-sm" style={{ animation: 'slideInRight 0.6s ease-out' }}>
              <div className="relative">
                <div className={`w-2 h-2 rounded-full ${
                  backendStatus === 'connected' ? 'bg-green-400' :
                  backendStatus === 'checking' ? 'bg-yellow-400' :
                  'bg-red-400'
                }`}></div>
                {backendStatus === 'connected' && (
                  <div className="absolute inset-0 w-2 h-2 bg-green-400 rounded-full" style={{ animation: 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite' }}></div>
                )}
              </div>
              <span className="text-sm text-gray-300 ml-2">
                {backendStatus === 'connected' ? 'Connected' : 
                 backendStatus === 'checking' ? 'Connecting...' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-12 relative z-10">
        <div className="max-w-7xl mx-auto">
          {!showResults ? (
            <div className="max-w-3xl mx-auto">
              <div className="text-center mb-12" style={{ animation: 'fadeInUp 0.8s ease-out' }}>
                <div className="inline-block mb-6">
                  <div className="relative">
                    <div className="text-6xl font-black mb-4 bg-gradient-to-r from-pink-400 via-purple-400 to-pink-400 bg-clip-text text-transparent" style={{ backgroundSize: '200% auto', animation: 'gradientShift 3s linear infinite' }}>
                      Transform Your Marketing
                    </div>
                    <div className="absolute -inset-4 bg-gradient-to-r from-pink-500/20 to-purple-500/20 blur-2xl -z-10" style={{ animation: 'pulse 3s ease-in-out infinite' }}></div>
                  </div>
                </div>
                <p className="text-xl text-gray-400" style={{ animation: 'fadeInUp 0.8s ease-out 0.2s both' }}>
                  AI-powered recommendations based on successful marketing patterns
                </p>
              </div>

              <div className="bg-gray-800/30 backdrop-blur-xl rounded-3xl p-8 border border-pink-500/20 shadow-2xl hover:shadow-pink-500/20 transition-shadow relative overflow-hidden" style={{ animation: 'scaleIn 0.5s ease-out 0.3s both' }}>
                <div className="absolute inset-0 bg-gradient-to-br from-pink-500/5 to-purple-500/5 opacity-0 hover:opacity-100 transition-opacity duration-500"></div>
                
                <div className="space-y-6 relative z-10">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2" style={{ animation: 'slideInLeft 0.5s ease-out 0.4s both' }}>
                      <label className="text-sm font-medium text-pink-400 flex items-center gap-2">
                        <Sparkles className="w-4 h-4" style={{ animation: 'float 2s ease-in-out infinite' }} />
                        Product Name *
                      </label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="e.g., Smart Blender Pro"
                        className="w-full px-4 py-3 bg-gray-900/50 border border-pink-500/30 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all text-white placeholder-gray-500 hover:border-pink-500/50"
                      />
                    </div>

                    <div className="space-y-2" style={{ animation: 'slideInRight 0.5s ease-out 0.4s both' }}>
                      <label className="text-sm font-medium text-pink-400 flex items-center gap-2">
                        <Box className="w-4 h-4" style={{ animation: 'float 2s ease-in-out infinite 0.5s' }} />
                        Category *
                      </label>
                      <input
                        type="text"
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        placeholder="e.g., Electronics"
                        className="w-full px-4 py-3 bg-gray-900/50 border border-pink-500/30 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all text-white placeholder-gray-500 hover:border-pink-500/50"
                      />
                    </div>
                  </div>

                  <div className="space-y-2" style={{ animation: 'fadeInUp 0.5s ease-out 0.5s both' }}>
                    <label className="text-sm font-medium text-pink-400 flex items-center gap-2">
                      <MessageCircle className="w-4 h-4" style={{ animation: 'float 2s ease-in-out infinite 1s' }} />
                      Product Description *
                    </label>
                    <textarea
                      name="description"
                      value={formData.description}
                      onChange={handleChange}
                      rows="5"
                      placeholder="Describe your product's features, benefits, and unique selling points..."
                      className="w-full px-4 py-3 bg-gray-900/50 border border-pink-500/30 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all text-white placeholder-gray-500 resize-none hover:border-pink-500/50"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2" style={{ animation: 'slideInLeft 0.5s ease-out 0.6s both' }}>
                      <label className="text-sm font-medium text-pink-400">Price (Optional)</label>
                      <input
                        type="number"
                        name="price"
                        value={formData.price}
                        onChange={handleChange}
                        placeholder="99.99"
                        step="0.01"
                        className="w-full px-4 py-3 bg-gray-900/50 border border-pink-500/30 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all text-white placeholder-gray-500 hover:border-pink-500/50"
                      />
                    </div>

                    <div className="space-y-2" style={{ animation: 'slideInRight 0.5s ease-out 0.6s both' }}>
                      <label className="text-sm font-medium text-pink-400 flex items-center gap-2">
                        <Target className="w-4 h-4" style={{ animation: 'spin 10s linear infinite' }} />
                        Target Audience
                      </label>
                      <select 
                        name="target_audience" 
                        value={formData.target_audience}
                        onChange={handleChange}
                        className="w-full px-4 py-3 bg-gray-900/50 border border-pink-500/30 rounded-xl focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all text-white hover:border-pink-500/50"
                      >
                        <option value="">Select Audience</option>
                        <option value="B2C">B2C Consumers</option>
                        <option value="B2B">B2B Businesses</option>
                        <option value="teenagers">Teenagers</option>
                        <option value="professionals">Professionals</option>
                        <option value="families">Families</option>
                      </select>
                    </div>
                  </div>

                  <button 
                    onClick={handleSubmit}
                    disabled={loading || backendStatus !== 'connected' || !formData.name || !formData.category || !formData.description}
                    className="w-full py-4 bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl font-semibold text-lg flex items-center justify-center gap-3 hover:shadow-2xl hover:shadow-pink-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group relative overflow-hidden"
                    style={{ animation: 'fadeInUp 0.5s ease-out 0.7s both' }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-pink-600 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative flex items-center gap-3">
                      {loading ? (
                        <>
                          <Loader2 className="w-5 h-5" style={{ animation: 'spin 1s linear infinite' }} />
                          Analyzing Your Product...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-5 h-5 group-hover:scale-110 transition-transform" />
                          Generate Marketing Strategy
                          <ArrowRight className="w-5 h-5 group-hover:translate-x-2 transition-transform" />
                        </>
                      )}
                    </div>
                  </button>
                </div>

                {error && (
                  <div className="mt-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-start gap-3" style={{ animation: 'shake 0.5s ease-in-out' }}>
                    <X className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                    <p className="text-red-400 text-sm">{error}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="flex items-center justify-between" style={{ animation: 'slideInDown 0.6s ease-out' }}>
                <div>
                  <h2 className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
                    Marketing Recommendations
                  </h2>
                  <p className="text-gray-400 mt-2 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-pink-400" style={{ animation: 'float 2s ease-in-out infinite' }} />
                    For {result?.input_product?.name}
                  </p>
                </div>
                <button
                  onClick={() => {
                    setShowResults(false);
                    setResult(null);
                  }}
                  className="px-6 py-3 bg-gray-800/50 hover:bg-gray-800 rounded-xl border border-pink-500/20 transition-all hover:scale-105 hover:border-pink-500/40"
                >
                  ← New Analysis
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <MetricCard icon={Target} label="Similar Products" value={result?.similar_products?.length || 3} color="pink" delay={100} />
                <MetricCard icon={TrendingUp} label="Avg Performance" value="8.2/10" color="purple" delay={200} />
                <MetricCard icon={Zap} label="Confidence" value={result?.performance_insights?.confidence_level || 'High'} color="pink" delay={300} />
                <MetricCard icon={BarChart3} label="Platforms" value={result?.marketing_strategy?.target_tones?.length || 3} color="purple" delay={400} />
              </div>

              <div className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-2 border border-pink-500/20" style={{ animation: 'scaleIn 0.5s ease-out 0.5s both' }}>
                <div className="flex gap-2 overflow-x-auto">
                  {[
                    { id: 'overview', label: 'Overview', icon: Sparkles },
                    { id: 'similar', label: 'Similar Products', icon: Target },
                    { id: 'content', label: 'Content Ideas', icon: MessageCircle },
                    { id: 'insights', label: 'Insights', icon: BarChart3 }
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex-1 px-4 py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 whitespace-nowrap ${
                        activeTab === tab.id
                          ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white shadow-lg scale-105'
                          : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
                      }`}
                    >
                      <tab.icon className="w-4 h-4" />
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="min-h-96">
                {activeTab === 'overview' && (
                  <div className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-8 border border-pink-500/20" style={{ animation: 'fadeIn 0.5s ease-out' }}>
                    <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                      <Sparkles className="w-6 h-6 text-pink-400" style={{ animation: 'pulse 2s ease-in-out infinite' }} />
                      Marketing Strategy Overview
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <div style={{ animation: 'slideInLeft 0.5s ease-out' }}>
                          <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                            <Zap className="w-4 h-4" />
                            Recommended Tones
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {(result?.marketing_strategy?.target_tones || ['Professional', 'Friendly', 'Energetic']).map((tone, idx) => (
                              <span 
                                key={idx} 
                                className="px-4 py-2 bg-pink-500/20 border border-pink-500/30 rounded-full text-sm hover:scale-105 transition-transform cursor-default"
                                style={{ animation: `fadeIn 0.3s ease-out ${idx * 0.1}s both` }}
                              >
                                {tone}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div style={{ animation: 'slideInLeft 0.5s ease-out 0.2s both' }}>
                          <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                            <Check className="w-4 h-4" />
                            Key Value Propositions
                          </h4>
                          <ul className="space-y-2">
                            {(result?.marketing_strategy?.key_value_propositions || [
                              'Boost your confidence with premium quality',
                              'Experience cutting-edge innovation',
                              'Exceptional quality at unbeatable value'
                            ]).map((prop, idx) => (
                              <li 
                                key={idx} 
                                className="flex items-start gap-2 text-gray-300 hover:text-white transition-colors"
                                style={{ animation: `slideInLeft 0.3s ease-out ${idx * 0.1}s both` }}
                              >
                                <Check className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" style={{ animation: 'float 3s ease-in-out infinite' }} />
                                {prop}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      
                      <div className="space-y-4">
                        <div style={{ animation: 'slideInRight 0.5s ease-out' }}>
                          <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                            <MessageCircle className="w-4 h-4" />
                            Core Message
                          </h4>
                          <p className="text-gray-300 bg-gray-900/50 p-4 rounded-xl border border-pink-500/10 hover:border-pink-500/30 transition-colors">
                            {result?.marketing_strategy?.core_message || 'Focus on innovation and quality to capture your target audience'}
                          </p>
                        </div>
                        
                        <div style={{ animation: 'slideInRight 0.5s ease-out 0.2s both' }}>
                          <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                            <BarChart3 className="w-4 h-4" />
                            Success Metrics
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {(result?.marketing_strategy?.success_metrics || ['engagement_rate', 'conversion_rate', 'brand_recall']).map((metric, idx) => (
                              <span 
                                key={idx} 
                                className="px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded-full text-sm capitalize hover:scale-105 transition-transform cursor-default"
                                style={{ animation: `fadeIn 0.3s ease-out ${idx * 0.1}s both` }}
                              >
                                {metric.replace('_', ' ')}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'similar' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {(result?.similar_products || [
                      { name: 'Premium Product A', category: 'Electronics', price: 149.99, similarity: 0.92, shared_features: ['wireless', 'premium', 'innovative', 'quality'], marketing_performance: { average_score: 8.5 } },
                      { name: 'Smart Device B', category: 'Electronics', price: 199.99, similarity: 0.88, shared_features: ['smart', 'efficient', 'modern', 'reliable'], marketing_performance: { average_score: 8.2 } },
                      { name: 'Tech Solution C', category: 'Electronics', price: 129.99, similarity: 0.85, shared_features: ['advanced', 'powerful', 'compact', 'durable'], marketing_performance: { average_score: 8.7 } }
                    ]).map((product, idx) => (
                      <ProductCard key={idx} product={product} index={idx} />
                    ))}
                  </div>
                )}

                {activeTab === 'content' && (
                  <div className="space-y-6">
                    {Object.entries(result?.platform_content || {
                      Instagram: {
                        caption_templates: [
                          "✨ Introducing the future of [category]!\n\n🚀 Key Features:\n• Feature 1\n• Feature 2\n• Feature 3\n\nReady to upgrade? 🔥\n\n#innovation #quality #musthave",
                          "🎯 What makes this special?\n\nIt's not just another product – it's a game-changer! 💫\n\nSwipe to see why everyone's talking about it 👉\n\n#trending #tech #lifestyle"
                        ],
                        hashtag_strategy: {
                          primary: ['#ProductName', '#Category', '#Brand']
                        }
                      }
                    }).map(([platform, content], idx) => (
                      <div 
                        key={platform} 
                        className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-8 border border-pink-500/20 hover:border-pink-500/30 transition-all"
                        style={{ animation: `slideUp 0.5s ease-out ${idx * 0.1}s both` }}
                      >
                        <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                          <Share2 className="w-6 h-6 text-pink-400" style={{ animation: 'pulse 2s ease-in-out infinite' }} />
                          {platform} Content Strategy
                        </h3>
                        
                        {content.caption_templates && (
                          <div className="space-y-4">
                            {content.caption_templates.slice(0, 2).map((template, templateIdx) => (
                              <div 
                                key={templateIdx} 
                                className="bg-gray-900/50 rounded-xl p-6 border border-gray-700 hover:border-pink-500/30 transition-all group"
                                style={{ animation: `fadeIn 0.3s ease-out ${templateIdx * 0.15}s both` }}
                              >
                                <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                                  <MessageCircle className="w-4 h-4" />
                                  Caption Template {templateIdx + 1}
                                </h4>
                                <p className="text-gray-300 whitespace-pre-wrap leading-relaxed group-hover:text-white transition-colors">
                                  {template}
                                </p>
                              </div>
                            ))}
                            
                            {content.hashtag_strategy && (
                              <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700 hover:border-pink-500/30 transition-all">
                                <h4 className="text-pink-400 font-semibold mb-3 flex items-center gap-2">
                                  <Target className="w-4 h-4" />
                                  Hashtag Strategy
                                </h4>
                                <div className="space-y-3">
                                  <div>
                                    <p className="text-xs text-gray-500 mb-2">Primary Hashtags</p>
                                    <div className="flex flex-wrap gap-2">
                                      {content.hashtag_strategy.primary?.map((tag, idx) => (
                                        <span 
                                          key={idx} 
                                          className="px-3 py-1 bg-pink-500/20 border border-pink-500/30 rounded-full text-sm hover:scale-105 transition-transform cursor-default"
                                          style={{ animation: `fadeIn 0.2s ease-out ${idx * 0.05}s both` }}
                                        >
                                          {tag}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'insights' && (
                  <div className="space-y-6">
                    <div className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-8 border border-pink-500/20" style={{ animation: 'scaleIn 0.5s ease-out' }}>
                      <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                        <BarChart3 className="w-6 h-6 text-pink-400" style={{ animation: 'pulse 2s ease-in-out infinite' }} />
                        Performance Insights
                      </h3>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700 hover:border-pink-500/30 transition-all group" style={{ animation: 'slideInLeft 0.5s ease-out' }}>
                          <h4 className="text-pink-400 font-semibold mb-4 flex items-center gap-2">
                            <TrendingUp className="w-5 h-5" />
                            Predicted Engagement
                          </h4>
                          <div className="flex items-center gap-4">
                            <div className="relative">
                              <div className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400 group-hover:scale-110 transition-transform">
                                {result?.performance_insights?.predicted_engagement || '8.2'}
                              </div>
                              <div className="absolute -inset-2 bg-gradient-to-r from-pink-500/20 to-purple-500/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            </div>
                            <div className="text-2xl text-gray-400">/10</div>
                          </div>
                          <div className="mt-4 flex items-center gap-2">
                            <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-gradient-to-r from-pink-500 to-purple-600 rounded-full transition-all duration-1000"
                                style={{ width: '82%', animation: 'slideInLeft 1s ease-out' }}
                              ></div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-500 mt-3 flex items-center gap-2">
                            <Zap className="w-4 h-4 text-yellow-400" style={{ animation: 'float 2s ease-in-out infinite' }} />
                            Confidence: {result?.performance_insights?.confidence_level || 'High'}
                          </p>
                        </div>
                        
                        <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700 hover:border-pink-500/30 transition-all" style={{ animation: 'slideInRight 0.5s ease-out' }}>
                          <h4 className="text-pink-400 font-semibold mb-4 flex items-center gap-2">
                            <Target className="w-5 h-5" />
                            Key Success Factors
                          </h4>
                          <ul className="space-y-3">
                            {(result?.performance_insights?.key_success_factors || [
                              'Strong professional tone resonates with target audience',
                              'Focus on innovation and quality features',
                              'Instagram optimization increases visibility'
                            ]).map((factor, idx) => (
                              <li 
                                key={idx} 
                                className="flex items-start gap-2 text-gray-300 text-sm hover:text-white transition-colors"
                                style={{ animation: `slideInRight 0.3s ease-out ${idx * 0.1}s both` }}
                              >
                                <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                                  <Check className="w-4 h-4 text-green-400" />
                                </div>
                                {factor}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-800/30 backdrop-blur-xl rounded-2xl p-8 border border-pink-500/20" style={{ animation: 'fadeInUp 0.5s ease-out 0.3s both' }}>
                      <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
                        <Rocket className="w-6 h-6 text-pink-400" style={{ animation: 'float 3s ease-in-out infinite' }} />
                        Implementation Guide
                      </h3>
                      
                      <div className="space-y-6">
                        <div style={{ animation: 'slideInLeft 0.5s ease-out' }}>
                          <h4 className="text-pink-400 font-semibold mb-4 flex items-center gap-2">
                            <BarChart3 className="w-5 h-5" />
                            Performance Tracking
                          </h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {(result?.implementation_guide?.performance_tracking || [
                              'Engagement rate per platform',
                              'Conversion rate from CTAs',
                              'Audience growth rate',
                              'Content shareability'
                            ]).map((metric, idx) => (
                              <div 
                                key={idx} 
                                className="bg-gray-900/50 rounded-xl p-4 border border-gray-700 hover:border-pink-500/20 transition-all hover:scale-105"
                                style={{ animation: `fadeIn 0.2s ease-out ${idx * 0.05}s both` }}
                              >
                                <p className="text-sm text-gray-300 flex items-center gap-2">
                                  <div className="w-2 h-2 bg-pink-400 rounded-full" style={{ animation: 'pulse 2s ease-in-out infinite' }}></div>
                                  {metric}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div style={{ animation: 'slideInRight 0.5s ease-out 0.2s both' }}>
                          <h4 className="text-pink-400 font-semibold mb-4 flex items-center gap-2">
                            <Zap className="w-5 h-5" />
                            Optimization Tips
                          </h4>
                          <ul className="space-y-3">
                            {(result?.implementation_guide?.optimization_tips || [
                              'A/B test different tones weekly',
                              'Monitor competitor strategies',
                              'Engage with user comments promptly',
                              'Update content based on performance data'
                            ]).map((tip, idx) => (
                              <li 
                                key={idx} 
                                className="flex items-start gap-3 text-gray-300 text-sm bg-gray-900/50 rounded-xl p-4 border border-gray-700 hover:border-yellow-500/30 transition-all hover:scale-[1.02]"
                                style={{ animation: `slideInRight 0.3s ease-out ${idx * 0.1}s both` }}
                              >
                                <Zap className="w-5 h-5 text-yellow-400 flex-shrink-0 mt-0.5" style={{ animation: 'pulse 2s ease-in-out infinite' }} />
                                <span className="leading-relaxed">{tip}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0) rotate(0deg);
          }
          50% {
            transform: translateY(-20px) rotate(5deg);
          }
        }

        @keyframes pulse {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.05);
          }
        }

        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        @keyframes shimmer {
          from {
            transform: translateX(-100%);
          }
          to {
            transform: translateX(100%);
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideInLeft {
          from {
            opacity: 0;
            transform: translateX(-30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes slideInRight {
          from {
            opacity: 0;
            transform: translateX(30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes slideInDown {
          from {
            opacity: 0;
            transform: translateY(-30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes scaleIn {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes gradientShift {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }

        @keyframes ping {
          75%, 100% {
            transform: scale(2);
            opacity: 0;
          }
        }

        @keyframes shake {
          0%, 100% {
            transform: translateX(0);
          }
          25% {
            transform: translateX(-5px);
          }
          75% {
            transform: translateX(5px);
          }
        }

        @keyframes moveGrid {
          0% {
            transform: translate(0, 0);
          }
          100% {
            transform: translate(50px, 50px);
          }
        }

        @keyframes twinkle {
          0%, 100% {
            opacity: 0.2;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.5);
          }
        }
      `}</style>
    </div>
  );
}