# E-Commerce Platform (Premium)

A modern, fast, and reliable full-stack e-commerce platform. Built with FastAPI (Backend) and Vue.js (Frontend), this project is fully Dockerized and optimized for production environments.

## Project Structure

```
e_commerce_project/
├── e_commerce_api/      # FastAPI Backend
├── e_commerce_web/      # Vue.js Frontend (Vite)
├── docker-compose.yml   # Docker Orchestrator
└── screenshots/        # Project Screenshots
```

## Key Features

- **SMS-OTP Registration**: Secure user registration via phone number and SMS code (stored in Redis).
- **Dynamic Translation (Multi-language)**: Support for multiple languages (TM/RU) for products, categories, and descriptions.
- **Visual Admin Dashboard**: Track sales revenue and order statistics through interactive Chart.js graphs.
- **User Management**: Administrative tools to manage, ban, or delete users.
- **Multi-Currency Support**: Automatic conversion between USD and TMT with administrative control over rates.
- **Caching System**: Enhanced performance using Redis for product lists and analytics.
- **Security**: Robust authentication using JWT and persistent storage with PostgreSQL.

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework.
- **PostgreSQL**: Powerful and reliable relational database.
- **Redis**: Fast in-memory storage for caching and OTP sessions.
- **SQLAlchemy**: Feature-rich SQL toolkit and ORM.
- **Docker**: Containerization for easy deployment and scalability.

### Frontend
- **Vue 3**: Composition API and modern standards.
- **Chart.js**: Visual data analytics and interactive charts.
- **Pinia**: Lightweight and intuitive state management.
- **Vue I18n**: Internationalization support for the user interface.
- **Vanilla CSS**: Premium, custom-designed UI without heavy frameworks.

## Installation and Setup (via Docker)

This is the recommended approach for a consistent environment.

1.  **Configure Environment**: Create a `.env` file in the `e_commerce_api` directory (refer to `.env.example`).
2.  **Run the Application**:
    ```bash
    docker compose build
    docker compose up -d
    ```

The application will be accessible at:
- **Frontend**: `http://localhost:5173` (or `http://localhost:8080` via Nginx)
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`

## API Endpoints (New & Key Features)

### Authentication
- `POST /api/auth/send-otp` - Send SMS code for registration.
- `POST /api/auth/register` - Register with OTP verification.
- `POST /api/auth/login` - Secure login (prevents access for banned users).

### Administration
- `GET /api/users/` - List all registered users.
- `PUT /api/users/{id}/status` - Ban or unban a specific user.
- `GET /api/reports/dashboard` - Analytical data for visual charts.

## Database (PostgreSQL)

The database port is exposed as `5434` to avoid conflicts with local instances.
- **Host**: `localhost`
- **Port**: `5434`
- **User**: `e_commerce_user`

## License

This project is private and proprietary. All rights reserved.

## Support

For issues or questions, please contact the development lead.
