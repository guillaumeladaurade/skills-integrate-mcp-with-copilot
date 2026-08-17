"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path
from database import init_db, populate_sample_data, get_db, Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on application startup"""
    init_db()
    populate_sample_data()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with their participants"""
    activities = db.query(Activity).all()
    
    # Convert to dictionary format for API response
    result = {}
    for activity in activities:
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [p.email for p in activity.participants]
        }
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if student is already signed up
    participant = db.query(Participant).filter(
        Participant.email == email,
        Participant.activities.any(Activity.id == activity.id)
    ).first()
    
    if participant:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )
    
    # Create or get the participant
    participant = db.query(Participant).filter(Participant.email == email).first()
    if not participant:
        participant = Participant(email=email)
        db.add(participant)
    
    # Add participant to activity
    activity.participants.append(participant)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Find the participant
    participant = db.query(Participant).filter(Participant.email == email).first()
    
    if not participant or participant not in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )
    
    # Remove participant from activity
    activity.participants.remove(participant)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}
