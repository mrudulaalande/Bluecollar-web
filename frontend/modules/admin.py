"""
Admin Dashboard
"""
import streamlit as st
from frontend.utils.api import (
    api_request, show_success, show_error, show_info,
    format_currency, format_datetime, get_current_user
)


def show_admin_dashboard():
    """Show admin dashboard"""
    
    user = get_current_user()
    st.markdown(f"""
    <div class='custom-header'>
        <h1>⚙️ Admin Dashboard</h1>
        <p>Platform management and analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "👥 Users", "📅 Bookings", "💳 Payments"])
    
    with tab1:
        show_analytics()
    
    with tab2:
        show_users_management()
    
    with tab3:
        show_bookings_management()
    
    with tab4:
        show_payments_management()


def show_analytics():
    """Show platform analytics"""
    
    st.markdown("### 📊 Platform Analytics")
    
    # Fetch dashboard data
    result = api_request("GET", "/api/admin/dashboard")
    
    if not result.get("success"):
        if "credentials" in result.get("error", "").lower():
            st.warning("🔐 Your session has expired. Please logout and login again to refresh your access.")
            if st.button("🚪 Relogin Now", key="relogin_btn"):
                from frontend.utils.api import logout_user
                logout_user()
                st.session_state.page = "Admin Panel"
                st.rerun()
        else:
            show_error(result.get("error", "Failed to load analytics"))
        return
    
    data = result["data"]
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{data.get('total_users', 0)}</p>
            <p class='stat-label'>Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{data.get('total_bookings', 0)}</p>
            <p class='stat-label'>Total Bookings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{data.get('completed_bookings', 0)}</p>
            <p class='stat-label'>Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number' style='font-size: 1.8rem;'>{format_currency(data.get('total_revenue', 0))}</p>
            <p class='stat-label'>Total Revenue</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clients", data.get('total_clients', 0))
    
    with col2:
        st.metric("Total Workers", data.get('total_workers', 0))
    
    with col3:
        st.metric("Pending Bookings", data.get('pending_bookings', 0))
    
    with col4:
        st.metric("Pending Approvals", data.get('pending_worker_approvals', 0))
    
    # Recent activity
    st.markdown("---")
    st.markdown("### 📈 Recent Activity (Last 7 Days)")
    st.metric("New Bookings", data.get('recent_bookings_7days', 0))


def show_users_management():
    """Show user management interface"""
    
    st.markdown("### 👥 User Management")
    
    # Filter by role
    role_filter = st.selectbox(
        "Filter by role",
        ["All", "client", "worker", "admin"]
    )
    
    # Fetch users
    params = {} if role_filter == "All" else {"role": role_filter}
    result = api_request("GET", "/api/admin/users", params=params)
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load users"))
        return
    
    users = result["data"]
    
    if not users:
        st.info("No users found")
        return
    
    st.markdown(f"**Total: {len(users)} users**")
    
    # Display users
    for user in users:
        role_color = {
            "client": "info",
            "worker": "primary",
            "admin": "danger"
        }.get(user["role"], "info")
        
        status_badge = "✅ Active" if user["is_active"] else "🔴 Suspended"
        approval_badge = "✅ Approved" if user["is_approved"] else "⏳ Pending"
        
        st.markdown(f"""
        <div class='worker-card' style='color: #000;'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div>
                    <h4 style='margin: 0; color: #0A1AFF;'>{user['full_name']}</h4>
                    <p style='margin: 0.5rem 0; color: #333;'>
                        📧 {user['email']}
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        📱 {user.get('phone', 'N/A')}
                    </p>
                    <p style='margin: 0.5rem 0;'>
                        <span class='badge badge-{role_color}'>{user['role'].upper()}</span>
                        <span class='badge {"badge-success" if user["is_active"] else "badge-danger"}'>{status_badge}</span>
                        {f"<span class='badge badge-warning'>{approval_badge}</span>" if user['role'] == 'worker' else ""}
                    </p>
                    <p style='margin: 0.25rem 0; font-size: 0.85rem; color: #333;'>
                        Joined: {format_datetime(user['created_at'])}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        if user["role"] != "admin":
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if user["role"] == "worker" and not user["is_approved"]:
                    if st.button("✅ Approve", key=f"approve_{user['id']}"):
                        approve_user(user['id'])
            
            with col2:
                if user["is_active"]:
                    if st.button("🔴 Suspend", key=f"suspend_{user['id']}"):
                        suspend_user(user['id'])
                else:
                    if st.button("✅ Activate", key=f"activate_{user['id']}"):
                        activate_user(user['id'])
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{user['id']}"):
                    if st.session_state.get(f"confirm_delete_{user['id']}", False):
                        delete_user(user['id'])
                    else:
                        st.session_state[f"confirm_delete_{user['id']}"] = True
                        show_info("Click again to confirm deletion")
        
        st.markdown("---")


def approve_user(user_id):
    """Approve a worker account"""
    
    with st.spinner("Approving user..."):
        result = api_request("PUT", f"/api/admin/users/{user_id}/approve")
    
    if result.get("success"):
        show_success("User approved successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Approval failed"))


