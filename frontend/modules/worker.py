"""
Worker Dashboard
"""
import streamlit as st
from frontend.utils.api import (
    api_request, show_success, show_error, show_info,
    format_currency, format_datetime, get_current_user
)


def show_worker_dashboard():
    """Show worker dashboard"""
    
    user = get_current_user()
    st.markdown(f"""
    <div class='custom-header'>
        <h1>👷 Welcome, {user.get('full_name', 'Worker')}!</h1>
        <p>Manage your profile and bookings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if worker has profile
    profile_result = api_request("GET", "/api/workers/profile/me")
    
    if not profile_result.get("success"):
        # No profile yet, show creation form
        show_profile_creation()
        return
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👤 My Profile", "📅 Bookings", "⭐ Reviews"])
    
    with tab1:
        show_worker_stats()
    
    with tab2:
        show_worker_profile(profile_result["data"])
    
    with tab3:
        show_worker_bookings()
    
    with tab4:
        show_worker_reviews()


def show_profile_creation():
    """Show profile creation form for new workers"""
    
    st.markdown("### 👤 Create Your Worker Profile")
    st.info("Please complete your profile to start receiving bookings")
    
    with st.form("profile_creation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_input(
                "🛠️ Skills (comma-separated)",
                placeholder="e.g., Plumbing, Electrical, Carpentry"
            )
            experience_years = st.number_input("💼 Years of Experience", min_value=0, max_value=50, value=1)
            location = st.text_input("📍 City/Location", placeholder="e.g., Mumbai")
        
        with col2:
            pincode = st.text_input("📮 Pincode", placeholder="e.g., 400001")
            availability = st.selectbox(
                "📅 Availability",
                ["Full-time", "Part-time", "Weekends"]
            )
            price_per_hour = st.number_input("💰 Price per Hour (₹)", min_value=100, max_value=10000, value=500, step=50)
        
        bio = st.text_area(
            "📝 Bio (Optional)",
            placeholder="Tell clients about yourself and your expertise..."
        )
        
        if st.form_submit_button("✅ Create Profile", use_container_width=True):
            create_worker_profile(skills, experience_years, location, pincode, availability, price_per_hour, bio)


def create_worker_profile(skills, experience_years, location, pincode, availability, price_per_hour, bio):
    """Create worker profile"""
    
    if not all([skills, location, pincode]):
        show_error("Please fill in all required fields")
        return
    
    with st.spinner("Creating profile..."):
        result = api_request(
            "POST",
            "/api/workers/profile",
            data={
                "skills": skills,
                "experience_years": experience_years,
                "location": location,
                "pincode": pincode,
                "availability": availability,
                "price_per_hour": price_per_hour,
                "bio": bio
            }
        )
    
    if result.get("success"):
        show_success("Profile created successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Profile creation failed"))


def show_worker_stats():
    """Show worker statistics dashboard"""
    
    st.markdown("### 📊 Your Statistics")
    
    # Fetch bookings
    bookings_result = api_request("GET", "/api/bookings/my-bookings")
    
    if not bookings_result.get("success"):
        show_error("Failed to load statistics")
        return
    
    bookings = bookings_result["data"]
    
    # Calculate stats
    total_bookings = len(bookings)
    pending_bookings = len([b for b in bookings if b["status"] == "Pending"])
    completed_bookings = len([b for b in bookings if b["status"] == "Completed"])
    total_earnings = sum(b["total_price"] for b in bookings if b["status"] == "Completed")
    
    # Display stats in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{total_bookings}</p>
            <p class='stat-label'>Total Bookings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{pending_bookings}</p>
            <p class='stat-label'>Pending</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number'>{completed_bookings}</p>
            <p class='stat-label'>Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <p class='stat-number' style='font-size: 2rem;'>{format_currency(total_earnings)}</p>
            <p class='stat-label'>Total Earnings</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent bookings
    st.markdown("### 📅 Recent Bookings")
    
    if not bookings:
        st.info("No bookings yet. Clients will find you through search!")
        return
    
    # Show last 5 bookings
    recent_bookings = sorted(bookings, key=lambda x: x["created_at"], reverse=True)[:5]
    
    for booking in recent_bookings:
        status_color = {
            "Pending": "warning",
            "Accepted": "info",
            "Completed": "success",
            "Cancelled": "danger"
        }.get(booking["status"], "info")
        
        st.markdown(f"""
        <div class='worker-card'>
            <div style='display: flex; justify-content: space-between;'>
                <div style='color: #000;'>
                    <h4 style='margin: 0; color: #0A1AFF;'>Booking #{booking['id']}</h4>
                    <p style='margin: 0.5rem 0;'>
                        👤 Client: <strong>{booking.get('client_name', 'N/A')}</strong>
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        📅 {format_datetime(booking['booking_date'])}
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        ⏱️ {booking['hours']} hours
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


def show_worker_profile(profile):
    """Show and edit worker profile"""
    
    st.markdown("### 👤 My Profile")
    
    # Display current profile
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem;'>
            <div style='width: 150px; height: 150px; margin: 0 auto; background: linear-gradient(135deg, #0A1AFF, #2ECC71); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 4rem; color: white;'>
                👷
            </div>
            <h3 style='margin: 1rem 0 0 0; color: #000000;'>{profile.get('full_name', 'Worker')}</h3>
            <p style='color: #000000;'>{profile.get('email', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Availability toggle
        is_available = profile.get('is_available', 1)
        st.markdown("### 📍 Availability Status")
        
        if st.button(
            f"{'🟢 Available' if is_available == 1 else '🔴 Busy'}",
            use_container_width=True
        ):
            toggle_availability(is_available)
    
    with col2:
        st.markdown(f"""
        <div class='worker-card' style='color: #000000;'>
            <h4 style='color: #0A1AFF;'>Professional Details</h4>
            <p style='color: #000000;'><strong>🛠️ Skills:</strong> {profile.get('skills', 'N/A')}</p>
            <p style='color: #000000;'><strong>💼 Experience:</strong> {profile.get('experience_years', 0)} years</p>
            <p style='color: #000000;'><strong>📍 Location:</strong> {profile.get('location', 'N/A')}</p>
            <p style='color: #000000;'><strong>📮 Pincode:</strong> {profile.get('pincode', 'N/A')}</p>
            <p style='color: #000000;'><strong>📅 Availability:</strong> {profile.get('availability', 'N/A')}</p>
            <p style='color: #000000;'><strong>💰 Price:</strong> {format_currency(profile.get('price_per_hour', 0))}/hour</p>
            <p style='color: #000000;'><strong>⭐ Rating:</strong> {profile.get('rating', 0):.1f} ({profile.get('total_reviews', 0)} reviews)</p>
            <p style='color: #000000;'><strong>📝 Bio:</strong> {profile.get('bio', 'No bio')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Edit profile form
    st.markdown("---")
    st.markdown("### ✏️ Edit Profile")
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_input("🛠️ Skills", value=profile.get('skills', ''))
            experience_years = st.number_input(
                "💼 Years of Experience",
                min_value=0,
                max_value=50,
                value=profile.get('experience_years', 0)
            )
            location = st.text_input("📍 Location", value=profile.get('location', ''))
        
        with col2:
            pincode = st.text_input("📮 Pincode", value=profile.get('pincode', ''))
            availability = st.selectbox(
                "📅 Availability",
                ["Full-time", "Part-time", "Weekends"],
                index=["Full-time", "Part-time", "Weekends"].index(profile.get('availability', 'Full-time'))
            )
            price_per_hour = st.number_input(
                "💰 Price per Hour (₹)",
                min_value=100,
                max_value=10000,
                value=int(profile.get('price_per_hour', 500)),
                step=50
            )
        
        bio = st.text_area("📝 Bio", value=profile.get('bio', ''))
        
        if st.form_submit_button("💾 Update Profile", use_container_width=True):
            update_worker_profile(skills, experience_years, location, pincode, availability, price_per_hour, bio)


def update_worker_profile(skills, experience_years, location, pincode, availability, price_per_hour, bio):
    """Update worker profile"""
    
    with st.spinner("Updating profile..."):
        result = api_request(
            "PUT",
            "/api/workers/profile",
            data={
                "skills": skills,
                "experience_years": experience_years,
                "location": location,
                "pincode": pincode,
                "availability": availability,
                "price_per_hour": price_per_hour,
                "bio": bio
            }
        )
    
    if result.get("success"):
        show_success("Profile updated successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Update failed"))


def toggle_availability(current_status):
    """Toggle worker availability"""
    
    new_status = 0 if current_status == 1 else 1
    
    with st.spinner("Updating availability..."):
        result = api_request(
            "PUT",
            "/api/workers/profile",
            data={"is_available": new_status}
        )
    
    if result.get("success"):
        show_success("Availability updated!")
        st.rerun()
    else:
        show_error(result.get("error", "Update failed"))


def show_worker_bookings():
    """Show worker's bookings"""
    
    st.markdown("### 📅 My Bookings")
    
    result = api_request("GET", "/api/bookings/my-bookings")
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load bookings"))
        return
    
    bookings = result["data"]
    
    if not bookings:
        st.info("No bookings yet. Keep your profile updated to attract clients!")
        return
    
    # Filter tabs
    status_filter = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Accepted", "Completed", "Cancelled"]
    )
    
    filtered_bookings = bookings if status_filter == "All" else [
        b for b in bookings if b["status"] == status_filter
    ]
    
    for booking in filtered_bookings:
        status_color = {
            "Pending": "warning",
            "Accepted": "info",
            "Completed": "success",
            "Cancelled": "danger"
        }.get(booking["status"], "info")
        
        st.markdown(f"""
        <div class='worker-card'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <h4 style='margin: 0;'>Booking #{booking['id']}</h4>
                    <p style='margin: 0.5rem 0;'>
                        👤 Client: <strong>{booking.get('client_name', 'N/A')}</strong>
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        📅 {format_datetime(booking['booking_date'])}
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        ⏱️ Duration: {booking['hours']} hours
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        📍 {booking.get('address', 'N/A')}
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        📝 {booking.get('description', 'No description')}
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
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if booking["status"] == "Pending":
                if st.button("✅ Accept", key=f"accept_{booking['id']}"):
                    update_booking_status(booking['id'], "Accepted")
        
        with col2:
            if booking["status"] == "Accepted":
                if st.button("✅ Complete", key=f"complete_{booking['id']}"):
                    update_booking_status(booking['id'], "Completed")
        
        with col3:
            if booking["status"] in ["Pending", "Accepted"]:
                if st.button("❌ Cancel", key=f"cancel_{booking['id']}"):
                    update_booking_status(booking['id'], "Cancelled")
        
        st.markdown("---")


def update_booking_status(booking_id, new_status):
    """Update booking status"""
    
    with st.spinner(f"Updating to {new_status}..."):
        result = api_request(
            "PUT",
            f"/api/bookings/{booking_id}/status",
            data={"status": new_status}
        )
    
    if result.get("success"):
        show_success(f"Booking {new_status.lower()} successfully!")
        st.rerun()
    else:
        show_error(result.get("error", "Update failed"))


def show_worker_reviews():
    """Show worker's reviews"""
    
    st.markdown("### ⭐ My Reviews")
    
    user = get_current_user()
    result = api_request("GET", f"/api/reviews/worker/{user['id']}")
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load reviews"))
        return
    
    reviews = result["data"]
    
    if not reviews:
        st.info("No reviews yet. Complete bookings to receive reviews from clients!")
        return
    
    # Calculate average rating
    avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
    
    st.markdown(f"""
    <div class='stat-card'>
        <p class='stat-number'>{avg_rating:.1f}</p>
        <p class='stat-label'>Average Rating</p>
        <p class='rating' style='font-size: 2rem;'>{'⭐' * int(avg_rating)}</p>
        <p style='color: #000000; margin-top: 0.5rem;'>{len(reviews)} total reviews</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for review in reviews:
        st.markdown(f"""
        <div class='worker-card'>
            <p style='margin: 0;'>
                <span class='rating'>{'⭐' * review['rating']}</span>
            </p>
            <p style='margin: 0.5rem 0; color: #000000;'>{review.get('comment', 'No comment')}</p>
            <p style='margin: 0.5rem 0; font-size: 0.85rem; color: #333;'>
                By {review.get('client_name', 'Anonymous')} • {format_datetime(review['created_at'])}
            </p>
        </div>
        """, unsafe_allow_html=True)
