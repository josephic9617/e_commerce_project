# E-Commerce Project

A full-stack e-commerce application with a FastAPI backend and Vue.js frontend, featuring product management, order processing, and multi-currency support.

## Project Structure

```
e_commerce_project/
├── e_commerce_api/      # FastAPI backend
├── e_commerce_web/      # Vue.js frontend
└── screenshots/        # Project screenshots
```

## Features

- **User Authentication**: Phone-based authentication with JWT tokens
- **Product Management**: Create, read, update, and delete products with image uploads
- **Category Management**: Organize products into categories
- **Order Processing**: Complete order management system with order items
- **Multi-Currency Support**: USD to TMT currency conversion
- **Admin Panel**: Administrative interface for managing the store
- **Internationalization**: Multi-language support (i18n)
- **Reports**: Sales and analytics reporting

## Technology Stack

### Backend (e_commerce_api)
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Uvicorn** - ASGI server

### Frontend (e_commerce_web)
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management
- **Axios** - HTTP client
- **Vue I18n** - Internationalization
- **Vite** - Build tool and dev server

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation

### Backend Setup

1. Navigate to the API directory:
```bash
cd e_commerce_api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (create `.env` file):
```env
SECRET_KEY=your-secret-key
ADMIN_PHONE=your-admin-phone
ADMIN_PASSWORD=your-admin-password
UPLOAD_DIR=uploads
```

### Frontend Setup

1. Navigate to the web directory:
```bash
cd e_commerce_web
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

From the project root directory:
```bash
./run_api.sh
```

Or manually:
```bash
cd e_commerce_api
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Start the Frontend

From the project root directory:
```bash
./run_web.sh
```

Or manually:
```bash
cd e_commerce_web
npm run dev
```

The web application will be available at: `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create category (admin)
- `PUT /api/categories/{id}` - Update category (admin)
- `DELETE /api/categories/{id}` - Delete category (admin)

### Orders
- `GET /api/orders` - List user orders
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}/status` - Update order status (admin)

### Currency
- `GET /api/currency` - Get current exchange rate
- `PUT /api/currency` - Update exchange rate (admin)

### Reports
- `GET /api/reports/sales` - Get sales reports (admin)

### Upload
- `POST /api/upload` - Upload image file

## Default Admin Credentials

The application creates a default admin user on first startup. Check your `.env` file for:
- Phone: Value of `ADMIN_PHONE`
- Password: Value of `ADMIN_PASSWORD`

## Database

The application uses SQLite database (`e_commerce.db`) which is automatically created on first run. The database includes:
- Users table
- Categories table
- Products table
- Orders and OrderItems tables
- Currency table

## File Uploads

Product images are stored in the `e_commerce_api/uploads/` directory and served via the `/uploads` endpoint.

## Development

### Backend Development
```bash
cd e_commerce_api
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd e_commerce_web
npm run dev
```

### Build for Production

Frontend:
```bash
cd e_commerce_web
npm run build
```

The production build will be in `e_commerce_web/dist/`

## Project Features in Detail

### User Roles
- **Customer**: Can browse products, place orders, view order history
- **Admin**: Full access to manage products, categories, orders, and view reports

### Order Management
- Shopping cart functionality
- Order creation with multiple items
- Order status tracking
- Order history for users

### Currency System
- Dynamic currency conversion (USD to TMT)
- Admin can update exchange rates
- Prices displayed in both currencies

## License

This project is private and proprietary.

## Support

For issues and questions, please contact the development team.
