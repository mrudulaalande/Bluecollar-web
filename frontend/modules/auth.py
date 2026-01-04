"""
Authentication page - Login and Signup
"""
import streamlit as st
from frontend.utils.api import login_user, api_request, show_success, show_error


def show_auth_page(default_role: str = "client"):
    """Show authentication page with login and signup"""
    
    # Header
    role_title = default_role.capitalize()
    st.markdown(f"""
    <div class='custom-header'>
        <h1>🔧 {role_title} Portal</h1>
        <p>Login or create an account to access the {default_role} services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if admin
    if default_role == "admin":
        st.markdown("### 🔐 Admin Secure Login")
        show_login_form()
        return

    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_signup_form(default_role=default_role)


def show_login_form():
    """Show login form"""
    
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    st.markdown("### Welcome Back!")
    st.markdown("Please enter your credentials to continue")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if not email or not password:
                show_error("Please fill in all fields")
                return
            
            # Clear any existing stale auth data before new login
            from frontend.utils.api import logout_user
            logout_user()
            
            with st.spinner("Logging in..."):
                result = login_user(email, password)
            
            if result.get("success"):
                show_success("Login successful!")
                st.session_state.page = "Admin Dashboard" if "admin" in email else "Client Dashboard"
                st.rerun()
            else:
                show_error(result.get("error", "Login failed"))
    
    st.markdown("</div>", unsafe_allow_html=True)


def show_signup_form(default_role="client"):
    """Show signup form"""
    
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    st.markdown("### Create Your Account")
    st.markdown("Join our platform to get started")
    
    with st.form("signup_form"):
        full_name = st.text_input("👤 Full Name", placeholder="John Doe")
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        phone = st.text_input("📱 Phone (Optional)", placeholder="+1234567890")
        password = st.text_input("🔒 Password", type="password", placeholder="Minimum 6 characters")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
        
        role_options = ["client", "worker"]
        role = st.selectbox(
            "👔 I am a...",
            role_options,
            index=role_options.index(default_role) if default_role in role_options else 0,
            format_func=lambda x: "Client (Looking for workers)" if x == "client" else "Worker (Offering services)"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            # Validation
            if not all([full_name, email, password, confirm_password]):
                show_error("Please fill in all required fields")
                return
            
            if len(password) < 6:
                show_error("Password must be at least 6 characters long")
                return
            
            if password != confirm_password:
                show_error("Passwords do not match")
                return
            
            # Create account
            with st.spinner("Creating account..."):
                result = api_request(
                    "POST",
                    "/api/auth/signup",
                    data={
                        "email": email,
                        "password": password,
                        "full_name": full_name,
                        "phone": phone if phone else None,
                        "role": role
                    },
                    require_auth=False
                )
            
            if result.get("success"):
                show_success("Account created successfully! Please login.")
                # Clear stale data after signup too
                from frontend.utils.api import logout_user
                logout_user()
                if role == "worker":
                    st.info("ℹ️ Your worker account will be activated after admin approval.")
            else:
                show_error(result.get("error", "Signup failed"))
    
    st.markdown("</div>", unsafe_allow_html=True)
