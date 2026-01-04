# 🔧 Blue Collar Worker Platform

A full-stack Python web application connecting clients with blue-collar workers (plumbers, electricians, carpenters, cleaners, etc.).

## 🌟 Features

### User Roles
- **Client**: Search, book, and rate workers
- **Worker**: Manage profile, accept bookings, track earnings
- **Admin**: Platform management, analytics, dispute resolution

### Core Functionality
- 🔐 Secure authentication with role-based access control
- 👤 Comprehensive user profiles
- 🔍 Advanced search and filtering
- 📅 Real-time booking system
- 💳 Payment gateway integration (Razorpay/Stripe)
- ⭐ Rating and review system
- 📊 Analytics dashboards

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: FastAPI
- **Database**: SQLAlchemy (SQLite dev, MySQL prod)
- **Security**: bcrypt, JWT tokens
- **Payment**: Razorpay/Stripe
- **Deployment**: Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bluecollarweb
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python -m backend.init_db
```

6. **Run the application**

Terminal 1 - Backend API:
```bash
uvicorn backend.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
streamlit run frontend/app.py
```

7. **Access the application**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
bluecollarweb/
├── backend/
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── core/             # Configuration & security
│   └── main.py           # FastAPI app
├── frontend/
│   ├── pages/            # Streamlit pages
│   ├── components/       # Reusable UI components
│   ├── utils/            # Helper functions
│   └── app.py            # Main Streamlit app
├── static/               # Static assets
├── uploads/              # User uploads
├── tests/                # Test suite
├── docker-compose.yml    # Docker configuration
├── Dockerfile            # Docker image
├── requirements.txt      # Python dependencies
└── README.md
```

## 🎨 Design Theme

- **Primary**: Deep Blue (#0A1AFF)
- **Secondary**: White (#FFFFFF)
- **Success**: Green (#2ECC71)
- **Background**: Light Gray (#F4F6F7)
- **Error**: Soft Red (#E74C3C)

## 🔒 Security Features

- Password hashing with bcrypt
- JWT-based authentication
- Role-based access control
- Session management
- Environment variable protection
- SQL injection prevention (ORM)

## 💳 Payment Integration

Supports both Razorpay and Stripe:
- Secure payment processing
- Transaction history
- Payment verification
- Refund handling

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

## 📝 Default Admin Credentials

- Email: admin@bluecollar.com
- Password: Admin@123

**⚠️ Change these credentials immediately in production!**

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT License

## 👥 Support

For issues and questions, please open a GitHub issue.
