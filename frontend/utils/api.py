"""
Utility functions for frontend
"""
import requests
from typing import Optional, Dict, Any
import streamlit as st


import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_headers() -> Dict[str, str]:
    """Get authorization headers with token"""
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    require_auth: bool = True
) -> Dict[str, Any]:
    """Make API request"""
    
    url = f"{API_BASE_URL}{endpoint}"
    headers = get_headers() if require_auth else {}
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"error": "Invalid HTTP method"}
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            error_detail = response.json().get("detail", "Unknown error")
            return {"success": False, "error": error_detail}
    
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API server. Please ensure the backend is running."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Login user and store token"""
    result = api_request(
        "POST",
        "/api/auth/login",
        data={"email": email, "password": password},
        require_auth=False
    )
    
    if result.get("success"):
        data = result["data"]
        st.session_state.token = data["access_token"]
        st.session_state.user = data["user"]
        return {"success": True}
    
    return result


def logout_user():
    """Logout user and clear auth session"""
    if "token" in st.session_state:
        del st.session_state.token
    if "user" in st.session_state:
        del st.session_state.user


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return "token" in st.session_state and "user" in st.session_state


def get_current_user() -> Optional[Dict]:
    """Get current user from session"""
    return st.session_state.get("user")


def get_user_role() -> Optional[str]:
    """Get current user role"""
    user = get_current_user()
    return user.get("role") if user else None


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


def format_datetime(dt_str: str) -> str:
    """Format datetime string"""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return dt_str


def show_success(message: str):
    """Show success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")


def show_info(message: str):
    """Show info message"""
    st.info(f"ℹ️ {message}")


def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")
