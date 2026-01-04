"""
Client Dashboard
"""
import streamlit as st
from datetime import datetime, timedelta
from frontend.utils.api import (
    api_request, show_success, show_error, show_info,
    format_currency, format_datetime, get_current_user
)


def show_client_dashboard():
    """Show client dashboard"""
    
    # Header
    user = get_current_user()
    st.markdown(f"""
    <div class='custom-header'>
        <h1>👋 Welcome, {user.get('full_name', 'Client')}!</h1>
        <p>Find and book skilled workers for your needs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Find Workers", "📅 My Bookings", "⭐ My Reviews"])
    
    with tab1:
        show_find_workers()
    
    with tab2:
        show_my_bookings()
    
    with tab3:
        show_my_reviews()


def show_find_workers():
    """Show worker search and filter"""
    
    st.markdown("### 🔍 Search for Workers")
    
    # Search filters
    with st.expander("🎯 Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            skill = st.text_input("🛠️ Skill", placeholder="e.g., Plumber, Electrician")
            location = st.text_input("📍 Location", placeholder="e.g., Mumbai, Delhi")
        
        with col2:
            min_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 0.0, 0.5)
            max_price = st.number_input("💰 Max Price/Hour (₹)", min_value=0, value=1000, step=100)
        
        with col3:
            availability = st.selectbox(
                "📅 Availability",
                ["All", "Full-time", "Part-time", "Weekends"]
            )
            is_available = st.checkbox("✅ Available Now", value=True)
    
    # Search button
    if st.button("🔍 Search Workers", use_container_width=True):
        search_workers(skill, location, min_rating, max_price, availability, is_available)
    
    # Display results
    if "search_results" in st.session_state:
        display_worker_results(st.session_state.search_results)


def search_workers(skill, location, min_rating, max_price, availability, is_available):
    """Search for workers with filters"""
    
    params = {}
    if skill:
        params["skill"] = skill
    if location:
        params["location"] = location
    if min_rating > 0:
        params["min_rating"] = min_rating
    if max_price > 0:
        params["max_price"] = max_price
    if availability != "All":
        params["availability"] = availability
    if is_available:
        params["is_available"] = 1
    
    with st.spinner("Searching for workers..."):
        result = api_request("GET", "/api/workers/search", params=params)
    
    if result.get("success"):
        workers = result["data"]
        st.session_state.search_results = workers
        show_success(f"Found {len(workers)} worker(s)")
    else:
        show_error(result.get("error", "Search failed"))


def display_worker_results(workers):
    """Display worker search results in cards"""
    
    if not workers:
        st.info("No workers found. Try adjusting your filters.")
        return
    
    st.markdown(f"### 📋 Results ({len(workers)} workers)")
    
    for worker in workers:
        with st.container():
            st.markdown(f"""
            <div class='worker-card fade-in'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <h3 style='margin: 0; color: #0A1AFF;'>{worker.get('full_name', 'Unknown')}</h3>
                        <p style='margin: 0.5rem 0; color: #000000;'>
                            <span class='badge badge-primary'>{worker.get('skills', 'N/A')}</span>
                        </p>
                        <p style='margin: 0.5rem 0; color: #000000;'>
                            📍 {worker.get('location', 'N/A')} | 📮 {worker.get('pincode', 'N/A')}
                        </p>
                        <p style='margin: 0.5rem 0; color: #000000;'>
                            💼 {worker.get('experience_years', 0)} years experience | 
                            📅 {worker.get('availability', 'N/A')}
                        </p>
                        <p style='margin: 0.5rem 0; color: #000000;'>
                            <span class='rating'>{'⭐' * int(worker.get('rating', 0))}</span>
                            {worker.get('rating', 0):.1f} ({worker.get('total_reviews', 0)} reviews)
                        </p>
                        <p style='margin: 0.5rem 0; font-size: 0.9rem; color: #000000;'>
                            {worker.get('bio', 'No bio available')}
                        </p>
                    </div>
                    <div style='text-align: right; margin-left: 2rem;'>
                        <h2 style='margin: 0; color: #2ECC71;'>{format_currency(worker.get('price_per_hour', 0))}</h2>
                        <p style='margin: 0.25rem 0; color: #000000; font-size: 0.9rem;'>per hour</p>
                        <p style='margin: 1rem 0 0 0;'>
                            <span class='badge {"badge-success" if worker.get("is_available") == 1 else "badge-warning"}'>
                                {"Available" if worker.get("is_available") == 1 else "Busy"}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Book button
            col1, col2, col3 = st.columns([3, 1, 3])
            with col2:
                if st.button(f"📅 Book", key=f"book_{worker['id']}", use_container_width=True):
                    st.session_state.booking_worker = worker
                    st.session_state.show_booking_form = True
    
    # Show booking form if triggered
    if st.session_state.get("show_booking_form"):
        show_booking_form()


def show_booking_form():
    """Show booking form modal"""
    
    worker = st.session_state.get("booking_worker")
    if not worker:
        return
    
    st.markdown("---")
    st.markdown(f"### 📅 Book {worker.get('full_name')}")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            booking_date = st.date_input(
                "📅 Date",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
            booking_time = st.time_input("🕐 Time", value=datetime.now().time())
        
        with col2:
            hours = st.number_input("⏱️ Hours", min_value=1.0, max_value=24.0, value=2.0, step=0.5)
            address = st.text_area("📍 Service Address", placeholder="Enter full address")
        
        description = st.text_area("📝 Description (Optional)", placeholder="Describe your requirements")
        
        # Calculate total
        total_price = hours * worker.get('price_per_hour', 0)
        st.markdown(f"### Total: {format_currency(total_price)}")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            if st.form_submit_button("✅ Confirm Booking", use_container_width=True):
                create_booking(worker, booking_date, booking_time, hours, address, description)
        with col3:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.show_booking_form = False
                st.rerun()


def create_booking(worker, booking_date, booking_time, hours, address, description):
    """Create a new booking"""
    
    if not address:
        show_error("Please enter service address")
        return
    
    # Combine date and time
    booking_datetime = datetime.combine(booking_date, booking_time)
    
    with st.spinner("Creating booking..."):
        result = api_request(
            "POST",
            "/api/bookings",
            data={
                "worker_id": worker['user_id'],
                "booking_date": booking_datetime.isoformat(),
                "hours": hours,
                "description": description,
                "address": address
            }
        )
    
    if result.get("success"):
        show_success("Booking created successfully!")
        st.session_state.show_booking_form = False
        st.session_state.pop("booking_worker", None)
        st.rerun()
    else:
        show_error(result.get("error", "Booking failed"))


def show_my_bookings():
    """Show client's bookings"""
    
    st.markdown("### 📅 My Bookings")
    
    # Fetch bookings
    result = api_request("GET", "/api/bookings/my-bookings")
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load bookings"))
        return
    
    bookings = result["data"]
    
    if not bookings:
        st.info("You haven't made any bookings yet. Search for workers to get started!")
        return
    
    # Filter tabs
    status_filter = st.selectbox(
        "Filter by status",
        ["All", "Pending", "Accepted", "Completed", "Cancelled"]
    )
    
    filtered_bookings = bookings if status_filter == "All" else [
        b for b in bookings if b["status"] == status_filter
    ]
    
    # Display bookings
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
                        👷 Worker: <strong>{booking.get('worker_name', 'N/A')}</strong>
                    </p>
                    <p style='margin: 0.25rem 0;'>
                        🛠️ Skills: {booking.get('worker_skills', 'N/A')}
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
            if booking["status"] in ["Pending", "Accepted"]:
                if st.button("❌ Cancel", key=f"cancel_{booking['id']}"):
                    cancel_booking(booking['id'])
        
        with col2:
            if booking["status"] == "Completed" and not has_review(booking['id']):
                if st.button("⭐ Review", key=f"review_{booking['id']}"):
                    st.session_state.review_booking = booking
                    st.session_state.show_review_form = True
        
        st.markdown("---")
    
    # Show review form if triggered
    if st.session_state.get("show_review_form"):
        show_review_form()


def cancel_booking(booking_id):
    """Cancel a booking"""
    
    with st.spinner("Cancelling booking..."):
        result = api_request("DELETE", f"/api/bookings/{booking_id}")
    
    if result.get("success"):
        show_success("Booking cancelled successfully")
        st.rerun()
    else:
        show_error(result.get("error", "Cancellation failed"))


def has_review(booking_id):
    """Check if booking has a review"""
    # This would need to be implemented with a proper API call
    return False


def show_review_form():
    """Show review form"""
    
    booking = st.session_state.get("review_booking")
    if not booking:
        return
    
    st.markdown("---")
    st.markdown(f"### ⭐ Review {booking.get('worker_name')}")
    
    with st.form("review_form"):
        rating = st.slider("Rating", 1, 5, 5)
        comment = st.text_area("Comment (Optional)", placeholder="Share your experience...")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            if st.form_submit_button("✅ Submit Review", use_container_width=True):
                submit_review(booking['id'], rating, comment)
        with col3:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.show_review_form = False
                st.rerun()


def submit_review(booking_id, rating, comment):
    """Submit a review"""
    
    with st.spinner("Submitting review..."):
        result = api_request(
            "POST",
            "/api/reviews",
            data={
                "booking_id": booking_id,
                "rating": rating,
                "comment": comment
            }
        )
    
    if result.get("success"):
        show_success("Review submitted successfully!")
        st.session_state.show_review_form = False
        st.session_state.pop("review_booking", None)
        st.rerun()
    else:
        show_error(result.get("error", "Review submission failed"))


def show_my_reviews():
    """Show client's reviews"""
    
    st.markdown("### ⭐ My Reviews")
    
    result = api_request("GET", "/api/reviews/my-reviews")
    
    if not result.get("success"):
        show_error(result.get("error", "Failed to load reviews"))
        return
    
    reviews = result["data"]
    
    if not reviews:
        st.info("You haven't written any reviews yet.")
        return
    
    for review in reviews:
        st.markdown(f"""
        <div class='worker-card'>
            <p style='margin: 0; color: #000000;'><strong>Booking #{review['booking_id']}</strong></p>
            <p style='margin: 0.5rem 0;'>
                <span class='rating'>{'⭐' * review['rating']}</span>
            </p>
            <p style='margin: 0.5rem 0; color: #000000;'>{review.get('comment', 'No comment')}</p>
            <p style='margin: 0.5rem 0; font-size: 0.85rem; color: #333;'>
                {format_datetime(review['created_at'])}
            </p>
        </div>
        """, unsafe_allow_html=True)
