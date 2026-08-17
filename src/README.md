# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Persistent data storage using SQLite database

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                      |

## Data Model

The application uses SQLAlchemy ORM with SQLite for persistent data storage:

1. **Activity** - Represents extracurricular activities:
   - Name (unique identifier)
   - Description
   - Schedule
   - Maximum number of participants
   - Participants (many-to-many relationship)

2. **Participant** - Represents students:
   - Email (unique identifier)
   - Activities (many-to-many relationship)

**Data Persistence**: All data is now stored in a SQLite database (`activities.db`) and persists across server restarts. Sample data is automatically loaded on first startup.
