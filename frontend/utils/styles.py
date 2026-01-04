"""
Custom CSS styles for the application
Premium Aesthetic with Glassmorphism and Vibrant Gradients
"""

def get_custom_css() -> str:
    """Return custom CSS for the application"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container background */
    .main {
        background: radial-gradient(circle at top right, #F0F4FF, #FFFFFF);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Elegant Sidebar with Deep Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* Custom Header with Modern Gradient */
    .custom-header {
        background: linear-gradient(110deg, #2563EB 0%, #4F46E5 100%);
        padding: 3rem 2.5rem;
        border-radius: 24px;
        margin: 0 0 2rem 0;
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .custom-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .custom-header h1 {
        color: white !important;
        margin: 0;
        font-weight: 800;
        font-size: 2.8rem;
        letter-spacing: -1px;
    }
    
    .custom-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 1rem 0 0 0;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Premium Cards with Glassmorphism */
    .worker-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: #000000 !important;
    }
    
    .worker-card * {
        color: #000000 !important;
    }
    
    .worker-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(37, 99, 235, 0.12);
        border-color: rgba(37, 99, 235, 0.3);
    }
    
    /* Modern Stats with Vibrant Accents */
    .stat-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.03);
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stat-card:hover {
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border-color: #E2E8F0;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563EB, #4F46E5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #000000 !important;
        margin-top: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Streamlit Metric Labels */
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    
    /* Ensure labels inside white cards are black, but global labels follow theme */
    .worker-card label, .stat-card label {
        color: #000000 !important;
    }

    /* Global support for white text on dark sections if needed */
    .dark-container {
        color: #FFFFFF !important;
    }
    .dark-container * {
        color: #FFFFFF !important;
    }
    
    /* Sexy Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #6366F1 100%);
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 2rem;
        font-weight: 700;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #4F46E5 100%);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.3);
        transform: scale(1.02);
    }
    
    /* Input field elegance */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 16px;
        border: 2px solid #F1F5F9;
        padding: 0.8rem 1.2rem;
        background-color: #F8FAFC;
        transition: all 0.3s ease;
        font-size: 1rem;
        color: #1E293B !important; /* Professional dark blue-gray for inputs */
    }

    /* Placeholder text visibility */
    ::placeholder {
        color: #666666 !important;
        opacity: 1;
    }
    
    input::placeholder {
        color: #666666 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3B82F6;
        background-color: white;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    }
    
    /* Rating Stars Glow */
    .rating {
        color: #F59E0B !important;
        font-size: 1.4rem;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }
    
    /* Vibrant Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 700;
        margin: 0.25rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .badge-primary { background: #E0E7FF; color: #4338CA !important; }
    .badge-success { background: #DCFCE7; color: #15803D !important; }
    .badge-warning { background: #FEF3C7; color: #B45309 !important; }
    .badge-danger { background: #FEE2E2; color: #B91C1C !important; }
    .badge-info { background: #E0F2FE; color: #0369A1 !important; }
    
    /* Tabs Overhaul */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(241, 245, 249, 0.5);
        padding: 0.5rem;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        background: transparent !important;
        border: none !important;
        font-weight: 700 !important;
        color: #000000 !important; /* Force black for inactive tabs */
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #2563EB !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Animations */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: slideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
    </style>
    """
