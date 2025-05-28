# ATS (Applicant Tracking System)

A Django-based Applicant Tracking System for recruiters to manage job applications.

## Features

- CRUD operations for candidate management
- Advanced search functionality for candidates
- RESTful API endpoints
- Efficient ORM-based search implementation

## Setup Instructions

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```env
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database Settings
   DB_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=ats_db
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   ```
5. Create the database:
   ```bash
   # For PostgreSQL
   createdb ats_db
   ```
6. Run migrations:
   ```bash
   python manage.py migrate
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/candidates` - Create a new candidate
- `GET /api/candidates` - List all candidates
- `GET /api/candidates/{id}` - Retrieve a specific candidate
- `PUT /api/candidates/{id}` - Update a candidate
- `DELETE /api/candidates/{id}` - Delete a candidate
- `GET /api/candidates/search?query={query}` - Search candidates by name

## Search Functionality

The search API implements a relevancy-based sorting system:
- Matches are based on the number of words in the search query that appear in the candidate's name
- Results are sorted by relevancy (most relevant first)
- Partial matches are included in the results
- Search is implemented using Django ORM for optimal performance 
