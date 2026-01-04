# 🚀 Quick Start Guide

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Initialize Database
```powershell
python -m backend.init_db
```

This will create the database and a default admin account:
- **Email**: admin@bluecollar.com
- **Password**: Admin@123

⚠️ **IMPORTANT**: Change the admin password after first login!

### 3. Start the Backend API
Open a terminal and run:
```powershell
uvicorn backend.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 4. Start the Frontend
Open a **new terminal** and run:
```powershell
streamlit run frontend/app.py
```

The application will open automatically in your browser at: http://localhost:8501

## 🎯 First Steps

### For Clients:
1. Sign up with role "Client"
2. Search for workers by skill, location, or rating
3. Book a worker for your needs
4. Make payment (integrated with Razorpay/Stripe)
5. Rate and review after service completion

### For Workers:
1. Sign up with role "Worker"
2. Wait for admin approval
3. Create your professional profile
4. Receive and accept bookings
5. Complete jobs and earn money

### For Admin:
1. Login with default credentials
2. Approve worker accounts
3. Monitor platform analytics
4. Manage users and bookings
5. View payment transactions

## 🔧 Configuration

### Payment Gateway Setup
To enable payments, add your API keys to `.env`:

For Razorpay:
```
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

For Stripe:
```
STRIPE_SECRET_KEY=your_secret_key
STRIPE_PUBLISHABLE_KEY=your_publishable_key
```

### Database Configuration
By default, SQLite is used for development. To use MySQL in production:

1. Install MySQL client:
```powershell
pip install pymysql
```

2. Update `.env`:
```
DATABASE_URL=mysql+pymysql://username:password@localhost/bluecollar_db
```

## 🐳 Docker Deployment

### Using Docker Compose:
```powershell
docker-compose up --build
```

This will start both backend and frontend services.

## 📱 Mobile Access

The application is mobile-responsive. Access from any device using your local network IP:
- Frontend: http://YOUR_IP:8501
- Backend: http://YOUR_IP:8000

## 🆘 Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed
- Check database connection in `.env`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check `API_BASE_URL` in `frontend/utils/api.py`
- Verify CORS settings in `backend/main.py`

### Database errors
- Delete `bluecollar.db` and run `python -m backend.init_db` again
- Check file permissions

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Streamlit Documentation: https://docs.streamlit.io/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/

## 🔒 Security Notes

1. Change default admin password immediately
2. Use strong SECRET_KEY in production
3. Enable HTTPS for production deployment
4. Regularly backup your database
5. Keep dependencies updated

## 💡 Tips

- Use the search filters to find the perfect worker
- Workers with higher ratings appear first
- Complete your profile to attract more clients
- Check the admin dashboard for platform insights
