# StudentExamPrep - IELTS Preparation Platform

## Project Overview

StudentExamPrep is a comprehensive web application designed to help students prepare for the IELTS examination. The platform provides structured practice materials, progress tracking, and personalized feedback across all four IELTS sections: Reading, Writing, Listening, and Speaking.

## Table of Contents
- [System Architecture](#system-architecture)
- [Backend Implementation](#backend-implementation)
- [Frontend Implementation](#frontend-implementation)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Development Workflow](#development-workflow)
- [Project Roadmap](#project-roadmap)
- [Current Status](#current-status)
- [Database Scaling and Connection Pooling](#database-scaling-and-connection-pooling)
- [Asset Management](#asset-management)
- [Comprehensive Error Handling](#comprehensive-error-handling)

## System Architecture

StudentExamPrep follows a Model-View-Controller (MVC) architecture using Flask as the web framework:

- **Model**: SQLAlchemy ORM with SQLite database (configurable for production environments)
- **View**: Jinja2 templates with Bootstrap CSS framework and custom styling
- **Controller**: Flask routes organized in blueprints

### Key Components:

```
StudentExamPrep/
├── app.py              # Application factory
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms.py            # Form definitions using Flask-WTF
├── utils.py            # Utility functions
├── routes/             # Route blueprints
├── static/             # Static assets (CSS, JS, images)
└── templates/          # Jinja2 templates
```

## Backend Implementation

### Flask Application Structure

The backend is built using Flask and follows a modular design with blueprints:

- **app.py**: Application factory pattern for initializing the Flask app with extensions
- **routes/**: Directory containing blueprint modules:
  - **auth.py**: User authentication routes (login, registration, password reset)
  - **admin.py**: Administrative functions
  - **student.py**: Student dashboard and profile
  - **practice.py**: Practice modules and exercises

### Key Dependencies

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **OpenAI**: AI-powered writing and speaking analysis

### Authentication Flow

1. User registration creates a new account in the system
2. Login validates credentials and creates a session using Flask-Login
3. Role-based access control determines available features
4. Session expiry managed through Flask-Login configuration

### Exercise Processing

1. Exercises are stored as JSON in the database with specific structures for each section type
2. When a user starts an exercise:
   - A PracticeRecord is created to track the attempt
   - Content is loaded from the database and formatted based on section type
3. When submitting answers:
   - Answers are compared with stored correct answers
   - For writing/speaking, AI analysis is performed
   - Scores are calculated and saved to the database
   - Badges and achievements are unlocked based on performance

## Frontend Implementation

### Template Structure

```
templates/
├── admin/           # Admin dashboard templates
├── auth/            # Authentication templates
├── practice/        # Practice module templates
│   ├── reading.html
│   ├── writing.html
│   ├── listening.html
│   ├── speaking.html
│   └── advanced_reading.html
├── student/         # Student dashboard templates
├── layout.html      # Base template with common elements
└── index.html       # Landing page
```

### UI Components

1. **Dashboard**: Student overview with recent activity, scores, and recommendations
2. **Progress Tracking**: Visual representation of scores and improvement over time
3. **Practice Modules**: Section-specific practice interfaces
4. **Mock Tests**: Complete test simulations with timing

### JavaScript Functionality

- **charts.js**: Visualization of student progress data
- **timer.js**: Exam timing functionality for realistic practice
- **darkMode.js**: Theme toggle between light and dark mode
- **audioRecorder.js**: Recording functionality for speaking practice

### CSS Architecture

- Base styling using Bootstrap framework
- Custom variables for theming and dark mode support
- Responsive design for mobile and desktop compatibility
- Section-specific styling for practice interfaces

## Database Schema

### Core Tables

1. **User**:
   - `id`: Primary key
   - `email`: Unique email address
   - `password_hash`: Securely hashed password
   - `first_name`, `last_name`: User details
   - `role_id`: Foreign key to Role table
   - `target_score`: User's target IELTS score
   - `points`: Accumulated points for gamification
   - `created_at`: Account creation timestamp

2. **Role**:
   - `id`: Primary key
   - `name`: Role name (admin, student, teacher)

3. **Exercise**:
   - `id`: Primary key
   - `title`: Exercise title
   - `section_id`: Foreign key to Section table
   - `difficulty_id`: Foreign key to Difficulty table
   - `duration`: Expected completion time in minutes
   - `points`: Points awarded for completion
   - `is_mock_test`: Boolean flag for mock test
   - `content`: JSON field containing exercise content
   - `created_at`: Creation timestamp

4. **PracticeRecord**:
   - `id`: Primary key
   - `user_id`: Foreign key to User table
   - `exercise_id`: Foreign key to Exercise table
   - `started_at`: Start timestamp
   - `completed_at`: Completion timestamp (null if incomplete)
   - `score`: Numerical score (0-9)
   - `answers`: JSON field containing submitted answers
   - `feedback`: Text feedback on performance
   - `points_earned`: Points earned from completion

5. **Section**:
   - `id`: Primary key
   - `name`: Section name (Reading, Writing, Listening, Speaking)

6. **Difficulty**:
   - `id`: Primary key
   - `name`: Difficulty level (Beginner, Intermediate, Advanced)

7. **Score**:
   - `id`: Primary key
   - `user_id`: Foreign key to User table
   - `reading`, `writing`, `listening`, `speaking`: Individual section scores
   - `overall`: Overall combined score
   - `recorded_at`: Recording timestamp
   - `mock_test`: Boolean indicating mock test result

### Relationship Tables

1. **Badge**:
   - `id`: Primary key
   - `name`: Badge name
   - `description`: Badge description
   - `criteria`: JSON field containing unlock criteria

2. **UserBadge**:
   - `id`: Primary key
   - `user_id`: Foreign key to User table
   - `badge_id`: Foreign key to Badge table
   - `earned_at`: Timestamp when badge was earned

## API Documentation

The application primarily uses server-rendered templates, but includes several API endpoints for dynamic functionality:

### Authentication APIs

- `POST /auth/login`: Authenticate user and create session
- `POST /auth/register`: Create new user account
- `POST /auth/reset-password`: Initiate password reset process

### Practice APIs

- `POST /practice/submit_answers/<record_id>`: Submit exercise answers
  - **Request Body**: 
    ```json
    {
      "answers": {}, // JSON object with answers
      "score": 0.0   // Optional calculated score
    }
    ```
  - **Response**:
    ```json
    {
      "success": true,
      "redirect": "/practice/results/123"
    }
    ```

### Student APIs

- `GET /student/dashboard/stats`: Get user statistics for dashboard
  - **Response**:
    ```json
    {
      "recent_activity": [],
      "section_scores": {},
      "completed_exercises": 0,
      "points": 100
    }
    ```

### Admin APIs

- `GET /admin/stats`: Get system-wide statistics
- `POST /admin/users/<user_id>`: Update user information
- `POST /admin/exercises/<exercise_id>`: Update exercise content

## Configuration

Environment-specific configuration is managed through the `config.py` file:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/ielts_prep.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
```

## Development Workflow

### Setup Instructions

1. Clone the repository
2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables or update config.py
5. Initialize the database
   ```
   python setup_db.py
   ```
6. Run the application
   ```
   python run_app.py
   ```

### Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Blueprint Structure**: Routes organized by functional area
3. **Database Abstraction**: All database operations through SQLAlchemy ORM
4. **Form Validation**: Input validation handled through WTForms
5. **Template Inheritance**: Base templates extended for specific views

### Testing

- Unit tests for model methods and utility functions
- Integration tests for route functionality
- End-to-end tests for critical user flows

## Project Roadmap

### Phase 1: Core Platform (Completed)
- ✅ User authentication system
- ✅ Basic practice modules for all four IELTS sections
- ✅ Progress tracking dashboard
- ✅ Admin panel for content management

### Phase 2: Enhanced Features (In Progress)
- ✅ Advanced UI with modern design patterns
- ✅ Improved progress visualization
- ✅ Dark mode support
- ✅ Mock test functionality
- ⏳ Speaking practice with audio recording and AI analysis
- ⏳ Writing feedback with detailed suggestions

### Phase 3: Future Development (Planned)
- 🔲 Personalized study plans based on performance
- 🔲 Community features (forums, study groups)
- 🔲 Mobile-optimized experience
- 🔲 Offline mode for practice without internet
- 🔲 Integration with external learning resources

## Current Status

The application is currently in Phase 2 of development with the following key features implemented:

1. **User System**:
   - Registration, login, and profile management
   - Role-based access control

2. **Practice Modules**:
   - Complete implementation of Reading, Writing, Listening sections
   - Basic implementation of Speaking section (pending enhanced AI analysis)
   - Mock tests with realistic timing and conditions

3. **Progress Tracking**:
   - Score history and visualization
   - Section-specific performance metrics
   - Personalized recommendations based on performance

4. **UI/UX**:
   - Modern dashboard with intuitive navigation
   - Mobile-responsive design
   - Dark/light theme support
   - Interactive charts and visualizations

### Recent Improvements

- Fixed critical bug in the reading module that prevented display of mock test content
- Completely redesigned the Progress page with modern UI components
- Enhanced data visualization with interactive charts
- Improved responsive behavior for mobile devices

### Known Issues

- Speaking section audio recording may not work in Safari browsers
- Exercise timer occasionally shows incorrect remaining time
- Dashboard performance may be slow with large datasets

## Contributing

We welcome contributions to the StudentExamPrep project. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Database Scaling and Connection Pooling

The application now supports database connection pooling and advanced scaling strategies through several key components:

### Connection Pooling

Connection pooling is configured through SQLAlchemy engine options:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
    'pool_recycle': 3600,  # Recycle connections after 1 hour
    'pool_pre_ping': True,  # Test connections before using them
    'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 20)),
}
```

These settings ensure optimal database connection management:
- `pool_size` determines the number of connections maintained in the pool
- `pool_recycle` ensures connections are refreshed periodically to avoid stale connections
- `pool_pre_ping` verifies connection validity before use
- `max_overflow` allows temporary additional connections during high-traffic periods

### Database Migrations

We've implemented database migrations with Flask-Migrate to enable seamless schema updates:

```bash
# Initialize migrations directory (first time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

### Multiple Database Support

The application supports different database engines based on environment:
- Development: SQLite for ease of setup
- Testing: In-memory SQLite for speed
- Production: PostgreSQL for reliability and scalability

Connection settings are determined through environment variables:

```bash
# PostgreSQL
export DATABASE_URL="postgresql://username:password@localhost:5432/ielts_prep"

# MySQL
export DATABASE_URL="mysql+pymysql://username:password@localhost:3306/ielts_prep"
```

## Asset Management

### Asset Versioning

Static assets are now versioned to ensure proper caching and updates:

```python
# In app.py
@app.template_global()
def asset_url_for(endpoint, **values):
    return AssetManager.url_for(endpoint, **values)
```

In templates, use:
```html
<link href="{{ asset_url_for('static', filename='css/style.css') }}" rel="stylesheet">
```

This automatically appends version parameters (e.g., `?v=1.2.3`) to asset URLs, ensuring clients load the latest versions after updates.

### CDN Support

Production environments can use Content Delivery Networks for improved performance:

```python
# In config.py
CDN_DOMAIN = os.environ.get('CDN_DOMAIN')
```

If configured, asset URLs will use the CDN domain instead of the application server.

### Caching Policy

Asset caching is configured based on content type:
- Static assets (CSS, JS, images): 30 days
- Dynamic content: 5 minutes by default, configurable per-route

### Secure File Uploading

File uploads are handled by the `FileUploader` utility which provides:
- File type validation based on extensions
- Content-type verification via MIME checking
- Secure filename generation using UUIDs
- Automatic organization into appropriate directories

## Comprehensive Error Handling

### Centralized Error Management

All error handling is centralized in the `error_handlers.py` module, providing:
- Standard error responses across the application
- Proper logging of errors with stack traces
- Different responses for API requests (JSON) and browser requests (HTML)

### Custom Error Pages

The application includes custom error pages for common HTTP status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

### Exception Handling

Routes use structured exception handling with appropriate user feedback:
```python
try:
    # Operation that might fail
    result = perform_operation()
except DatabaseError as e:
    current_app.logger.error(f"Database error: {str(e)}")
    flash("A database error occurred. Please try again later.", "danger")
except Exception as e:
    current_app.logger.error(f"Unexpected error: {str(e)}")
    flash("An unexpected error occurred.", "danger")
```

### Logging Configuration

Comprehensive logging is configured to capture errors and important events:
- Console output for development
- File-based logging with rotation for production
- Log levels adjusted based on environment (DEBUG in development, INFO in production)

## Running the Application

### Prerequisites

- Python 3.8+ (3.13 recommended)
- pip or other Python package manager
- PostgreSQL for production (optional)
- Redis for caching in production (optional)

### Development Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd StudentExamPrep
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   ```
   # Windows
   set FLASK_ENV=development
   set FLASK_DEBUG=1
   
   # macOS/Linux
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   ```

5. Initialize database:
   ```
   python setup_db.py
   ```

6. Run the application:
   ```
   python run_app.py
   ```

7. Access the application at http://localhost:5000

### Production Deployment

For production, set appropriate environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY=<your-secure-key>
export DATABASE_URL=<database-connection-string>
export SESSION_COOKIE_SECURE=true
export ASSET_VERSION=1.0.0
```

Use a proper WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run_app:app
``` 