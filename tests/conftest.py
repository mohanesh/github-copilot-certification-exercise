import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def clean_activities():
    """Reset the in-memory `activities` dict to a known clean state for each test."""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis skill development and friendly matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ashley@mergington.edu"]
        },
        "Music Band": {
            "description": "Learn and perform music in a group setting",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["ryan@mergington.edu", "maya@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore hands-on experiments and scientific discovery",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["liam@mergington.edu", "sophia@mergington.edu"]
        }
    }

    # Reset the shared in-memory activities structure
    activities.clear()
    activities.update(original_activities)

    yield activities

    # Ensure we restore the original state (defensive)
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client(clean_activities):
    """Provide a TestClient that depends on the clean_activities fixture."""
    return TestClient(app)
