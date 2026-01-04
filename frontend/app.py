"""
Main Streamlit Application
Blue Collar Worker Platform
"""
import streamlit as st
from frontend.utils.styles import get_custom_css
from frontend.utils.api import is_authenticated, get_user_role, logout_user

# Page configuration
st.set_page_config(
    page_title="Blue Collar Hub - Fit For All",
    page_icon="frontend/assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64
def get_base64_logo():
    try:
        with open("frontend/assets/logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_BASE64 = get_base64_logo()

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

def show_app_description():
    """Show application description and home page"""
    st.markdown(f"""<div class='custom-header'>
<div style='display: flex; align-items: center; gap: 1.5rem;'>
<img src="data:image/png;base64,{LOGO_BASE64}" style='height: 80px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));'>
<div>
<h1 style='margin: 0;'>Blue Collar Hub</h1>
<p style='margin: 0;'>Fit For All - Connecting Professionals</p>
</div>
</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class='fade-in'>
<div class='worker-card' style='padding: 2.5rem; background: white;'>
<h2 style='color: #2563EB;'>Welcome to the Next Generation Blue-Collar Marketplace</h2>
<p style='font-size: 1.15rem; line-height: 1.7; color: #1E293B;'>
Our platform streamlines the process of finding, booking, and paying for professional blue-collar services.
Whether you're a homeowner looking for a plumber or a skilled electrician looking for work, we provide the tools you need to succeed.
</p>

<div style='display: flex; gap: 2rem; margin-top: 2.5rem; flex-wrap: wrap;'>
<div style='flex: 1; min-width: 280px; background: #F8FAFC; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; border-top: 6px solid #2563EB;'>
<h3 style='margin-top: 0; color: #1E293B;'>👤 For Clients</h3>
<ul style='color: #334155; line-height: 1.8;'>
<li>Search verified workers by skill</li>
<li>Real-time availability tracking</li>
<li>Secure online payments</li>
<li>Trust-based rating system</li>
</ul>
</div>

<div style='flex: 1; min-width: 280px; background: #F8FAFC; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; border-top: 6px solid #2ECC71;'>
<h3 style='margin-top: 0; color: #1E293B;'>👷 For Workers</h3>
<ul style='color: #334155; line-height: 1.8;'>
<li>Professional profile management</li>
<li>Digital booking dashboard</li>
<li>Automated earnings tracking</li>
<li>Direct client connection</li>
</ul>
</div>

<div style='flex: 1; min-width: 280px; background: #F8FAFC; padding: 2rem; border-radius: 20px; border: 1px solid #E2E8F0; border-top: 6px solid #F43F5E;'>
<h3 style='margin-top: 0; color: #1E293B;'>⚙️ For Admins</h3>
<ul style='color: #334155; line-height: 1.8;'>
<li>Comprehensive platform analytics</li>
<li>Worker verification workflow</li>
<li>Payment and booking oversight</li>
<li>User account management</li>
</ul>
</div>
</div>

<div style='margin-top: 3rem; text-align: center; background: linear-gradient(135deg, #2563EB, #4F46E5); padding: 3rem; border-radius: 24px; color: white;'>
<h3 style='color: white; font-size: 2rem;'>Ready to get started?</h3>
<p style='color: rgba(255,255,255,0.9); font-size: 1.2rem;'>Select your role from the sidebar to sign in or create an account.</p>
</div>
</div>
</div>""", unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 1rem;'>
            <img src="data:image/png;base64,{LOGO_BASE64}" style='width: 100%; max-width: 180px; margin-bottom: 1rem;'>
            <h2 style='color: white; font-size: 1.5rem; margin: 0; font-weight: 800;'>BLUE COLLAR HUB</h2>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; font-weight: 500; letter-spacing: 2px;'>FIT FOR ALL</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.1); margin: 1rem 0;'></div>", unsafe_allow_html=True)
        
        # Use session state to track page for better persistence
        if "page" not in st.session_state:
            st.session_state.page = "App Description"

        # Prepare navigation options based on auth state
        if not is_authenticated():
            nav_options = ["App Description", "Client Area", "Worker Area", "Admin Panel"]
        else:
            role = get_user_role()
            dashboard_name = {
                "client": "Client Dashboard",
                "worker": "Worker Dashboard",
                "admin": "Admin Dashboard"
            }.get(role, "Dashboard")
            nav_options = ["App Description", dashboard_name]
            
            # Auto-switch to dashboard if we were just on a login page
            if st.session_state.page in ["Client Area", "Worker Area", "Admin Panel"]:
                st.session_state.page = dashboard_name

        # Ensure current page is in options
        if st.session_state.page not in nav_options:
            st.session_state.page = "App Description"

        st.markdown("<p style='padding: 0 1rem; color: #94A3B8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>Navigation</p>", unsafe_allow_html=True)
        
        # Radio button updates session state directly
        st.radio(
            "Navigate",
            nav_options,
            index=nav_options.index(st.session_state.page),
            label_visibility="collapsed",
            key="main_nav_radio_widget",
            on_change=lambda: setattr(st.session_state, "page", st.session_state.main_nav_radio_widget)
        )
        
        page = st.session_state.page

        st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.1); margin: 2rem 0;'></div>", unsafe_allow_html=True)

        if is_authenticated():
            user = st.session_state.get("user", {})
            role = get_user_role()
            st.markdown(f"""
            <div style='color: white; padding: 1.5rem; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; margin-bottom: 2rem;'>
                <p style='margin: 0; font-size: 0.8rem; color: #94A3B8; font-weight: 600;'>ACCOUNT</p>
                <p style='margin: 0.75rem 0 0 0; font-weight: 700; font-size: 1.1rem; color: white !important;'>{user.get('full_name', 'User')}</p>
                <div style='margin-top: 1rem;'>
                    <span style='background: #2563EB; color: white !important; padding: 0.3rem 1rem; border-radius: 100px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.5px;'>
                        {role.upper() if role else 'USER'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.session_state.page = "App Description"
                st.rerun()
        else:
            st.info("👋 Hello! Please sign in to access your secure dashboard.")
                
    # Page Routing
    if page == "App Description":
        show_app_description()
        
    elif page in ["Client Area", "Client Dashboard"]:
        if not is_authenticated():
            from frontend.modules import auth
            auth.show_auth_page(default_role="client")
        else:
            if get_user_role() == "client":
                from frontend.modules import client
                client.show_client_dashboard()
            else:
                st.warning(f"You are logged in as a {get_user_role()}. Please logout to access the Client area.")
                
    elif page in ["Worker Area", "Worker Dashboard"]:
        if not is_authenticated():
            from frontend.modules import auth
            auth.show_auth_page(default_role="worker")
        else:
            if get_user_role() == "worker":
                from frontend.modules import worker
                worker.show_worker_dashboard()
            else:
                st.warning(f"You are logged in as a {get_user_role()}. Please logout to access the Worker area.")
                
    elif page in ["Admin Panel", "Admin Dashboard"]:
        if not is_authenticated():
            from frontend.modules import auth
            auth.show_auth_page(default_role="admin")
        else:
            if get_user_role() == "admin":
                from frontend.modules import admin
                admin.show_admin_dashboard()
            else:
                st.warning(f"You are logged in as an Admin. Please logout to access the Admin panel.")

if __name__ == "__main__":
    main()