def suspend_user(user_id):
    """Suspend a user account"""
    
    with st.spinner("Suspending user..."):
        result = api_request("PUT", f"/api/admin/users/{user_id}/suspend")
    
    if result.get("success"):
        show_success("User suspended successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Suspension failed"))


def activate_user(user_id):
    """Activate a user account"""
    
    with st.spinner("Activating user..."):
        result = api_request("PUT", f"/api/admin/users/{user_id}/activate")
    
    if result.get("success"):
        show_success("User activated successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Activation failed"))


def delete_user(user_id):
    """Delete a user account"""
    
    with st.spinner("Deleting user..."):
        result = api_request("DELETE", f"/api/admin/users/{user_id}")
    
    if result.get("success"):
        show_success("User deleted successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Deletion failed"))


def show_bookings_management():
    """Show bookings management"""
    
    st.markdown("### 📅 Bookings Management")
    
    # Filter by status
    status_filter = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Accepted", "Completed", "Cancelled"]
    )
    
    # Fetch bookings
    params = {} if status_filter == "All" else {"status": status_filter}
    result = api_request("GET", "/api/admin/bookings", params=params)
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load bookings"))
        return
    
    bookings = result["data"]
    
    if not bookings:
        st.info("No bookings found")
        return
    
    st.markdown(f"**Total: {len(bookings)} bookings**")
    
    # Display bookings
    for booking in bookings:
        status_color = {
            "Pending": "warning",
            "Accepted": "info",
            "Completed": "success",
            "Cancelled": "danger"
        }.get(booking["status"], "info")
        
        st.markdown(f"""
        <div class='worker-card' style='color: #000;'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <h4 style='margin: 0; color: #0A1AFF;'>Booking #{booking['id']}</h4>
                    <p style='margin: 0.5rem 0; color: #333;'>
                        👤 Client: <strong>{booking.get('client_name', 'N/A')}</strong> ({booking.get('client_email', 'N/A')})
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        👷 Worker: <strong>{booking.get('worker_name', 'N/A')}</strong> ({booking.get('worker_email', 'N/A')})
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        🛠️ Skills: {booking.get('worker_skills', 'N/A')}
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        📅 {format_datetime(booking['booking_date'])}
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        ⏱️ Duration: {booking['hours']} hours
                    </p>
                    <p style='margin: 0.25rem 0; font-size: 0.85rem; color: #333;'>
                        Created: {format_datetime(booking['created_at'])}
                    </p>
                </div>
                <div style='text-align: right;'>
                    <h3 style='margin: 0; color: #2ECC71;'>{format_currency(booking['total_price'])}</h3>
                    <p style='margin: 0.5rem 0;'>
                        <span class='badge badge-{status_color}'>{booking['status']}</span>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")


def show_payments_management():
    """Show payments management"""
    
    st.markdown("### 💳 Payments Management")
    
    # Fetch payments
    result = api_request("GET", "/api/admin/payments")
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load payments"))
        return
    
    payments = result["data"]
    
    if not payments:
        st.info("No payments found")
        return
    
    st.markdown(f"**Total: {len(payments)} payments**")
    
    # Calculate totals
    total_amount = sum(p['amount'] for p in payments)
    successful_payments = [p for p in payments if p['status'] == 'Success']
    successful_amount = sum(p['amount'] for p in successful_payments)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Payments", len(payments))
    
    with col2:
        st.metric("Successful", len(successful_payments))
    
    with col3:
        st.metric("Total Amount", format_currency(total_amount))
    
    st.markdown("---")
    
    # Display payments
    for payment in payments:
        status_color = {
            "Pending": "warning",
            "Success": "success",
            "Failed": "danger",
            "Refunded": "info"
        }.get(payment["status"], "info")
        
        st.markdown(f"""
        <div class='worker-card' style='color: #000;'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <h4 style='margin: 0; color: #0A1AFF;'>Payment #{payment['id']}</h4>
                    <p style='margin: 0.5rem 0; color: #333;'>
                        📋 Booking ID: {payment['booking_id']}
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        👤 Client: <strong>{payment.get('client_name', 'N/A')}</strong>
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        👷 Worker: <strong>{payment.get('worker_name', 'N/A')}</strong>
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        💳 Method: {payment['payment_method']}
                    </p>
                    <p style='margin: 0.25rem 0; color: #333;'>
                        🔑 Transaction ID: {payment.get('transaction_id', 'N/A')}
                    </p>
                    <p style='margin: 0.25rem 0; font-size: 0.85rem; color: #333;'>
                        Created: {format_datetime(payment['created_at'])}
                    </p>
                </div>
                <div style='text-align: right;'>
                    <h3 style='margin: 0; color: #2ECC71;'>{format_currency(payment['amount'])}</h3>
                    <p style='margin: 0.5rem 0;'>
                        <span class='badge badge-{status_color}'>{payment['status']}</span>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
