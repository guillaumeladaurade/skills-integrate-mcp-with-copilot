"""
Database configuration and models for the Mergington High School Activities API
"""

from sqlalchemy import create_engine, Column, String, Integer, Text, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pathlib import Path

# Database setup
DATABASE_URL = "sqlite:///./activities.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Association table for many-to-many relationship between activities and participants
activity_participants = Table(
    "activity_participants",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activity.id"), primary_key=True),
    Column("participant_email", String, ForeignKey("participant.email"), primary_key=True),
)


class Activity(Base):
    """Activity model representing extracurricular activities"""
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    schedule = Column(String)
    max_participants = Column(Integer)
    
    # Relationship to participants
    participants = relationship(
        "Participant",
        secondary=activity_participants,
        back_populates="activities"
    )


class Participant(Base):
    """Participant model representing students"""
    __tablename__ = "participant"

    email = Column(String, primary_key=True, index=True)
    
    # Relationship to activities
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database with tables"""
    Base.metadata.create_all(bind=engine)


def populate_sample_data():
    """Populate database with sample data if empty"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Activity).first() is not None:
        db.close()
        return
    
    # Sample data
    sample_activities = [
        {
            "name": "Chess Club",
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        {
            "name": "Programming Class",
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        {
            "name": "Gym Class",
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        {
            "name": "Soccer Team",
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        {
            "name": "Basketball Team",
            "description": "Practice and play basketball with the school team",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        {
            "name": "Art Club",
            "description": "Explore your creativity through painting and drawing",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        },
        {
            "name": "Drama Club",
            "description": "Act, direct, and produce plays and performances",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
        },
        {
            "name": "Math Club",
            "description": "Solve challenging problems and participate in math competitions",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
        },
        {
            "name": "Debate Team",
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
        }
    ]
    
    # Create activities and participants
    for activity_data in sample_activities:
        participants_emails = activity_data.pop("participants")
        
        # Create or get participants
        participants = []
        for email in participants_emails:
            participant = db.query(Participant).filter(Participant.email == email).first()
            if not participant:
                participant = Participant(email=email)
                db.add(participant)
            participants.append(participant)
        
        db.flush()  # Flush to ensure participants are created before adding to activity
        
        # Create activity
        activity = Activity(**activity_data)
        activity.participants = participants
        db.add(activity)
    
    db.commit()
    db.close()
